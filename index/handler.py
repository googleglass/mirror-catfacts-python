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


import jinja2
import webapp2

import util


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    autoescape=True)


class IndexHandler(webapp2.RequestHandler):
  """Request handler to display the index page."""

  def get(self):
    """Display the index page."""
    approval_prompt = 'auto'
    button_display = 'none'
    if self.request.get('approvalPrompt') == 'force':
      approval_prompt = 'force'
      button_display = 'block'
    template_data = {
        'approvalPrompt': approval_prompt,
        'buttonDisplay': button_display,
        'clientId': util.get_client_id(),
        'scope': ' '.join(util.SCOPES),
    }
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_data))


INDEX_ROUTES = [
    ('/', IndexHandler),
]
