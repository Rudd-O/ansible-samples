# Complete XMPP server with updated support for modern XEPs — ideal for Conversations

This Ansible role deploys a full Prosody XMPP server on your Fedora 25
(or higher) server.  It also deploys a number of modules to make the operation
of the server most compatible with [excellent features of modern chat clients
such as Conversations](https://github.com/siacs/Conversations/blob/master/README.md#xmpp-features).

See the file `defaults/main.yml` for more information on how to configure the
role from your playbook.  Note that you may have to configure your Ansible's
`hash_behavior` to `merge` dictionaries.

## Prerequisites

### Firewall notes

You will need to open TCP ports on the machine that will act as XMPP server:

* 5000
* 5222
* 5269
* 5281

### SSL notes

See the instructions for the mailserver recipe in this repo to understand how
to configure the SSL certificates for your XMPP server.

The SSL certificate must be for the "virtual domain" of your server, not for
the hostname or IP of the actual machine that will run the XMPP service.
See https://prosody.im/doc/certificates for more information on that.

### DNS notes

You will need to add DNS records for your client to find the server.

Assuming your server (and the SSL certificate) are `example.com`, here is a
good example of how the DNS records in the `example.com` zone file would look like:

```
$ttl	38400
@	IN	SOA	ns1.example.com. example.example.com. (
			2017020603
			1800
			1800
			604800
			1800 )

			IN	NS  ns1.example.com.
			IN	NS  ns1.backupdns.com.
			
			IN	A   1.2.3.4

.
.
.

xmpp                    IN  A       1.2.3.4
_xmpp-client._tcp 18000 IN SRV 0 5 5222 xmpp.example.com.
_xmpp-server._tcp 18000 IN SRV 0 5 5269 xmpp.example.com.
_xmpps-client._tcp 18000 IN SRV 0 5 5222 xmpp.example.com.
_xmpps-server._tcp 18000 IN SRV 0 5 5269 xmpp.example.com.
.
.
.
```

See https://prosody.im/doc/dns for more information on the matter.

## Usage

Check you have met the prerequisites.

Create a playbook that includes this role.

In that playbook, override the default variables available in
`defaults/main.yml` with variables of your own that make sense for
your use case.

Then simply run your new playbook against your intended Fedora server.
