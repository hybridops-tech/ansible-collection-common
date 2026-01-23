# hybridops.common – Shared Plugins and Utility Roles

Shared plugins and utility roles for the HybridOps.Studio automation platform.  
The collection provides a consistent HybridOps-specific dialect for tags, environment defaults and evidence metadata, and exposes lightweight guard roles that other collections can reuse.

---

## 1. Collection scope

**Collection name:** `hybridops.common`  
**Galaxy namespace/name:** `hybridops.common` (planned)  
**Source repository:** [github.com/hybridops-studio/ansible-collection-common](https://github.com/hybridops-studio/ansible-collection-common)

Scope:

- Filter, lookup, module, and module_utils plugins consumed by other `hybridops.*` collections.
- Small, cross-cutting roles for environment governance, inventory helpers, connectivity checks, and baseline host preparation.

The collection is primarily a dependency for `hybridops.app`, `hybridops.helper`, and `hybridops.network`, but it can also be used independently.

---

## 2. Plugins

Representative plugins (names may evolve as the platform grows):

| Plugin type  | Name                        | Purpose                                                                 |
|--------------|-----------------------------|-------------------------------------------------------------------------|
| filter       | `hybridops_env_tag`         | Build standard labels such as `env-dev_role-rke2-node`.                |
| lookup       | `hybridops_env_default`     | Read environment variables with CI- and secret-friendly defaults.      |
| module_utils | `hybridops_common.result`   | Helpers for consistent module results and evidence metadata.           |
| module       | `hybridops_info`            | Return environment and role information for debugging and evidence.    |

These plugins are imported by roles in other collections so tagging, evidence, and environment handling remain consistent across the platform.

---

## 3. Utility roles

Key roles (see role-level READMEs for details):

| Role name            | Purpose                                                                      |
|----------------------|------------------------------------------------------------------------------|
| `env_guard`          | Environment governance, risk scoring, approvals, and audit artefacts.       |
| `connectivity_test`  | Multi-protocol connectivity checks with structured JSON/JSONL artefacts.    |
| `gen_inventory`      | Generate environment-specific inventories from structured environment data. |
| `host_selector`      | Governed host targeting (manual, group-based, hierarchical, bulk).          |
| `ip_mapper`          | Environment-aware IP mapping (placeholders → real addresses at runtime).    |

Additional roles (for example baseline Linux preparation) may be included for internal use by the HybridOps.Studio platform.

Each role ships with its own `README.md` and a `tests/` harness for smoke-testing.

---

## 4. Requirements

- Ansible **2.13+** (aligned with role `meta/` and Galaxy metadata).
- Python **3.10+** on the control node.

Plugins run on the control node and work with any inventory supported by consuming `hybridops.*` collections.

---

## 5. Installation

Install directly:

```bash
ansible-galaxy collection install hybridops.common
```

Or via `collections/requirements.yml`:

```yaml
collections:
  - name: hybridops.common
    version: "*"
```

---

## 6. Example usage

Example use of common plugins in a playbook:

```yaml
- name: Demonstrate common plugins
  hosts: localhost
  gather_facts: false
  collections:
    - hybridops.common

  vars:
    raw_env: "{{ lookup('hybridops.common.hybridops_env_default', 'HOS_ENV', default='dev') }}"
    standard_tag: "{{ raw_env | hybridops_env_tag('rke2-node') }}"

  tasks:
    - name: Show derived tag
      ansible.builtin.debug:
        msg: "Standard tag for this run: {{ standard_tag }}"
```

Roles such as `env_guard`, `gen_inventory`, `host_selector`, `ip_mapper`, and `connectivity_test` can then be composed into an end-to-end Environment Guard Framework (EGF) pipeline.

---

## 7. Testing and CI

This collection is tested in two ways:

1. **Role-local smoke tests**  
   Each role may provide a `tests/` harness (for example `tests/smoke.yml` and a small test inventory) that can be run with `ansible-playbook` directly.

2. **Platform-level integration tests**  
   The HybridOps.Studio platform repository includes deployment and CI playbooks under `deployment/` that exercise `hybridops.common` alongside other `hybridops.*` collections (including connectivity gates and governance checks).

A separate **collections harness Makefile** in the mono-repo can run:

- Connectivity gates against a `cicd-test` inventory.
- Role-level smoke tests for individual roles.
- Galaxy build/release dry runs.

This keeps core helpers testable in isolation while proving them in realistic platform pipelines.

---

## 8. Development and releases

Layout (simplified):

```text
ansible_collections/hybridops/common/
├── plugins/
│   ├── filter/
│   ├── lookup/
│   ├── module_utils/
│   └── modules/
├── roles/
│   └── <role_name>/
│       ├── defaults/
│       ├── tasks/
│       ├── meta/
│       ├── tests/
│       └── README.md
└── README.md
```

Guidelines:

- Keep plugin and role interfaces backward-compatible where practical.
- Add tests in `tests/` or in consuming repositories for non-trivial logic.
- Ensure plugin docstrings render correctly in `ansible-doc`.

Release process (high-level):

1. Update `galaxy.yml` and the changelog.
2. Tag the repository (for example `v0.1.0-common`).
3. Build and (optionally) publish:

   ```bash
   ansible-galaxy collection build
   ansible-galaxy collection publish hybridops-common-<version>.tar.gz
   ```

The full release workflow (version bumps, changelog updates, build, publish, and evidence capture) is documented in `MAINTAINERS.md` and ADR-0606.

---

## 9. Releases

This collection is versioned with Semantic Versioning and published to Ansible Galaxy as `hybridops.common`.

Contribution guidelines are documented in `CONTRIBUTING.md` in this repository.

For maintainers, the end-to-end release workflow (versioning, changelog updates, build, publish and evidence capture) follows the standard HybridOps.Studio collections process described in ADR-0606:

- [ADR-0606 – Ansible collections release process](https://docs.hybridops.studio/adr/ADR-0606-ansible-collections-release-process/)

---

## 10. Licence

- Code in this collection: **MIT-0**.  
- Documentation in this repository: **CC BY 4.0**.

Project-wide licence details are documented in the HybridOps.Studio platform repository.
