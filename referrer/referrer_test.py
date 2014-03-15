from referrer import *
from nose.tools import assert_equals

def test_relative_url():
  referrer = Referrer.parse('buh')
  expected_referrer = {
    'type': Referrer.Types.INDIRECT,
    'url': 'buh',
    'domain': '',
  }
  assert_equals(expected_referrer, referrer)

def test_direct_simple():
  referrer = Referrer.parse('http://example.com', direct_domains=['example.com', 'sample.com'])
  expected_referrer = {
    'type': Referrer.Types.DIRECT,
    'url': 'http://example.com',
    'domain': 'example.com',
  }
  assert_equals(expected_referrer, referrer)

def test_indirect_simple():
  referrer = Referrer.parse('http://walrus.com/', direct_domains=['example.com', 'sample.com'])
  expected_referrer = {
    'type': Referrer.Types.INDIRECT,
    'url': 'http://walrus.com/',
    'domain': 'walrus.com',
  }
  assert_equals(expected_referrer, referrer)

def test_email_simple():
  referrer = Referrer.parse('https://mail.google.com/9aifaufasodf8usafd')
  expected_referrer = {
    'type': Referrer.Types.EMAIL,
    'label': 'Gmail',
    'url': 'https://mail.google.com/9aifaufasodf8usafd',
    'domain': 'mail.google.com',
  }
  assert_equals(expected_referrer, referrer)

def test_social_simple():
  referrer = Referrer.parse('https://twitter.com/snormore/status/391149968360103936')
  expected_referrer = {
    'type': Referrer.Types.SOCIAL,
    'label': 'Twitter',
    'url': 'https://twitter.com/snormore/status/391149968360103936',
    'domain': 'twitter.com',
  }
  assert_equals(expected_referrer, referrer)

def test_social_with_prefix_www():
  referrer = Referrer.parse('https://www.twitter.com/snormore/status/391149968360103936')
  expected_referrer = {
    'type': Referrer.Types.SOCIAL,
    'label': 'Twitter',
    'url': 'https://www.twitter.com/snormore/status/391149968360103936',
    'domain': 'twitter.com',
  }
  assert_equals(expected_referrer, referrer)

def test_social_with_prefix_m():
  referrer = Referrer.parse('https://m.twitter.com/snormore/status/391149968360103936')
  expected_referrer = {
    'type': Referrer.Types.SOCIAL,
    'label': 'Twitter',
    'url': 'https://m.twitter.com/snormore/status/391149968360103936',
    'domain': 'twitter.com',
  }
  assert_equals(expected_referrer, referrer)

def test_social_google_plus():
  referrer = Referrer.parse('http://plus.url.google.com/url?sa=z&n=1394219098538&url=http%3A%2F%2Fjoe.blogspot.ca&usg=jo2tEVIcI5Wh-6t--v-1ODEeGG8.')
  expected_referrer = {
    'type': Referrer.Types.SOCIAL,
    'label': 'Google+',
    'url': 'http://plus.url.google.com/url?sa=z&n=1394219098538&url=http%3A%2F%2Fjoe.blogspot.ca&usg=jo2tEVIcI5Wh-6t--v-1ODEeGG8.',
    'domain': 'plus.url.google.com',
  }
  assert_equals(expected_referrer, referrer)


