import os
import sys
from setuptools import find_packages, setup

VERSION = "3.0.2"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-ratings.svg
    :target: https://pypi.python.org/pypi/pinax-ratings/

=============
Pinax Ratings
=============

.. image:: https://img.shields.io/pypi/v/pinax-ratings.svg
    :target: https://pypi.python.org/pypi/pinax-ratings/

\ 

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-ratings.svg
    :target: https://circleci.com/gh/pinax/pinax-ratings
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-ratings.svg
    :target: https://codecov.io/gh/pinax/pinax-ratings
.. image:: https://img.shields.io/github/contributors/pinax/pinax-ratings.svg
    :target: https://github.com/pinax/pinax-ratings/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-ratings.svg
    :target: https://github.com/pinax/pinax-ratings/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-ratings.svg
    :target: https://github.com/pinax/pinax-ratings/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/

\ 

``pinax-ratings`` is a ratings app for Django.

Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+-----+
| Django / Python | 2.7 | 3.4 | 3.5 | 3.6 |
+=================+=====+=====+=====+=====+
|  1.11           |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
|  2.0            |     |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
"""


# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()


setup(
    author="Pinax Team",
    author_email="team@pinaxprojects.com",
    description="a ratings app for Django",
    name="pinax-ratings",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-ratings/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "pinax.ratings": [
            "static/pinax/ratings/img/*",
            "static/pinax/ratings/js/*",
            "templates/pinax/ratings/*"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
        "django-user-accounts>=2.0.3",
    ],
    tests_require=[
        "django-test-plus>=1.0.22"
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
