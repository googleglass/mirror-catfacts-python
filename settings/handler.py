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

"""Settings handlers."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'


import webapp2
import json

import errors
from model import UserSettings
import util


class SettingsHandler(webapp2.RequestHandler):
  """Handler for the settings endpoint."""

  @errors.error_aware
  def get(self):
    """Retrieve settings for the provided user."""
    self._get_user()
    util.write_response(self, self._user.to_dict())

  @errors.error_aware
  def put(self):
    """Update settings for the provided user."""
    self._get_user()
    self._process_request_body()
    util.write_response(self, self._user.to_dict())

  def _get_user(self):
    userid = util.verify_token(self.request.headers.get('Authorization'))
    if not userid:
      raise errors.BadRequestError('Unknown client ID')
    self._user = UserSettings.get_by_key_name(userid)
    if not self._user:
      raise errors.NotFoundError('Unknown user')

  def _process_request_body(self):
    """Parse the request body."""
    try:
      data = json.loads(self.request.body)
      self._user.night_mode = data.get('nightMode', self._user.night_mode)
      self._user.frequency = data.get('frequency', self._user.frequency)
      self._user.timezone_offset = data.get(
          'timezoneOffset', self._user.timezone_offset)
      self._user.put()
    except ValueError:
      raise errors.BadRequestError('Unsupported request body')


SETTINGS_ROUTES = [
    ('/settings', SettingsHandler),
]
