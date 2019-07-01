#!/bin/sh

# Copyright (c) 2000-2019, Board of Trustees of Leland Stanford Jr. University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#######################################
# Check if package(s) are installed
# Globals:
#   None
# Arguments:
#   a  package to check
# Returns:
#   None
#######################################
ipm_check_native() {
  dpkg --status "${1}" 2> /dev/null | grep --quiet 'Status:.*installed'
}

#######################################
# Clean package cache
# Globals:
#   None
# Arguments:
#  None
# Returns:
#######################################
ipm_clean_native() {
  apt-get --assume-yes clean
}

#######################################
# Install the package(s)
# Globals:
#   None
# Arguments:
#   a list of packages to install
# Returns:
#   None
#######################################
ipm_install_native() {
  apt-get --assume-yes install "$@"
}

#######################################
# Uninstall the package(s)
# Globals:
#   None
# Arguments:
#   a list of packages to uninstall
# Returns:
#   None
#######################################
ipm_uninstall_native() {
  apt-get --assume-yes remove "$@"
}

#######################################
# Update installed package(s)
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
ipm_update_native() {
  apt-get update
}

#######################################
# Upgrade installed package(s)
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
#######################################
ipm_upgrade_native() {
  apt-get --assume-yes upgrade
}
