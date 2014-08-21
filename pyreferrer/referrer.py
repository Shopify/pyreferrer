from __future__ import unicode_literals
from .ruleset import Ruleset
import json
import tldextract
from urlparse import urlparse, parse_qs

class Referrer:

  class Types:
    INVALID  = 'invalid'
    INDIRECT = 'indirect'
    DIRECT   = 'direct'
    SEARCH   = 'search'
    SOCIAL   = 'social'
    EMAIL    = 'email'

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

    query_params = parse_qs(url.query, keep_blank_values=True)
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
    return query

  @staticmethod
  def is_valid_url(url, domain_info):
    return url.scheme and domain_info.domain and domain_info.tld

  @staticmethod
  def parse(raw_url, custom_rules=None):
    if raw_url is None:
      return Referrer.BLANK_REFERRER
    raw_url = raw_url.strip()
    rules = custom_rules or Referrer.rules
    url = urlparse(raw_url)
    domain_info = tldextract.extract(raw_url)

    referrer = {
      'type': Referrer.Types.INDIRECT,
      'url': raw_url,
      'subdomain': domain_info.subdomain,
      'domain': domain_info.domain,
      'label': domain_info.domain.title(),
      'tld': domain_info.suffix,
      'path': url.path,
      'query': ''
    }

    if Referrer.is_valid_url(url, domain_info):
      # First check for an exact match of the url. Then check for a match with different combinations of domain, subdomain and tld
      known_url = rules.get(url.netloc + url.path)\
                  or rules.get(domain_info.registered_domain + url.path)\
                  or rules.get(url.netloc)\
                  or rules.get(domain_info.registered_domain)

      if known_url:
        referrer['label'] = known_url['label']
        referrer['type'] = known_url['type']
        referrer['query'] = Referrer.parse_query_string(url, known_url.get('parameters'))
    else:
      referrer['type'] = Referrer.Types.INVALID if raw_url else Referrer.Types.DIRECT

    return referrer

def parse(raw_url):
  return Referrer(raw_url).parse
