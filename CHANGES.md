# `lockss-installer` Release Notes

## Unreleased

### Fixes

*   New `scripts/extract-reindex-auids` script fetches the V2 migration error report from the repository service and writes the AUs that failed to migrate with "Attempt to finishBulkStore of AU not in bulk store mode" to `<LOCKSS_DATA_DIR>/<stack>-repo-data/state/index/auids-to-reindex`, which the repository service reads at startup to reindex just those AUs.  Refuses to overwrite an existing list without `-f`/`--force`.
*   Fix the "reindex artifacts" signal, which had no effect: `signal_reindex` (and `scripts/assemble-lockss`) created `state/index/reindex`, but the repository service looks for `state/index/reindexing`.  This makes `scripts/reindex-artifacts`, and the reindex signalled by the Solr home upgrade, work again.
*   `scripts/reindex-artifacts` runs under `bash` rather than `/bin/sh`, which it requires because it sources `scripts/_util`.
*   `scripts/reindex-artifacts` removes any unrotated `state/store/reindexed-warcs` ledger before signalling.  The repository consults that ledger to resume an interrupted reindex, so a run that died before finishing would otherwise cause the requested reindex to silently skip the WARCs that run had already read.  Rotated `reindexed-warcs.<timestamp>` files are the audit record of completed runs and are kept.

## 2.0.81-beta1

Release date: 2024-07-29

### Fixes

*   Force use of upgrade script after version upgrade.
*   Force use of `configure-lockss` after running upgrade script.
*   `start-lockss`, `stop-lockss` and `restart-lockss` scripts accept `-s "<semocolon-separated-list-of-services>"` to start, stop, or restart only those services.
*   Set `<SVC>_PORTS_ADDITIONAL=<host-port>:<container-port>` in `~/lockss-installer/config/env.mustache.opt` to map additional port to the container (e.g., for profiling).
*   Speed up stop script.
*   Set env var `SUPRESS_STD_REDIR` before running start-lockss to bypass stderr redirection to stack's `stdout.log` file, which can result in truncation on startup errors.
