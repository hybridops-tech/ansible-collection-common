# Changelog

All notable changes to the `hybridops.common.connectivity_test` role are documented in this file.

## [0.2.1] - 2026-01-04

### Added
- Enriched `test_results` payload and artefacts with:
  - `os_family` to align connectivity evidence with CI smoke outputs.
  - `inventory_group` so downstream jobs can see which inventory slice a host came from.
- Documented these additional fields in the role README alongside existing CID and environment attributes.

### Changed
- Tightened defaults and examples around CID usage to emphasise inheritance from `env_guard` or environment variables.
- Clarified README positioning of the role within the Environment Guard Framework (EGF) pipeline and the canonical logs tree.

## [0.2.0] - 2026-01-03

### Changed
- Moved connectivity logs under the canonical evidence tree:
  - `output/logs/ansible/connectivity_logs/<run_id>/…`
  instead of role-local paths, to align with the wider HybridOps.Tech output layout.
- Normalised project-root discovery in `defaults/main.yml` to support execution from:
  - platform CI playbooks (`deployment/ci/playbooks/...`), and
  - collection-local role tests (`roles/.../tests`).
- Consolidated logging configuration under the `connectivity.paths` and `connectivity.audit` structure while keeping legacy keys (`timeout`, `log_directory`, `report_filename`, `csv_filename`, `jsonl_filename`) for backwards compatibility.
- Standardised variable names (`connectivity_timeout`, `connectivity_use_cid`, etc.) to avoid reserved names and improve readability.

### Added
- Centralised result writer (`save_results.yml`) that:
  - aggregates per-host `test_results` into a single structure; and
  - writes both JSON (pretty) and JSONL (one-event-per-line) artefacts per run.
- `set_stats` publishing of:
  - `connectivity_logs_root`
  - `connectivity_run_id`
  - `connectivity_run_dir`
  - `connectivity_json_path`
  - `connectivity_jsonl_path`
  for CI pipelines and external evidence collectors.
- Hardened smoke test flow that:
  - runs the role against `cicd_test` targets; and
  - validates artefact presence and copies them into `tests/output/<run_id>` for local inspection.
- CID-aware defaults so that, when a correlation ID is provided (for example from `env_guard` or environment variables), it is propagated into the connectivity result payloads.

## [0.1.0] - 2025-09-09

### Added
- Initial implementation of the `connectivity_test` role with multi-protocol checks:
  - ICMP
  - SSH
  - Telnet
  - HTTP
  - HTTPS
- Per-host result compilation (`compile_results.yml`) producing a normalised `test_results` fact including:
  - target hostname and IP
  - per-protocol success booleans
  - UTC timestamp
  - operator identity (`tested_by`).
- First JSON and JSONL artefact generation under a role-local logs directory, together with a summary debug line per host for quick CLI inspection.
