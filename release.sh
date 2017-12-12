#!/usr/bin/env bash

RELEASE=$(printf "from twitter_ads.utils import get_version\nprint(get_version())" | python)

# tag the release
git tag "v$RELEASE"
git push --tags

# clean and build new docs
cd docs && make clean && make html && cd ..

# release new docs
git checkout gh-pages
rm -rf reference/*
cp -R docs/build/html/* reference/
git add reference
git commit -m "\"[update] docs refresh for $RELEASE\""
git push origin HEAD:gh-pages
git checkout master

# push to pypi (deprecated)
# python setup.py sdist upload --sign --identity="Twitter Ads API <twitterdev-ads@twitter.com>"

# push using twine
# build
python setup.py sdist bdist_wheel
# upload
twine upload dist/* --sign --identity="Twitter Ads API <twitterdev-ads@twitter.com>"