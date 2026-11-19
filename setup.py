import io

from setuptools import setup

VERSION = '0.6.7'  # maintained by release tool

with io.open("README.md", encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()


setup(
    name="pyreferrer",
    version=VERSION,
    description="A referrer parser for Python.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="http://github.com/Shopify/pyreferrer",
    author="Shopify Data Acceleration",
    author_email="data-acceleration@shopify.com",
    license="MIT",
    packages=["pyreferrer"],
    package_data={"pyreferrer": ["data/*"]},
    install_requires=["tldextract>=2.0.2,<=2.2.1", "six>=1.11.0"],
    extras_require={"test": ["nose"]},
    classifiers=[
        "Development Status :: 7 - Inactive",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
	"Programming Language :: Python :: 3.7"
    ],
    include_package_data=True,
    zip_safe=False,
)
