#!/usr/bin/env python3
"""Acceptance tests for approval binding in the decision pipeline."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]
DISPATCHER_TEMPLATE = REPO_ROOT / "roles/decision_dispatcher/templates/decision-dispatcher.py.j2"
CONSUMER_TEMPLATE = REPO_ROOT / "roles/decision_consumer/templates/decision-consumer.py.j2"


def _load_runtime(template: Path, placeholder: str, runtime_root: Path) -> dict:
    source = template.read_text(encoding="utf-8").replace(placeholder, str(runtime_root))
    namespace = {"__name__": f"test_{template.stem}"}
    exec(compile(source, str(template), "exec"), namespace)
    return namespace


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")


class ApprovalBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.requests_dir = self.root / "requests"
        self.approvals_dir = self.root / "approvals"
        self.executions_dir = self.root / "executions"
        self.dispatcher = _load_runtime(
            DISPATCHER_TEMPLATE,
            "{{ decision_dispatcher_root }}",
            self.root / "dispatcher",
        )
        self.consumer = _load_runtime(
            CONSUMER_TEMPLATE,
            "{{ decision_consumer_root }}",
            self.root / "consumer",
        )
        self.dispatcher["REQUESTS_DIR"] = self.requests_dir

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _dispatch(self, *, requires_approval: bool = True) -> dict:
        decision = {
            "decision_id": "decision-001",
            "decision_type": "cutover",
            "rationale": "primary path failed validation",
            "checks": [
                {"name": "primary_ready", "status": "failed"},
                {"name": "burst_ready", "status": "passed"},
            ],
        }
        route = {
            "execution_plane": "runner-local",
            "target_kind": "blueprint",
            "target_ref": "dr/postgresql-ha-failover-gcp@v1",
            "target_env": "prod",
            "requires_approval": requires_approval,
        }
        result = self.dispatcher["_emit_dispatch_request"](
            decision=decision,
            route=route,
            config={"execution_mode": "record-only", "require_approval": True},
        )
        return json.loads(Path(result["request_file"]).read_text(encoding="utf-8"))

    def _consumer_config(self) -> dict:
        return {
            "dispatch_requests_dir": str(self.requests_dir),
            "approval_dir": str(self.approvals_dir),
            "executions_dir": str(self.executions_dir),
            "execution_mode": "approval-only",
            "require_approval": True,
            "poll_seconds": 5,
        }

    def _write_approval(self, request: dict, **overrides: object) -> Path:
        payload = {
            "dispatch_id": request["dispatch_id"],
            "approval_payload_version": request["approval_payload_version"],
            "approval_artifact_sha256": request["approval_artifact_sha256"],
            "approved_by": "operator@example.com",
            "approved_at": "2026-09-12T12:00:00Z",
            "note": "approved for the planned change window",
        }
        payload.update(overrides)
        path = self.approvals_dir / f"{request['dispatch_id']}.approved.json"
        _write_json(path, payload)
        return path

    def _execution_records(self) -> list[dict]:
        if not self.executions_dir.exists():
            return []
        return [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(self.executions_dir.glob("*.json"))
        ]

    def test_exact_approved_artifact_is_promoted(self) -> None:
        request = self._dispatch()
        self.assertEqual(request["approval_payload_version"], 1)
        self.assertEqual(len(request["approval_artifact_sha256"]), 64)
        self.assertEqual(
            request["approval_artifact_sha256"],
            self.consumer["_approval_artifact_sha256"](request),
        )
        self._write_approval(request)

        state = self.consumer["_process"](self._consumer_config(), {})
        records = self._execution_records()

        self.assertEqual(state["processed_count"], 1)
        self.assertEqual(state["pending_count"], 0)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["status"], "approved-ready")
        self.assertEqual(
            records[0]["approval_artifact_sha256"],
            request["approval_artifact_sha256"],
        )
        self.assertEqual(
            records[0]["approval"]["artifact_sha256"],
            request["approval_artifact_sha256"],
        )
        self.assertEqual(records[0]["approval"]["approved_by"], "operator@example.com")

    def test_changed_artifact_makes_prior_approval_stale(self) -> None:
        request = self._dispatch()
        original_digest = request["approval_artifact_sha256"]
        self._write_approval(request)

        request["target_ref"] = "dr/postgresql-ha-failover-gcp@v2"
        request["approval_artifact_sha256"] = self.consumer["_approval_artifact_sha256"](request)
        self.assertNotEqual(request["approval_artifact_sha256"], original_digest)
        _write_json(self.requests_dir / f"{request['dispatch_id']}.json", request)

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(state["reason"], f"stale-approval:{request['dispatch_id']}")
        self.assertEqual(self._execution_records(), [])

        self._write_approval(request)
        retried = self.consumer["_process"](self._consumer_config(), state)

        self.assertEqual(retried["processed_count"], 1)
        self.assertEqual(retried["pending_count"], 0)
        self.assertEqual(len(self._execution_records()), 1)

    def test_request_digest_tampering_is_rejected(self) -> None:
        request = self._dispatch()
        request["approval_artifact_sha256"] = "0" * 64
        _write_json(self.requests_dir / f"{request['dispatch_id']}.json", request)

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(state["reason"], f"stale-approval:{request['dispatch_id']}")
        self.assertEqual(self._execution_records(), [])

    def test_request_dispatch_id_must_match_its_filename(self) -> None:
        request = self._dispatch()
        original_dispatch_id = request["dispatch_id"]
        request["dispatch_id"] = "../../another-request"
        _write_json(self.requests_dir / f"{original_dispatch_id}.json", request)

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(
            state["reason"],
            f"invalid-approval-identity:{original_dispatch_id}",
        )
        self.assertEqual(self._execution_records(), [])

    def test_wrong_request_payload_version_is_rejected(self) -> None:
        request = self._dispatch()
        request["approval_payload_version"] = 2
        _write_json(self.requests_dir / f"{request['dispatch_id']}.json", request)

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(
            state["reason"],
            f"invalid-approval-identity:{request['dispatch_id']}",
        )
        self.assertEqual(self._execution_records(), [])

    def test_approval_posture_cannot_be_changed_to_bypass_approval(self) -> None:
        request = self._dispatch()
        request["requires_approval"] = False
        _write_json(self.requests_dir / f"{request['dispatch_id']}.json", request)

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(state["reason"], f"stale-approval:{request['dispatch_id']}")
        self.assertEqual(self._execution_records(), [])

    def test_rationale_and_checks_are_approval_relevant(self) -> None:
        request = self._dispatch()
        original_digest = request["approval_artifact_sha256"]
        mutations = (
            {"rationale": "operator selected another recovery path"},
            {"checks": [{"name": "primary_ready", "status": "passed"}]},
        )

        for mutation in mutations:
            with self.subTest(mutation=mutation):
                changed = dict(request)
                changed.update(mutation)
                self.assertNotEqual(
                    self.consumer["_approval_artifact_sha256"](changed),
                    original_digest,
                )

    def test_missing_approval_identity_is_rejected(self) -> None:
        request = self._dispatch()
        self._write_approval(request, approval_artifact_sha256="")

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(
            state["reason"],
            f"invalid-approval-identity:{request['dispatch_id']}",
        )
        self.assertEqual(self._execution_records(), [])

    def test_wrong_approval_version_can_be_corrected_and_retried(self) -> None:
        request = self._dispatch()
        self._write_approval(request, approval_payload_version=2)

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(
            state["reason"],
            f"invalid-approval-identity:{request['dispatch_id']}",
        )
        self.assertEqual(self._execution_records(), [])

        self._write_approval(request)
        retried = self.consumer["_process"](self._consumer_config(), state)

        self.assertEqual(retried["processed_count"], 1)
        self.assertEqual(retried["pending_count"], 0)
        self.assertEqual(len(self._execution_records()), 1)

    def test_approval_requires_audit_context(self) -> None:
        request = self._dispatch()
        self._write_approval(request, approved_by="")

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(
            state["reason"],
            f"invalid-approval-context:{request['dispatch_id']}",
        )
        self.assertEqual(self._execution_records(), [])

        self._write_approval(request, approved_at="")
        state = self.consumer["_process"](self._consumer_config(), state)

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(
            state["reason"],
            f"invalid-approval-context:{request['dispatch_id']}",
        )
        self.assertEqual(self._execution_records(), [])

    def test_non_object_approval_is_rejected(self) -> None:
        request = self._dispatch()
        approval_path = self.approvals_dir / f"{request['dispatch_id']}.approved.json"
        approval_path.parent.mkdir(parents=True, exist_ok=True)
        approval_path.write_text("[]", encoding="utf-8")

        state = self.consumer["_process"](self._consumer_config(), {})

        self.assertEqual(state["processed_count"], 0)
        self.assertEqual(state["pending_count"], 1)
        self.assertEqual(
            state["reason"],
            f"invalid-approval-identity:{request['dispatch_id']}",
        )
        self.assertEqual(self._execution_records(), [])

    def test_no_approval_route_retains_existing_semantics(self) -> None:
        request = self._dispatch(requires_approval=False)

        state = self.consumer["_process"](self._consumer_config(), {})
        records = self._execution_records()

        self.assertEqual(state["processed_count"], 1)
        self.assertEqual(state["pending_count"], 0)
        self.assertEqual(len(records), 1)
        self.assertFalse(records[0]["approval"]["required"])
        self.assertEqual(
            records[0]["approval_artifact_sha256"],
            request["approval_artifact_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
