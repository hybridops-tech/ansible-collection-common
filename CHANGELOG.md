# Changelog

All notable changes to the `hybridops.common` collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `vyos_site_extension_onprem` can now derive consumer SNAT source and
  destination CIDRs from state-backed cloud prefixes and static route prefixes.
- `vyos_site_extension_onprem` can now derive the consumer SNAT translation
  address from `onprem_router_id` when that is the intended edge translation
  address.

## [0.1.5] - 2026-03-14

### Changed

- Prepared the collection runtime inside CI before direct `ansible-lint` so smoke playbooks resolve `hybridops.common` consistently on GitHub runners.

### Fixed

- Completed the remaining fatal lint and metadata issues that were still surfacing after the previous Galaxy cut.
- Corrected the changelog compare links to the `hybridops-tech` repository namespace.

## [0.1.4] - 2026-03-13

### Changed

- Tightened the release surface for the published control-plane roles and collection metadata.
- Cleaned the CI and lint path so release branches validate consistently before Galaxy publish.

## [0.1.3] - 2026-03-13

### Fixed

- Added lookup-plugin documentation for `hybridops_env_default` so Galaxy import can inspect the collection cleanly.
- Added missing role root READMEs for the live PowerDNS and VyOS WAN/site-extension roles.

## [0.1.2] - 2026-03-10

### Changed

- Added repository-local `yamllint` configuration so release and CI checks run consistently.
- Normalized YAML in the live WAN and site-extension roles to keep Galaxy release branches lint-clean.

## 0.1.0 - 2026-01-02

### Added

- Initial publication of the `hybridops.common` collection.
- Core shared roles:
  - `connectivity_test`
  - `env_guard`
  - `gen_inventory`
  - `host_selector`
  - `ip_mapper`
  - `linux_harden_ssh`
  - `linux_user_management`
- Shared plugin surface (filters, lookups, modules, `module_utils`) for HybridOps.Tech.
- Role-local `tests/` harnesses where appropriate.
- `galaxy.yml` metadata for namespace `hybridops` and collection name `common`.

[Unreleased]: https://github.com/hybridops-tech/ansible-collection-common/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/hybridops-tech/ansible-collection-common/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/hybridops-tech/ansible-collection-common/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/hybridops-tech/ansible-collection-common/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/hybridops-tech/ansible-collection-common/compare/v0.1.1...v0.1.2
