This role waits for a file to be present on a host.

This weird and extremely convoluted way to wait until a file exists
(disregarding reboots) was borrowed from RedHat themselves:

    https://www.ansible.com/blog/tolerable-ansible
