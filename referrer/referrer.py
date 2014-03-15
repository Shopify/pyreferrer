from .rules import Rules
import json
from urlparse import urlparse

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
    pass

  @staticmethod
  def parse_search(raw_url, url=None):
    if not url:
      url = urlparse(raw_url)
    domain = url.netloc
    if domain not in Referrer.rules.search:
      return None
    rule = Referrer.rules.social[domain]
    return {
      'type': Referrer.Types.SEARCH,
      'url': raw_url,
      'domain': rule['domain'],
      'label': rule['label'],
      'query': '',
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

# func parseDirect(rawUrl string, u *url.URL, directDomains []string) *Direct {
#   for _, host := range directDomains {
#     if host == u.Host {
#       return &Direct{URL: rawUrl, Domain: u.Host}
#     }
#   }
#   return nil
# }

# func parseSocial(rawUrl string, u *url.URL) *Social {
#   if rule, ok := SocialRules[u.Host]; ok {
#     return &Social{URL: rawUrl, Domain: rule.Domain, Label: rule.Label}
#   }
#   return nil
# }

# func parseEmail(rawUrl string, u *url.URL) *Email {
#   if rule, ok := EmailRules[u.Host]; ok {
#     return &Email{URL: rawUrl, Domain: rule.Domain, Label: rule.Label}
#   }
#   return nil
# }

# func parseSearch(rawUrl string, u *url.URL) *Search {
#   query, _ := url.ParseQuery(u.Fragment)
#   if query == nil {
#     query = make(url.Values)
#   }
#   for key, values := range u.Query() {
#     query[key] = values
#   }

#   if rule, ok := SearchRules[u.Host]; ok {
#     for _, param := range rule.Parameters {
#       if param == ParameterWildcard {
#         return &Search{URL: rawUrl, Domain: rule.Domain, Label: rule.Label, Query: ""}
#       }
#       if search, ok := query[param]; ok {
#         return &Search{URL: rawUrl, Domain: rule.Domain, Label: rule.Label, Query: search[0]}
#       }
#     }
#   }
#   return nil
# }

# func fuzzyParseSearch(u *url.URL) *Search {
#   hostParts := strings.Split(u.Host, ".")

#   query, _ := url.ParseQuery(u.Fragment)
#   if query == nil {
#     query = make(url.Values)
#   }
#   for key, values := range u.Query() {
#     query[key] = values
#   }

#   for _, hostPart := range hostParts {
#     if engine, present := SearchEngines[hostPart]; present {
#       for _, param := range engine.Parameters {
#         if param == ParameterWildcard {
#           return &Search{Label: engine.Label, Query: "", Domain: u.Host}
#         }
#         if search, ok := query[param]; ok {
#           return &Search{Label: engine.Label, Query: search[0], Domain: u.Host}
#         }
#       }
#     }
#   }
#   return nil
# }