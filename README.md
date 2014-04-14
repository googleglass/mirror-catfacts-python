mirror-catfacts-python
======================

This sample delivers periodic cat fact notifications using users'
preferences.

## Getting Started

1. [Create a Google App Engine application](https://developers.google.com/appengine/docs/python/gettingstartedpython27/uploading).
2. Enter your Google App Engine App ID in the `app.yaml` file.
3. [Create a Google API Project](https://developers.google.com/console/help/#creatingdeletingprojects)
   and enable the `Google+ API` and the `Google Mirror API`.
4. [Create an OAuth 2.0 client ID](https://developers.google.com/console/help/#generatingoauth2),
   setting your application's URL as an authorized `JavaScript origins`.
5. Enter your OAuth 2.0 client ID and client Secret in the
   `client_secrets.json` file.
6. Upload your Google App Engine application:

    $ appcfg.py --oauth2 update .

Credits
-------

* Original compliation of Cat Facts can be found on this
  [reddit thread](http://www.reddit.com/r/funny/comments/oyokn/it_seems_to_be_catching_on/c3l5v8r)
