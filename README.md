Sample Ansible playbooks
============================================

Here are a few sample playbooks.  These assume that you already have an
Ansible setup going.  You can then drop the files of the example
directly into your setup.

* [mailserver/](mailserver/) sets up a mail server with Dovecot, Postfix,
   the SSL certificates you provide yourself, SPF, and the DKIM
   certificates that you create.  See `vars/mail.yml` inside this
   directory for instructions on domains, users, host names,
   SSL and DKIM.
* [jenkins/](jenkins/) sets up a Jenkins server with a number of plugins.

Licensing
---------

Everything under this repository is distributed under the GNU GPL v2
or later.
