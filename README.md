# `hybridops.common`

Shared plugins and reusable platform roles for HybridOps.

This collection carries the cross-cutting automation surface used across the current HybridOps runtime: environment guardrails, connectivity and inventory helpers, PostgreSQL service primitives, container runtime bootstrap, DNS and control-plane services, and VyOS-based WAN roles.

Role-level variables and assumptions are documented in each role's `README.md`. Broader operator guidance lives at [docs.hybridops.tech](https://docs.hybridops.tech).

## Scope

- Shared plugins under `plugins/` for use across `hybridops.*` collections.
- Reusable roles for platform governance, connectivity, inventory shaping, container/bootstrap services, DNS control, and WAN edge configuration.
- Control-node and target-node helpers intended to be consumed directly or through HybridOps modules and blueprints.

## Roles

| Role | Purpose |
|------|---------|
| `connectivity_test` | Connectivity checks with structured results. |
| `decision_service` | Deploy the decision service control-plane component. |
| `dns_routing` | Publish and update internal DNS routing records. |
| `docker_compose_stack` | Deploy Docker Compose based service stacks. |
| `docker_engine` | Install and configure Docker Engine. |
| `edge_observability` | Deploy edge observability services. |
| `env_guard` | Environment governance and guardrail execution. |
| `gen_inventory` | Inventory generation helpers. |
| `host_selector` | Governed host targeting helpers. |
| `ip_mapper` | Environment-aware IP mapping helpers. |
| `postgresql_service` | Install and configure standalone PostgreSQL service instances. |
| `powerdns_authority` | Deploy and manage authoritative PowerDNS service. |
| `vyos_edge_wan` | Configure Hetzner/GCP WAN edge behavior on VyOS. |
| `vyos_site_extension_edge` | Configure Hetzner-side site extension on VyOS. |
| `vyos_site_extension_onprem` | Configure on-prem site extension on VyOS. |

## Requirements

- Ansible `ansible-core` 2.15+
- Python 3.10+ on the control node

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

```yaml
- name: Install Docker Engine and deploy a compose stack
  hosts: service_hosts
  become: true
  collections:
    - hybridops.common

  roles:
    - role: hybridops.common.docker_engine
    - role: hybridops.common.docker_compose_stack
```

## Testing

- Role-local smoke tests are provided where isolated validation is useful.
- Platform integration is proven through HybridOps modules and blueprints in `hybridops-core`.

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)
- Documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the project licensing guidance at [docs.hybridops.tech](https://docs.hybridops.tech).
