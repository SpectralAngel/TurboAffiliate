# -*- coding: utf-8 -*-
"""This module contains functions called from console script entry points."""

import sys
from os import getcwd
from os.path import dirname, exists, join

import pkg_resources
try:
    pkg_resources.require("TurboGears>=1.1rc1")
except pkg_resources.DistributionNotFound:
    print """\
This is a TurboGears (http://www.turbogears.org) application. It seems that
you either don't have TurboGears installed or it can not be found.

Please check if your PYTHONPATH is set correctly. To install TurboGears, go to
http://docs.turbogears.org/Install and follow the instructions there. If you
are stuck, visit http://docs.turbogears.org/GettingHelp for support options."""
    sys.exit(1)
try:
    pkg_resources.require("SQLObject>=0.10.1")
except pkg_resources.DistributionNotFound:
    from turbogears.util import missing_dependency_error
    print missing_dependency_error('SQLObject')
    sys.exit(1)

import cherrypy
import turbogears

cherrypy.lowercase_api = True


class ConfigurationError(Exception):
    pass


def start():
    """Start the CherryPy application server."""

    setupdir = dirname(dirname(__file__))
    curdir = getcwd()

    # First look on the command line for a desired config file,
    # if it's not on the command line, then look for 'setup.py'
    # in the current directory. If there, load configuration
    # from a file called 'dev.cfg'. If it's not there, the project
    # is probably installed and we'll look first for a file called
    # 'prod.cfg' in the current directory and then for a default
    # config file called 'default.cfg' packaged in the egg.
    if len(sys.argv) > 1:
        configfile = sys.argv[1]
    elif exists(join(setupdir, "setup.py")):
        configfile = join(setupdir, "dev.cfg")
    elif exists(join(curdir, "prod.cfg")):
        configfile = join(curdir, "prod.cfg")
    else:
        try:
            configfile = pkg_resources.resource_filename(
              pkg_resources.Requirement.parse("TurboAffiliate"),
                "config/default.cfg")
        except pkg_resources.DistributionNotFound:
            raise ConfigurationError("Could not find a configuration file.")

    turbogears.update_config(configfile=configfile,
        modulename="turboaffiliate.config")

    from turboaffiliate.controllers import root

    turbogears.start_server(root.Root())
