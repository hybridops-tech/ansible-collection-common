# `hybridops.common`

Shared plugins and utility roles used across the HybridOps.Studio automation platform. The collection provides cross-cutting helpers for environment governance, connectivity checks, inventory utilities, and common tagging or metadata patterns.

Role- and plugin-level behaviour is documented in each role’s `README.md` and plugin docstrings.

High-level platform context is maintained at [docs.hybridops.studio](https://docs.hybridops.studio).

## Scope

- Plugins under `plugins/` (filters, lookups, modules, and module utilities) intended for reuse across `hybridops.*` collections.
- Utility roles for environment governance, connectivity checks, inventory helpers, and lightweight baseline preparation.

## Plugins

Representative plugin families:

- Filters for standard tag and label composition.
- Lookups for environment defaults and secret-friendly variable resolution.
- Module utilities for consistent results and metadata.
- Modules for structured debug and evidence-friendly output.

Exact plugin names and usage are documented via `ansible-doc` and repository sources.

## Roles

Key roles (see role-level READMEs for variables and examples):

| Role | Purpose |
|------|---------|
| `env_guard` | Environment governance and guardrail execution. |
| `connectivity_test` | Connectivity checks with structured outputs. |
| `gen_inventory` | Inventory generation helpers. |
| `host_selector` | Governed host targeting helpers. |
| `ip_mapper` | Environment-aware IP mapping helpers. |

## Requirements

- Ansible `ansible-core` 2.15+.
- Python 3.10+ on the control node.

Plugins execute on the control node and are consumed by playbooks and roles in other collections.

## Installation

Install from Ansible Galaxy:

```bash
ansible-galaxy collection install hybridops.common
```

Pin in `collections/requirements.yml`:

```yaml
collections:
  - name: hybridops.common
    version: ">=0.1.0"
```

## Usage

Example using a collection lookup and filter:

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

## Testing

- Role-local smoke tests should be provided under `roles/<role>/tests/`.
- Molecule scenarios may be provided where isolated validation is valuable.
- Platform integration tests are executed via HybridOps.Studio pipelines and lab inventories.

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)  
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the [HybridOps.Studio licensing overview](https://docs.hybridops.studio/briefings/legal/licensing/)
for project-wide licence details, including branding and trademark notes.
