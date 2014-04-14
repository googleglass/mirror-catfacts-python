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

"""Error classes."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'

import json

import util


class Error(Exception):
  """Base API error used inside this module."""
  code = 500


class BadRequestError(Error):
  """Bad request error."""
  code = 400


class UnauthorizedError(Error):
  """Unauthorized error."""
  code = 401


class NotFoundError(Error):
  """Not found error."""
  code = 404


class InternalServerError(Error):
  """Unauthorized error."""
  code = 500


def error_aware(method):
  """Decorator catching Cat Facts errors.

  Args:
    method: Method being decorated.
  Returns:
    Decorated method.
  """

  def _request(request_handler, *args):
    """Surround request_handler.method(*args) with try/except for errors.

    Args:
      request_handler: Request handler which method is being called.
    """
    try:
      method(request_handler, *args)
    except Error, error:
      response_body = {
          'error': {
              'status': error.code,
              'message': error.message
          }
      }
      request_handler.response.clear()
      request_handler.response.set_status(error.code)
      util.write_response(request_handler, response_body)
  return _request
