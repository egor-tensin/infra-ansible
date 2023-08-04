infra-ansible
=============

Some common Ansible roles used by me to manage things.

Usage
-----

requirements.yml:

```
collections:
  - source: https://github.com/egor-tensin/infra-ansible.git
    type: git
    version: master # Or a git tag
```

```
$ ansible-galaxy install -r requirements.yml
```

Then you can use roles in your playbook:

```
- name: Test playbook
  hosts: all
  roles:
    - tensin.infra.apt
    - tensin.infra.journald
    ...
```

License
-------

Distributed under the MIT License.
See [LICENSE.txt] for details.

[LICENSE.txt]: LICENSE.txt
