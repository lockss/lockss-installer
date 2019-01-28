#!/usr/bin/env python3

# A CGI script that uses HTML Form data to query the
# WASAPI interface and produce an HTML page of the
# results

import sys
from argparse import ArgumentParser
import requests
import json
import cgi 
import cgitb
cgitb.enable(display=0, logdir="/usr/local/apache2/logs/cgitb")
localHost = "demo.laaws.lockss.org"
serviceHost = 'localhost'

message = 'Content-Type:text/html' + '\n\n' + '<html>\n'
message += '<head>\n'
message += '<meta http-equiv="content-type" content="text/html; charset=windows-1252">\n'
message += '<title>Response from WASAPI Service</title>\n'
message += '<link rel="stylesheet" type="text/css" media="all" href="http://' + localHost + '/style.css" />\n'
message += '</head>\n'
message += '<body>\n'
message += '<br style="clear:both;"/>\n'
message += '<div id="primary">\n'
message += '<div id="content" role="main">\n'
message += '<img src="http://' + localHost + '/438x150lockss3.jpg">\n'
message += '<article>\n'
message += '<header class="entry-header"><h1 class="entry-title">Response from WASAPI Service</h1></header>\n'
message += '<div class="entry-content">\n'
message += '<h3 style="text-align: justify;"><strong>Request</strong></h3>\n'
message += '<div>\n'
message += '<p>\n'

# URL prefix for WASAPI service
service = 'http://' + serviceHost + ':8880/v0'

# Return a Dictionary with the params for the WSAPI request
def formMakeWasapiParams():
    # get data from web page form
    input_data=cgi.FieldStorage()
    ret = None
    if 'auid' in input_data:
        ret = {}
        ret['query'] = input_data['auid'].value
        ret['function'] = 'auid'
    else:
        if 'Search' in input_data:
            ret = {}
            ret['query'] = input_data['Search'].value
            ret['function'] = 'Search'
    return ret

def argsMakeWasapiParams():
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

params1 = None
if(len(sys.argv) > 1):
    # Run from command line
    params1 = argsMakeWasapiParams()
else:
    # Run from form
    params1 = formMakeWasapiParams()
if params1 != None:
    try:
        message += "Request params:<br /> {}<br />\n".format(json.dumps(params1))
        # query the service
        wasapiResponse = requests.post(service + "/jobs", data=params1)
        status = wasapiResponse.status_code
        message += '<h3 style="text-align: justify;"><strong>Response</strong></h3>\n'
        if(status == 200):
            # WASAPI request successful
            # parse the JSON we got back
            wasapiDict = json.loads(wasapiResponse.json())
            message += "<br /> {}<br />\n".format(json.dumps(wasapiDict))
            if 'files' in wasapiDict:
                for f in wasapiDict['files']:
                    for link in f['locations']:
                        message += '<br /><a href="' + link + '">Download WARC</a> name '
                        message += f['filename'] + ' checksum ' + f['checksum']
                        message += '<br />\n'
            else:
                message += "<br />\n"
        else:
            # WASAPI request unsuccessful
            message += "<br />WASAPI request error: {0}<br />\n{1}<br />".format(status,wasapiResponse)
    except:
        e = sys.exc_info()
        message += cgitb.text(e)
else:
    message += "<br />WASAPI request parameters missing<br />\n"
print(message)
