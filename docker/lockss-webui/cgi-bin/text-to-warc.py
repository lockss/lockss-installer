#!/usr/bin/env python3
from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders

import tempfile
import requests
import json
import cgi
import cgitb
import sys
import os.path
import hashlib
from functools import partial
cgitb.enable(display=0, logdir="/usr/local/apache2/logs/cgitb")

# URL prefix for SOLR query service
# XXX should work with both EDINA and BL
service = "http://laaws-indexer-solr:8983/solr/test-core/select"
# URL prefix for OpenWayback
wayback = "http://demo.laaws.lockss.org:8080/wayback/*"
message = 'Content-Type:text/html' + '\n\n' + '<h1>Text Search</h1>\n'
urlArray = []
warcPath1 = "/usr/local/apache2/htdocs/"
warcDir = "warcs/"
warcDirPath = warcPath1 + warcDir
warcFile = tempfile.NamedTemporaryFile(dir=warcDirPath, suffix=".warc.gz", delete=False)
warcName = os.path.basename(warcFile.name)
warcPath = warcDirPath + warcName
warcHost = 'demo.laaws.lockss.org'

repoName = None
ingestdate = "20170201"

def writeWarc(uris, warcFile):
    ret = ""
    with warcFile as output:
        writer = WARCWriter(output, gzip=True)

        stem = wayback + ingestdate + '/'
        owuri = 'foo'
        try:
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
                    ret += '<a href="' + owuri + '">' + uri + '</a>:'
                else:
                    ret += owuri + ': ' + format(resp.status_code)
                ret += '<br />\n'
        except requests.exceptions.ConnectTimeout:
            ret += 'Timeout connecting to service {}\n'.format(owuri)
            ret += '<br />\n'
            e = sys.exc_info()
            ret += cgitb.text(e)
        except requests.exceptions.ConnectionError:
            ret += 'Cannot connect to service {}\n'.format(owuri)
            ret += '<br />\n'
            e = sys.exc_info()
            ret += cgitb.text(e)
        except:
            e = sys.exc_info()
            try:
                ret += cgitb.text(e)
            except AttributeError:
                ret += "Got AttributeError: {}\n".format(e[0])
            ret += '<br />\n'
    with open(warcFile.name, mode='rb') as f:
        m = hashlib.sha1()
        for buf in iter(partial(f.read, 4096), b''):
            m.update(buf)
    ret += "<br />WARC SHA1: " + m.hexdigest() + '<br />\n'
    return ret

# return a Dictionary with the query params
def queryParams(s):
    if 'Search' in s:
        ret = {}
        ret['q'] = s["Search"].value
        ret['indent'] = "on"
        ret['wt'] = "json"
    else:
        ret = None
    return ret

try:
    if(len(sys.argv) > 1):
        # Run from command line
        params = {}
        params['q'] = sys.argv[1]
        params['indent'] = "on"
        params['wt'] = "json"
    else:
        # get data from web page form
        input_data=cgi.FieldStorage()
        # convert to SOLR query params
        params = queryParams(input_data)
    
    if params != None:
        message +=  "WARC from search for {}<br />\n<br />\n".format(params['q'])
        # query the service
        solrResponse = requests.get(service, params=params)
        status = solrResponse.status_code
        if(status == 200):
            # parse the JSON we got back
            solrData = solrResponse.json()
            # XXX response is paginated
            if "response" in solrData and "docs" in solrData["response"]:
                docs = solrData["response"]["docs"]
                if(len(docs) < 1 or docs[0] == None):
                    message +=  "docs is empty"
                else:
                    for doc in docs:
                        url = None
                        if "response_url" in doc:
                            url = doc["response_url"][0]
                        elif "url" in doc:
                            url = doc["url"]
                        if url != None:
                            urlArray.append(url)
                message += writeWarc(sorted(urlArray), warcFile)
                message += "<br />"
                message += '<a href="http://' + warcHost + '/' + warcDir + warcName + '">Download WARC</a>'
                message += "<br />"

            else:
                message +=  "No docs found\n"
        else:
            # SOLR search query unsuccessful
            message +=  "SOLR service response: {}\n".format(status)
    else:
        # No search data from form
        message +=  "No search string from form\n"
except requests.exceptions.ConnectTimeout:
    message +=  'Timeout connecting to text search service {}\n'.format(service)
except requests.exceptions.ConnectionError:
    message +=  'Cannot connect to text search service {}\n'.format(service)
print(message)
