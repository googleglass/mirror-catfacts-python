/*
 * Copyright (c) 2014 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

/**
 * User's accessToken retrieved from Google's authentication servers.
 */
var accessToken = null;

/**
 * Notifies the user that their settings have been saved by fading in the
 * status bar.
 */
var showStatus = function(message) {
  $('#status-bar').text(message);
  $('#status-bar').clearQueue().fadeIn(250).delay(3000).fadeOut();
};

/**
 * Processes the authentication flow.
 */
var signInCallback = function(authResult) {
  if (authResult['code'] || authResult['access_token']) {
    // Hide the sign-in button now that the user is authorized.
    $('#signin-button').hide();

    accessToken = authResult['access_token'];
    // Send the code to the server
    showStatus('Loading settings...');
    $.ajax({
      type: 'POST',
      url: '/auth',
      contentType: 'application/json',
      success: function(result) {
        $('#result').show();
        $('#frequency').val(result['frequency']);
        $('#night-mode').prop('checked', result['nightMode']);
        // Make sure that the cat background is in the correct state when the
        // page loads.
        if ($('#night-mode').prop('checked')) {
          $('.cat-bg.night').show();
        }
        showStatus('Welcome to Cat Facts!');
      },
      error: function(response) {
        // Could not find a refresh token for the current user.
        if (response.status == 401) {
          window.location = './?approvalPrompt=force'
        }
      },
      processData: false,
      data: JSON.stringify({
        'code': authResult['code'],
        'timezoneOffset': new Date().getTimezoneOffset()
      })
    });
  } else if (authResult['error']) {
    // There was an error.
    // Possible error codes:
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatially log in the user
    // console.log('There was an error: ' + authResult['error']);

    // Show the sign-in button.
    $('#signin-button').show();
  }
}

/**
 * Updates the user settings.
 */
var updateSettings = function() {
  showStatus('Saving settings...');
  $.ajax({
    type: 'PUT',
    url: '/settings',
    contentType: 'application/json',
    headers: {
      'Authorization': accessToken
    },
    success: function(result) {
      $('#frequency').val(result['frequency']);
      $('#night-mode').prop('checked', result['nightMode']);
      showStatus('Your settings have been saved.');
    },
    processData: false,
    data: JSON.stringify({
      'frequency': parseInt($('#frequency').val(), 10),
      'nightMode': $('#night-mode').prop('checked'),
      'timezoneOffset': new Date().getTimezoneOffset()
    })
  });
};

/**
 * Adds callbacks when document is ready.
 */
$(function() {
  // Update the cat background and the server state when the night mode
  // checkbox is changed.
  $('#night-mode').change(function() {
    if ($(this).prop('checked')) {
      $('.cat-bg.night').fadeIn(250);
    } else {
      $('.cat-bg.night').fadeOut(250);
    }
    updateSettings();
  });

  // Update the server state when the night mode checkbox is changed.
  $('#frequency').change(function() {
    updateSettings();
  });
});
