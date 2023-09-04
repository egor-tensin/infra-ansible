This role configures iptables rules in /etc/iptables/rules.v{4,6}, to be used
by iptables-persistent.

I found it easier and more flexible to configure a firewall this way; for
example, I found that cloud provider's firewalls are often less flexible.
iptables frontends like ufw, on the other hand, are hard to make work with
Docker.
