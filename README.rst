Getting Started |Build Status| |Code Climate| |PyPy Version|
------------------------------------------------------------

Installation
''''''''''''

.. code:: bash

    # installing the latest signed release
    pip install twitter-ads

Quick Start
'''''''''''

.. code:: python

    from twitter_ads.client import Client
    from twitter_ads.campaign import Campaign

    CONSUMER_KEY = 'your consumer key'
    CONSUMER_SECRET = 'your consumer secret'
    ACCESS_TOKEN = 'access token'
    ACCESS_TOKEN_SECRET = 'access token secret'
    ACCOUNT_ID = 'account id'

    # initialize the client
    client = Client(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # load the advertiser account instance
    account = client.accounts(ACCOUNT_ID)

    # load and update a specific campaign
    campaign = account.campaigns().next()
    campaign.name = 'updated campaign name'
    campaign.paused = True
    campaign.save()

    # iterate through campaigns
    for campaign in account.campaigns():
        print(campaign.id)



Command Line Helper
'''''''''''''''''''

.. code:: bash

    # The twitter-ads command launches an interactive session for testing purposes
    # with a client instance automatically loaded from your .twurlrc file.

    ~ ❯ twitter-ads

For more help please see our `Examples and Guides`_ or check the online
`Reference Documentation`_.

Compatibility & Versioning
--------------------------

This project is designed to work with Python 2.7 or greater. While it
may work on other version of Python, below are the platform and runtime
versions we officially support and regularly test against.

+------------+-------------------------+
| Platform   | Versions                |
+============+=========================+
| CPython    | 2.7, 3.3, 3.4, 3.5      |
+------------+-------------------------+
| PyPy       | 2.x, 4.x                |
+------------+-------------------------+

All releases adhere to strict `semantic versioning`_. For Example,
major.minor.patch-pre (aka. stick.carrot.oops-peek).

Development
-----------

If you’d like to contribute to the project or try an unreleased
development version of this project locally, you can do so quite easily
by following the examples below.

.. code:: bash

    # clone the repository
    git clone git@github.com:twitterdev/twitter-python-ads-sdk.git
    cd twitter-python-ads-sdk

    # install dependencies
    pip install -r requirements.txt

    # installing a local unsigned release
    pip install -e .

We love community contributions! If you’re planning to send us a pull
request, please make sure read our `Contributing Guidelines`_ first.

Feedback and Bug Reports
------------------------

Found an issue? Please open up a `GitHub issue`_ or even better yet
`send us`_ a pull request. Have a question? Want to discuss a new
feature? Come chat with us in the `Twitter Community Forums`_.

Error Handling
--------------

Like the `Response`_ and `Request`_ classes, the Ads API SDK fully models
all `error objects`_ for easy error handling.

|error-hierarchy|

License
-------

The MIT License (MIT)

Copyright (C) 2015 Twitter, Inc.

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

.. _Examples and Guides: https://github.com/twitterdev/twitter-python-ads-sdk/tree/master/examples
.. _Reference Documentation: http://twitterdev.github.io/twitter-python-ads-sdk/reference/index.html
.. _semantic versioning: http://semver.org
.. _Contributing Guidelines: https://github.com/twitterdev/twitter-python-ads-sdk/blob/master/CONTRIBUTING.rst
.. _GitHub issue: https://github.com/twitterdev/twitter-python-ads-sdk/issues
.. _send us: https://github.com/twitterdev/twitter-python-ads-sdk/blob/master/CONTRIBUTING.rst
.. _Twitter Community Forums: https://twittercommunity.com/c/advertiser-api

.. |Build Status| image:: https://travis-ci.org/twitterdev/twitter-python-ads-sdk.svg?branch=master
   :target: https://travis-ci.org/twitterdev/twitter-python-ads-sdk
.. |Code Climate| image:: https://codeclimate.com/github/twitterdev/twitter-python-ads-sdk/badges/gpa.svg
   :target: https://codeclimate.com/github/twitterdev/twitter-python-ads-sdk
.. |PyPy Version| image:: https://badge.fury.io/py/twitter-ads.svg
   :target: http://badge.fury.io/py/twitter-ads

.. _Request: https://github.com/twitterdev/twitter-python-ads-sdk/blob/master/twitter_ads/http.py#L28
.. _Response: https://github.com/twitterdev/twitter-python-ads-sdk/blob/master/twitter_ads/http.py#L118
.. _error objects: https://github.com/twitterdev/twitter-python-ads-sdk/blob/master/twitter_ads/error.py
.. |error-hierarchy| image:: http://i.imgur.com/XcLDWLO.png
