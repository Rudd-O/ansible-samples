Sample Ansible playbooks
============================================

Here are a few sample playbooks.  These assume that you already have an
Ansible setup going.  You can then drop the files of the example
directly into your setup.

Roles:

* [roles/mailserver/](roles/mailserver/) sets up a mail server with Dovecot, Postfix,
   the SSL certificates you provide yourself, SPF, and the DKIM
   certificates that you create.
* [roles/jenkins/](roles/jenkins/) sets up a Jenkins server with a number of plugins.
* [roles/zfsupdates/](roles/zfsupdates/) aids you in keeping ZFS up to date on your
   Fedora system which boots from ZFS.
* [roles/updates/](roles/updates/) updates your system packages.
* [roles/distupgrade/](roles/distupgrade/) upgrades your Fedora machine to a newer
  release, taking appropriate recovery precautions.
* [roles/prosodyxmpp/](roles/prosodyxmpp/) sets up Prosody XMPP on your Fedora
  box, with up-to-date XEPS for use with modern XMPP clients.
* [roles/qubeskde/](roles/qubeskde/) sets up KDE on any Qubes OS dom0,
  since Qubes OS decided to stop shipping KDE in the dom0.
* [roles/install-package](roles/install-package/) deploys a package
  whether to a dom0 or a regular machine.

Modules:
* [library/gconf.py](library/gconf.py) changes GConf settings on GNOME desktops,
  both user settings and system-wide defaults.

See `README.md` files inside each directory, when they exist.

Licensing
---------

Everything under this repository is distributed under the GNU GPL v2
or later.
