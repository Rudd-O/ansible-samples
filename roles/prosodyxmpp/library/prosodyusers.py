#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2017, Rudd-O.  GPLv2+.

import errno
import glob
import os
import re
import subprocess
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote


DOCUMENTATION = """
---
module: prosodyusers
author: Rudd-O
short_description: manage Prosody users.
description:
  - This module allows you to manage Prosody users on a server.
options:
  jids:
    required: true
"""

EXAMPLES = ""


def process(module, jids):
    changed = False
    rets = {"changed": False, "msg": []}
    for jid, password in jids.items():
        accts = glob.glob("/var/lib/prosody/*/accounts/*.dat")
        accts = [unquote(s[len("/var/lib/prosody/"):-4]) for s in accts]
        accts = [(x.split(os.path.sep)[0], x.split(os.path.sep)[-1]) for x in accts]
        user, domain = jid.split("@", 1)
        exists = False
        for existing_domain, existing_user in accts:
            if existing_domain == domain and existing_user == user.lower():
                exists = True
        if password not in (None, "None", "") and not exists:
            if not module.check_mode:
                cmd = ["prosodyctl", "adduser", jid]
                p = subprocess.Popen(cmd,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
                stdout, _ = p.communicate(("%s\n%s\n" % (password, password)).encode("utf-8"))
                ret = p.wait()
                if ret != 0:
                    if stdout == b"That user already exists\n":
                        cmd = ["prosodyctl", "passwd", jid]
                        p = subprocess.Popen(cmd,
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT)
                        stdout, _ = p.communicate(("%s\n%s\n" % (password, password)).encode("utf-8"))
                        ret = p.wait()
                        if ret != 0:
                            module.fail_json(rc=ret, msg="While running %s: %s" % (cmd, stdout))
                        else:
                            rets['changed'] = True
                            rets['msg'].append("changed password of account %s@%s" % (user, domain))
                    else:
                        module.fail_json(rc=ret, msg="While running %s: %s" % (cmd, stdout))
                else:
                    rets['changed'] = True
                    rets['msg'].append("created new account %s@%s" % (user, domain))
        elif password in (None, "None", "") and exists:
            if not module.check_mode:
                cmd = ["prosodyctl", "deluser", jid]
                p = subprocess.Popen(cmd,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
                stdout, _ = p.communicate(("%s\n%s\n" % (password, password)).encode("utf-8"))
                ret = p.wait()
                if ret != 0:
                    module.fail_json(rc=ret, msg="While running %s: %s" % (cmd, stdout))
            rets['changed'] = True
            rets['msg'].append("deleted account %s@%s" % (user, domain))
    if rets['msg']:
        rets['msg'] == ", ".join(rets['msg'])
    else:
        rets['msg'] == "Nothing to do"
    module.exit_json(**rets)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            jids=dict(required=True, type="raw"),
        ),
        supports_check_mode=True
    )

    params = module.params
    jids = params["jids"]
    process(module, jids)


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *


main()
