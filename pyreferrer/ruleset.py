from __future__ import absolute_import
from __future__ import unicode_literals
from pkg_resources import resource_filename
from io import open
import json


class Ruleset:
    def __init__(self, data_path='data/referrers.json'):
        self.data_path = data_path

        raw_rules_path = resource_filename(__name__, data_path)
        raw_rules = json.load(open(raw_rules_path))

        self.rules = self.generate_rules(raw_rules)

    def generate_rules(self, raw_rules):
        rules = {}
        for rule_type, raw_rule in raw_rules.items():
            for label, rule in raw_rule.items():
                for domain in rule['domains']:
                    rules[domain] = {'label': label, 'domain': domain, 'parameters': rule.get('parameters'), 'type': rule_type}
        return rules
