This role installs certbot and requests certificates from Let's Encrypt.

It uses the [DNS-01 challenge type] instead of the usual thing where it puts
a file in your web server's root directory. That way, you don't need to launch
the web server at all to obtain the certificates; most often, the configured
web server would fail to start at all at first launch since the certificates
are missing.

[DNS-01 challenge type]: https://letsencrypt.org/docs/challenge-types/

Using the DNS challenge, the certificates are obtained before starting the web
server for the first time, which avoids tinkering with its configuration. It
does come with some downsides: namely, this role explicitly uses certbot's
DigitalOcean plugin, (because I use DO for my domains); and the access token is
stored in a .ini file in /root.

This role prompts for token; set it in the `DIGITALOCEAN_TOKEN` environment
variable to disable the prompt.
