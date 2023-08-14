This role configures a WireGuard interface using wireguard-tools and the
wg-quick systemd service.

It accepts the interface name, the private key and a list of peers; see the
template file to discover what parameters are supported. I use it to set up all
of my WireGuard servers.
