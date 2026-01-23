# Changelog

All notable changes to the `hybridops.common` collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- No unreleased changes yet.

## [0.1.0] - 2026-01-02

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
- Shared plugin surface (filters, lookups, modules, `module_utils`) for HybridOps.Studio.
- Role-local `tests/` harnesses where appropriate.
- `galaxy.yml` metadata for namespace `hybridops` and collection name `common`.

[Unreleased]: https://github.com/hybridops-studio/ansible-collection-common/compare/v0.1.0-common...HEAD
[0.1.0]: https://github.com/hybridops-studio/ansible-collection-common/releases/tag/v0.1.0-common