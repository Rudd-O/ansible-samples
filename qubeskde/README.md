# Install KDE on your Qubes OS system

This Ansible playbook installs KDE on your Qubes OS dom0, and performs
a few fixes that are necessary for KDE to work properly under Qubes OS.

## Instructions

Enable Ansible Qubes on your Qubes OS system, as per [the instructions found
here](https://github.com/Rudd-O/ansible-qubes/blob/master/doc/Enhance%20your%20Ansible%20with%20Ansible%20Qubes.md).  Ensure that the step *Allow `managevm` to
manage `dom0`* is followed.

Now, from your VM where Ansible is set up and ready to fire, add:

```
dom0 ansible_connection=qubes
```

to your Ansible `hosts` file.

You are now ready to fire.  Run the playbook `role-qubeskde.yml` — it will
deploy KDE on your `dom0`.

After this, simply log off.

At the login screen, select *Plasma* using the top-right corner session
selector.  Then finish logging in.

That's all!
