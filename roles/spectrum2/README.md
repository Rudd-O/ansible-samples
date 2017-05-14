# Spectrum2 IM transport for interoperability between XMPP and other protocols.

This Ansible role deploys a full [Spectrum2 IM](http://spectrum.im/) server on
your Fedora 25 (or higher) server.  Together with
[../prosodyxmpp/](the Prosody XMPP role), it gives you interoperability
between your XMPP server and many other non-XMPP protocols.

## Configuration details

See the file `defaults/main.yml` for more information on how to configure the
role from your playbook.  Note that you may have to configure your Ansible's
`hash_behavior` to `merge` dictionaries.

At the very minimum, you will have to:

* clone the `xmpp.services` subtree example
  rename the sample service from `SAMPLE_xmpp` to the subdomain you want for
  the Spectrum service, then 
  set up the `component_jid` and `component_password` variables.
  * The component JID is the full JID of the component as declared in your
    XMPP server configuration.
  * The component password is the password that corresponds to the component
    declared in your XMPP server configuration.
  * These two values must have been created in your XMPP server configuration
    prior to launching Spectrum via this role.
  * Check out the [../prosodyxmpp/](`prosodyxmpp` role) for an easy way to set
    up a compliant XMPP server with support for external components such as
    Spectrum. 

*Removing services:* defining a service's key contents to be `None`,
`False` or empty string causes the service to be stopped and removed
when the role is run.

## Setting up DNS for your gateway.

You need a DNS entry for the subdomain (`<service>.example.com`) if you
want to be able to log in to the Spectrum2 component.  Given that this role
is designed to run on the same machine as [../prosodyxmpp/](the `prosodyxmpp`
role), the DNS record should probably be a `CNAME` DNS entry pointing to your
XMPP server's `A` record.  See the `README.md` file for the `prosodyxmpp`
role for more information.
