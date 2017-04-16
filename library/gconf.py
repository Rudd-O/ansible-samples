#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Rudd-O.  GPLv2+.

import subprocess

DOCUMENTATION = """
---
module: gconf
author: Rudd-O
short_description: Deploy (currently only system-wide) gconf settings.
description:
  - This module will allow you to deploy gconf settings.
options:
  key:
    required: true
  value:
    required: false
    description:
      - Specify the value that the key should have.
        Only required when state=present.
  type:
    required: false
    description:
      - Specify the type of the value associated with the key.
        Only required when state=present.
  mode:
    required: false
    default: user
    choices: [ "user", "default" ] # "mandatory" not yet implemented
    description:
      - Specify "user" to change the user configuration belonging to
        the user that Ansible is logged in as, or "default" to change
        system-wide default configuration.
  state:
    required: false
    choices: [ "present", "absent" ]
    default: "present"
"""

EXAMPLES = r"""
- gconf:
    key: /apps/desktop/gnome/interface/can_change_accels
    state: present
    value: true
    type: boolean
    mode: default
"""

defaultmode = ["gconftool-2", "--direct",
               "--config-source",
               "xml:readwrite:/etc/gconf/gconf.xml.defaults"]
usermode = ["gconftool-2"]


def present(module, key, type_, value, mode):
    if value == "True" and type_ == "boolean":
        value = "true"
    elif value == "False" and type_ == "boolean":
        value = "false"
    elif not hasattr(value, "endswith"):
        value = str(value)
    changed = False
    msg = "Key %s is already at its desired value" % (key,)

    cmd = defaultmode if mode == "default" else usermode
    p = subprocess.check_output(cmd + ["--get", key])[:-1]
    if p != value:
        if not module.check_mode:
            p = subprocess.check_output(cmd + ["--type", type_,
                                               "--set", key,
                                               value])
        changed = True
        msg = "Key %s has been set to %s" % (key, value)
    module.exit_json(changed=changed, msg=msg)


def absent(module, key, mode):
    changed = False
    msg = "Key %s is already not set" % (key,)

    cmd = defaultmode if mode == "default" else usermode
    p = subprocess.check_output(cmd + ["--get", key])[:-1]
    if p != "":
        if not module.check_mode:
            p = subprocess.check_output(cmd + ["--unset", key,
                                               value])
        changed = True
        msg = "Key %s has been unset" % (key,)
    module.exit_json(changed=changed, msg=msg)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            key=dict(required=True),
            type=dict(required=False),
            value=dict(required=False),
            state=dict(default='present', choices=['present', 'absent']),
            mode=dict(default='user', choices=['user', 'default']),
        ),
        supports_check_mode=True
    )

    params = module.params
    if params["state"] == "present":
        if 'type' not in params:
            module.fail_json(msg='the "type" parameter is required when state is "present"')
        if 'value' not in params:
            module.fail_json(msg='the "value" parameter is required when state is "present"')
        present(module, params['key'], params['type'], params['value'], params['mode'])
    else:
        absent(module, params['key'], params['mode'])

        
# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *


main()
