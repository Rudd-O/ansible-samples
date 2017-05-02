# Complete XMPP server with updated support for modern XEPs — ideal for Conversations

This Ansible role deploys a full Prosody XMPP server on your Fedora 25
(or higher) server.  It also deploys a number of modules to make the operation
of the server most battery-optimized and compatible with [excellent features of
modern chat clients such as
Conversations](https://github.com/siacs/Conversations/blob/master/README.md#xmpp-features),
including:

* [push support](https://github.com/siacs/Conversations#how-do-xep-0357-push-notifications-work) to greatly minimize idle battery use (via module `cloud_notify`);
* [stream management](https://xmpp.org/extensions/xep-0198.html) to improve operation in flaky connectivity (via module `smacks`);
* [message archive management](https://xmpp.org/extensions/xep-0313.html) to receive queued messages after network changes (via module `smacks`);
* [HTTP file upload](https://xmpp.org/extensions/xep-0363.html) to support (end-to-end encrypted) file transfer to (even offline) users (via module `http_upload`);
* [message carbons](https://xmpp.org/extensions/xep-0280.html) to get messages across all your devices (via module `carbons`);
* [client state indication](https://xmpp.org/extensions/xep-0352.html) for superior battery life (via module `csi`);
* [simple blocking](https://xmpp.org/extensions/xep-0191.html) to make it easy to block annoying people (via module `blocking`);
* and more!

This is the [compliance tester](https://github.com/iNPUTmice/ComplianceTester#usage)
result for a server configured with the defaults this role ships with,
and whose DNS server is configured according to the recommendations in
this guide:

```
Use compliance suite 'Conversations Compliance Suite' to test example.com

Server is Prosody 0.9.12
running XEP-0115: Entity Capabilities…		PASSED
running XEP-0163: Personal Eventing Protocol…		PASSED
running Roster Versioning…		PASSED
running XEP-0280: Message Carbons…		PASSED
running XEP-0191: Blocking Command…		PASSED
running XEP-0045: Multi-User Chat…		FAILED
running XEP-0198: Stream Management…		PASSED
running XEP-0313: Message Archive Management…		PASSED
running XEP-0352: Client State Indication…		PASSED
running XEP-0363: HTTP File Upload…		PASSED
running XEP-0065: SOCKS5 Bytestreams (Proxy)…		PASSED
running XEP-0357: Push Notifications…		PASSED
running XEP-0368: SRV records for XMPP over TLS…		PASSED

passed 12/13
```

## Configuration details

See the file `defaults/main.yml` for more information on how to configure the
role from your playbook.  Note that you may have to configure your Ansible's
`hash_behavior` to `merge` dictionaries.

At the very minimum, you will have to:

* define the `ssl` tree of settings for the domain you will run — the keys of
  the `ssl` tree define the domain name of your server;
* add a few JIDs with their initial passwords under `xmpp.jids`.

## Prerequisites

### Firewall notes

You will need to open TCP ports on the machine that will act as XMPP server:

* 5000
* 5222
* 5223
* 5269
* 5281

### SELinux notes

This role works out of the box with SELinux policy as it ships in Fedora.

Changes to any of the three default ports in variables `xmpp.ports.*` will
likely cause Prosody to fail to listen to said ports.  You will have to add a
type enforcement exception for your desired port.

Consult role `selinux-module` in this repo for more information on how to
add exceptions for services.

### SSL notes

See the instructions for the `mailserver` role in this repo to understand how
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
_xmpp-client._tcp       IN SRV 0 5 5222 xmpp.example.com.
_xmpp-server._tcp       IN SRV 0 5 5269 xmpp.example.com.
_xmpps-client._tcp       IN SRV 5 5 5223 xmpp.example.com.
.
.
.
```

Of course, if you set any of the `xmpp.ports.*` variables to `False`
(which disables the use of the port set to `False`), then remove
the corresponding DNS record for that port.  Correspondingly, if you change
any of these ports, you should adjust your DNS configuration to match.

See https://prosody.im/doc/dns for more information on the matter.

## Usage

Check you have met the prerequisites.

Create a playbook that includes this role.

In that playbook, override the default variables available in
`defaults/main.yml` with variables of your own that make sense for
your use case.

Then simply run your new playbook against your intended Fedora server.
