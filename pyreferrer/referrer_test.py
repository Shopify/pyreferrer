# coding=utf-8

from referrer import *
from nose.tools import assert_equals

def test_parse_splits_the_url_into_its_components():
  referrer = Referrer.parse('http://mysubdomain.myothersubdomain.supersite.co.uk/party/time?q=ohyeah&t=555')
  expected_referrer = {
    'type': Referrer.Types.INDIRECT,
    'url': 'http://mysubdomain.myothersubdomain.supersite.co.uk/party/time?q=ohyeah&t=555',
    'subdomain': 'mysubdomain.myothersubdomain',
    'domain': 'supersite',
    'label': 'Supersite',
    'tld': 'co.uk',
    'path': '/party/time',
    'query': ''
  }
  assert_equals(expected_referrer, referrer)

def test_blank_referrer_is_classified_as_direct():
  blank_referrer = Referrer.parse('')
  whitespace_referrer = Referrer.parse('     ')
  expected_referrer = {
    'type': Referrer.Types.DIRECT,
    'url': '',
    'subdomain': '',
    'domain': '',
    'label': '',
    'tld': '',
    'path': '',
    'query': ''
  }
  assert_equals(expected_referrer, blank_referrer)
  assert_equals(expected_referrer, whitespace_referrer)

def test_a_url_that_does_not_match_any_known_urls_is_classified_as_indirect():
  referrer = Referrer.parse('http://walrus.com/')
  assert_equals(Referrer.Types.INDIRECT, referrer['type'])

def test_a_url_that_does_not_match_any_known_urls_has_its_label_set_as_the_capitalized_domain():
  referrer = Referrer.parse('http://walrus.com/')
  assert_equals('Walrus', referrer['label'])

def test_an_invalid_url_or_absolute_url_is_classified_as_invalid():
  urls = [
      'blap',
      'blap blap',
      'http://blapblap',
      'http://.com',
      'http://',
      '/',
    ]
  for url in urls:
    referrer = Referrer.parse(url)
    assert_equals(Referrer.Types.INVALID, referrer['type'])

def test_parse_with_nonetype_passed_in_is_invalid():
  referrer = Referrer.parse(None)
  assert_equals(Referrer.Types.INVALID, referrer['type'])

def test_parse_tries_to_match_a_known_url_using_everything_but_the_query_string():
  rules = {"www.zambo.com/search": {"type": "search", "label": "Zambo"}}
  referrer = Referrer.parse("http://www.zambo.com/search?q=hello!", rules)
  assert_equals('search', referrer['type'])

def test_parse_tries_to_match_a_known_url_using_the_domain_and_tld_and_path():
  rules = {"zambo.com/search": {"type": "search", "label": "Zambo"}}
  referrer = Referrer.parse("http://www.zambo.com/search?q=hello!", rules)
  assert_equals('search', referrer['type'])

def test_parse_tries_to_match_a_known_url_using_the_subdomains_domain_and_tld():
  rules = {"www.zambo.com": {"type": "search", "label": "Zambo"}}
  referrer = Referrer.parse("http://www.zambo.com/search?q=hello!", rules)
  assert_equals('search', referrer['type'])

def test_parse_tries_to_match_a_known_url_using_the_domain_and_tld():
  rules = {"zambo.com": {"type": "search", "label": "Zambo"}}
  referrer = Referrer.parse("http://www.zambo.com/search?q=hello!", rules)
  assert_equals('search', referrer['type'])

def test_email_simple():
  referrer = Referrer.parse('https://mail.google.com/9aifaufasodf8usafd')
  expected_referrer = {
    'type': Referrer.Types.EMAIL,
    'label': 'Gmail',
    'url': 'https://mail.google.com/9aifaufasodf8usafd',
    'subdomain': 'mail',
    'domain': 'google',
    'tld': 'com',
    'path': '/9aifaufasodf8usafd',
    'query': ''
  }
  assert_equals(expected_referrer, referrer)

def test_social_simple():
  referrer = Referrer.parse('https://twitter.com/snormore/status/391149968360103936')
  expected_referrer = {
    'type': Referrer.Types.SOCIAL,
    'label': 'Twitter',
    'url': 'https://twitter.com/snormore/status/391149968360103936',
    'domain': 'twitter',
    'subdomain': '',
    'tld': 'com',
    'path': '/snormore/status/391149968360103936',
    'query': ''
  }
  assert_equals(expected_referrer, referrer)

def test_social_with_subdomain():
  referrer = Referrer.parse('https://puppyanimalbarn.tumblr.com')
  expected_referrer = {
    'type': Referrer.Types.SOCIAL,
    'label': 'Tumblr',
    'url': 'https://puppyanimalbarn.tumblr.com',
    'domain': 'tumblr',
    'subdomain': 'puppyanimalbarn',
    'tld': 'com',
    'path': '',
    'query': ''
  }
  assert_equals(expected_referrer, referrer)


def test_social_google_plus():
  referrer = Referrer.parse('http://plus.url.google.com/url?sa=z&n=1394219098538&url=http%3A%2F%2Fjoe.blogspot.ca&usg=jo2tEVIcI5Wh-6t--v-1ODEeGG8.')
  expected_referrer = {
    'type': Referrer.Types.SOCIAL,
    'label': 'Google+',
    'url': 'http://plus.url.google.com/url?sa=z&n=1394219098538&url=http%3A%2F%2Fjoe.blogspot.ca&usg=jo2tEVIcI5Wh-6t--v-1ODEeGG8.',
    'domain': 'google',
    'subdomain': 'plus.url',
    'tld': 'com',
    'path': '/url',
    'query': ''
  }
  assert_equals(expected_referrer, referrer)

def test_search_simple():
  referrer = Referrer.parse('http://search.yahoo.com/search?p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search?p=hello',
    'domain': 'yahoo',
    'subdomain': 'search',
    'tld': 'com',
    'path': '/search',
    'query': 'hello'
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_query_in_fragment():
  referrer = Referrer.parse('http://search.yahoo.com/search#p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search#p=hello',
    'domain': 'yahoo',
    'subdomain': 'search',
    'tld': 'com',
    'path': '/search',
    'query': 'hello'
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_yahoo_country():
  referrer = Referrer.parse('http://ca.search.yahoo.com/search?p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://ca.search.yahoo.com/search?p=hello',
    'domain': 'yahoo',
    'subdomain': 'ca.search',
    'tld': 'com',
    'path': '/search',
    'query': 'hello'
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_yahoo_country_and_query_in_fragment():
  referrer = Referrer.parse('http://ca.search.yahoo.com/search#p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://ca.search.yahoo.com/search#p=hello',
    'domain': 'yahoo',
    'subdomain': 'ca.search',
    'tld': 'com',
    'path': '/search',
    'query': 'hello'
  }
  assert_equals(expected_referrer, referrer)

def test_search_bing_not_live():
  referrer = Referrer.parse('http://bing.com/?q=blargh')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Bing',
    'url': 'http://bing.com/?q=blargh',
    'domain': 'bing',
    'subdomain': '',
    'tld': 'com',
    'path': '/',
    'query': 'blargh'
  }
  assert_equals(expected_referrer, referrer)

def test_search_non_ascii():
  assert_equals.__self__.maxDiff = None
  referrer = Referrer.parse('http://search.yahoo.com/search;_ylt=A0geu8fBeW5SqVEAZ2vrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDWmxUdFhVZ2V1eVVMYVp6c1VmRmRMUXUyMkxfbjJsSnVlY0VBQlhDWQRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANVRFRzSGFBUVF0ZUZHZ2hzZ0N3VDNBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgbXlzaG9waWZ5IHJlbmf4cmluZyBta29iZXRpYwR0X3N0bXADMTM4Mjk3MjM1NDIzMwR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+myshopify+rengøring+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search;_ylt=A0geu8fBeW5SqVEAZ2vrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDWmxUdFhVZ2V1eVVMYVp6c1VmRmRMUXUyMkxfbjJsSnVlY0VBQlhDWQRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANVRFRzSGFBUVF0ZUZHZ2hzZ0N3VDNBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgbXlzaG9waWZ5IHJlbmf4cmluZyBta29iZXRpYwR0X3N0bXADMTM4Mjk3MjM1NDIzMwR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+myshopify+rengøring+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1',
    'domain': 'yahoo',
    'subdomain': 'search',
    'tld': 'com',
    'path': '/search',
    'query': 'vinduespudsning myshopify rengøring mkobetic',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_cyrillics():
  assert_equals.__self__.maxDiff = None
  referrer = Referrer.parse('http://www.yandex.com/yandsearch?text=%D0%B1%D0%BE%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%20packer-shoes&lr=87&msid=22868.18811.1382712652.60127&noreask=1')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yandex',
    'url': 'http://www.yandex.com/yandsearch?text=%D0%B1%D0%BE%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%20packer-shoes&lr=87&msid=22868.18811.1382712652.60127&noreask=1',
    'domain': 'yandex',
    'subdomain': 'www',
    'tld': 'com',
    'path': '/yandsearch',
    'query': 'ботинки packer-shoes',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_explicit_plus():
  referrer = Referrer.parse('http://search.yahoo.com/search;_ylt=A0geu8nVvm5StDIAIxHrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDSjNTOW9rZ2V1eVVMYVp6c1VmRmRMUkdDMkxfbjJsSnV2dFVBQmZyWgRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANDc01MSGlnTVFOS2k2cDRqcUxERzRBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgSk9LQVBPTEFSICIxMSArIDExIiBta29iZXRpYwR0X3N0bXADMTM4Mjk4OTYwMjg3OQR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+JOKAPOLAR+"11+%2B+11"+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search;_ylt=A0geu8nVvm5StDIAIxHrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDSjNTOW9rZ2V1eVVMYVp6c1VmRmRMUkdDMkxfbjJsSnV2dFVBQmZyWgRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANDc01MSGlnTVFOS2k2cDRqcUxERzRBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgSk9LQVBPTEFSICIxMSArIDExIiBta29iZXRpYwR0X3N0bXADMTM4Mjk4OTYwMjg3OQR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+JOKAPOLAR+"11+%2B+11"+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1',
    'domain': 'yahoo',
    'subdomain': 'search',
    'tld': 'com',
    'path': '/search',
    'query': 'vinduespudsning JOKAPOLAR "11 + 11" mkobetic',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_empty_query():
  referrer = Referrer.parse('https://yahoo.com?p=&sa=t&rct=j&p=&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'https://yahoo.com?p=&sa=t&rct=j&p=&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk',
    'domain': 'yahoo',
    'subdomain': '',
    'tld': 'com',
    'path': '',
    'query': '',
  }
  assert_equals(expected_referrer, referrer)

def test_search_google_https_with_no_params():
  referrer = Referrer.parse('https://google.com')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Google',
    'url': 'https://google.com',
    'domain': 'google',
    'subdomain': '',
    'tld': 'com',
    'path': '',
    'query': '',
  }
  assert_equals(expected_referrer, referrer)

def test_search_google_with_query():
  referrer = Referrer.parse('https://www.google.co.in/url?sa=t&rct=j&q=test&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Google',
    'url': 'https://www.google.co.in/url?sa=t&rct=j&q=test&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk',
    'domain': 'google',
    'subdomain': 'www',
    'tld': 'co.in',
    'path': '/url',
    'query': 'test',
  }
  assert_equals(expected_referrer, referrer)
