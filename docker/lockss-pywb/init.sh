#!/bin/sh

# Copyright (c) 2000-2018, Board of Trustees of Leland Stanford Jr. University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Create a demo collection within PyWb
wb-manager init ${PYWB_COLLECTION}

# Mount a HDFS path if one was provided
if [ ! -z ${HDFS_HOST} ]; then
  echo "Mounting HDFS path to PyWb archive directory (hdfs://${HDFS_HOST:-localhost}:${HDFS_FSMD:-9000}/ -> ${PYWB_HDFSMNT})"

  # Wait for HDFS to become available
  while ! nc -z ${HDFS_HOST:-localhost} ${HDFS_FSMD:-9000} ; do
      echo "Could not connect to hdfs://${HDFS_HOST:-localhost}:${HDFS_FSMD:-9000}/; retrying in 5 seconds..."
      sleep 5
  done

  # Create mount point
  mkdir -p ${PYWB_HDFSMNT}

  # Attempt to mount HDFS sealed WARCs to OpenWayback watch directory
  hadoop-fuse-dfs "dfs://${HDFS_HOST:-localhost}:${HDFS_FSMD:-9000}/" ${PYWB_HDFSMNT}

  # Ensure the sealed directory exists under HDFS (-p doesn't work - only used here so that mkdir is quiet if the directory already exists)
  mkdir -p ${PYWB_HDFSMNT}/${REPO_BASEDIR}
  mkdir -p ${PYWB_HDFSMNT}/${REPO_BASEDIR}/sealed

  # Create a symlink from the sealed directory to the demo collections ./archive directory
  rmdir ${PYWB_BASEDIR}/collections/${PYWB_COLLECTION}/archive
  ln -s ${PYWB_WATCHDIR} ${PYWB_BASEDIR}/collections/${PYWB_COLLECTION}/archive
fi

# Start PyWb
uwsgi /uwsgi/uwsgi.ini
