This role is the most specialized and opinionated of all. It can be used to
clone a bunch of repositories to /srv/workspace; it then tries to run either
`make` or `docker-compose up -d` in each of these repositories, which are
called "projects".

This is how my web "projects" are set up; typically, a project is a repository
with a Makefile which calls docker-compose in a bunch of sub-directories. This
feels like a lame hack, but has worked pretty well so far.
