# `lockss-installer` Release Notes

## Changes Since LOCKSS Installer version 2.0-alpha3

### Features

*   Switched MicroK8s Kubernetes to K3s Kubernetes.
*   Support alternative Kubernetes installs.
*   Add script to remove MicroK8s install.
*   Add script to bring up a local Kubernetes dashboard.
*   Enable SSL LCAP if keystores and password found in `~lockss/config/keys`.
*   Start command waits until pods are reachable and optionally until services have started, and stop command waits until pods have exited.
*   Add log file for install scripts.
*   Add logging support for Pywb, OpenWayback and PostgreSQL.

### Fixes

*   Speed up stop script.
*   More robust firewall and DNS checking.
*   All container logging is now in the host machine's time zone.

### Security

*   Access to Solr is now password protected.
*   Containers no longer run as `root` internally.
*   The `lockss` user on the host machine no longer requires `sudo` privileges.
*   Compatibility with `firewalld` and `ufw` reinstated.
