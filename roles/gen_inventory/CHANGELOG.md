# Changelog

All notable changes to the **gen_inventory** role are documented here.  
This project follows **Semantic Versioning** and the **Keep a Changelog** format.

## [2.1.0] - 2025-09-01
### Added
- Environment-aware inventory generation with support for `dev`, `staging`, and `prod` tiers.
- Governance integration with `env_guard`, requiring a validated environment before inventories are generated.
- Placeholder IP model (`XX.XX.XX.00`) for security-by-design, ensuring no real IP addresses are committed to version control.
- Host naming conventions and group structures suitable for hybrid and multi-site topologies.

### Changed
- Consolidated inventory generation logic into a single role to reduce duplication across playbooks.
- Documentation updated to emphasise that this role is primarily a **bridge helper** for environments without NetBox or another IPAM source.

### Deprecated
- Direct use of `gen_inventory` as a long-term source of truth for production inventories.
  - For new platforms, prefer a **NetBox-first** design with dynamic inventory, and treat this role as an optional bootstrap or demo helper.

## [2.0.0] - 2025-08-20
### Added
- Initial release of the `gen_inventory` role:
  - Generation of static inventories from environment profiles.
  - Basic group structures for servers and network infrastructure.
  - Integration points for downstream roles such as `host_selector`, `ip_mapper`, and `connectivity_test`.

---

**Maintainer:** HybridOps.Studio
