This role waits until cloud-init is done initializing an cloud VM.

This is supposed to be the first role in a playbook; facts gathering should be
disabled so that the role can handle connectivity issues.
