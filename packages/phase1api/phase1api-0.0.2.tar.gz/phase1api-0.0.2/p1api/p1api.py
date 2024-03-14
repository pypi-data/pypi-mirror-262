"""
This file provides an example binding to ESO's RESTful phase 1 programmatic interface.
The data required and returned by many of the API calls is instrument-specific.
In order to fully understand the data and behaviour of the API please consult
the documentation at https://www.eso.org/cop1/apidoc/phase1.html
The api URL specified with each API should help to locate the corresponding
API documentation at the above URL.

Unless otherwise mentioned, each API call consistently returns a tuple (data, version):
    * data    - returned data in JSON format
    * version - version of the data, required for future modifications (HTTP ETags are used for this versioning)
___________________________________________________________________________
MIT License
___________________________________________________________________________
Copyright (c) 2024 Thomas Bierwirth, European Southern Observatory

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import print_function
import os
import io
import json
import requests


## The hatchling way...
try:
    from p1api.__about__ import __version__
except:
    # Need this construct to run in VSCode
    from __about__ import __version__
P1_API_VERSION = __version__


API_URL = {
    'production' : 'https://www.eso.org/cop1/api',
    'demo'       : 'https://www.eso.org/cop1demo/api'
}

class P1Error(Exception):
    pass

class ApiConnection(object):
# ---------- PUBLIC API ----------
    def __init__(self, environment, username, password, debug=False):
        """Initiate a connection to the p1 API, to be used for subsequent API calls.

        Supported environments are
            - 'production'         : for proposal submission in production environment
            - 'demo'               : for proposal submission in demo environment

        usage:
            import p1api
            api = p1api.ApiConnection('demo', '52052', 'tutorial')
            api = p1api.ApiConnection('demo', '52052', 'tutorial', True)
            api = p1api.ApiConnection(environment='demo', username='52052', password='tutorial', debug=True)
        """
        if environment not in API_URL.keys() :
            raise P1Error(500, 'POST', environment, 'environment not supported')

        self.debug = debug
        self.request_count = 0
        self.apiUrl = API_URL[environment] + '/v1/p1'
        self.session = self.requests_retry_session()

        loginUrl = API_URL[environment] + '/login'
        r = requests.post(loginUrl, data = { 'username': username, 'password': password })
        if r.status_code == requests.codes.ok:
            body = r.json()
            self.access_token = body['access_token']
        else:
            raise P1Error(r.status_code, 'POST', loginUrl, 'cannot login')

# ---------- PROPOSAL APIs ----------
    def getProposals(self):
        """Get list of my proposals.

        api: GET /proposals

        usage:
            proposals, _ = api.getProposals()
        """
        return self.get('/proposals')
    
    def createProposal(self, cycleId, programmeType, title):
        """Create a new proposal.

        api: POST /proposals

        usage:
            proposal, _ = api.createProposal(2696, 'Normal', 'My First Proposal')
        """
        return self.post('/proposals', {'cycleId': cycleId, 'programmeType': programmeType, 'title': title})

    def getProposal(self, proposalId):
        """Get a proposal.

        api: GET /proposals/{proposalId}

        usage:
            proposal, _ = api.getProposal(42)
        """
        return self.get('/proposals/%d' % proposalId)

    def updateProposal(self, proposal, version):
        """Update a proposal.

        api: PUT /proposals/{proposalId}

        usage:
            proposal, version  = api.getProposal(42)
            proposal['title'] = 'New Title'
            proposal, version = api.updateProposal(proposal, version)
        """
        return self.put('/proposals/%d' % proposal['proposalId'], proposal, version)

    def deleteProposal(self, proposalId, version):
        """Delete a proposal.

        api: DELETE /proposals/{proposalId}

        usage:
            proposal, version = api.getProposal(proposalId)
            api.deleteProposal(proposalId, version)
        """
        return self.delete('/proposals/%d' % proposalId, etag=version)

# ---------- TARGET APIs ----------
    def getTargets(self, proposalId):
        """Get list of targets for given proposal.

        api: GET /proposals/{proposalId}/targets

        usage:
            targets, version = api.getTargets(42)
        """
        return self.get('/proposals/%d/targets' % proposalId)
    
    def createTarget(self, proposalId, target):
        """Create new target in given proposal.

        api: POST /proposals/{proposalId}/targets

        usage:
            target = {
                "name": "M81",
                "ra": "09:55:33.173",
                "dec": "69:03:55.06",
                "coordinateSystem": "J2000",
                "inSolarSystem": False,
                "movement": {
                    "properMotionRa": 0,
                    "properMotionDec": 0,
                    "epoch": 2000,
                    "parallax": 0,
                    "radialVelocity": 0,
                    "redShift": 0,
                    "useRedShift": False
                  },
                "sed": "none",
                "brightness": [
                   {
                        "band": "VVEGA",
                        "magnitude": 8
                    }
                ]
            }
            target, version = api.createTarget(proposalId, target)
        """
        return self.post('/proposals/%d/targets' % proposalId, target)

    def getTarget(self, targetId):
        """Get a target.

        api: GET /targets/{targetId}

        usage:
            target, version = api.getTarget(targetId)
        """
        return self.get('/targets/%d' % targetId)

    def updateTarget(self, target, version):
        """Update a target.

        api: PUT /targets/{targetId}

        usage:
            target, version  = api.getTarget(targetId)
            target['name'] = 'My First Target'
            target, version = api.updateTarget(target, version)
        """
        return self.put('/targets/%d' % target['targetId'], target, version)
    
    def deleteTarget(self, targetId, version):
        """Delete a target.

        api: DELETE /targets/{targetId}

        usage:
            api.deleteTarget(targetId)
        """
        return self.delete('/targets/%d' % targetId, version)

    def reorderTargets(self, proposalId, targets, version): 
        """Reorder list of observing runs.

        api: PUT /proposals/{proposalId}/targets

        usage:
            targets, version  = api.getTargets(proposalId)
            targets.reverse()
            targets, version = api.reorderTargets(proposalId, targets, version)
        """
        return self.put('/proposals/%d/targets' % proposalId, targets, version)
    
# ---------- RUN APIs ----------
    def getRuns(self, proposalId):
        """Retrieve list of observing runs.

        api: GET /proposals/{proposalId}/obsRuns

        usage:
              runs, version = api.getRuns(42)
        """
        return self.get('/proposals/%d/obsRuns' % proposalId)

    def createRun(self, proposalId, title, instrument, periodNumber, observingMode, telescopeSetup, runType):
        """Create a new observing run.

        api: POST /proposals/{proposalId}/obsRuns

        usage:
              runs, version = api.getRuns(proposalId)  
              run, version = api.createRun(proposalId, 'MyRun 1', 'UVES', 114, 'SM', 'UT2', 'Normal')
        """
        return self.post('/proposals/%d/obsRuns' % proposalId,
                         { 'title': title, 'instrument': instrument, 'periodNumber': periodNumber, 'observingMode': observingMode, 'telescopeSetup': telescopeSetup, 'runType': runType })
    
    def getRun(self, runId):
        """Get an observing run.

        api: GET /obsRuns/{runId}

        usage:
            runs, _ = api.getRuns(42)
            run, version = api.getRun(runs[0]['runId'])
        """
        return self.get('/obsRuns/%d' % runId)

    def updateRun(self, run, version):
        """Update an observing run.

        api: PUT /obsRuns/{runId}

        usage:
            runs, _ = api.getRuns(42)
            run, version = api.getRun(runs[0]['runId'])
            run['title'] = 'Updated Run'
            run, version = api.updateRun(run, version)
        """
        return self.put('/obsRuns/%d' % run['runId'], run, version)

    def deleteRun(self, runId, version):         
        """Delete a n observing run.

        api: DELETE /proposals/{proposalId}

        usage:
            runs, _ = api.getRuns(42)
            run, version = api.getRun(runs[0]['runId'])
            api.deleteRun(run['runId'], version)
        """
        return self.delete('/obsRuns/%d' % runId, etag=version)

    def reorderRuns(self, proposalId, runs, version):
        """Reorder list of observing runs.

        api: PUT /proposals/{proposalId}/obsRuns

        usage:
            runs, version  = api.getRuns(42)
            runs.reverse()
            runs, version = api.reorderRuns(proposalId, runs, version)
        """
        return self.put('/proposals/%d/obsRuns' % proposalId, runs, version)

    def getTelescopeTimes(self, runId):
        """Get telescope time of an observing run.

        api: GET /obsRuns/{runId}/telescopeTimes

        usage:
            telescopeTimes = api.getTelescopeTime(runId)
        """
        return self.get('/obsRuns/%d/telescopeTimes' % runId)

# ---------- RUN-TARGET APIs ----------
    def getRunTargets(self, runId):
        """Retrieve list of targets for given run.

        api: GET /obsRuns/{runId}/targets

        usage:
            ::
            targets, version  = api.getRunTargets(runId)
        """
        return self.get('/obsRuns/%d/targets' % runId)
   
    def updateRunTargets(self, runId, targets, version):
        """Update list of targets for given run.

        api: PUT /obsRuns/{runId}/targets

        usage:
            targets, version  = api.getRunTargets(runId)
            targets.append(targetId)
            targets, version = api.updateRunTargets(targets)
        """
        return self.put('/obsRuns/%d/targets' % runId, targets, version)
   
# ---------- OBSERVING SETUP APIs ----------
    def getObservingSetups(self, runId):
        """Retrieve list of observing setups.

        api: GET /obsRuns/{runId}/observingSetups

        usage:
              observingSetups, version = api.getObservingSetups(runId)
        """
        return self.get('/obsRuns/%d/observingSetups' % runId)

    def createObservingSetup(self, runId, name):
        """Create an observing setup.

        api: POST /obsRuns/{runId}/observingSetups

        usage:
            observingSetups, version = api.getObservingSetups(runId)
        """
        return self.post('/obsRuns/%d/observingSetups' % runId, { 'name': name })

    def getObservingSetup(self, obsSetupId):
        """Get an observing setup.

        api: GET /observingSetups/{obsSetupId}

        usage:
            observingSetup, _ = api.getObservingSetup(obsSetupId)
        """
        return self.get('/observingSetups/%d' % obsSetupId)

    def updateObservingSetup(self, obsSetup, version):
        """Update an observing setup.

        api: PUT /observingSetups/{obsSetupId}

        usage:
            observingSetup, version = api.getObservingSetup(obsSetupId)
            observingSetup['name'] = 'New Name'
            observingSetup, version = api.updateObservingSetup(obsSetup, version)
        """
        return self.put('/observingSetups/%d' % obsSetup['obsSetupId'], obsSetup, version)

    def deleteObservingSetup(self, obsSetupId, version):
        """Delete an observing setup.

        api: DELETE /observingSetups/{obsSetupId}

        usage:
            observingSetup, version = api.getObservingSetup(obsSetupId)
            api.deleteObservingSetup(obsSetupId, version)
        """
        return self.delete('/observingSetups/%d' % obsSetupId, version)

    def reorderObservingSetups(self, runId, observingSetups, version):
        """Reorder list of observing setups.

        api: PUT /obsRuns/{runId}/observingSetups

        usage:
            observingSetups, version = api.getObservingSetups(runId)
            observingSetups.reverse()
            observingSetups, version = api.reorderObservingSetups(runId, observingSetups, version)
        """
        return self.put('/obsRuns/%d/observingSetups' % runId, observingSetups, version)

# ---------- TEMPLATE APIs ----------
    def getTemplates(self, obsSetupId):
        """Get list of templates for a given observing setup.

        api: GET /observingSetups/{obsSetupId}/templates

        usage:
              templates, version = api.getTemplates(obsSetupId)
        """
        return self.get('/observingSetups/%d/templates' % obsSetupId)
    
    def createTemplate(self, obsSetupId, templateName): 
        """Append a new template to a given observing setup.

        api: PUT /observingSetups/{obsSetupId}/templates

        usage:
            template, version = api.createTemplate(obsSetupId, 'HAWKI_img_obs_GenericOffset')
        """
        return self.post('/observingSetups/%d/templates' % obsSetupId, { 'templateName': templateName })

    def getTemplate(self, obsSetupId, templateId):
        """Get a template.

        api: GET /observingSetups/{obsSetupId}/templates/{templateId}

        usage:
            template, _ = api.getTemplate(obsSetupId, templateId)
        """
        return self.get('/observingSetups/%d/templates/%d' % (obsSetupId, templateId))
    
    def updateTemplate(self, obsSetupId, template, version):
        """Update a template.

        api: PUT /observingSetups/{obsSetupId}/templates/{templateId}

        usage:
            template, version = api.getTemplate(obsSetupId, templateId)
            filterParam = [p for p in template['parameters'] if p['name'] == 'INS.FILT.NAME'][0]
            filterParam['value'] = 'NB2090'
            template, version = api.updateTemplate(26993, template, version)
        """
        return self.put('/observingSetups/%d/templates/%d' % (obsSetupId, template['templateId']), template, version)

    def deleteTemplate(self, obsSetupId, templateId, version):
        """Delete a template.

        api: DELETE /observingSetups/{obsSetupId}/templates/{templateId}

        usage:
            template, version = api.getTemplate(obsSetupId, templateId)
            api.deleteTemplate(obsSetupId, template['templateId'], version)
        """
        return self.delete('/observingSetups/%d/templates/%d' % (obsSetupId, templateId), version)

    def reorderTemplates(self, obsSetupId, templates, version):
        """Reorder list of templates.

        api: PUT /observingSetups/{obsSetupId}/templates

        usage:
            templates, version  = api.getTemplates(obsSetupId)  
            temp = templates[1]
            templates[1] = templates[2]
            templates[2] = temp
            templates, version = api.reorderTemplates(obsSetupId, templates, version)
        """
        return self.put('/observingSetups/%d/templates' % obsSetupId, templates, version)

# ---------- OBSERVATION APIs ----------
    def getObservations(self, runId):
        """Retrieve, for the given run
            - all observing setups including their templates
            - all observations including their templates for all targets

        api: GET /obsRuns/{runId}/observations

        usage:
              observations, _ = api.getObservations(runId)
        """
        return self.get('/obsRuns/%d/observations' % runId)

    def getObservation(self, targetId, obsSetupId):
        """Get an observation (including its templates).

        api: GET /targets/{targetId}/observations/{obsSetupId}

        usage:
            observation, version = api.getObservation(targetId, obsSetupId)
        """
        return self.get('/targets/%d/observations/%d' % (targetId, obsSetupId))

    def updateObservation(self, targetId, observation, version):
        """Update an observation.

        api: PUT /targets/{targetId}/observations/{obsSetupId}

        usage:
             observation, version = api.getObservation(targetId, obsSetupId)
             observation['telescopeTime'] = 1000
             observation['repeatCount'] = 42
        """
        return self.put('/targets/%d/observations/%d' % (targetId, observation['obsSetupId']), observation, version)

    def getObservationTemplate(self, targetId, templateId):
        """Get an observation template.

        api: GET /targets/{targetId}/templates/{templateId}

        usage:
            obsTemplate, _ = api.getObservationTemplate(targetId, templateId)
        """
        return self.get('/targets/%d/templates/%d' % (targetId, templateId))
 
    def updateObservationTemplate(self, targetId, obsTemplate, version):
        """Update an observation template.

        api: PUT /targets/{targetId}/templates/{templateId}

        usage:
            obsTemplate, version = api.getObservationTemplate(targetId, templateId)
            obsTemplate['integrationTime'] = 420
            obsTemplate['overheads'] = 30
            obsTemplate['snr'] = 50
            obsTemplate, version = api.updateObservationTemplate(targetId, obsTemplate, version)                      
        """
        return self.put('/targets/%d/templates/%d' % (targetId, obsTemplate['templateId']), obsTemplate, version)

# ---------- CYCLE APIs ----------
    def getCycles(self):
        """Get list of submission cycles.

        api: GET /cycles

        usage:
            cycles, _ = api.getCycles()
        """
        return self.get('/cycles')

# ---------- private methods ----------
#  Retry Handling for requests
# See https://www.peterbe.com/plog/best-practice-with-retries-with-requests
# Or https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
    def requests_retry_session(self):
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session = requests.Session()
        session.mount('https://', adapter)
        return session
    
    def request(self, method, url, data=None, etag=None):
        self.request_count += 1

        # configure request headers
        assert self.access_token is not None
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'
        }
        if data is not None:
            headers['Content-Type'] = 'application/json'
        if etag is not None:
            headers['If-Match'] = etag

        # make request
        url = self.apiUrl + url
        if self.debug:
            print(method, url, data)
        r = self.session.request(method, url, headers=headers, data=json.dumps(data))
        content_type = r.headers['Content-Type'].split(';')[0]
        etag = r.headers.get('ETag', None)

        # handle response
        if 200 <= r.status_code < 300:
            if content_type == 'application/json':
                data = r.json()
                return data, etag
            return None, etag
        elif content_type == 'application/json' and 'error' in r.json():
            raise P1Error(r.status_code, method, url, r.json()['error'])
        else:
            raise P1Error(r.status_code, method, url, 'oops unknown error')

    def uploadFile(self, method, url, filename, contentType, etag=None):
        basename = os.path.basename(filename)
        assert self.access_token is not None
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Disposition': 'inline; filename="%s"' % basename,
            'Content-Type': contentType
        }
        if etag is not None:
            headers['If-Match'] = etag
        with open(filename, 'rb') as f:
            r = self.session.request(method, self.apiUrl + url, data=f, headers=headers)
            if r.status_code == 201 or r.status_code == 204:
                etag = r.headers.get('ETag', None)
                return basename, etag
            else:
                content_type = r.headers['Content-Type'].split(';')[0]
                if content_type == 'application/json' and 'error' in r.json():
                    raise P1Error(r.status_code, method, url, r.json()['error'])
                else:
                    raise P1Error(r.status_code, method, url, 'oops unknown error')

    def downloadTextFile(self, url, filename):
        assert self.access_token is not None
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'text/plain'
        }
        r = self.session.request('GET', self.apiUrl + url, stream=True, headers=headers)
        with open(filename, 'wb') as f:
            for line in r.iter_lines():
                f.write(line + b'\n')
        return None, r.headers.get('ETag', None)

    def downloadBinaryFile(self, url, filename):
        assert self.access_token is not None
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }
        r = self.session.request('GET', self.apiUrl + url, stream=True, headers=headers)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        return None, None

    def get(self, url):
        return self.request('GET', url)

    def put(self, url, data, etag=None):
        return self.request('PUT', url, data, etag)

    def post(self, url, data=None, etag=None):
        return self.request('POST', url, data, etag)

    def delete(self, url, etag=None):
        return self.request('DELETE', url, etag=etag)