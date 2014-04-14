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

"""Poll handlers."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'


import datetime
import logging
import webapp2

import httplib2
from apiclient.http import BatchHttpRequest
from oauth2client.appengine import StorageByKeyName
from oauth2client.client import AccessTokenRefreshError

from model import UserSettings
import util


MINUTES_PER_HOUR = 60

# 8am in minutes.
DAY_TIME_START = 8 * MINUTES_PER_HOUR

# 8pm in minutes.
DAY_TIME_STOP = 20 * MINUTES_PER_HOUR

# Limit requests per batch request to 50.
BATCH_REQUEST_COUNT = 50


def _insert_cat_fact_callback(userid, response, exception):
  """Callback for the Mirror API insert batch request."""
  if exception:
    logging.error(
        'Failed to insert cat fact for user %s: %s', userid, exception)


class PushCronHandler(webapp2.RequestHandler):
  """Handler for push cron job."""

  def get(self):
    """Retrieve all users and add taskqueue to poll Twitter feed."""
    body = {
        'text': util.get_cat_fact(),
        'notification': {'level': 'DEFAULT'}
    }
    # Limit 50 requests per batch request.
    batch_requests = []
    count = BATCH_REQUEST_COUNT
    for user_settings in self.entities_to_process():
      request = self._get_cat_fact_insert_request(
          user_settings.key().name(), body)
      if request:
        if count >= BATCH_REQUEST_COUNT:
          batch = BatchHttpRequest(callback=_insert_cat_fact_callback)
          batch_requests.append(batch)
          count = 0
        batch.add(request)
        count += 1
    for batch in batch_requests:
      batch.execute()

  def entities_to_process(self):
    """Yield entities that should be processed."""
    now = datetime.datetime.utcnow()
    quarter_mark = (now.minute / 15) * 15
    now_minute = now.hour * 60 + quarter_mark
    query = UserSettings.all()
    if quarter_mark == 30:
      query.filter('frequency IN', [15, 30])
    elif quarter_mark == 15 or quarter_mark == 45:
      query.filter('frequency =', 15)
    for user_settings in query:
      if user_settings.night_mode:
        yield user_settings
      else:
        shifted_now = (now_minute - user_settings.timezone_offset) % 1440
        # Verify that this is day time in the user's timezone.
        if shifted_now >= DAY_TIME_START and shifted_now < DAY_TIME_STOP:
          yield user_settings

  def _get_cat_fact_insert_request(self, userid, body):
    """Poll Twitter feed for the provided user."""
    try:
      creds = StorageByKeyName(UserSettings, userid, 'credentials').get()
      creds.refresh(httplib2.Http())
      service = util.create_service('mirror', 'v1', creds)
      return service.timeline().insert(body=body)
    except AccessTokenRefreshError:
      logging.error('Unable to refresh token for user %s', userid)
      return None


PUSH_ROUTES = [
    ('/push', PushCronHandler)
]
