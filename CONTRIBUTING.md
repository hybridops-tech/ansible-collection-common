# Contributing to `hybridops.common`

`hybridops.common` provides shared plugins and utility roles used across the
HybridOps runtime. Changes can affect multiple collections and Core operations.

## Contribution scope

Appropriate changes include:

- Improvements to shared roles (for example `connectivity_test`, `env_guard`, `gen_inventory`, `host_selector`, `ip_mapper`, baseline and account management roles).
- New generic helpers that are not tied to a specific business domain.
- Enhancements to `plugins/` (filters, lookups, modules).

Avoid platform-specific business logic in this collection; prefer `hybridops.app` or `hybridops.network` when behaviour is domain-specific.

## Development workflow

### Local setup

Use versions compatible with `requirements.txt`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Change guidelines

- Keep interfaces stable where practical.
- Treat breaking changes as explicit and documented (`CHANGELOG.md` and pull request summary).
- Ensure plugins behave consistently in CI and ad-hoc playbooks.

### Tests

Role-local smoke tests:

```bash
cd roles/<role_name>
ansible-playbook -i tests/inventory.example.ini tests/smoke.yml
```

Changes that affect Core operations must also pass the relevant
[`hybridops-core`](https://github.com/hybridops-tech/hybridops-core) checks.

### Pull requests

Include:

- Summary of changes and expected impact.
- Test evidence (smoke and/or platform integration).
- Notes on compatibility when interfaces change.

## Role and plugin expectations

Each role should provide:

- `roles/<role_name>/tests/smoke.yml`
- `roles/<role_name>/tests/inventory.example.ini`

New or updated plugins should be documented and include a minimal usage example that demonstrates expected behaviour.

## Security and secrets

- Do not commit secrets, tokens, or environment-specific endpoints.
- Consume sensitive values via variables, Vault, or environment lookups.
- Avoid logging sensitive values in debug output or task messages.

Report vulnerabilities through the [security
policy](SECURITY.md), not a public issue.
