# Copyright (C) 2013 Google Inc.
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

"""OAuth 2.0 handlers."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'

import json
import webapp2

from oauth2client.appengine import StorageByKeyName
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import errors
import model
import util


# Defaults to EST.
DEFAULT_TIMEZONE_OFFSET = 240


class OAuthCodeExchangeHandler(webapp2.RequestHandler):
  """Request handler for OAuth 2.0 code exchange."""

  @errors.error_aware
  def post(self):
    """Handle code exchange."""
    self._process_request_body()
    self._exchange_code()
    user = self._create_user()
    util.write_response(self, user.to_dict())

  def _process_request_body(self):
    """Parse the request body."""
    try:
      request = json.loads(self.request.body)

      self._code = request.get('code')
      if not self._code:
        raise errors.BadRequestError('`code` attribute is required')

      self._timezone_offset = request.get(
          'timezoneOffset', DEFAULT_TIMEZONE_OFFSET)
    except ValueError:
      raise errors.BadRequestError('Unsupported request body')

  def _exchange_code(self):
    """Retrieve credentials for the current user."""
    oauth_flow = self._create_oauth_flow()
    # Perform the exchange of the code.
    try:
      creds = oauth_flow.step2_exchange(self._code)
    except FlowExchangeError, e:
      raise errors.InternalServerError('Unable to exchange code: ', e.message)

    # Verify that the token has been issued for our application.
    self._userid = util.verify_token(creds.access_token)
    if not self._userid:
      raise errors.BadRequestError('Unknown client ID')

    # Verify that we can retrieve valid refresh token for the current user.
    if creds.refresh_token:
      # Store the credentials in the data store using the userid as the key.
      StorageByKeyName(
          model.UserSettings, self._userid, 'credentials').put(creds)
    else:
      # Look for existing credentials in our datastore.
      creds = StorageByKeyName(
          model.UserSettings, self._userid, 'credentials').get()
      if not creds or not creds.refresh_token:
        raise errors.UnauthorizedError('No refresh token')
    return creds

  def _create_user(self):
    """Create a new user model."""
    user_settings = model.UserSettings.get_by_key_name(self._userid)
    user_settings.timezone_offset = self._timezone_offset
    user_settings.put()
    return user_settings

  def _create_oauth_flow(self):
    """Create OAuth2.0 flow controller."""
    flow = flow_from_clientsecrets(
        util.CLIENT_SECRETS_FILE, scope=' '.join(util.SCOPES))
    flow.redirect_uri = 'postmessage'
    return flow


OAUTH_ROUTES = [
    ('/auth', OAuthCodeExchangeHandler),
]
