# Copyright (C) 2014 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility classes and methods for Mirror Cat Facts."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'


import logging
import json
import random
import webapp2

import httplib2
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials


CLIENT_SECRETS_FILE = 'client_secrets.json'

SCOPES = [
    'https://www.googleapis.com/auth/glass.timeline',
    'https://www.googleapis.com/auth/plus.login'
]

TOKENINFO_URL = 'https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=%s'

CAT_FACTS_FILENAME = 'cat_facts.txt'


def create_service(service, version, creds=None):
  """Create a Google API service.

  Load an API service from a discovery document and authorize it with the
  provided credentials.
  This sends a request to Google's Discovery API everytime the function is
  called. A more efficient way to use this API is to cache the API discovery
  file and use apiclient.discovery.build_from_document instead.

  Args:
    service: Service name (e.g 'mirror', 'oauth2').
    version: Service version (e.g 'v1').
    creds: Credentials used to authorize service.
  Returns:
    Authorized Google API service.
  """
  # Instantiate an Http instance
  http = httplib2.Http()
  if creds:
    # Authorize the Http instance with the passed credentials
    creds.authorize(http)
  return build(service, version, http=http)


def verify_token(access_token):
  """Verify that the access token has been issued for our application.

  Args:
    access_token: Token to verify.
  Returns:
    User ID if access_token is valid and has been issued for our application.
  """
  url = TOKENINFO_URL % access_token
  http = httplib2.Http()
  tokeninfo = json.loads(http.request(url, 'GET')[1])
  if tokeninfo.get('audience') != get_client_id():
    return None
  # Verify that the token has the required scopes.
  token_scopes = tokeninfo.get('scope').split(' ')
  for required_scope in SCOPES:
    if required_scope not in token_scopes:
      return None
  return tokeninfo['user_id']


def get_client_id():
  """Return the application's client ID."""
  client_secrets = json.load(file('client_secrets.json'))
  return client_secrets['web']['client_id']


def write_response(request, data):
  """Write a request's response body as JSON."""
  request.response.headers['Content-type'] = 'application/json'
  request.response.out.write(json.dumps(data))


def get_cat_fact():
  """Retrieve a random cat fact."""
  # This should probably cached.
  f = open(CAT_FACTS_FILENAME)
  facts = list(f)
  if facts:
    return facts[random.randrange(0, len(facts))]
  else:
    return 'No cat fact found :('
