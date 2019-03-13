from distutils.core import setup

setup(name='pyreferrer',
      version='0.5.0',
      description='A referrer parser for Python.',
      url='http://github.com/Shopify/pyreferrer',
      author='Shopify Data Acceleration',
      author_email='data-acceleration@shopify.com',
      license='MIT',
      packages=['pyreferrer'],
      package_data={'pyreferrer': ['data/*', ]},
      install_requires=['git+https://github.com/prabcs/tldextract.git@3ed52ab482033c7ec5b3d133a0258fe32d187281#egg=tldextract'],
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
