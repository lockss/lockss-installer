#!/usr/bin/env python3

import requests
import json
import cgi
import cgitb
import sys
cgitb.enable(display=0, logdir="/usr/local/apache2/logs/cgitb")

# URL prefix for SOLR query service
# XXX should work with both EDINA and BL
service = "http://laaws-indexer-solr:8983/solr/test-core/select"
# URL prefix for OpenWayback
wayback = "http://demo.laaws.lockss.org:8080/wayback/*"
message = 'Content-Type:text/html' + '\n\n' + '<h1>Text Search</h1>\n'
redirectTo = None
urlArray = []

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
        message = message + "SOLR search for {}<br />\n<br />\n".format(params['q'])
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
                    message = message + "docs is empty"
                else:
                    for doc in docs:
                        url = None
                        if "response_url" in doc:
                            url = doc["response_url"][0]
                        elif "url" in doc:
                            url = doc["url"]
                        if url != None:
                            urlArray.append(url)
            else:
                message = message + "No docs found\n"
        else:
            # SOLR search query unsuccessful
            message = message + "SOLR service response: {}\n".format(status)
    else:
        # No search data from form
        message = message + "No search string from form\n"
    if(len(urlArray) == 1):
        message = "Location: {}".format(urlArray[0]) + '\n'
    elif len(urlArray) > 1:
        # multiple urls, create page of links
        message = message + '<ol>\n'
        # Sorted neede to ensure consistent output order for testing
        for url in sorted(urlArray):
            message = message + '<li><a href="{0}/{1}">'.format(wayback,url) + "{}</a></li>\n".format(url)
        message = message + "</ol>\n"
    else:
        message = message + "<br />\nError: No URLs returned\n"
except requests.exceptions.ConnectTimeout:
    message = message + 'Timeout connecting to DOI resolution service {}\n'.format(service)
except requests.exceptions.ConnectionError:
    message = message + 'Cannot connect to DOI resolution service {}\n'.format(service)
except:
    e = sys.exc_info()
    try:
        message = message + cgitb.text(e)
    except AttributeError:
        message = message + "Got AttributeError: {}\n".format(e[0])
print(message)
