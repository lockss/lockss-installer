# LOCKSS Installer

The `lockss-installer` project provides a collection of scripts to setup and run the [LOCKSS 2.0-alpha2](https://lockss.github.io/administrators/releases/2.0-alpha2) system. LOCKSS 2.0-alpha2 is the second publicly available prototype of the next generation of the [LOCKSS Program](https://www.lockss.org/)'s distributed digital preservation system.

## Resources

*   [**LOCKSS 2.0-alpha2 Release Page**](https://lockss.github.io/administrators/releases/2.0-alpha2)
*   [**LOCKSS 2.0-alpha2 System Manual**](https://lockss.github.io/administrators/manual/2.0-alpha2)

## Quickstart

Please refer to the LOCKSS 2.0-alpha2 [release page](https://lockss.github.io/administrators/releases/2.0-alpha2) and [manual](https://lockss.github.io/administrators/manual/2.0-alpha2/) for [system pre-requisites](https://lockss.github.io/administrators/manual/2.0-alpha2/installing/system-pre-requisites), [installation](https://lockss.github.io/administrators/manual/2.0-alpha2/installing) and [upgrade](https://lockss.github.io/administrators/manual/2.0-alpha2/upgrading) instructions, and [frequently asked questions](https://lockss.github.io/administrators/releases/2.0-alpha1#frequently-asked-questions). This section presents an abbreviated version of this information.

In order to install and test the LOCKSS 2.0-alpha2 system, you will need:

*   64-bit Linux host (physical or virtual) with at least 4 cores and 8 GB of memory
*   Docker running in Swarm mode and with the Local-Persist Docker volume plugin
*   Git to download this project from GitHub

To bring up a LOCKSS 2.0-alpha2 system:

*   `git clone https://github.com/lockss/lockss-installer`
*   `cd lockss-installer`
*   `scripts/configure-lockss`
*   `scripts/start-lockss`
*   Use the system (try `http://<your IP address>:24600`)
*   `scripts/shutdown-lockss`

Please contact LOCKSS Support by writing to `lockss-support (at) lockss (dot) org`
for questions and help.

## Git Branches

The `master` branch contains stable releases; day to day development activities happen in the `develop` branch and its offshoots.
