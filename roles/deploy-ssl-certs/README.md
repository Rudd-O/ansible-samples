# Deploy SSL certificates

This Ansible playbook deploys sets of SSL certificates to a server, following
best practices.

## Usage

Here is how you use this role in an example playbook:

```yaml
- hosts: mywebserver
  become: True
  vars:
    ssl:
      example.com:
        key:           '{{ lookup("file", "secrets/example.com.key") }}'
        intermediates:
          - '{{ lookup("file", "secrets/example.com.ca-bundle") }}'
        certificate:   '{{ lookup("file", "secrets/example.com.crt") }}'
  tasks:
  - name: deploy SSL certificates
    include_role:
      name: deploy-ssl-certs
  - name: visualize SSL certificate path
    debug: msg='The path to the deployed certificate is {{ sslconf['example.com'].certificate.path }}'
```

See the file `defaults/main.yml` for more information on how to configure the
role from your playbook.  Note that you may have to configure your Ansible's
`hash_behavior` to `merge` dictionaries.

## Results

The results of the deployment are stored in the variable
`sslconf` which you can use in later stages of your playbook.  Said variable
looks like this:

```
changed: <boolean, whether the deployment changed at all>
result:
  <domain>:
    key:
      path: <path to created key file>
    certificate:
      path: <path to created certificate file>
    assembled_certificate:
      path: <path to certificate bundled with intermediaries>
```
