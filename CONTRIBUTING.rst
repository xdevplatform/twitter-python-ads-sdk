Contributing Guidelines
=======================

We love pull requests from everyone!

We encourage community contributions for all kinds of changes both big
and small, but we ask that you adhere to the following guidelines for
contributing code.

Proposing Changes
'''''''''''''''''

As a starting point for all changes, we recommend `reporting an issue`_
before you begin making any changes. Make sure to search the issues on
this repository first to check and see the issue has already been
previously discussed and whether or not it’s already being worked on.

-  For small changes, improvements and bug fixes please feel free to
   send us a pull request with proposed changes along-side the issue you
   report.

-  For larger more involved or design related changes, please open an
   issue and discuss the changes with the other contributors before
   submitting any pull requests.

Submitting A Pull Request
'''''''''''''''''''''''''

1) Fork us and clone the repository locally.

.. code:: bash

    git clone git@github.com:twitterdev/twitter-python-ads-sdk.git

2) Install development dependencies (`virtualenv recommended`_):

.. code:: bash

    pip install -r requirements.txt

3) Make sure all tests pass before you start:

.. code:: bash

    python setup.py test

4) Make your changes! (Don’t forget tests and documentation)

5) Check style and test your changes again to make sure everything is green:

.. code:: bash

    python setup.py flake8 && python setup.py test

The test suite will automatically enforce test coverage and code style.
This project adhere’s fully to the `PEP-8 style guide`_ (100 character line
length allowed) and we use `Flake8`_ to enforce style and code quality.

6) Submit your changes!

-  `Squash`_ your development commits. Put features in a single clean commit whenever possible or logically split it into a few commits (no development commits). Test coverage can be included in a separate commit if preferred.
-  Write a `good commit message`_ for your change.
-  Push to your fork.
-  Submit a `pull request`_.

We try to at least comment on pull requests within one business day and
may suggest changes.

Release Schedule and Versioning
'''''''''''''''''''''''''''''''

We have a regular release cadence and adhere to `semantic versioning`_.
When exactly your change ships will depend on the scope of your changes
and what type of upcoming release its best suited for.

.. _reporting an issue: https://github.com/twitterdev/twitter-python-ads-sdk/issues?q=is%3Aopen+is%3Aissue
.. _PEP-8 style guide: https://www.python.org/dev/peps/pep-0008
.. _Flake8: https://github.com/twitterdev/twitter-python-ads-sdk/blob/master/setup.cfg
.. _good commit message: http://chris.beams.io/posts/git-commit/
.. _pull request: https://github.com/thoughtbot/suspenders/compare/
.. _semantic versioning: http://semver.org/
.. _virtualenv recommended: https://virtualenv.readthedocs.org
.. _Squash: http://eli.thegreenplace.net/2014/02/19/squashing-github-pull-requests-into-a-single-commit
