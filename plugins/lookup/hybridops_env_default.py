DOCUMENTATION = r"""
name: hybridops_env_default
author: HybridOps.Tech
short_description: Read an environment variable with an optional default
description:
  - Returns the value of an environment variable.
  - If the variable is unset, returns the provided default value or an empty string.
options:
  _terms:
    description:
      - The environment variable name to read.
      - Optionally pass a second term as the default value.
    required: true
"""

EXAMPLES = r"""
- name: Read HYOPS_ENV or default to dev
  ansible.builtin.debug:
    msg: "{{ lookup('hybridops.common.hybridops_env_default', 'HYOPS_ENV', 'dev') }}"

- name: Read HOME without a default
  ansible.builtin.debug:
    msg: "{{ lookup('hybridops.common.hybridops_env_default', 'HOME') }}"
"""

RETURN = r"""
_raw:
  description:
    - The resolved environment variable value.
  type: list
  elements: str
"""

import os
from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if len(terms) == 0:
            raise AnsibleError("hybridops_env_default requires at least one term (variable name)")

        var_name = str(terms[0])
        default = str(terms[1]) if len(terms) > 1 else ""

        value = os.getenv(var_name, default)
        return [value]
