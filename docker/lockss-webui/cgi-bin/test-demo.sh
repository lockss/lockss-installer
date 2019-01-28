#!/bin/sh

# Runs a set of tests against the LAAWS demo using the
# capability of running the CGI scripts from the command
# line. Run it by:
# CONT=laawsdemo_laaws-demo_1
# CMD=/usr/local/apache2/cgi-bin/test-demo.sh
# docker exec ${CONT} ${CMD}
#
# Needs additional tests as new functions added to demo
# Hash values need updating if script output is changed

PASS=0
# Search for non-existent DOI
RES=`/usr/local/apache2/cgi-bin/doi-search.py 10.1234/foobar | md5sum`
if [ "${RES}" != "f6a80f6f39eceb608389ceafd3e64e85  -" ]
then
	PASS=1
	echo "${RES}" 10.1234/foobar
fi
# Search for existing DOI
RES=`/usr/local/apache2/cgi-bin/doi-search.py 10.5339/nmejre.2014.3 | md5sum`
if [ "${RES}" != "f7386d87426ce6a2749e8cebbb51c8a6  -" ]
then
	PASS=1
	echo "${RES}" 10.5339/nmejre.2014.3
fi
# Search for invalid OpenURL
RES=`/usr/local/apache2/cgi-bin/openurl-search.py ISSN 1234-5678 Volume 1 Author "Arthur Dent" | md5sum`
if [ "${RES}" != "0690663a0cd65ecd4182f71eebaeef99  -" ]
then
	PASS=1
	echo "${RES}" 'ISSN 1234-5678 Volume 1 Author "Arthur Dent"'
fi
# Search for existing OpenURL
RES=`/usr/local/apache2/cgi-bin/openurl-search.py ISSN 1703-1958 Volume 2014 Issue 1 "Start Page" 5 | md5sum`
if [ "${RES}" != "b882aa738c9b76b1072b63420f701c94  -" ]
then
	PASS=1
	echo "${RES}" 'ISSN 1703-1958 Volume 2014 Issue 1 "Start Page" 5'
fi
# Search for text known not present
RES=`/usr/local/apache2/cgi-bin/text-search.py foobar | md5sum`
if [ "${RES}" != "630f5e5678dcb9e5f3fa83ddfd093ffe  -" ]
then
	PASS=1
	echo "${RES}" foobar
fi
# Search for text known present
RES=`/usr/local/apache2/cgi-bin/text-search.py Qatar | md5sum`
if [ "${RES}" != "f10559e46a636b2e0b11c174b568abab  -" ]
then
	PASS=1
	echo "${RES}" Qatar
fi
if [ ${PASS} -lt 1 ]
then
	echo PASS
else
	echo FAIL
fi
exit ${PASS}
