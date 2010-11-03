# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from turbogears.finddata import find_package_data
from turboaffiliate import release

import os
execfile(os.path.join("turboaffiliate", "release.py"))

packages=find_packages()
package_data = find_package_data(where='turboaffiliate',
    package='turboaffiliate')
if os.path.isdir('locales'):
    packages.append('locales')
    package_data.update(find_package_data(where='locales',
        exclude=('*.po',), only_in_packages=False))

setup(
    name="TurboAffiliate",
    version=release.version,
    # uncomment the following lines if you fill them out in release.py
    #description=description,
    #long_descriptopn=long_description,
    author=release.author,
    author_email=release.email,
    #url=url,
    download_url=release.download_url,
    license=license,

    install_requires=[
        "TurboGears >= 1.1",
        "WebTest",
        "SQLObject>=0.12.5"
    ],
    zip_safe=False,
    packages=packages,
    package_data=package_data,
    keywords=[
        # Use keywords if you'll be adding your package to the
        # Python Cheeseshop

        # if this has widgets, uncomment the next line
        # 'turbogears.widgets',

        # if this has a tg-admin command, uncomment the next line
        # 'turbogears.command',

        # if this has identity providers, uncomment the next line
        # 'turbogears.identity.provider',

        # If this is a template plugin, uncomment the next line
        # 'python.templating.engines',

        # If this is a full application, uncomment the next line
        'turbogears.app',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # if this is an application that you'll distribute through
        # the Cheeseshop, uncomment the next line
        'Framework :: TurboGears :: Applications',

        # if this is a package that includes widgets that you'll distribute
        # through the Cheeseshop, uncomment the next line
        # 'Framework :: TurboGears :: Widgets',
    ],
    test_suite='nose.collector',
    entry_points = {
        'console_scripts': [
            'start-turboaffiliate = turboaffiliate.command:start',
            # See the turboaffiliate.command.bootstrap function for details
            #'bootstrap-turboaffiliate = turboaffiliate.command:bootstrap',
        ],
    },
    # Uncomment next line and create a default.cfg file in your project dir
    # if you want to package a default configuration in your egg.
    #data_files = [('config', ['default.cfg'])],
    )
