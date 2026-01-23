# Contributing to `hybridops.common`

`hybridops.common` provides shared plugins and utility roles used across the HybridOps.Studio platform, including:

- Environment guards and connectivity checks.
- Inventory and host-selection helpers.
- Common Linux baselines and account management.

These roles and plugins are used heavily in CI, runbooks, and HOWTOs, so changes here can have wide impact.

---

## 1. Contribution scope

Good fits for this collection:

- Improvements to roles such as:
  - `connectivity_test`
  - `env_guard`
  - `gen_inventory`
  - `host_selector`
  - `ip_mapper`
  - `linux_harden_ssh`
  - `linux_user_management`
- New generic helpers that are **not** tied to a specific business domain.
- Enhancements to filters, lookups, and modules under `plugins/`.

Avoid adding platform-specific business logic here — that belongs in collections such as `hybridops.app` or `hybridops.network`.

---

## 2. Development workflow

1. **Fork and branch**

   - Fork the repository.
   - Create a topic branch: `feature/<short-description>` or `fix/<short-description>`.

2. **Local setup**

   - Use a Python and `ansible-core` version compatible with `requirements.txt`.
   - Install dependencies:

     ```bash
     python3 -m venv .venv
     . .venv/bin/activate
     pip install -r requirements.txt
     ```

3. **Make your change**

   - Keep helpers generic and reusable across environments.
   - Ensure plugins behave well in both CI and ad-hoc playbooks.
   - Preserve existing interfaces where possible; if you must introduce a breaking change, call it out clearly in the pull request and in `CHANGELOG.md`.

4. **Run tests**

   - For roles:

     ```bash
     cd ansible_collections/hybridops/common/roles/<role_name>
     ansible-playbook -i tests/inventory.example.ini tests/smoke.yml
     ```

   - For plugins (filters, lookups, modules):
     - Add or update tests where appropriate.
     - Validate with `ansible-playbook` and any existing harnesses.

   - From the shared `ansible-galaxy-hybridops` workspace, integration tests can also exercise these helpers:

     ```bash
     make venv.refresh
     make test ROLE=connectivity_test
     ```

5. **Open a pull request**

   - Explain what changed and why.
   - Describe how you tested the change.
   - Highlight any impact on other collections or CI jobs.

---

## 3. Expectations for roles and plugins

Roles should:

- Provide a minimal test harness:
  - `tests/smoke.yml`
  - `tests/inventory.example.ini`
- Document key variables and assumptions in role-level `README.md` files where necessary.

New plugins should:

- Be documented via clear docstrings and, where helpful, examples in the README.
- Have simple tests or usage examples so behaviour is easy to understand.

`hybridops.common` is the toolbox for other collections — favour clarity, stability, and predictable behaviour over cleverness.

---

## 4. Style and quality

- Maintain idempotency wherever practical.
- Avoid hard-coding inventory group names, hostnames, or environment-specific details.
- Keep comments concise and focused on non-obvious behaviour or design decisions.
- Use the linting and formatting tools configured in this repository (`pre-commit`, `yamllint`, `ansible-lint`, etc.) before opening a pull request.

---

## 5. Security and secrets

- Do not commit secrets, tokens, or environment-specific endpoints.
- Design helpers to consume secrets via variables, Ansible Vault, or environment variables — never hardcoded values.
- Avoid logging sensitive information in debug output or task messages.