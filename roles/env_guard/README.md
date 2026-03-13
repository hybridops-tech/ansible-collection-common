# Environment Guard Framework (`env_guard`)

**Deployment governance for Ansible infrastructure**

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![Ansible](https://img.shields.io/badge/ansible-2.13%2B-red.svg)](https://ansible.com)

**ADR:** [ADR-0600 – Environment Guard Framework](https://docs.hybridops.tech/adr/ADR-0600-environment-guard-framework/)

---

## 1. Overview

`env_guard` is an Ansible role that places a governance control point in front of deployments:

- Validates the **target environment** (`dev`, `staging`, `prod`).
- Calculates a **risk score** and enforces approval rules.
- Applies **maintenance window** rules for higher-risk environments.
- Emits a **correlation ID (CID)** and writes audit outputs.

It is designed to run before any change workflow (deployments, infrastructure updates, migrations).

---

## 2. Behaviours

### 2.1 Environment model

By default, the role ships with three environments (from `defaults/main.yml`):

| Environment | Risk | Approval            | Window                | Impact           |
|-------------|------|---------------------|-----------------------|------------------|
| `dev`       | 1/10 | Auto                | `always`              | Development only |
| `staging`   | 5/10 | Auto                | `business_hours`      | Pre-production   |
| `prod`      |10/10 | Manual required     | `maintenance_window`  | Live systems     |

These values can be overridden via `env_guard.environments` in your own vars.

### 2.2 Correlation ID

Each run receives a correlation ID, exposed as `env_guard_correlation_id`:

- Primary: UUID from `uuidgen` (when available).
- Fallback: `envguard-<16-hex>` generated via `ansible.builtin.password`.

The CID is:

- Returned as a fact: `env_guard_correlation_id`.
- Referenced in audit logs and report filenames (shortened form).

---

## 3. Logging and outputs

### 3.1 Default locations

The role discovers the project root dynamically and writes under the canonical `output` tree:

```yaml
# defaults/main.yml (excerpt)
_project_root: >-
  {{
    playbook_dir
    | regex_replace('/deployment/ci/playbooks.*$', '')
    | regex_replace('/common/playbooks.*$', '')
    | regex_replace('/roles/.*$', '')
  }}

env_guard:
  paths:
    project_root: "{{ _project_root }}"
    logs_dir: "{{ _project_root }}/output/logs/ansible"
    env_guard_logs_dir: "{{ _project_root }}/output/logs/ansible/env_guard_logs"
  audit:
    enabled: true
    log_file: "env_guard_audit.log"
    report_prefix: "env_guard_report"
```

Directory layout at runtime:

```text
output/logs/ansible/env_guard_logs/
└── 20260103T225237Z/
    ├── env_guard_audit.log
    └── env_guard_report_20260103T225237Z_<cid8>.md
```

A `latest` symlink is maintained to the most recent run when the OS supports it.

---

## 4. Inputs and outputs

### 4.1 Inputs

Primary input:

- `env` – target environment (`dev`, `staging`, `prod`).

If `env` is not provided, the role will:

1. Try to read `HOS_ENV` from the environment (for example in CI pipelines).
2. Fall back to **interactive selection** (prompt) when both are absent.

Optional inputs:

- `env_guard` overrides – to replace or extend defaults, for example:

```yaml
env_guard:
  environments:
    prod:
      risk_level: 10
      approval_required: true
      monitoring_level: "comprehensive"
      deployment_window: "maintenance_window"
```

### 4.2 Facts set by the role

On success, the role sets:

- `validated_env` – normalised environment (e.g. `production` → `prod`).
- `env_guard_passed` – `true` when validation succeeded.
- `env_guard_risk_score` – numeric risk level for `validated_env`.
- `env_guard_correlation_id` – correlation ID used for audit outputs.
- `env_guard_version` – framework version string.
- `env_guard_timestamp` – timestamp for the run (ISO 8601).
- `env_guard_user` – user under which the run is executed.
- `env_monitoring_level` – environment monitoring profile.
- `env_deployment_window` – named deployment window for the environment.

Downstream roles (deployments, connectivity checks, reporting) can consume these facts or surface them into CI logs.

---

## 5. Typical usage

### 5.1 Interactive gate before deployment

```yaml
- name: Governed deployment
  hosts: localhost
  gather_facts: true

  roles:
    - role: hybridops.common.env_guard
      vars:
        # If omitted, the role can prompt for environment selection.
        env: dev

    - role: myorg.app_deploy
      when: env_guard_passed | bool
```

For production:

```bash
ansible-playbook site.yml -e env=prod
```

The role will:

1. Resolve environment to `prod`.
2. Compute risk score and timing (maintenance window).
3. Require justification and a confirmation step (when configured to do so).
4. Write audit logs and reports under `output/logs/ansible/env_guard_logs/...`.

---

## 6. CI / non-interactive usage

A non-interactive CI harness can drive the environment from an environment variable (for example `HOS_ENV`) and rely on assertions:

```yaml
- name: Environment guard CI validation
  hosts: localhost
  connection: local
  gather_facts: true

  vars:
    target_environment: "{{ (lookup('env', 'HOS_ENV') | default('dev', true)) | lower }}"

  tasks:
    - name: Execute env_guard role (non-interactive)
      ansible.builtin.include_role:
        name: hybridops.common.env_guard
      vars:
        env: "{{ target_environment }}"

    - name: Validate env_guard outputs
      ansible.builtin.assert:
        that:
          - validated_env == target_environment
          - env_guard_passed | bool
          - env_guard_correlation_id is defined
          - env_guard_correlation_id | length > 0
        fail_msg: "Environment guard CI validation failed"
```

Artefact paths for CI:

- Root: `output/logs/ansible/env_guard_logs`
- Latest run: `output/logs/ansible/env_guard_logs/latest` (or newest timestamp directory)
- Audit file: `env_guard_audit.log`
- Reports: `env_guard_report_*.md`

---

## 7. Relationship to other roles

`env_guard` is typically the first gate in an Environment Guard Framework (EGF) pipeline. It usually precedes roles such as:

- `gen_inventory` – generate inventories or placeholders.
- `host_selector` – constrain targets based on environment and rules.
- `ip_mapper` – resolve hostnames/placeholders to concrete IPs.
- `connectivity_test` – validate basic reachability before deployment.
- Application or infrastructure `deployment` roles.

A common pattern:

```yaml
env_guard
→ gen_inventory
→ host_selector
→ ip_mapper
→ connectivity_test
→ deployment
```

---

## 8. Documentation and further reading

- **ADR-0600 – Environment Guard Framework**  
  Design rationale, pipeline ordering, CID model, and run-record layout.  
  See: [ADR-0600 – Environment Guard Framework](https://docs.hybridops.tech/adr/ADR-0600-environment-guard-framework/)

- **Environments & guardrails concept**  
  Business-level view of dev/staging/prod guardrails and how EGF supports them.  
  See: [Environments & Guardrails](https://docs.hybridops.tech/guides/concepts/environments-and-guardrails/)

- **Ansible role index**  
  Position of `env_guard` within the HybridOps collections and pipelines.  
  See: [Ansible role index](https://docs.hybridops.tech/guides/reference/ansible-role-index/)

---

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)  
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the [HybridOps licensing overview](https://docs.hybridops.tech/briefings/legal/licensing/)
for project-wide licence details, including branding and trademark notes.
