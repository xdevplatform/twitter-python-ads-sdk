import sys
import string
import random

def with_resource(resource):
    return 'https://ads-api.twitter.com{resource}'.format(resource=resource)

def with_fixture(name):
    f = open('tests/fixtures/{name}.json'.format(name=name), 'r')
    return f.read()

def characters(length):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
