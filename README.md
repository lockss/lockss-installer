# LOCKSS Installer

The `lockss-installer` project provides a collection of scripts to setup and run the [LOCKSS 2.0-alpha](https://lockss.github.io/software/releases/2.0-alpha) system. LOCKSS 2.0-alpha is the first publicly available prototype of the next generation of the [LOCKSS Program](https://www.lockss.org/)'s distributed digital preservation system.

## Resources

*   **LOCKSS 2.0-alpha release page: <https://lockss.github.io/software/releases/2.0-alpha>**
*   **LOCKSS system manual: <https://lockss.github.io/software/manual>**

## Quickstart

Please refer to the [LOCKSS 2.0-alpha release page](https://lockss.github.io/software/releases/2.0-alpha) for system pre-requisites, installation instructions and frequently asked questions. This section presents an abbreviated version of this information.

In order to install and test the LOCKSS 2.0-alpha system, you will need:

*   64-bit Linux host (physical or virtual) with 4 cores and 8 GB of memory
*   Docker running in Swarm mode and with the Local-Persist volume plugin
*   Git to download a small project from GitHub
*   The Setuptools and Pystache Python modules

To bring up a LOCKSS 2.0-alpha cluster:

*   `git clone https://github.com/lockss/lockss-installer`
*   `cd lockss-installer`
*   `scripts/configure-lockss`
*   `scripts/generate-lockss`
*   `scripts/assemble-lockss`
*   `scripts/deploy-lockss`
*   Use the system (try `http://<your IP address>:24600`)
*   `scripts/shutdown-lockss`

Please contact LOCKSS Support by writing to `lockss-support (at) lockss (dot) org`
for questions and help.

## Git Branches

The `master` branch contains stable releases; the `develop` branch is where day to day development work happens.
