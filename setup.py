from distutils.core import setup

setup(name='pyreferrer',
      version='0.5.1',
      description='A referrer parser for Python.',
      url='http://github.com/Shopify/pyreferrer',
      author='Shopify Data Acceleration',
      author_email='data-acceleration@shopify.com',
      license='MIT',
      packages=['pyreferrer'],
      package_data={'pyreferrer': ['data/*', ]},
      install_requires=['tldextract==2.0.2'],
      extras_require={
          'test': ['nose'],
      },
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
      ],
      include_package_data=True,
      zip_safe=False)
