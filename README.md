# LOCKSS Installer

The `lockss-installer` project provides a collection of scripts to setup and run the [LOCKSS 2.0-alpha2](https://lockss.github.io/software/releases/2.0-alpha2) system. LOCKSS 2.0-alpha2 is the first publicly available prototype of the next generation of the [LOCKSS Program](https://www.lockss.org/)'s distributed digital preservation system.

## Resources

*   **LOCKSS 2.0-alpha2 release page: <https://lockss.github.io/software/releases/2.0-alpha2>**
*   **LOCKSS system manual: <https://lockss.github.io/software/manual>**

## Quickstart

Please refer to the [LOCKSS 2.0-alpha2 release page](https://lockss.github.io/software/releases/2.0-alpha2) for system pre-requisites, installation instructions and frequently asked questions. This section presents an abbreviated version of this information.

In order to install and test the LOCKSS 2.0-alpha system, you will need:

*   64-bit Linux host (physical or virtual) with 4 cores and 8 GB of memory
*   Docker running in Swarm mode and with the Local-Persist volume plugin
*   Git to download a small project from GitHub

To bring up a new LOCKSS 2.0-alpha2 cluster:

*   `git clone https://github.com/lockss/lockss-installer`
*   `cd lockss-installer`
*   `scripts/configure-lockss`
*   `scripts/start-lockss`
*   Use the system (try `http://<your IP address>:24600`)

To upgrade a LOCKSS 2.0-alpha1 cluster to LOCKSS 2.0-alpha2 cluster:
*   `git pull` on the master branch
*   `scripts/update-alpha1-to-alpha2`
*   `scripts/configure-lockss`
*   `scripts/start-lockss`

To shutdown a running LOCKSS 2.0-alpha2 cluster:
*   `scripts/shutdown-lockss`

To start a stopped LOCKSS 2.0-alpha2 cluster:
*   `scripts/start-lockss`

To restart a running or shutdown LOCKSS 2.0-alpha2 cluster:
*   `scripts/restart-lockss`

To run the most recent release of LOCKSS 2.0-alpha2 cluster:
*   `git pull` on the master branch
*   `scripts/update-lockss`

## Scripts Summary

### The Building Blocks
*   `configure-lockss`: Collects host system info from the user and writes it to config/system.cfg.
*   `generate-lockss`: Uses the system.cfg file to generate from templates the files needed to deploy a stack.
*   `assemble-lockss`: Adds into docker the volumes, configuration files and networks from generate-lockss
*   `deploy-lockss`: Deploy the LOCKSS 2.0-alpha2 cluster.
*   `shutdown-lockss`: Undeploy the LOCKSS 2.0-alpha2 cluster. This removes docker stack.
*   `uninstall-lockss`: Remove all lockss elements from docker. This will not remove files from the persistent store.

### The Convenience Scripts
*   `start-lockss`: Calls in turn generate-lockss, assemble-lockss and deploy-lockss.
*   `restart-lockss`: Calls shutdown-lockss and start-lockss. This will run with the system unchanged.
*   `update-lockss`: Nearly identical to `start-lockss` but this will pull newest docker image.

### Support Scripts:
*   `check_sys`: used to determine and if possible install elements missing from the host system..
*   `upgrade-alpha1-to-alpha2`: called once to upgrade from an older alpha1 system.
*   `upgrade-alpha1-solr`: called once to upgrade from an older alpha1 solr.

Please contact LOCKSS Support by writing to `lockss-support (at) lockss (dot) org`
for questions and help.

## Git Branches

The `master` branch contains stable releases; the `develop` branch is where day to day development work happens.
