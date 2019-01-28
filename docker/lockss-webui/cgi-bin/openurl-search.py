#!/usr/bin/env python3

import requests
import json
import cgi
import cgitb
import sys
import re
import urllib.parse
cgitb.enable(display=0, logdir="/usr/local/apache2/logs/cgitb")

# URL prefix for OpenURL query service
service = "http://laaws-metadataservice:8889/urls/openurl"
# URL prefix for OpenWayback
wayback = "http://demo.laaws.lockss.org:8080/wayback/*"
message = 'Content-Type:text/html' + '\n\n' + '<h1>DOI to URL</h1>\n'
redirectTo = None
issnRegex = '[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9X]'

# Return true if d is a syntactically valid ISSN
def validate(i):
    regex = re.compile(issnRegex)
    # XXX should do digit check see Wikipedia page
    ret = regex.match(i)
    return ret

# Return a Dictionary with the params for the OpenURL query
def parseOpenURL(s):
    # "rft.volume":"16","rft.spage":"222","rft.issn":"1434-4599"
    ret = {}
    for param in s:
        if(param.lower() == "issn"):
            if (validate(s[param].value)):
                ret["rft.issn"] = s[param].value
            else:
                message = message + "invalid ISSN: " + s[param].value
                return {}
        else:
            ret["rft." + param.lower()] = s[param].value
    return ret

try:
    params = {}
    if(len(sys.argv) > 1):
        # Run from command line
        for i in range(1,len(sys.argv)//2+1):
            params["rft." + sys.argv[i*2-1].lower()] = sys.argv[i*2]
    else:
        # get data from web page form
        input_data=cgi.FieldStorage()
        params = parseOpenURL(input_data)

    if(params != {}):
        message = message + "OpenURL request:<br />\n"
        # Sorted needed to ensure consistent output order for testing
        for p in sorted(params.keys()):
            message = message + p + ": " + params[p] + "<br />\n"
        message = message + "<br />\n"
        # query the service
        queryurl = service
        if len(params) > 0:
            queryurl = '{0}?{1}'.format(queryurl, '&'.join(['params={0}={1}'.format(p, urllib.parse.quote_plus(params[p])) for p in sorted(params)]))
        openurlResponse = requests.get(queryurl)
        status = openurlResponse.status_code
        if(status == 200):
            # parse the JSON we got back
            openurlData = openurlResponse.json()
            if "urls" in openurlData:
                urlList = openurlData["urls"]
                # XXX MDQ returns list [null] not []
                if(len(urlList) == 1 and urlList[0] != None):
                    # 1 url - redirect to it
                    url = urlList[0]
                    redirectTo = "{0}/{1}".format(wayback,url)
                elif(len(urlList) > 1):
                    # multiple urls, create page of links
                    # XXX at present MDQ can only return one URL except for multiple publishers
                    message = message + "<ol>\n"
                    # Sorted need to ensure consistent output order for testing
                    for url in sorted(urlList):
                        message = message + '<li><a href="{0}/{1}">'.format(wayback,url) + "{}</a></li>\n".format(url)
                    message = message + "</ol>\n"
                else:
                    message = message + "OpenURL query succeeded but no URL<br />\n"
            else:
                # JSON from OpenURL search lacked "urls"
                message = message + "OpenURL query result lacked urls<br />\n"
        elif(status == 500): # XXX MDQ service should not return 500 on empty result
            message = message + "OpenURL query result empty - (XXX error 500 is a bug)"
        else:
            # OpenURL search query unsuccessful
            message = message + "OpenURL service error: {0}\n{1}".format(status,openurlResponse)
    else:
        # Got params but invalid
        message = message + "Invalid query: {0}".format(input_data)
    if(redirectTo != None):
        message = "Location: {}".format(redirectTo) + '\n'
except requests.exceptions.ConnectTimeout:
    message = message + 'Timeout connecting to DOI resolution service {}\n'.format(service)
except requests.exceptions.ConnectionError:
    message = message + 'Cannot connect to DOI resolution service {}\n'.format(service)
except:
    e = sys.exc_info()
    try:
        message = message + cgitb.text(e)
    except AttributeError:
        message = message + "Got AttributeError: {}\n".format(e)
        
print(message)
