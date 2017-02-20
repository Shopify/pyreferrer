pyreferrer
==========

`pyreferrer` is a Python package that analyzes and classifies different kinds of referrer URLs (search, social, ...). The Shopify Data Team uses it in production by passing web traffic referrerals through the library. This powers our logic behind how we can slice and dice website traffic. 

### Installing

`pip install pyreferrer`

### Quick Start

Use `Referrer.parse(referrer)` to return metadata about the referrer plus a parsed url. 

```python
from pyreferrer import Referrer

# social example
referrer = 'https://twitter.com/snormore/status/524524090938245120'
print Referrer.parse(referrer)
"""
{'domain': 'twitter',
 'label': 'Twitter',
 'path': '/snormore/status/524524090938245120',
 'query': '',
 'subdomain': '',
 'tld': 'com',
 'type': 'social',
 'url': 'https://twitter.com/snormore/status/524524090938245120'
}
"""
```

If `referrer` is a search engine results page, PyReferrer will try to extract the query term from the path, based on the domain.

```python
# search example
referrer = 'http://www.bing.com/search?q=test&go=Submit&qs=n&form=QBLH&pq=test&sc=9-4'
print Referrer.parse(referrer)
"""
{'domain': 'bing',
 'label': 'Bing',
 'path': '/search',
 'query': 'test',
 'subdomain': 'www',
 'tld': 'com',
 'type': 'search',
 'url': 'http://www.bing.com/search?q=test&go=Submit&qs=n&form=QBLH&pq=test&sc=9-4'}
 """
```

Often when clicking a link in a mobile app, the app will load another app and we lose the referrer information. In some cases, the app will use a shell of a browser, and include information in the user agent. By passing in the (optional) user-agent, we can extract the referrer again. 

```python
 # social user agent example
referrer = ''
user_agent_from_pinterest_app = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a [Pinterest/iOS]'
print Referrer.parse(referrer, user_agent=user_agent_from_pinterest_app)
"""
{'domain': 'pinterest',
 'label': 'Pinterest',
 'path': '',
 'query': '',
 'subdomain': '',
 'tld': 'com',
 'type': 'social',
 'url': 'pinterest://pinterest.com'}
 """

```


### Contributing

To contribute, please fork the repository and add the features/data you want. After merging a submitted pull request, we will deploy the package to PyPI. 

Most of the metadata is controlled by the file `pyreferrer/data/referrers.json'. Additions to this are appreciated the most, as the entire community benefits. 


