# SELinux module configurator

This Ansible role deploys a `.te` (type enforcement) SELinux policy module
to a running server, and activates it.  Alternatively, with `state` set
to `disabled`, the specific module will be disabled.

## Variables

- `policy_file`: path to a local policy file (`.te`) that will be
  deployed to the server.  Files get deployed to
  `/etc/selinux/targeted/local`.  Alternatively, to do multiple
  files at once, use variable:
- `policy_files`: a list of paths to local policy files.  Mutually
  exclusive with `policy_file`.
- `state`: either `enabled` or `disabled` for the respective
  action w.r.t. the module.

The name of the module in the target system will be the same
name of the file (specifically, its basename), without the
`.te` extension.

## Generating and using a module

To generate a module, you can use the `audit2allow` program.

Then, deploy the generated `.te` file to your Ansible repository.

Then, install it with your playbook a follows (example):

    - name: do selinux workaround for NginX to Icecast
      include_role:
        name: selinux-module
      vars:
        policy_file: files/myplaybook/my-policy-module.te
        state: enabled
      tags:
      - selinux

## Caution

Ensure, prior to deploying a SELinux policy module, that another
module with the same name is not already loaded in the target
system.  You can find out which modules are loaded by using the
command `semodule -l` on the target system.
