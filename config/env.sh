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
##
## Load user conf
##


CFG_IMG='lockss/laaws-configuration-service'
CFG_VERSION='1.1.0-SNAPSHOT'
CFG_HOST='lockss-configuration-service'
CFG_REST_PORT='24620'
CFG_UI_PORT='24621'
#CFG_URL="http://${LOCKSS_ADMIN_USER}:${LOCKSS_ADMIN_PASSWORD}@${CFG_HOST}:${CFG_REST_PORT}"

JMS_HOST="${CFG_HOST}"
JMS_DEFAULT_PORT='61616'
JMS_PORT='24606'
JMS_URI="tcp://${JMS_HOST}:${JMS_PORT}"

MDQ_IMG='lockss/laaws-metadata-service'
MDQ_VERSION='1.0.0-SNAPSHOT'
MDQ_HOST=lockss-metadata-service
MDQ_REST_PORT='24650'
MDQ_UI_PORT='24651'

MDX_IMG='lockss/laaws-metadata-extraction-service'
MDX_VERSION='1.1.0-SNAPSHOT'
MDX_REST_PORT='24640'
MDX_UI_PORT='24641'

POL_IMG='lockss/laaws-poller'
POL_VERSION='1.0.0-SNAPSHOT'
POL_REST_PORT='24630'
POL_UI_PORT='24631'

# LAAWS repository service configuration
REPO_IMG='lockss/laaws-repository-service'
REPO_VERSION='1.8.0-SNAPSHOT'
REPO_HOST=lockss-repository-service
REPO_REST_PORT='24610'
REPO_BASEDIR='/lockss'

# PostgreSQL database configuration
POSTGRES_IMG='postgres'
POSTGRES_VERSION='9.6.12-alpine'
POSTGRES_HOST='lockss-postgres'
POSTGRES_DEFAULT_PORT='5432'
POSTGRES_PORT='24602'
POSTGRES_USER=LOCKSS
POSTGRES_DB=postgres

# Solr container configuration
SOLR_IMG='solr'
SOLR_VERSION='6.6.0-alpine'
SOLR_HOST='lockss-solr'
SOLR_DEFAULT_PORT='8983'
SOLR_PORT='24603'
SOLR_CORE_REPO='lockss-repo'
SOLR_CMD="solr-precreate ${SOLR_CORE_REPO}"

# HDFS container configuration
HDFS_IMG='lockss/lockss-hdfs'
HDFS_VERSION='1.2'
HDFS_HOST=lockss-hdfs
HDFS_FS_PORT='24619'
HDFS_DEFAULT_FS_PORT='9000'
HDFS_STATUI_PORT='50070'
HDFS_DNUI_PORT='50075'

# PyWb container settings
PYWB_IMG='lockss/lockss-pywb'
PYWB_VERSION='2.2.20190311-1'
PYWB_HOST='lockss-repository-service'
PYWB_PORT='24681'
PYWB_DEFAULT_PORT='8080'