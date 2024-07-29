# `lockss-installer` Release Notes

## 2.0.81-beta1

Release date: 2024-07-29

### Fixes

*   Force use of upgrade script after version upgrade
*   Force use of `configure-lockss` after running upgrade script
*   `start-lockss`, `stop-lockss` and `restart-lockss` scripts accept `-s "<semocolon-separated-list-of-services>"` to start, stop, or restart only those services
*   Set `<SVC>_PORTS_ADDITIONAL=<host-port>:<container-port>` to map additional port to the container (e.g., for profiling).
*   Speed up stop script.
*   Set env var `SUPRESS_STD_REDIR` before running start-lockss to bypass stderr redirection to stack's `stdout.log` file, which can result in truncation on startup errors.
