#!/usr/bin/env python3
import os, sys
import json
import requests
from datetime import datetime, timezone
from base64 import b64decode
import hashlib

localHost = 'demo.laaws.lockss.org'
auid_to_json = 'http://' + localHost + '/cgi-bin/auid-to-json.py'
text_to_json = 'http://' + localHost + '/cgi-bin/text-to-json.py'
cgi_script = None
persistentFile = '/tmp/wsapiJobs'

# WSAPI API
def jobs_post(query = None, function = None, parameters = None) -> str:
    # WARC creation is supposed to be asynchronous, but for now we
    # make it synchonous, so all jobs are in status 'complete'
    if function == 'auid' and query != None:
        params = { 'auid' : query }
        cgi_script = auid_to_json
    else:
        if function == 'Search' and query != None:
            params = { 'Search' : query }
            cgi_script = text_to_json
        else:
            return json.dumps( { 'function' : function , 'query' : query } )
    resp = requests.post(cgi_script, data=params)
    if resp.status_code == 200:
        results = resp.json()
        jobId = makeJobId()
        results['status'] = "200"
        results['jobToken'] = jobId
        putJob(jobId, params, results)
    else:
        results = { 'status' : "{}".format(resp.status_code) ,
            'message' : resp.text ,
            'function' : function ,
            'query' : query }
    return json.dumps(results)

def not_jobs_post(query = None, function = None, parameters = None) -> str:
    # WARC creation is supposed to be asynchronous, but for now we
    # make it synchonous, so all jobs are in status 'complete'
    results = {
        'query' : query ,
        'function' : function ,
        'parameters' : parameters
    }
    return json.dumps(results)

def webdata_get(filename = None, contentType = None) -> str:
    # Not yet implemented
    message = {
        'status': '400',
        'message': 'Content filtering not supported'
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp

def jobs_get() -> str:
    ret = {}
    jobs = getJobs()
    ret = json.dumps(jobs)
    return ret

def jobs_job_token_get(jobToken) -> str:
    ret = []
    job = getJob(jobToken)
    if job != None:
        params = job['params']
        ret['function'] = params['function']
        ret['jobtoken'] = jobToken
        ret['query'] = params['query']
        ret['state'] = 'complete'
        ret['submit-time'] = jobs['submit-time']
    return json.dumps(ret)

# Persistent state - i.e. jobs database
def putJob(jobId, params, results = None):
    ret = None
    state = {'params' : params,
        'results' : results,
        'submit-time' : encodeTime()}
    try:
        fileState = os.stat(persistentFile)
    except FileNotFoundError as ex:
        jobs = {}
    else:
        if fileState.st_size > 0:
            with open(persistentFile, 'r') as f:
                jobs = json.load(f)
        else:
            jobs = {}
    with open(persistentFile, 'w') as f:
        jobs[jobId] = state
        json.dump(jobs, f)
        ret = jobId
    return ret

def getJob(jobId):
    try:
        with open(persistentFile, 'r') as f:
            # XXX need to lock file
            jobs = json.load(f)
            return jobs[jobId]
    except FileNotFoundError:
        return None
def getJobs():
    try:
        with open(persistentFile, 'r') as f:
            # XXX need to lock file
            jobs = json.load(f)
            return jobs
    except FileNotFoundError:
        return []

def encodeTime():
    local_time = datetime.now(timezone.utc).astimezone()
    return local_time.isoformat()

def makeJobId():
    # XXX for now, jobId is submission time
    return encodeTime()

# Return the body of the POST response
def makePostResponse(jobId, params, results):
    ret = {
        "includes-extras":False,
        "files":[
            {
                "checksum":"sha1:" + results['sha1'],
                "content-type":"application/warc",
                "filename":results['name'],
                "locations":[
                    "http://"+host+"/export/"+results['name']
                ],
                "size":results['size']
            }
        ]
    }
    return json.dumps(ret)
