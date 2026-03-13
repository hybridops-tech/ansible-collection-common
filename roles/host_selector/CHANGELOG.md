# Changelog

All notable changes to the **host_selector** role are documented here.  
This project follows **Semantic Versioning** and the **Keep a Changelog** format.

## [2.3.0] - 2025-09-08
### Added
- Improved Method B UX with columnised group listing in the interactive prompt for better readability.
- Refined Method C behaviour with consistent 1-based indexing and clearer user feedback on invalid selections.

### Changed
- Simplified and centralised input normalisation and validation logic across all selection methods to reduce edge-case handling in playbooks.

## [2.2.0] - 2025-09-07
### Added
- Method D for bulk selection of all infrastructure hosts, enabling fast “select everything” operations in controlled environments.
- Correlation ID (CID) logging integration with `env_guard`, ensuring that selection summaries and error messages can be traced to a specific execution context.

## [2.0.0] - 2025-08-30
### Added
- Method A for manual IP/hostname targeting (ad-hoc or emergency operations).
- Method B for group-based selection using existing Ansible inventory groups.
- Method C for hierarchical category/group selection to support exploratory workflows.
- Initial CID generation and environment validation hooks, designed to integrate with the Environment Guard Framework (EGF).

---

**Maintainer:** HybridOps.Studio
