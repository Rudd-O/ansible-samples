#!/usr/bin/python
# -*- coding: utf-8 -*-

# Ansible blockinfile module
#
# Licensed under GPL version 3 or later
# (c) 2014 YAEGASHI Takeshi <yaegashi@debian.org>
# (c) 2013 Evan Kaufman <evan@digitalflophouse.com>

import re
import os
import tempfile

DOCUMENTATION = """
---
module: blockinfile
author: YAEGASHI Takeshi
short_description: Insert/update/remove a text block
                   surrounded by marker lines.
version_added: 0.0
description:
  - 'This module will insert/update/remove a block of multi-line text
    surrounded by customizable marker lines
    (default: "# {BEGIN/END} ANSIBLE MANAGED BLOCK").
    Some functionality is taken from M(replace) module by Evan Kaufman.'
options:
  dest:
    required: true
    aliases: [ name, destfile ]
    description:
      - The file to modify.
  marker:
    required: false
    default: "# {mark} ANSIBLE MANAGED BLOCK"
    description:
      - The marker line template.
        "{mark}" will be replaced with "BEGIN" or "END".
  content:
    required: false
    default: ""
    description:
      - The text to insert inside the marker lines.
        If it's empty string, marker lines will also be removed.
  create:
    required: false
    default: "no"
    choices: [ "yes", "no" ]
    description:
      - Create a new file if it doesn't exist.
  backup:
    required: false
    default: "no"
    choices: [ "yes", "no" ]
    description:
      - Create a backup file including the timestamp information so you can
        get the original file back if you somehow clobbered it incorrectly.
  validate:
    required: false
    description:
      - validation to run before copying into place
    required: false
    default: None
  others:
    description:
      - All arguments accepted by the M(file) module also work here.
    required: false
"""

EXAMPLES = r"""
- blockinfile: dest=/etc/ssh/sshd_config content="Match User ansible-agent\nPasswordAuthentication no"

- blockinfile: |
    dest=/etc/network/interfaces backup=yes
    content="iface eth0 inet static
        address 192.168.0.1
        netmask 255.255.255.0"

- blockinfile: |
    dest=/var/www/html/index.html backup=yes
    marker="<!-- {mark} ANSIBLE MANAGED BLOCK -->"
    content="<h1>Welcome to {{ansible_hostname}}</h1>"
"""

def write_changes(module,contents,dest):

    tmpfd, tmpfile = tempfile.mkstemp()
    f = os.fdopen(tmpfd,'wb')
    f.write(contents)
    f.close()

    validate = module.params.get('validate', None)
    valid = not validate
    if validate:
        if "%s" not in validate:
            module.fail_json(msg="validate must contain %%s: %s" % (validate))
        (rc, out, err) = module.run_command(validate % tmpfile)
        valid = rc == 0
        if rc != 0:
            module.fail_json(msg='failed to validate: '
                                 'rc:%s error:%s' % (rc,err))
    if valid:
        module.atomic_move(tmpfile, dest)

def check_file_attrs(module, changed, message):

    file_args = module.load_file_common_arguments(module.params)
    if module.set_file_attributes_if_different(file_args, False):

        if changed:
            message += " and "
        changed = True
        message += "ownership, perms or SE linux context changed"

    return message, changed

def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(required=True, aliases=['name', 'destfile']),
            marker=dict(default='# {mark} ANSIBLE MANAGED BLOCK', type='str'),
            content=dict(default='', type='str'),
            create=dict(default='no', choices=BOOLEANS, type='bool'),
            backup=dict(default='no', choices=BOOLEANS, type='bool'),
            validate=dict(default=None, type='str'),
        ),
        add_file_common_args=True,
        supports_check_mode=True
    )

    params = module.params
    dest = os.path.expanduser(params['dest'])

    if os.path.isdir(dest):
        module.fail_json(rc=256, msg='Destination %s is a directory !' % dest)

    if not os.path.exists(dest):
        if not module.boolean(params['create']):
            module.fail_json(rc=257, msg='Destination %s does not exist !' % dest)
        contents = ''
    else:
        f = open(dest, 'rb')
        contents = f.read()
        f.close()

    mfunc = lambda x: re.sub(r'{mark}', x, params['marker'], 0)
    markers = tuple(map(mfunc, ("BEGIN", "END")))
    markers_escaped = tuple(map(lambda x: re.escape(x), markers))
    if params['content'] == '':
        repl = ''
    else:
        repl = '%s\n%s\n%s\n' % (markers[0], params['content'], markers[1])
    mre = re.compile('^%s\n(.*\n)*%s\n' % markers_escaped, re.MULTILINE)
    result = re.subn(mre, repl, contents, 0)
    if result[1] == 0 and repl != '':
        mre = re.compile('(\n)?\Z', re.MULTILINE)
        result = re.subn(mre, '\n%s' % repl, contents, 0)
    if result[1] > 0 and contents != result[0]:
        msg = '%s replacements made' % result[1]
        changed = True
    else:
        msg = ''
        changed = False

    if changed and not module.check_mode:
        if module.boolean(params['backup']) and os.path.exists(dest):
            module.backup_local(dest)
        write_changes(module, result[0], dest)

    msg, changed = check_file_attrs(module, changed, msg)
    module.exit_json(changed=changed, msg=msg)

# this is magic, see lib/ansible/module_common.py
#<<INCLUDE_ANSIBLE_MODULE_COMMON>>

main()

