# LOCKSS Installer

The `lockss-installer` project provides a collection of scripts to setup and run the [LOCKSS 2.0-alpha3](https://lockss.github.io/administrators/releases/2.0-alpha3) system. LOCKSS 2.0-alpha3 is the third publicly available prototype of the next generation of the [LOCKSS Program](https://www.lockss.org/)'s distributed digital preservation system.

## Resources

*   [**LOCKSS 2.0-alpha3 Release Page**](https://lockss.github.io/administrators/releases/2.0-alpha3)
*   [**LOCKSS 2.0-alpha3 System Manual**](https://lockss.github.io/administrators/manual/2.0-alpha3)

## Quickstart

Please refer to the LOCKSS 2.0-alpha3 [release page](https://lockss.github.io/administrators/releases/2.0-alpha3) and [manual](https://lockss.github.io/administrators/manual/2.0-alpha3/) for [system pre-requisites](https://lockss.github.io/administrators/manual/2.0-alpha3/introduction/prerequisites), [installation](https://lockss.github.io/administrators/manual/2.0-alpha3/installing) and [upgrade](https://lockss.github.io/administrators/manual/2.0-alpha3/upgrading) instructions, and [frequently asked questions](https://lockss.github.io/administrators/releases/2.0-alpha3#frequently-asked-questions). This section presents an abbreviated version of this information.

In order to install and test the LOCKSS 2.0-alpha3 system, you will need:

*   64-bit Linux host (physical or virtual) with at least 4 cores, 8 GB of memory and 50 GB of diskspace
*   64-bit Linux host compatible with Systemd, Snap, and the lightweight Kubernetes runtime MicroK8s.
*   Git to download this project from GitHub

At a high level, to bring up a LOCKSS 2.0-alpha3 system:

*   Install Git, Snap, MicroK8s
*   `git clone https://github.com/lockss/lockss-installer`
*   `cd lockss-installer`
*   `scripts/configure-dns`
*   `scripts/configure-lockss`
*   `scripts/start-lockss`
*   Use the system (try `http://<your IP address>:24621`)
*   `scripts/shutdown-lockss`

Please contact LOCKSS Support by writing to `lockss-support (at) lockss (dot) org`
for questions and help.

## Git Branches

The `master` branch contains stable releases; day to day development activities happen in the `develop` branch and its offshoots.
