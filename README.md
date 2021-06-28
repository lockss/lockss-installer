# LOCKSS Installer

The `lockss-installer` project provides a collection of scripts to setup and run the [LOCKSS 2.0-alpha4](https://lockss.readthedocs.io/projects/manual/en/2.0-alpha4/) system. LOCKSS 2.0-alpha4 is the fourth publicly available prototype of the next generation of the [LOCKSS Program](https://www.lockss.org/)'s distributed digital preservation system.

## Resources

*   [**LOCKSS 2.0-alpha4 Manual**](https://lockss.readthedocs.io/projects/manual/en/2.0-alpha4/)

## Quickstart

Please refer to the LOCKSS 2.0-alpha4 [release page](https://lockss.readthedocs.io/projects/manual/en/2.0-alpha4/) for [system pre-requisites](https://lockss.github.io/administrators/manual/2.0-alpha4/introduction/prerequisites), [installation](https://lockss.github.io/administrators/manual/2.0-alpha4/installing) and [upgrade](https://lockss.github.io/administrators/manual/2.0-alpha4/upgrading) instructions, and [frequently asked questions](https://lockss.github.io/administrators/releases/2.0-alpha4#frequently-asked-questions). This section presents an abbreviated version of this information.

In order to install and test the LOCKSS 2.0-alpha4 system, you will need:

*   64-bit **Linux** host (physical or virtual) with at least 4 cores and 8 GB of memory.

*   **K3s** (a lightweight Kubernetes environment).

*   **Git** to download the LOCKSS Installer from GitHub.

At a high level, to bring up a LOCKSS 2.0-alpha4 system:

*   Create a `lockss` system user (as `root`):

    *   `useradd --system --user-group --create-home --shell=/bin/bash lockss`

*   Install Git (as `root`), for example (OS-dependent):

    *   `apt update ; apt install --assume-yes git`

    *   `dnf --assumeyes install git`

    *   `pacman -Sy --noconfirm git`

    *   `yum --assumeyes install git`

    *   `zypper refresh ; zypper --non-interactive install git`

*   Download the LOCKSS Installer from GitHub with Git (as `lockss`):

    *   `git clone https://github.com/lockss/lockss-installer`

    *   `cd lockss-installer`

    *   `git config --local pull.rebase true`

*   Install and check K3s (as `root`):

    *   `scripts/install-k3s`

    *   `scripts/check-k3s`

    *   `k3s check-config` (which sometimes fails unnecessarily; see <https://lockss.readthedocs.io/projects/manual/en/2.0-alpha4/troubleshooting/k3s.html#when-the-k3s-configuration-checker-fails>)

    *   `scripts/check-sys`

*   Configure the LOCKSS system (as `lockss`):

    *   `scripts/configure-lockss`

*   Start the LOCKSS stack (as `lockss`):

    *   `scripts/start-lockss`

*   Use the system (try `http://<your HOSTNAME>:24621`)

*   Shut down the LOCKSS stack:

    *   `scripts/stop-lockss`

Please contact LOCKSS Support by writing to `lockss-support (at) lockss (dot) org`
for questions and help.

## Git Branches

The `master` branch contains stable releases; day to day development activities happen in the `develop` branch and its offshoots.
