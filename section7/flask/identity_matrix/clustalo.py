# Clustal Omega API from EMBL-EBI
# https://www.ebi.ac.uk/Tools/msa/clustalo/
# http://europepmc.org/abstract/MED/30976793

import os
import sys
import time
import requests
import platform
from xmltramp2 import xmltramp
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.request import __version__ as urllib_version

baseUrl = 'https://www.ebi.ac.uk/Tools/services/rest/clustalo'
version = '2019-07-03 12:51'
pollFreq = 1    # wait time between result checks

# # Clustal Omega API options
# options = {
#     'email': 'jrsacher@broadinstitute.org',  # required
#     'sequence': 'temp_in.fasta',  # required
#     'outfile': 'temp_out.aln',  # required
#     'outfmt': 'clustal',
#     'stype': 'protein',
#     'title': 'identity_matrix',
#     'guidetreeout': 'true',
#     'dismatout': 'true',
#     'dealign': 'false',
#     'mbed': 'true',
#     'mbediteration': 'true',
#     'iterations': 0,
#     'gtiterations': -1,
#     'hmmiterations': -1,
#     'order': 'aligned'
# }


def getUserAgent():
    # Agent string for urllib2 library.
    urllib_agent = 'Python-urllib/%s' % urllib_version
    clientRevision = version
    # Prepend client specific agent string.
    try:
        pythonversion = platform.python_version()
        pythonsys = platform.system()
    except ValueError:
        pythonversion, pythonsys = "Unknown", "Unknown"
    user_agent = 'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
        clientRevision, os.path.basename(__file__),
        pythonversion, pythonsys, urllib_agent)
    return user_agent


def serviceRun(options):
    requestUrl = baseUrl + '/run/'
    requestData = urlencode(options)

    # Errors are indicated by HTTP status codes.
    try:
        # Set the HTTP User-agent.
        user_agent = getUserAgent()
        http_headers = {'User-Agent': user_agent}
        req = Request(requestUrl, None, http_headers)
        # Make the submission (HTTP POST).
        reqH = urlopen(req, requestData.encode(
            encoding='utf_8', errors='strict'))
        jobId = reqH.read().decode('utf-8')
        reqH.close()
    except HTTPError as ex:
        print(xmltramp.parse(ex.read()))[0][0]
        quit()

    return jobId


def restRequest(url):
    try:
        # Set the User-agent.
        user_agent = getUserAgent()
        http_headers = {'User-Agent': user_agent}
        req = Request(url, None, http_headers)
        # Make the request (HTTP GET).
        reqH = urlopen(req)
        result = reqH.read().decode('utf-8')
        reqH.close()
    # Errors are indicated by HTTP status codes.
    except HTTPError:
        result = requests.get(url).content
    return result


def clientPoll(jobId):
    requestUrl = baseUrl + '/status/' + jobId
    result = 'PENDING'
    while result == 'PENDING' or result == 'RUNNING':
        result = restRequest(requestUrl)
        if result == 'PENDING' or result == 'RUNNING':
            time.sleep(pollFreq)


def getResult(jobId, options):
    # Check status and wait if necessary
    clientPoll(jobId)

    # Get the result in clustal format
    requestUrl_result = baseUrl + '/result/' + jobId + '/aln-clustal'
    result = restRequest(requestUrl_result)

    if type(result) != str:
        result = 'error'

    with open(options['outfile'], 'w') as f:
        f.write(result)


def align(options):
    ''' options is a dictionary of Clustal options '''

    # Read file
    with open('temp_in.fasta', 'r') as f:
        options['sequence'] = f.read()

    jobId = serviceRun(options)
    # Wait for job to run
    time.sleep(pollFreq)
    getResult(jobId, options)
