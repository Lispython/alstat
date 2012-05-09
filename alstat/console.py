#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
alstat.console
~~~~~~~~~~~~~~

Console interface for alstat

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""

import time
import logging
import sys

logger = logging.getLogger('alstat')

def main():
    from alstat import get_version
    from alstat.parsers import NginxParser
    t = time.time()

    from optparse import OptionParser
    usage = "%prog [options] field1, field2, field3 ...  "
    parser = OptionParser(usage)

    parser.add_option("-d", "--logs-dir", dest="dirname",
                      help="Logs dir", metavar="DIR")
    parser.add_option("-p", "--names-pattern", help="Log files name pattern",
                      action="store", type="string", dest="pattern", metavar="PATTERN", default="*")

    parser.add_option("-f", "--log_format",
                      action="store", type="string", dest="log_format", metavar="LOG FORMAT",
                      help="Can be nginx|base", default="nginx")
    parser.add_option("-l", action="store_true", dest="fields_list", help="Show list of available fields")
    parser.add_option("-v", action="store_true", dest="verbose", help="Verbose mode")
    parser.add_option("-V", "--version", action="store_true", dest="version", help="Print version")

    (options, args) = parser.parse_args()

    if options.version:
        print("Alstat version {version}".format(version=get_version()))
        sys.exit(1)

    if options.verbose:
        print("Alstat v{version} start at {time}".format(version=get_version(), time=time.ctime(t)))

    if options.fields_list:
        print("You can use fieldnames: " + ", ".join(NginxParser.PATTERNS_MAP.keys()))
        sys.exit(1)

    if not args:
        parser.error("You need specify field name")

    if options.log_format not in ('nginx', 'base'):
        parser.error("Log format can be nginx | base")

    if not options.dirname:
        parser.error("You need to specify logs dir")

    log_parser = NginxParser(options.dirname, options.pattern)
    for x in log_parser.get_fields():
        print(" ".join([v for k, v in x.iteritems() if k in args]))

    if options.verbose:
        print("Analyze completed {time_duration} sec at {time} ".fortam(time_duration=(time.time()-t) * 10, time=time.ctime()))
    sys.exit(1)

