# coding=utf-8
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

def test_search_simple():
  referrer = Referrer.parse('http://search.yahoo.com/search?p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search?p=hello',
    'domain': 'search.yahoo.com',
    'query': 'hello',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_query_in_fragment():
  referrer = Referrer.parse('http://search.yahoo.com/search#p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search#p=hello',
    'domain': 'search.yahoo.com',
    'query': 'hello',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_fuzzy_yahoo_country():
  referrer = Referrer.parse('http://ca.search.yahoo.com/search?p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://ca.search.yahoo.com/search?p=hello',
    'domain': 'ca.search.yahoo.com',
    'query': 'hello',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_fuzzy_yahoo_country_and_query_in_fragment():
  referrer = Referrer.parse('http://ca.search.yahoo.com/search#p=hello')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://ca.search.yahoo.com/search#p=hello',
    'domain': 'ca.search.yahoo.com',
    'query': 'hello',
  }
  assert_equals(expected_referrer, referrer)

def test_search_bing_not_live():
  referrer = Referrer.parse('http://bing.com/?q=blargh')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Bing',
    'url': 'http://bing.com/?q=blargh',
    'domain': 'bing.com',
    'query': 'blargh',
  }
  assert_equals(expected_referrer, referrer)

def test_search_non_ascii():
  assert_equals.__self__.maxDiff = None
  referrer = Referrer.parse('http://search.yahoo.com/search;_ylt=A0geu8fBeW5SqVEAZ2vrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDWmxUdFhVZ2V1eVVMYVp6c1VmRmRMUXUyMkxfbjJsSnVlY0VBQlhDWQRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANVRFRzSGFBUVF0ZUZHZ2hzZ0N3VDNBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgbXlzaG9waWZ5IHJlbmf4cmluZyBta29iZXRpYwR0X3N0bXADMTM4Mjk3MjM1NDIzMwR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+myshopify+rengøring+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search;_ylt=A0geu8fBeW5SqVEAZ2vrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDWmxUdFhVZ2V1eVVMYVp6c1VmRmRMUXUyMkxfbjJsSnVlY0VBQlhDWQRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANVRFRzSGFBUVF0ZUZHZ2hzZ0N3VDNBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgbXlzaG9waWZ5IHJlbmf4cmluZyBta29iZXRpYwR0X3N0bXADMTM4Mjk3MjM1NDIzMwR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+myshopify+rengøring+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1',
    'domain': 'search.yahoo.com',
    'query': 'vinduespudsning myshopify rengøring mkobetic',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_cryllics():
  assert_equals.__self__.maxDiff = None
  referrer = Referrer.parse('http://www.yandex.com/yandsearch?text=%D0%B1%D0%BE%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%20packer-shoes&lr=87&msid=22868.18811.1382712652.60127&noreask=1')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yandex',
    'url': 'http://www.yandex.com/yandsearch?text=%D0%B1%D0%BE%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%20packer-shoes&lr=87&msid=22868.18811.1382712652.60127&noreask=1',
    'domain': 'www.yandex.com',
    'query': 'ботинки packer-shoes',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_explicit_plus():
  referrer = Referrer.parse('http://search.yahoo.com/search;_ylt=A0geu8nVvm5StDIAIxHrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDSjNTOW9rZ2V1eVVMYVp6c1VmRmRMUkdDMkxfbjJsSnV2dFVBQmZyWgRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANDc01MSGlnTVFOS2k2cDRqcUxERzRBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgSk9LQVBPTEFSICIxMSArIDExIiBta29iZXRpYwR0X3N0bXADMTM4Mjk4OTYwMjg3OQR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+JOKAPOLAR+"11+%2B+11"+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'http://search.yahoo.com/search;_ylt=A0geu8nVvm5StDIAIxHrFAx.;_ylc=X1MDMjExNDcyMTAwMwRfcgMyBGJjawMwbXFjc3RoOHYybjlkJTI2YiUzRDMlMjZzJTNEYWkEY3NyY3B2aWQDSjNTOW9rZ2V1eVVMYVp6c1VmRmRMUkdDMkxfbjJsSnV2dFVBQmZyWgRmcgN5ZnAtdC03MTUEZnIyA3NiLXRvcARncHJpZANDc01MSGlnTVFOS2k2cDRqcUxERzRBBG10ZXN0aWQDbnVsbARuX3JzbHQDMARuX3N1Z2cDMARvcmlnaW4DY2Euc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAwRxc3RybAM0NARxdWVyeQN2aW5kdWVzcHVkc25pbmcgSk9LQVBPTEFSICIxMSArIDExIiBta29iZXRpYwR0X3N0bXADMTM4Mjk4OTYwMjg3OQR2dGVzdGlkA01TWUNBQzE-?p=vinduespudsning+JOKAPOLAR+"11+%2B+11"+mkobetic&fr2=sb-top&fr=yfp-t-715&rd=r1',
    'domain': 'search.yahoo.com',
    'query': 'vinduespudsning JOKAPOLAR "11 + 11" mkobetic',
  }
  assert_equals(expected_referrer, referrer)

def test_search_with_empty_query():
  referrer = Referrer.parse('https://yahoo.com?p=&sa=t&rct=j&p=&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Yahoo!',
    'url': 'https://yahoo.com?p=&sa=t&rct=j&p=&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk',
    'domain': 'yahoo.com',
    'query': '',
  }
  assert_equals(expected_referrer, referrer)

def test_search_google_https_with_no_params():
  referrer = Referrer.parse('https://google.com')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Google',
    'url': 'https://google.com',
    'domain': 'google.com',
    'query': '',
  }
  assert_equals(expected_referrer, referrer)

def test_search_google_with_query():
  referrer = Referrer.parse('https://www.google.co.in/url?sa=t&rct=j&q=test&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk')
  expected_referrer = {
    'type': Referrer.Types.SEARCH,
    'label': 'Google',
    'url': 'https://www.google.co.in/url?sa=t&rct=j&q=test&esrc=s&source=web&cd=1&ved=0CDkQFjAA&url=http%3A%2F%2Fwww.yellowfashion.in%2F&ei=aZCPUtXmLcGQrQepkIHACA&usg=AFQjCNE-R5-7CENi9oqYe4vG-0g0E7nCSQ&bvm=bv.56988011,d.bmk',
    'domain': 'www.google.co.in',
    'query': 'test',
  }
  assert_equals(expected_referrer, referrer)
