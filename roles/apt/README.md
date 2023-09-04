This role upgrades packages on Debian/Ubuntu and installs any additional
packages.

* Upgrade all installed packages (apt dist-upgrade).
* Clean up dependencies that are no longer needed (apt autoremove).
* Optionally, install any additional apt packages required on this host.
* Optionally, configure unattended-upgrades to install latest security fixes.
