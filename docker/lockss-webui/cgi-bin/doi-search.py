#!/usr/bin/env python3

import re
import requests
import json
import cgi
import cgitb
import urllib.parse
import sys
cgitb.enable(display=0, logdir="/usr/local/apache2/logs/cgitb")

# URL prefix for DOI query service
service = "http://laaws-metadataservice:8889/urls/doi"
# URL prefix for OpenWayback
wayback = "http://demo.laaws.lockss.org:8080/wayback/*"
# Regex to match syntactically valid DOIs
doiRegex = '10\.[0-9]+\/'
err = "Error: "
message = 'Content-Type:text/html' + '\n\n' + '<h1>DOI to URL</h1>\n' 
redirectTo = None
doi = "bogus"


# Return true if d is a syntactically valid DOI
def validate(d):
    regex = re.compile(doiRegex)
    ret = regex.match(d)
    return ret

try:
    if(len(sys.argv) > 1):
        # Run from command line
        doi = sys.argv[1]
    else:
        # get data from web page form
        input_data=cgi.FieldStorage()
        if "DOI" in input_data:
            doi=input_data["DOI"].value
    if validate(doi):
        message = message + "DOI: " + doi + "<br />\n<br />\n"
        # query the service
        serviceUrl = "{0}/{1}".format(service, urllib.parse.quote_plus(doi))
        doiResponse = requests.get(serviceUrl, timeout=10)
        status = doiResponse.status_code
        if(status == 200):
            # parse the JSON we got back
            doiData = doiResponse.json()
            if "urls" in doiData:
                urlList = doiData["urls"]
                if(len(urlList) == 1):
                    url = urlList[0]
                    redirectTo = "{0}/{1}".format(wayback,url)
                elif(len(urlList) == 0):
                    message = message + "DOI query succeeded but no URL"
                else:
                    err = ""
                    message = message + "Multiple URLs for DOI\n<ul>\n"
                    for url in urlList:
                        message = message + '<li><a href="{}">'.format(url) + "{}</a></li>\n".format(url)
                    message = message + "</ul>\n"
            else:
                # JSON from DOI search lacked "urls"
                message = message + "DOI query result lacked urls: {}".format(doiData)
        else:
            # DOI search query unsuccessful
            message = message + "DOI service error: {}".format(status)
    else:
        # Got DOI but invalid
        message = message + "Invalid DOI: {}".format(doi)
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
        message = message + "Got AttributeError: {}\n".format(e[0])
print(message)
