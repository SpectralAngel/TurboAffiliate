#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Start script for the TurboAffiliate TurboGears project.

This script is only needed during development for running from the project
directory. When the project is installed, easy_install will create a
proper start script.
"""

import os
import locale

locale_name = None
if os.name == 'nt':
    locale_name = 'Spanish_Honduras.1252'
else:
    locale_name = "es_HN.utf8"

locale.setlocale(locale.LC_ALL, locale_name)

import sys
from turboaffiliate.command import start, ConfigurationError

if __name__ == "__main__":
    try:
        start()
    except ConfigurationError, exc:
        sys.stderr.write(str(exc))
        sys.exit(1)
