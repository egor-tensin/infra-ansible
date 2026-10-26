This is a meta-role, it simply pulls in other roles as dependencies. It's used
for general maintenance of all my Debian-based cloud VMs.

* Whatever basic things the role "linux" does.
* Configure unattended upgrades.
* Set up firewall.
* Set up [linux-status], because I use it.

[linux-status]: https://github.com/egor-tensin/linux-status
