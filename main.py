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

"""RequestHandlers for starter project."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'


# Add the library location to the path
import sys
sys.path.insert(0, 'libs')

import webapp2

from index.handler import INDEX_ROUTES
from oauth.handler import OAUTH_ROUTES
from push.handler import PUSH_ROUTES
from settings.handler import SETTINGS_ROUTES


ROUTES = OAUTH_ROUTES + SETTINGS_ROUTES + INDEX_ROUTES + PUSH_ROUTES


app = webapp2.WSGIApplication(ROUTES)
