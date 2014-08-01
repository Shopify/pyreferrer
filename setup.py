from distutils.core import setup

setup(name='pyreferrer',
      version='0.2.4',
      description='A referrer parser for Python.',
      url='http://github.com/snormore/pyreferrer',
      author='Steven Normore',
      author_email='snormore@gmail.com',
      license='MIT',
      packages=['pyreferrer'],
      package_data={'pyreferrer': ['data/*', ]},
      include_package_data=True,
      zip_safe=False)
