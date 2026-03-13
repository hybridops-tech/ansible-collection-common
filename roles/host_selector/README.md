# Host Selector Role

**Host targeting with governance integration**

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![Ansible](https://img.shields.io/badge/ansible-2.13%2B-red.svg)](https://ansible.com)

---

## Overview

Host selection role for Ansible-based automation. It provides controlled targeting with four selection methods and governance integration via `env_guard`.

**Highlights:**

- Reduces host-selection errors and accidental targeting.
- Enforces environment isolation using `validated_env`.
- Creates a predictable group (`targets_to_ping`) for downstream roles such as `ip_mapper` and `connectivity_test`.

---

## Features

- **Four selection methods** — manual, group-based, hierarchical, and bulk selection.
- **Governance-aware** — expects `env_guard` to set `validated_env` and (optionally) a correlation ID.
- **Pipeline-ready** — emits a consolidated host group for later stages.
- **Validated input** — clear, fail-fast messaging for invalid choices.
- **Traceable runs** — debug output can be tagged with a correlation ID.

---

## Pipeline integration

```text
env_guard → gen_inventory → host_selector → ip_mapper → connectivity_test → deployment
#           (sets env + CID)  (targeting)     (IP mapping)     (reachability)
```

### Selection methods

| Method | Use case          | Example input                  |
|--------|-------------------|--------------------------------|
| **A**  | Ad-hoc/emergency  | `172.16.10.10,server01.local` |
| **B**  | Group operations  | `cisco_routers,Tokyo`         |
| **C**  | Discovery/browse  | Navigate categories → select  |
| **D**  | Bulk operations   | All infrastructure hosts      |

Example Method B prompt:

```text
Available groups:
arista_switches       cisco_routers          cisco_switches
docker_hosts          grafana_servers        k8s_pods
linux_servers         monitoring             nas_storage
pfsense_firewalls     prometheus_servers     routers
servers               switches               tokyo_devices
vyos_routers          windows_servers

Enter group name(s), comma-separated:
```

---

## Correlation ID behaviour

The role supports an optional Correlation ID (CID) for log traceability.

Resolution order:

1. `correlation_id` (play variable) or `egf_correlation_id` (from `env_guard`).
2. `EGF_CORR_ID` environment variable.
3. Generated at runtime (if enabled and no value is provided).

CID is used for logging and debug messages only; it is not propagated to managed hosts.

You can disable CID usage via:

```yaml
host_selector_use_cid: false
```

---

## Usage

Minimal example:

```yaml
- hosts: localhost
  gather_facts: true
  roles:
    - role: hybridops.common.env_guard
    - role: hybridops.common.host_selector
```

Downstream roles can then target the group created by `host_selector` (for example `targets_to_ping`), depending on how the role is configured in your playbooks.

### Key variables

| Variable                       | Type | Default | Purpose                                                       |
|--------------------------------|------|---------|---------------------------------------------------------------|
| `host_selector_use_cid`        | bool | `true`  | Toggle CID logging behaviour.                                 |
| `host_selector_inherited_cid`  | str  | _empty_ | CID from `env_guard` (`correlation_id` / `egf_correlation_id`). |
| `host_selector_env_cid`        | str  | _empty_ | CID from the `EGF_CORR_ID` environment variable.              |
| `host_selector_cid_pre`        | str  | _empty_ | First non-empty candidate; used before runtime fallback.      |

---

## Testing

Interactive test harness (example layout):

```bash
ansible-playbook -i tests/inventory/test_inventory.ini tests/test_role.yml
```

Non-interactive (CI-style) example:

```bash
ansible-playbook -i tests/inventory/test_inventory.ini tests/test_role.yml \
  -e "validated_env=staging correlation_id=ci-run-12345 method=D"
```

---

## Dependencies

Typical upstream and downstream roles:

- `env_guard` – sets `validated_env` and (optionally) seeds correlation ID.
- `gen_inventory` – generates placeholder hosts (when not using an external CMDB).
- `ip_mapper` – resolves placeholder IPs to real environment addresses.
- `connectivity_test` – validates reachability of the selected hosts.

---

## Further documentation

- **ADR-0600 – Environment Guard Framework**  
  Design rationale for the `env_guard → gen_inventory → host_selector → ip_mapper → connectivity_test` pipeline.  
  [Read ADR-0600](https://docs.hybridops.tech/adr/ADR-0600-environment-guard-framework/)

- **Environments & guardrails concept**  
  Business-level view of dev/staging/prod guardrails and how host selection fits into that model.  
  [Environments & guardrails](https://docs.hybridops.tech/guides/concepts/environments-and-guardrails/)

- **Ansible role index**  
  Position of `host_selector` within the HybridOps collections and pipelines.  
  [Ansible role index](https://docs.hybridops.tech/guides/reference/ansible-role-index/)

---

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)  
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the [HybridOps licensing overview](https://docs.hybridops.tech/briefings/legal/licensing/)
for project-wide licence details, including branding and trademark notes.
