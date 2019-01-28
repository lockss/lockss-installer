#!/usr/bin/env python3

# CGI script to extract content of AU as WARC and report result
# in JSON as specified in WASAPI

from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders

from argparse import ArgumentParser
import requests
import json

import tempfile
import re
import cgi
import cgitb
import urllib.parse
import sys
import os.path
import hashlib
from functools import partial
# Disable traceback to requester as output must be JSON
cgitb.enable(display=0, logdir="/usr/local/apache2/logs/cgitb")

message = 'Content-Type:application/json' + '\n\n'

# URL prefix for WSAPI service
service = "http://laaws-repo:8080/repos/"

warcPath1 = "/usr/local/apache2/htdocs/"
warcDir = "warcs/"
warcDirPath = warcPath1 + warcDir
warcFile = tempfile.NamedTemporaryFile(dir=warcDirPath, suffix=".warc.gz", delete=False)
warcName = os.path.basename(warcFile.name)
warcPath = warcDirPath + warcName
warcHost = 'demo.laaws.lockss.org'
repoName = None
# URL prefix for OpenWayback
wayback = "http://laaws-openwayback:8080/wayback/"
ingestdate = "20170201"

# Return a Dictionary with the params for the LAAWS repo request
def makeRepoParamsFromArgs():
    parser = ArgumentParser()

    parser.add_argument("--artifact", dest="my_artifact", help="Artifact ID")
    parser.add_argument("--auid", dest="my_auid", help="AU ID of artifact")
    parser.add_argument("--uri", dest="my_uri", help="URI of artifact")
    parser.add_argument("--aspect", dest="my_aspect", help="Aspect of artifact")
    parser.add_argument("--timestamp", dest="my_timestamp", help="Datetime of artifact")
    parser.add_argument("--acquired", dest="my_acquired", help="Datetime acquired")
    parser.add_argument("--hash", dest="my_hash", help="Artifact hash")
    parser.add_argument("--committed", dest="my_committed", help="False means uncommitted only", default="true")
    parser.add_argument("--includeAllAspects", dest="my_includeAllAspects", help="True means include all aspects", default="false")
    parser.add_argument("--includeAllVersions", dest="my_includeAllVersions", help="True means include all versions", default="false")
    parser.add_argument("--limit", dest="my_limit", help="Count of artifacts for paging")
    parser.add_argument("--next_artifact", dest="my_next_artifact", help="Next artifact index")

    args = parser.parse_args()
    ret = {}

    if (args.my_artifact != None):
        ret['artifact'] = args.my_artifact
    if (args.my_auid != None):
        ret['auid'] = args.my_auid
    if (args.my_uri != None):
        ret['uri'] = args.my_uri
    if (args.my_aspect != None):
        ret['aspect'] = args.my_aspect
    if (args.my_timestamp != None):
        ret['timestamp'] = args.my_timestamp
    if (args.my_acquired != None):
        ret['acquired'] = args.my_acquired
    if (args.my_hash != None):
        ret['hash'] = args.my_hash
    if (args.my_committed != None):
        ret['committed'] = args.my_committed
    if (args.my_includeAllAspects != None):
        ret['includeAllAspects'] = args.my_includeAllAspects
    if (args.my_includeAllVersions != None):
        ret['includeAllVersions'] = args.my_includeAllVersions
    if (args.my_limit != None):
        ret['limit'] = args.my_limit
    if (args.my_next_artifact != None):
        ret['next'] = args.my_next
    if (ret == {}):
        ret['committed'] = "false"
    return ret

def processRepoData(data):
    uris = []
    items = data['items']
    if ( 'auid' in params1 ):
        for art in items:
            if ( art['auid'] == params1['auid'] ):
                uris.append(art['uri'])
    else:
        for art in items:
            uris.append(art['uri'])
    return uris

def reportError(report):
    descriptor = {
        "includes-extras":False,
        "files":[
        ],
        "error":report
    }
    ret = json.dumps(descriptor)
    return ret

def writeWarc(uris, warcFile):
    ret = ""
    sha1 = ""
    if len(uris) < 1:
        ret = reporError("No URIs to export")
    else:
        with warcFile as output:
            writer = WARCWriter(output, gzip=True)
    
            stem = wayback + ingestdate + '/'
            owuri = 'foo'
            for uri in uris:
                owuri = stem + uri
                resp = requests.get(owuri, headers={'Accept-Encoding': 'identity'},
                                    stream=True)
        
                if (resp.status_code == 200):
                    # get raw headers from urllib3
                    headers_list = resp.raw.headers.items()
            
                    http_headers = StatusAndHeaders('200 OK', headers_list,
                                                    protocol='HTTP/1.0')
            
                    record = writer.create_warc_record(uri, 'response',
                                                        payload=resp.raw,
                                                        http_headers=http_headers)
                    writer.write_record(record)
        with open(warcFile.name, mode='rb') as f:
            m = hashlib.sha1()
            bytes = 0
            for buf in iter(partial(f.read, 4096), b''):
                m.update(buf)
                bytes += len(buf)
        sha1 = m.hexdigest()
        descriptor = {
            "includes-extras":False,
            "files":[
                {
                    "checksum":"sha1:" + sha1,
                    "content-type":"application/warc",
                    "filename":warcName,
                    "locations":[
                        'http://' + warcHost + '/' + warcDir + warcName
                    ],
                    "size":"{}".format(bytes)
                }
            ]
        }
        ret = json.dumps(descriptor)
    return ret

params1 = {}
try:
    if(len(sys.argv) > 1):
        # Run from command line
        params1 = makeRepoParamsFromArgs()
    else:
        # get data from web page form
        input_data=cgi.FieldStorage()
        if 'auid' in input_data:
            params1['auid'] = input_data['auid'].value
        params1['committed'] = "false"
    # Find the repo
    repoResponse = requests.get(service)
    status = repoResponse.status_code
    if (status == 200):
        repoData = repoResponse.json()
        repoName = repoData[0]
    else:
        message += reportError("Repo request error: {0}\n{1}".format(status,repoResponse))
    if (repoName != None):
        # List the artifacts
        repoResponse = requests.get(service + repoName + "/artifacts/", params=params1)

        status = repoResponse.status_code
        if(status == 200):
            # LAAWS repo request successful
            # parse the JSON we got back
            repoData = repoResponse.json()
            uris = processRepoData(repoData)
            message += writeWarc(uris, warcFile)
        else:
            # LAAWS repo request unsuccessful
            message += reportError("repo request error: {0}\n{1}".format(status,repoResponse))
except:
    e = sys.exc_info()
    message += reportError(cgitb.text(e))
print(message)
