from .rules import Rules
import json
from urlparse import urlparse, parse_qs

class Referrer:

  class Types:
    INDIRECT = 'indirect'
    DIRECT   = 'direct'
    SEARCH   = 'search'
    SOCIAL   = 'social'
    EMAIL    = 'email'

  rules = Rules()

  @staticmethod
  def parse_direct(raw_url, direct_domains, url=None):
    if not url:
      url = urlparse(raw_url)
    domain = url.netloc
    if domain not in direct_domains:
      return None
    return {
      'type': Referrer.Types.DIRECT,
      'url': raw_url,
      'domain': domain,
    }

  @staticmethod
  def parse_email(raw_url, url=None):
    if not url:
      url = urlparse(raw_url)
    domain = url.netloc
    if domain not in Referrer.rules.email:
      return None
    rule = Referrer.rules.email[domain]
    return {
      'type': Referrer.Types.EMAIL,
      'url': raw_url,
      'domain': rule['domain'],
      'label': rule['label'],
    }

  @staticmethod
  def parse_social(raw_url, url=None):
    if not url:
      url = urlparse(raw_url)
    domain = url.netloc
    if domain not in Referrer.rules.social:
      return None
    rule = Referrer.rules.social[domain]
    return {
      'type': Referrer.Types.SOCIAL,
      'url': raw_url,
      'domain': rule['domain'],
      'label': rule['label'],
    }

  @staticmethod
  def parse_search_fuzzy(raw_url, url=None):
    if not url:
      url = urlparse(raw_url)
    domain = url.netloc
    host_parts = domain.split('.')
    for host_part in host_parts:
      if host_part not in Referrer.rules.search_fuzzy:
        continue
      rule = Referrer.rules.search_fuzzy[host_part]
      query_params = parse_qs(url.query, keep_blank_values=True)
      query_common = set.intersection(set(query_params.keys()), set(rule['parameters']))
      fragment_params = parse_qs(url.fragment, keep_blank_values=True)
      fragment_common = set.intersection(set(fragment_params.keys()), set(rule['parameters']))
      query = None
      if len(query_common) > 0:
        query = query_params[list(query_common)[0]][0]
      elif len(fragment_common) > 0:
        query = fragment_params[list(fragment_common)[0]][0]
      elif '*' in rule['parameters']:
        query = ''
      if query is not None:
        return {
          'type': Referrer.Types.SEARCH,
          'url': raw_url,
          'domain': domain,
          'label': rule['label'],
          'query': query,
        }
    return None

  @staticmethod
  def parse_search(raw_url, url=None):
    if not url:
      url = urlparse(raw_url)
    domain = url.netloc
    if domain not in Referrer.rules.search:
      return Referrer.parse_search_fuzzy(raw_url, url=url)
    rule = Referrer.rules.search[domain]
    query_params = parse_qs(url.query, keep_blank_values=True)
    query_common = set.intersection(set(query_params.keys()), set(rule['parameters']))
    fragment_params = parse_qs(url.fragment, keep_blank_values=True)
    fragment_common = set.intersection(set(fragment_params.keys()), set(rule['parameters']))
    query = ''
    if len(query_common) > 0:
      query = query_params[list(query_common)[0]][0]
    elif len(fragment_common) > 0:
      query = fragment_params[list(fragment_common)[0]][0]
    elif '*' in rule['parameters']:
      query = ''
    else:
      return Referrer.parse_search_fuzzy(raw_url, url=url)
    return {
      'type': Referrer.Types.SEARCH,
      'url': raw_url,
      'domain': rule['domain'],
      'label': rule['label'],
      'query': query,
    }

  @staticmethod
  def parse_indirect(raw_url, url=None):
    if not url:
      url = urlparse(raw_url)
    return {
      'type': Referrer.Types.INDIRECT,
      'url': raw_url,
      'domain': url.netloc,
    }

  @staticmethod
  def parse(raw_url, direct_domains=[]):
    url = urlparse(raw_url)

    referrer = Referrer.parse_direct(raw_url, direct_domains, url=url); 
    if referrer:
      return referrer

    referrer = Referrer.parse_email(raw_url, url=url)
    if referrer:
      return referrer

    referrer = Referrer.parse_social(raw_url, url=url)
    if referrer:
      return referrer

    referrer = Referrer.parse_search(raw_url, url=url)
    if referrer:
      return referrer

    return Referrer.parse_indirect(raw_url, url=url)

def parse(raw_url, direct_domains=[]):
  return Referrer(raw_url, direct_domains).parse
