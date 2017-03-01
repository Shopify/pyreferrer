from __future__ import unicode_literals
from __future__ import absolute_import
from pyreferrer.ruleset import Ruleset
from pyreferrer.ip import is_valid_ip
import tldextract

try:
    # Python2
    from urlparse import urlparse, parse_qs
except ImportError:
    # Python3
    from urllib.parse import urlparse, parse_qs


class Referrer:

    class Types:
        INVALID = 'invalid'
        INDIRECT = 'indirect'
        DIRECT = 'direct'
        SEARCH = 'search'
        SOCIAL = 'social'
        EMAIL = 'email'

    USER_AGENT_SUBSTRINGS = [
        (['Twitter'], {'tld': 'com', 'domain': 'twitter', 'url': 'twitter://twitter.com', 'registered_domain': 'twitter.com'}),
        (['Pinterest'], {'tld': 'com', 'domain': 'pinterest', 'url': 'pinterest://pinterest.com', 'registered_domain': 'pinterest.com'}),
        (['FBAV', 'Facebook', 'FBAN', 'FB_IAB'], {'tld': 'com', 'domain': 'facebook', 'url': 'facebook://facebook.com', 'registered_domain': 'facebook.com'}),
        (['Instagram'], {'tld': 'com', 'domain': 'instagram', 'url': 'instagram://instagram.com', 'registered_domain': 'instagram.com'}),
    ]

    BLANK_REFERRER = {
        'type': Types.INVALID,
        'url': '',
        'subdomain': '',
        'domain': '',
        'label': '',
        'tld': '',
        'path': '',
        'query': ''
    }

    rules = Ruleset().rules

    @staticmethod
    def parse_query_string(url, parameters):
        if not parameters:
            return ''
        query_params = parse_qs(url.query.encode('utf-8'), keep_blank_values=True)
        query_common = set.intersection(set(query_params.keys()), set(parameters))
        fragment_params = parse_qs(url.fragment, keep_blank_values=True)
        fragment_common = set.intersection(set(fragment_params.keys()), set(parameters))
        query = ''
        if len(query_common) > 0:
            query = query_params[list(query_common)[0]][0]
        elif len(fragment_common) > 0:
            query = fragment_params[list(fragment_common)[0]][0]
        elif '*' in parameters:
            query = ''
        return query.decode('utf-8')

    @staticmethod
    def is_valid_url(url, domain_info):
        return url.scheme and domain_info.domain and domain_info.suffix

    @staticmethod
    def is_valid_ip(url):
        return url.scheme and is_valid_ip(url.netloc)

    @staticmethod
    def extract_user_agent_info(user_agent):
            empty_info = {'domain': '', 'url': '', 'tld': '', 'registered_domain': ''}
            if user_agent is None:
                    return empty_info
            for substrings, domain_info in Referrer.USER_AGENT_SUBSTRINGS:
                    if any(substring in user_agent for substring in substrings):
                            return domain_info
            return empty_info

    @staticmethod
    def parse(raw_url, custom_rules=None, user_agent=None):
        if raw_url is None and user_agent is None:
            return Referrer.BLANK_REFERRER
        raw_url = raw_url.strip()
        rules = custom_rules or Referrer.rules
        parsed_url = urlparse(raw_url)
        domain_info = tldextract.extract(raw_url)
        user_agent_info = Referrer.extract_user_agent_info(user_agent)

        referrer = {
            'type': Referrer.Types.INDIRECT,
            'url': raw_url or user_agent_info['url'],
            'subdomain': domain_info.subdomain,
            'domain': domain_info.domain or user_agent_info['domain'],
            'label': domain_info.domain.title(),
            'tld': domain_info.suffix or user_agent_info['tld'],
            'path': parsed_url.path,
            'query': ''
        }

        if Referrer.is_valid_url(parsed_url, domain_info) or Referrer.is_valid_ip(parsed_url):
            # First check for an exact match of the url. Then check for a match with different combinations of domain, subdomain and tld
            known_url = rules.get(parsed_url.netloc + parsed_url.path) \
                or rules.get(domain_info.registered_domain + parsed_url.path) \
                or rules.get(parsed_url.netloc) \
                or rules.get(domain_info.registered_domain)

            if known_url:
                referrer['label'] = known_url['label']
                referrer['type'] = known_url['type']
                referrer['query'] = Referrer.parse_query_string(parsed_url, known_url.get('parameters'))
        elif user_agent_info['registered_domain']:
            known_url = rules.get(user_agent_info['registered_domain'])

            if known_url:
                referrer['label'] = known_url['label']
                referrer['type'] = known_url['type']
                referrer['query'] = Referrer.parse_query_string(parsed_url, known_url.get('parameters'))
        else:
            referrer['type'] = Referrer.Types.INVALID if raw_url else Referrer.Types.DIRECT
        return referrer
