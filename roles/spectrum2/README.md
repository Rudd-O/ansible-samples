# Spectrum2 IM transport for interoperability between XMPP and other protocols.

This Ansible role deploys a full [Spectrum2 IM](http://spectrum.im/) server on
your Fedora 25 (or higher) server.  Together with
[../prosodyxmpp/](the Prosody XMPP role), it gives you interoperability
between your XMPP server and many other non-XMPP protocols.

## Setup

This is an Ansible role with many variables.

See the file `defaults/main.yml` for more information on how to configure the
role from your playbook.  Note that you may have to configure your Ansible's
`hash_behavior` to `merge` dictionaries.

### Configuration details

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

Once you're satisfied with the configuration, then apply the role to
your XMPP server.

### Setting up DNS for your gateway.

You need a DNS entry for the subdomain (`<service>.example.com`) if you
want to be able to log in to the Spectrum2 component.  Given that this role
is designed to run on the same machine as [../prosodyxmpp/](the `prosodyxmpp`
role), the DNS record should probably be a `CNAME` DNS entry pointing to your
XMPP server's `A` record.  See the `README.md` file for the `prosodyxmpp`
role for more information.

## Using the transport

Most clients don't support registering with transports, though they will
operate normally once you've registered.  Fortunately, there are some
which do support registering with the transport.  Let's see how.

Using a compliant client like Gajim, log onto your XMPP account as usual.

Then, open the *Discover services* dialog.  You will see the transport listed
there.

Register with the transport now.  It will prompt you for the credentials of
the service you're planning to log onto.

For example, if you're logging to Google Hangouts, you'll want to specify
your `@gmail.com` address as the XMPP JID, and your Google password.
If you are using Google, ensure you have either activated
*Allow less secure apps*, or created an application password specific
for the transport.  Also make sure to pay attention to your Gmail inbox,
as Google may decide it doesn't accept the IP address from where the
transport is logging on.  If that happens, tell Google it's fine, then
log out of your XMPP server, and then log into it again in 15 minutes.
You should receive a notification that your Google Hangouts contacts
are being added to your XMPP account's roster.

That's it!
