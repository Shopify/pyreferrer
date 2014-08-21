from distutils.core import setup

setup(name='pyreferrer',
      version='0.3.0',
      description='A referrer parser for Python.',
      url='http://github.com/Shopify/pyreferrer',
      author='Steven Normore',
      author_email='snormore@gmail.com',
      license='MIT',
      packages=['pyreferrer'],
      package_data={'pyreferrer': ['data/*', ]},
      install_requires=['tldextract'],
      include_package_data=True,
      zip_safe=False)
