from setuptools import setup

setup(name='pyreferrer',
      version='0.1',
      description='A referrer parser for Python.',
      url='http://github.com/snormore/pyreferrer',
      author='Steven Normore',
      author_email='snormore@gmail.com',
      license='MIT',
      packages=['pyreferrer'],
      package_data={'pyreferrer': ['data/referrers.json', 'search.csv', ]},
      include_package_data=True,
      zip_safe=False)
