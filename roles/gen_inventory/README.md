# Gen Inventory Role

Generate placeholder Ansible inventories for the Environment Guard Framework (EGF).

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![Ansible](https://img.shields.io/badge/ansible-2.13%2B-red.svg)](https://ansible.com)

**Maintainer:** HybridOps.Studio  
**Status:** Optional / legacy-friendly

---

## Purpose

`gen_inventory` creates **environment-specific inventories using placeholder addresses** (for example `XX.XX.XX.00`) that are later resolved by `ip_mapper`.

In the current HybridOps.Studio design, **NetBox is the primary source of truth for inventories and IPAM**. This role is retained for:

- Homelab and training scenarios
- EGF pipeline demos where NetBox is not yet available
- Backwards compatibility with early EGF examples

If you already use NetBox with dynamic inventory, this role is usually **not required**.

---

## Where it fits

Typical EGF pipeline (pre-NetBox or lab mode):

```text
env_guard → gen_inventory → host_selector → ip_mapper → connectivity_test → deployment
```

- `env_guard` validates the target environment and seeds correlation IDs.
- `gen_inventory` builds a small, environment-scoped inventory with placeholder IPs.
- `ip_mapper` replaces placeholders with real IPs at runtime.
- `connectivity_test` validates reachability before any change is applied.

In NetBox-first environments, `gen_inventory` is replaced by **NetBox + dynamic inventory**.

---

## Quick start (lab/demo)

Generate a simple inventory for a given environment and inspect the result:

```bash
ansible-playbook   -i localhost,   roles/common/gen_inventory/tests/test_role.yml   -e env=dev
```

The test harness keeps everything local to the role’s `tests/` directory so it does not interfere with real inventories.

---

## Behaviour (conceptual)

At a high level the role:

- Creates **environment-specific host groups** (for example `dev`, `staging`, `prod`).
- Assigns **stable hostnames** with **placeholder IPs** (no real addresses written to Git).
- Ensures the generated inventory can be consumed by:
  - `host_selector` (for target selection)
  - `ip_mapper` (for runtime resolution)
  - `connectivity_test` (for reachability checks)

Exact file paths and formats are implementation details of the role; see `defaults/main.yml` and the `tests/` playbooks inside the collection for the current behaviour.

---

## Testing

From the collection repository:

```bash
cd roles/common/gen_inventory
ansible-playbook -i localhost, tests/test_role.yml
```

The test playbook validates that:

- An inventory is generated without errors.
- Expected groups and hosts exist for the chosen environment.
- Output is structurally compatible with downstream EGF roles.

---

## Dependencies and related roles

This role is designed to sit alongside other EGF components:

- `env_guard` – governance and environment validation
- `host_selector` – secure host targeting
- `ip_mapper` – runtime IP resolution for placeholder addresses
- `connectivity_test` – connectivity validation and reporting

In NetBox-based environments, prefer:

- NetBox + dynamic inventory for host data
- `connectivity_test` for network validation
- `env_guard` for governance and audit

---

## Further documentation

- **ADR-0600 – Environment Guard Framework**  
  How `gen_inventory` fits into the `env_guard → host_selector → ip_mapper → connectivity_test` pipeline.  
  [Read ADR-0600](https://docs.hybridops.studio/adr/ADR-0600-environment-guard-framework/)

- **ADR-0002 – NetBox-Driven Inventory**  
  Why NetBox is the primary source of truth and when `gen_inventory` is still used as a bridge.  
  [Read ADR-0002](https://docs.hybridops.studio/adr/ADR-0002-netbox-driven-inventory/)

- **Ansible role index**  
  Position of `gen_inventory` within the HybridOps collections and how it’s used in pipelines.  
  [Ansible role index](https://docs.hybridops.studio/guides/reference/ansible-role-index/)

  ---

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)  
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the [HybridOps.Studio licensing overview](https://docs.hybridops.studio/briefings/legal/licensing/)
for project-wide licence details, including branding and trademark notes.
