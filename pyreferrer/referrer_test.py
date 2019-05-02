# coding=utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from pyreferrer.referrer import Referrer
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
        'query': 'vinduespudsning myshopify rengøring mkobetic'
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
        'query': 'vinduespudsning JOKAPOLAR "11 + 11" mkobetic'
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
        'query': ''
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
        'query': ''
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
        'query': 'test'
    }
    assert_equals(expected_referrer, referrer)


def test_search_google_image():
    referrer = Referrer.parse('https://www.google.ca/imgres?q=tbn:ANd9GcRXBkHjJiAvKXkjGzSEhilZS5vJX0UPFmyZTlmmRFpiv-IYQmj4')
    expected_referrer = {
        'type': Referrer.Types.SEARCH,
        'label': 'Google Images',
        'url': 'https://www.google.ca/imgres?q=tbn:ANd9GcRXBkHjJiAvKXkjGzSEhilZS5vJX0UPFmyZTlmmRFpiv-IYQmj4',
        'domain': 'google',
        'subdomain': 'www',
        'tld': 'ca',
        'path': '/imgres',
        'query': 'tbn:ANd9GcRXBkHjJiAvKXkjGzSEhilZS5vJX0UPFmyZTlmmRFpiv-IYQmj4'
    }
    assert_equals(expected_referrer, referrer)


def test_search_google_adwords():
    referrer = Referrer.parse('http://www.google.ca/aclk?sa=l&ai=Cp3RJ8ri&sig=AOD64f7w&clui=0&rct=j&q=&ved=0CBoQDEA&adurl=http://www.domain.com/')
    expected_referrer = {
        'type': Referrer.Types.SEARCH,
        'label': 'Google',
        'url': 'http://www.google.ca/aclk?sa=l&ai=Cp3RJ8ri&sig=AOD64f7w&clui=0&rct=j&q=&ved=0CBoQDEA&adurl=http://www.domain.com/',
        'domain': 'google',
        'subdomain': 'www',
        'tld': 'ca',
        'path': '/aclk',
        'query': ''
    }
    assert_equals(expected_referrer, referrer)


def test_search_google_pagead():
    referrer = Referrer.parse('http://www.googleadservices.com/pagead/aclk?sa=l&q=flowers&ohost=www.google.com')
    expected_referrer = {
        'type': Referrer.Types.SEARCH,
        'label': 'Google',
        'url': 'http://www.googleadservices.com/pagead/aclk?sa=l&q=flowers&ohost=www.google.com',
        'domain': 'googleadservices',
        'subdomain': 'www',
        'tld': 'com',
        'path': '/pagead/aclk',
        'query': 'flowers'
    }
    assert_equals(expected_referrer, referrer)


def test_blank_referrer_with_user_agent_is_enchanced_by_user_agent():
    user_agent_from_twitter = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a Twitter for iPhone'
    blank_referrer_with_twitter_ua = Referrer.parse('', user_agent=user_agent_from_twitter)
    expected_referrer = {
        'type': Referrer.Types.SOCIAL,
        'url': 'twitter://twitter.com',
        'subdomain': '',
        'domain': 'twitter',
        'label': 'Twitter',
        'tld': 'com',
        'path': '',
        'query': ''
    }
    assert_equals(expected_referrer, blank_referrer_with_twitter_ua)


def test_twitter_user_agent_gives_the_same_info_as_twitter_url_except_for_url():
    user_agent_from_twitter = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a Twitter for iPhone'

    referrer_with_url = Referrer.parse('https://twitter.com')
    referrer_with_ua = Referrer.parse('', user_agent=user_agent_from_twitter)
    del referrer_with_url['url']
    del referrer_with_ua['url']
    assert_equals(referrer_with_ua, referrer_with_url)


def test_canonical_user_agent_with_twitter_gives_the_same_info_as_twitter_url_except_for_url():
    canonical_user_agent_from_twitter = 'Mobile Safari 7.1 using iOS 7.1 on Mobile with Twitter Mobile App'

    referrer_with_url = Referrer.parse('https://twitter.com')
    referrer_with_ua = Referrer.parse('', user_agent=canonical_user_agent_from_twitter)
    del referrer_with_url['url']
    del referrer_with_ua['url']
    assert_equals(referrer_with_ua, referrer_with_url)


def test_providing_both_user_agent_and_url_is_okay():
    user_agent = 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10'

    referrer_with_url_and_ua = Referrer.parse('https://twitter.com', user_agent=user_agent)
    expected_referrer = {
        'type': Referrer.Types.SOCIAL,
        'url': 'https://twitter.com',
        'subdomain': '',
        'domain': 'twitter',
        'label': 'Twitter',
        'tld': 'com',
        'path': '',
        'query': ''
    }
    assert_equals(expected_referrer, referrer_with_url_and_ua)


def test_provided_twitter_url_overrides_what_is_present_in_twitter_useragent():
    user_agent_from_pinterest = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a [Pinterest/iOS]'
    referrer_with_twitter_url_and_pinterest_ua = Referrer.parse('https://twitter.com', user_agent=user_agent_from_pinterest)
    expected_referrer = {
        'type': Referrer.Types.SOCIAL,
        'url': 'https://twitter.com',
        'subdomain': '',
        'domain': 'twitter',
        'label': 'Twitter',
        'tld': 'com',
        'path': '',
        'query': ''
    }
    assert_equals(expected_referrer, referrer_with_twitter_url_and_pinterest_ua)


def test_doesnt_fail_if_empty_referrer_url_and_non_social_ua():
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a'
    referrer = Referrer.parse('', user_agent=user_agent)
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
    assert_equals(expected_referrer, referrer)


def test_ua_isnt_applied_if_url_is_not_blank():
    social_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a  [Pintest/iOS]'
    referrer = Referrer.parse('https://www.savealoonie.com', user_agent=social_user_agent)
    expected_referrer = {
        'type': Referrer.Types.INDIRECT,
        'url': 'https://www.savealoonie.com',
        'subdomain': 'www',
        'domain': 'savealoonie',
        'label': 'Savealoonie',
        'tld': 'com',
        'path': '',
        'query': ''
    }
    assert_equals(expected_referrer, referrer)


def test_pyreferrer_works_with_unicode_urls():
    referrer = Referrer.parse(u'http://президент.рф/')
    expected_referrer = {
        'domain': u'президент',
        'query': u'',
        'tld': u'рф',
        'url': u'http://президент.рф/',
        'path': u'/',
        'subdomain': u'',
        'type': u'indirect',
        'label': u'Президент'
    }
    assert_equals(referrer, expected_referrer)


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
        'query': 'ботинки packer-shoes'
    }
    assert_equals(expected_referrer, referrer)


def test_pyreferrer_works_with_unicode_query_terms():
    referrer = Referrer.parse(u'https://buy.theanimalrescuesite.greatergood.com/products/74275-pet-lovers-ultralite-woven-mary-jane-shoes?utm_source=ARS-ARS-LAL&utm_medium=paid-fb&utm_term=02052017&utm_content=Photo&utm_campaign=PetLoversUltralite™WovenMaryJaneShoes_74275&origin=ARS_face_sponsor_ARS-LAL_PetLoversUltralite™WovenMaryJaneShoes_74275_02052017')
    expected_referrer = {
        'domain': 'greatergood',
        'label': 'Greatergood',
        'path': '/products/74275-pet-lovers-ultralite-woven-mary-jane-shoes',
        'query': '',
        'subdomain': 'buy.theanimalrescuesite',
        'tld': 'com',
        'type': 'indirect',
        'url': 'https://buy.theanimalrescuesite.greatergood.com/products/74275-pet-lovers-ultralite-woven-mary-jane-shoes?utm_source=ARS-ARS-LAL&utm_medium=paid-fb&utm_term=02052017&utm_content=Photo&utm_campaign=PetLoversUltralite™WovenMaryJaneShoes_74275&origin=ARS_face_sponsor_ARS-LAL_PetLoversUltralite™WovenMaryJaneShoes_74275_02052017'
    }
    assert_equals(referrer, expected_referrer)

def test_different_domain_suffix_maps_to_known_label():
    pinterest_com = Referrer.parse('https://pinterest.com')
    pinterest_uk = Referrer.parse('https://pinterest.co.uk')
    pinterest_au = Referrer.parse('https://www.pinterest.com.au')
    pinterest_ca = Referrer.parse('https://pinterest.ca')
    pinterest_non_registered_domain = Referrer.parse('https://pinterest.bs')

    expected_com = {
        'type': Referrer.Types.SOCIAL,
        'label': 'Pinterest',
        'url': 'https://pinterest.com',
        'domain': 'pinterest',
        'subdomain': '',
        'tld': 'com',
        'path': '',
        'query': ''
    }

    expected_uk = {
        'type': Referrer.Types.SOCIAL,
        'label': 'Pinterest',
        'url': 'https://pinterest.co.uk',
        'domain': 'pinterest',
        'subdomain': '',
        'tld': 'co.uk',
        'path': '',
        'query': ''
    }

    expected_au = {
        'type': Referrer.Types.SOCIAL,
        'label': 'Pinterest',
        'url': 'https://www.pinterest.com.au',
        'domain': 'pinterest',
        'subdomain': 'www',
        'tld': 'com.au',
        'path': '',
        'query': ''
    }

    expected_ca = {
        'type': Referrer.Types.SOCIAL,
        'label': 'Pinterest',
        'url': 'https://pinterest.ca',
        'domain': 'pinterest',
        'subdomain': '',
        'tld': 'ca',
        'path': '',
        'query': ''
    }

    # .bs is not a registered domain for Pinterest so it should map to INDIRECT
    expected_bs = {
        'type': Referrer.Types.INDIRECT,
        'label': 'Pinterest',
        'url': 'https://pinterest.bs',
        'domain': 'pinterest',
        'subdomain': '',
        'tld': 'bs',
        'path': '',
        'query': ''
    }

    assert_equals(pinterest_com, expected_com)
    assert_equals(pinterest_uk, expected_uk)
    assert_equals(pinterest_au, expected_au)
    assert_equals(pinterest_ca, expected_ca)
    assert_equals(pinterest_non_registered_domain, expected_bs)
