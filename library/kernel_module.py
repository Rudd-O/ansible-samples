#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Rudd-O.  GPLv2+.

import errno
import re
import subprocess


DOCUMENTATION = """
---
module: module
author: Rudd-O
short_description: Load kernel modules now and on boot
description:
  - This module will allow you configure kernel module load.
options:
  name:
    required: true
  state:
    required: false
    choices: [ "loaded" ]
    default: "loaded"
"""

EXAMPLES = r"""
- kernel_module:
    name: uinput
    state: loaded
"""

def loaded(module, name):
    sanitized = re.sub(r'\W+', '', name)
    sanitized = "/etc/modules-load.d/%s.conf" % sanitized
    try:
        f = file(sanitized)
        text = f.read()
        f.close()
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        text = ""
    changed = False
    msg = "Nothing to do"
    if text != name:
        if not module.check_mode:
            p = subprocess.Popen(["modprobe", "--", name],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            out = p.communicate()[0].strip()
            ret = p.wait()
            if ret != 0:
                return module.fail_json(rc=ret, msg=out)
            f = file(sanitized, "wb")
            f.write(name)
            f.close()
            os.chmod(sanitized, 0644)
        changed = True
        msg = "%s created" % sanitized
    module.exit_json(changed=changed, msg=msg)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            state=dict(default='loaded', choices=['loaded']),
        ),
        supports_check_mode=True
    )

    params = module.params
    name = params["name"]
    if params["state"] == "loaded":
        loaded(module, name)

        
# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *


main()
