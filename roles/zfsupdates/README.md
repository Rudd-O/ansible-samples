# Maintain your ZFS updated

This Ansible role installs ZFS on your Fedora system, and makes sure that
the ZFS packages on your system are always up-to-date, down to the contents
of the initial RAM disks that are necessary to boot from a ZFS root file
system.  It takes care of a few steps that normal DNF update does not:

* Setting up DNF to keep old kernel-devel packages installed.
* Wiping old DKMS-built modules and refreshing them with the new
  ZFS modules shipped with the ZFS updates.
* Regenerating the initial RAM disks so they will contain ZFS and your
  system will boot reliably from a ZFS root.

The updated packages are fetched from the official
[ZFS on Linux repo](https://github.com/zfsonlinux/zfs/wiki/Fedora).

This playbook is ideal to keep systems built by
[zfs-fedora-installer](https://github.com/Rudd-O/zfs-fedora-installer)
up-to-date, and I myself use it for that.

## Instructions

Preparation:

1. [Build and install the `grub-zfs-fixer` package on your target Fedora system](https://github.com/Rudd-O/zfs-fedora-installer/tree/master/grub-zfs-fixer).  You can skip this step if your system was deployed using the `zfs-fedora-installer` system, as that system already performs this step.

Usage:

Every time you want to update ZFS on your target system, run this role against it.

If you have another playbook that perform system updates, make sure to include this role as follows:

```
...
...

- include_role:
    name: zfsupdates
  vars:
    deployzfs_stage: one

- name: task that updates your system
  package: name=* state=latest

- include_role:
    name: zfsupdates
  vars:
    deployzfs_stage: one

...
...
```

That's all!
