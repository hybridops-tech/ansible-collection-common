# hybridops.common.decision_consumer

Installs the HybridOps decision consumer as a `systemd` service.

The consumer watches dispatch requests, waits for approval when required, and writes normalized execution records. It does not execute `hyops` in v1.

## Approval binding

When a dispatch request requires approval, the approval must identify the exact request artefact that was reviewed. The dispatcher writes:

- `approval_payload_version`
- `approval_artifact_sha256`

The approval file remains named `<dispatch_id>.approved.json`, but its contents must include the same identity:

```json
{
  "dispatch_id": "dispatch-...",
  "approval_payload_version": 1,
  "approval_artifact_sha256": "<sha256>",
  "approved_by": "operator@example.com",
  "approved_at": "2026-09-12T12:00:00Z",
  "note": "approved change window"
}
```

Immediately before promotion, the consumer recomputes the SHA-256 digest from the current approval-relevant request contents. Promotion is refused when the request identity is missing, when the approval references another request identity, or when the artefact no longer matches what was approved. A stale or invalid approval never produces `approved-ready`.

`approved_by` and `approved_at` must be non-empty strings. An approval without that audit context is not promoted.

Every request must retain the identity written by the dispatcher. Routes with `requires_approval: false` keep their existing no-approval behavior after that identity is verified. Their execution records still carry the current artefact identity for provenance.
