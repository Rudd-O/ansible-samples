# Spectrum2 IM transport for interoperability between XMPP and other protocols.

This Ansible role deploys a full [Spectrum2 IM](http://spectrum.im/) server on
your Fedora 25 (or higher) server.  Together with
[the Prosody XMPP role](../prosodyxmpp/), it gives you interoperability
between your XMPP server and many other non-XMPP protocols.

## Setup

### The basics

This software works in concert with an XMPP server to provide gateway services
to other IM and non-IM services:

* Your XMPP server runs normally on a machine.
* This role deploys the Spectrum2 frontend and backends.
* The Spectrum2 frontend that gets deployed connects
  to your XMPP Server.
* The Spectrum2 backends (services, see below) connect to
  the Spectrum2 frontend.
* The Spectrum2 frontend mediates the communications between its
  own backends and your XMPP server, presenting those backends as
  *services* (also known as *transports*) to your XMPP server.
* You — the end user — gain the ability to use those services
  right from your XMPP client.

```
---------------         ---------------
| Your client |  ---->  | XMPP server |
---------------         ---------------
                               |
                               v
                        ---------------
                        |  Spectrum2  |
         /------------  |  frontend   |
         |              ---------------
         |                     |
         v                     v
   --------------       ---------------
   |  Spectrum2 |       |  Spectrum2  |
   |   backend  |       |   backend   |
   --------------       ---------------
          |                    |
          v                    v
   --------------       ---------------
   |   Google   |       |   Twitter   |
   |  Hangouts  |       |             |
   --------------       ---------------
```

This role is in charge of setting up the Spectrum2 frontend and the Spectrum2
backends of your choice.  After that, you are in charge of registering your
accounts with the running backends (see usage instructions below).

### Configuration details

See the file `defaults/main.yml` for more information on how to configure the
role from your playbook.  Note that you may have to configure your Ansible's
`hash_behavior` to `merge` dictionaries.

At the very minimum, you will have to:

* clone the `xmpp.services` subtree example, then
* rename the sample service from `SAMPLE_xmpp` to the subdomain you want for
  the Spectrum service, then
* set up the `component_jid` and `component_password` variables.
  * The component JID is the full JID of the component as declared in your
    XMPP server configuration.
  * The component password is the password that corresponds to the component
    declared in your XMPP server configuration.
  * These two values must have been created in your XMPP server configuration
    prior to launching Spectrum via this role.
  * Check out the [`prosodyxmpp` role](../prosodyxmpp/) for an easy way to set
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
is designed to run on the same machine as [the `prosodyxmpp`
role](../prosodyxmpp/), the DNS record should probably be a `CNAME` DNS entry pointing to your
XMPP server's `A` record.  See the `README.md` file for the `prosodyxmpp`
role for more information.

## Using the transports

Most clients don't support registering with transports, though they will
operate normally once you've registered.  Fortunately, there are some
which do support registering with the transport.  Let's see how.

Using a compliant client like Gajim, log onto your XMPP account as usual.

Then, open the *Discover services* dialog.  You will see the transport listed
there.

Register with a transport now.  It will prompt you for the credentials of
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

Repeat the same process for the other transports.

That's it!
