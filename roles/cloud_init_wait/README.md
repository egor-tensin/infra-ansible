This role is used to wait until cloud-init is done initializing an instance.
This is supposed to be the first role in a playbook; it is advisable to disable
facts gathering so that the playbook can wait until a connection is
established.
