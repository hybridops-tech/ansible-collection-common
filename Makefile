# purpose: Test wrapper for Molecule scenarios in hybridops.common collection
# adr: ADR-0606-ansible-collections-release-process
# maintainer: HybridOps.Studio

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

COLLECTION_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
ROLES_DIR       := $(COLLECTION_ROOT)/ansible_collections/hybridops/commons/roles

ROLE ?=

PIP_REQUIREMENTS    := $(COLLECTION_ROOT)/requirements.txt
GALAXY_REQUIREMENTS := $(COLLECTION_ROOT)/requirements.yml

MOLECULE_ROLES := $(shell \
  find "$(ROLES_DIR)" -mindepth 1 -maxdepth 1 -type d 2>/dev/null \
    | while read -r d; do \
        if [ -d "$$d/molecule/default" ]; then basename "$$d"; fi; \
      done \
)

ifeq ($(strip $(ROLE)),)
TEST_ROLES := $(MOLECULE_ROLES)
else
TEST_ROLES := $(ROLE)
endif

.PHONY: help
help:
	@echo "Targets:"
	@echo "  make deps              # install python + galaxy dependencies"
	@echo "  make deps-py           # install python dependencies (requirements.txt)"
	@echo "  make deps-galaxy       # install galaxy dependencies (requirements.yml)"
	@echo "  make test              # run molecule test for all roles with scenarios"
	@echo "  make test ROLE=<name>  # run molecule test for a single role"
	@echo ""
	@echo "Detected roles with Molecule scenarios:"
	@echo "  $(MOLECULE_ROLES)"

.PHONY: test
test:
	@if [ -z "$(strip $(TEST_ROLES))" ]; then \
	  echo "No roles with Molecule scenarios found under $(ROLES_DIR)"; \
	  exit 1; \
	fi; \
	for r in $(TEST_ROLES); do \
	  role_dir="$(ROLES_DIR)/$$r"; \
	  if [ ! -d "$$role_dir/molecule/default" ]; then \
	    echo "Skipping $$r (no molecule/default scenario)"; \
	    continue; \
	  fi; \
	  echo "==> molecule test for role: $$r"; \
	  cd "$$role_dir" && molecule test || exit $$?; \
	done

	.PHONY: deps deps-py deps-galaxy
deps: deps-py deps-galaxy ## Install python and galaxy dependencies

deps-py:
	@if [ -f "$(PIP_REQUIREMENTS)" ]; then \
	  python3 -m pip install -r "$(PIP_REQUIREMENTS)"; \
	else \
	  echo "No $(PIP_REQUIREMENTS) found; skipping pip dependencies."; \
	fi

deps-galaxy:
	@if [ -f "$(GALAXY_REQUIREMENTS)" ]; then \
	  ansible-galaxy role install -r "$(GALAXY_REQUIREMENTS)"; \
	else \
	  echo "No $(GALAXY_REQUIREMENTS) found; skipping galaxy dependencies."; \
	fi