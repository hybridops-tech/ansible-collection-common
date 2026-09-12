# decision_dispatcher

Deploys a deterministic dispatcher runtime as a systemd service.

Role scope (v1):

- Watches the decision-service records directory.
- Writes normalized dispatch requests under its own state directory.
- Does not execute HyOps directly.

Default behavior is `record-only`.

Each dispatch request also carries a deterministic approval identity:

- `approval_payload_version`
- `approval_artifact_sha256`

The digest covers the approval-relevant request fields, including the decision type, execution plane, target scope, approval posture, rationale and checks. Runtime metadata such as the generated `dispatch_id`, timestamp and request status is kept outside that digest.

The identity exists even when a route does not require approval so downstream records can preserve the exact request artefact that was promoted. When approval is required, the matching consumer must reject approval that does not reference the current digest.
