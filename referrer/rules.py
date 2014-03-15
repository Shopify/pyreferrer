from pkg_resources import resource_filename
import json
import csv

class Rules:
  PARAMETER_WILDCARD = '*'

  def __init__(self, data_path='data/referrers.json', search_data_path='data/search.csv'):
    self.data_path = data_path
    self.search_data_path = search_data_path

    raw_rules_path = resource_filename(__name__, data_path)
    raw_rules = json.load(open(raw_rules_path))

    fuzzy_search_rules_path = resource_filename(__name__, search_data_path)
    raw_fuzzy_search_rules = csv.reader(open(fuzzy_search_rules_path), delimiter=',')

    self.search = self.generate_search_rules(raw_rules['search'], raw_fuzzy_search_rules)
    self.social = self.generate_social_rules(raw_rules['social'])
    self.email = self.generate_email_rules(raw_rules['email'])

  def generate_search_rules(self, raw_rules, fuzzy_search_rules):
    rules = {}
    for label, rule in raw_rules.items():
      for domain in rule['domains']:
        rules[domain] = {'label': label, 'domain': domain}
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

# type SearchRule struct {
#   Label      string
#   Domain     string
#   Parameters []string
# }

# // RuleSet maps the JSON structure in the file
# type RuleSet map[string]map[string][]string

# func mappedSearchRules(rawRules RuleSet) map[string]SearchRule {
#   mappedRules := make(map[string]SearchRule)
#   for label, rawRule := range rawRules {
#     for _, domain := range rawRule["domains"] {
#       rule := SearchRule{Label: label, Domain: domain}
#       rawParams := rawRule["parameters"]
#       params := make([]string, len(rawParams))
#       for _, param := range rawParams {
#         params = append(params, param)
#       }
#       rule.Parameters = params
#       mappedRules[rule.Domain] = rule
#     }
#   }
#   return mappedRules
# }

# func readSearchEngines(enginesPath string) (map[string]SearchRule, error) {
#   enginesCsv, err := ioutil.ReadFile(enginesPath)
#   if err != nil {
#     return nil, err
#   }
#   engines := make(map[string]SearchRule)
#   scanner := bufio.NewScanner(strings.NewReader(string(enginesCsv)))
#   for scanner.Scan() {
#     line := strings.Trim(scanner.Text(), " \n\r\t")
#     if line != "" && line[0] != '#' {
#       tokens := strings.Split(line, ":")
#       params := strings.Split(tokens[2], ",")
#       engines[tokens[1]] = SearchRule{Label: tokens[0], Domain: tokens[1], Parameters: params}
#     }
#   }
#   return engines, nil
# }