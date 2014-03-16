from pkg_resources import resource_filename
import json
import csv

class Rules:
  def __init__(self, data_path='data/referrers.json', search_data_path='data/search.csv'):
    self.data_path = data_path
    self.search_data_path = search_data_path

    raw_rules_path = resource_filename(__name__, data_path)
    raw_rules = json.load(open(raw_rules_path))

    fuzzy_search_rules_path = resource_filename(__name__, search_data_path)
    raw_fuzzy_search_rules = csv.reader(open(fuzzy_search_rules_path), delimiter=':')

    self.search = self.generate_search_rules(raw_rules['search'])
    self.search_fuzzy = self.generate_search_fuzzy_rules(raw_fuzzy_search_rules)
    self.social = self.generate_social_rules(raw_rules['social'])
    self.email = self.generate_email_rules(raw_rules['email'])

  def generate_search_rules(self, raw_rules):
    rules = {}
    for label, rule in raw_rules.items():
      for domain in rule['domains']:
        rules[domain] = {'label': label, 'domain': domain, 'parameters': rule['parameters']}
    return rules

  def generate_search_fuzzy_rules(self, raw_rules):
    rules = {}
    for row in raw_rules:
      rules[row[1]] = {'label': row[0], 'domain': row[1], 'parameters': row[2].split(',')}
    return rules

  def generate_social_rules(self, raw_rules):
    rules = {}
    for label, raw_rule in raw_rules.items():
      for domain in raw_rule['domains']:
        rule = {'label': label, 'domain': domain}
        rules[domain] = rule
        for prefix in ['www', 'm']:
          rules['%s.%s' % (prefix, domain, )] = rule
    return rules

  def generate_email_rules(self, raw_rules):
    rules = {}
    for label, rule in raw_rules.items():
      for domain in rule['domains']:
        rules[domain] = {'label': label, 'domain': domain}
    return rules
