#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
alstats
~~~~~~~

Collection of tools to analyze logs

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""


import sys
import os
try:
    import subprocess
    has_subprocess = True
except:
    has_subprocess = False

from setuptools import Command, setup

__version__ = (0, 0, 6)


try:
    readme_content = open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "README.rst")).read()
except Exception, e:
    print(e)
    readme_content = __doc__


class DebugManage(Command):
    description = "Interface to django manage command from setup.py"
    user_options = []

    def initialize_options(self):
        all = None

    def finalize_options(self):
        pass

    def run(self):
        from django.core.management import execute_manager
        from tests.manage import settings as manage_settings

        execute_manager(manage_settings, argv=sys.argv)


class run_audit(Command):
    """Audits source code using PyFlakes for following issues:
        - Names which are used but not defined or used before they are defined.
        - Names which are redefined without having been used.
    """
    description = "Audit source code with PyFlakes"
    user_options = []

    def initialize_options(self):
        all = None

    def finalize_options(self):
        pass

    def run(self):
        try:
            import pyflakes.scripts.pyflakes as flakes
        except ImportError:
            print "Audit requires PyFlakes installed in your system."""
            sys.exit(-1)

        dirs = ['alstat']
        # Add example directories
        for dir in []:
            dirs.append(os.path.join('examples', dir))
        # TODO: Add test subdirectories
        warns = 0
        for dir in dirs:
            for filename in os.listdir(dir):
                if filename.endswith('.py') and filename != '__init__.py':
                    warns += flakes.checkPath(os.path.join(dir, filename))
        if warns > 0:
            print ("Audit finished with total %d warnings." % warns)
        else:
            print ("No problems found in sourcecode.")


setup(
    name="alstat",
    version=".".join(map(str, __version__)),
    description="Collection of advanced utils to parse logfiles in different formats and build statistic reports",
    long_description=readme_content,
    author="Alex Lispython",
    author_email="alex@obout.ru",
    maintainer = "Alexandr Lispython",
    maintainer_email = "alex@obout.ru",
    url="https://github.com/lispython/alstat",
    install_requires=[
#        'tornadoweb',
        ],
    license="BSD",
#    test_suite="nose.collector",
    platforms = ['Linux', 'Mac'],
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries"
        ],
    cmdclass={'audit': run_audit},
    entry_points=dict(
        console_scripts=['alstat=alstat.console:main']
        ),
    test_suite = 'tests.suite'
    )
