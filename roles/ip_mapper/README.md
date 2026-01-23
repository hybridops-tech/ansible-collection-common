# IP Mapper Role

**Environment-aware IP mapping with governance integration**

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![Ansible](https://img.shields.io/badge/ansible-2.13%2B-red.svg)](https://ansible.com)

**Maintainer:** HybridOps.Studio

> **Status:** Bridge role. In NetBox‑first deployments, this role becomes **optional** or a **fallback**.
> It remains for environments still migrating from file/TF outputs to NetBox as the single source of truth.

---

## Purpose

`ip_mapper` resolves placeholder IPs (for example `XX.XX.XX.00`) into real, environment-specific addresses at run time.  
It is designed to sit behind an environment-governance layer (for example `env_guard`) so that the same playbook can be
used across dev, staging, and prod while keeping real IPs out of version control.

Typical use cases:

- Migrating from static inventories toward dynamic / NetBox-backed IPAM while keeping existing playbooks working.
- Running drills or demos where hostnames are stable but addresses differ by environment.
- Demonstrating “no secrets in Git” patterns for infra-as-code reviews.

---

## Pipeline context

The role is usually used as part of the Environment Guard Framework (EGF) chain:

```text
env_guard → gen_inventory → host_selector → ip_mapper → connectivity_test → deployment
#           (valid env + CID) (target set)       (real IPs)        (reachability)
```

It also works standalone if you provide both:

- A `validated_env` (for example `dev`, `staging`, `prod`).
- A mapping structure (group → list of `{ name, ip }`) via group vars or another source of truth.

---

## How it works

At a high level the role:

1. Reads the **current environment** (for example `validated_env` from `env_guard`).
2. Loads **per-environment host mappings**, typically from inventory or group vars, such as:

   ```yaml
   ip_mapper_environments:
     staging:
       cisco_routers:
         - { name: test-router-01, ip: 10.0.1.1 }
       cisco_switches:
         - { name: test-switch-01, ip: 10.0.1.10 }
   ```

3. For each host in scope, replaces placeholder addresses (for example `XX.XX.XX.00`) with the mapped `ip`.
4. Emits concise debug output and clear failures when a host cannot be mapped.

No IPs are committed to Git; all resolution happens at run time in Ansible.

---

## Status and usage in NetBox-first estates

This role is now a **bridge/fallback** in NetBox-first environments:

- Graceful migration from legacy YAML/TF mappings to NetBox.
- Fallback when NetBox is temporarily unavailable.
- Supplemental resolution for ad-hoc hosts not yet modeled in NetBox.

---

## Requirements

- Ansible **2.13+** (tested with newer ansible-core releases).
- An inventory that provides:
  - A `validated_env` variable (or equivalent) indicating the active environment.
  - Per-environment mapping data (for example `ip_mapper_environments`) in group or host vars.

`env_guard` is recommended but not strictly required if you provide `validated_env` yourself.

---

## Minimal example

```yaml
- name: Map IPs for current environment
  hosts: all
  gather_facts: false
  vars:
    validated_env: staging
    ip_mapper_environments:
      staging:
        linux_servers:
          - { name: web-01, ip: 10.0.1.10 }
          - { name: web-02, ip: 10.0.1.11 }
  roles:
    - role: hybridops.common.ip_mapper
```

After the role runs, affected hosts will have `ansible_host` set to the environment-specific IPs. Subsequent roles
(such as `connectivity_test` or deployment playbooks) use those addresses transparently.

---

## CID behaviour (optional)

The role can optionally tag debug paths and error messages with a **Correlation ID (CID)** so that a single run can be
traced across multiple roles and playbooks.

CID is typically inherited from:

1. `correlation_id` or `egf_correlation_id` set by `env_guard`.
2. The `EGF_CORR_ID` environment variable.
3. A generated value, if both are missing.

Example log line when CID is enabled:

```text
[cid=egf-20250910-abcd1234] Unmapped hosts in staging: web-03
```

CID tagging is for traceability only; it does not change inventory or address resolution.

---

## Testing

A lightweight test harness can be provided under `roles/common/ip_mapper/tests/` in consuming repositories, for example:

```bash
# Interactive (prompts for environment)
ansible-playbook -i roles/common/ip_mapper/tests/inventory/test_inventory.ini   roles/common/ip_mapper/tests/test_role.yml

# Non-interactive (CI)
ansible-playbook -i roles/common/ip_mapper/tests/inventory/test_inventory.ini   roles/common/ip_mapper/tests/test_role.yml   -e validated_env=dev
```

Common test assertions:

- Hosts with placeholders receive an environment-specific `ansible_host`.
- Unmapped hosts are reported clearly (and optionally fail the run).
- CID, if enabled, appears in debug and error messages.

---

## Further documentation

- [ADR-0600 – Environment Guard Framework](https://docs.hybridops.studio/adr/ADR-0600-environment-guard-framework/)
- [ADR-0002 – Source of Truth: NetBox-Driven Inventory](https://docs.hybridops.studio/adr/ADR-0002-netbox-driven-inventory/)
- [Ansible role index](https://docs.hybridops.studio/guides/reference/ansible-role-index/)

---

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)  
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the [HybridOps.Studio licensing overview](https://docs.hybridops.studio/briefings/legal/licensing/)
for project-wide licence details, including branding and trademark notes.
