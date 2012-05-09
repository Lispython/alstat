#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tests
~~~~~

alstat unittests module

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""

import unittest
import os
import re
from collections import defaultdict
from itertools import chain

from alstat.utils import find_files, open_files, parse_line
from alstat.parsers import BaseParser, NginxParser


PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))


def rel(*parts):
    return os.path.join(PROJECT_ROOT, *parts)


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.log_dir = rel('logs')
        self.nginx_default_log_format = r'remote_addr - remote_user [time_local] "request" status bytes_sent "http_referer" "http_user_agent" "gzip_ratio"'

    def test_utils(self):
        print("test utils")

    def test_find_files(self):
        self.assertEquals(len([x for x in find_files("access.nginx.*", self.log_dir)]), 1)

    def test_parser(self):
        files = open_files(find_files("access.nginx.*", self.log_dir))
        lines = chain(*files)

        for x in parse_line(lambda x: x[:20], lines):
            self.assertEquals(len(x), 20)

    def test_base_parser(self):
        base_parser = BaseParser(self.log_dir, "access.nginx.*")

        self.assertEquals(base_parser.root_path, self.log_dir)
        self.assertEquals(base_parser.file_name_pattern, "access.nginx.*")
        self.assertEquals(len([x for x in base_parser.get_files()]), 1)

        self.assertEquals(len([x for x in base_parser.get_lines()]), 13)
        self.assertEquals(len([x for x in base_parser.grep(r'\[.*\]')]), 13)

        for x in base_parser.apply_func(lambda x: x[:20]):
            self.assertEquals(len(x), 20)

    def test_nginx_parser(self):
        nginx_parser = NginxParser(self.log_dir, "access.nginx.*")
        control_re_pattern = r'^(?P<remote_addr>(?:\d{1,3}\.){3}\d{1,3}).*'\
                             r'\[(?P<time_local>.+)\].*'\
                             r'"(?P<http_method>POST|GET)\s'\
                             r'(?P<url>.*)\s'\
                             r'(?P<http_protocol>.*)"\s'\
                             r'(?P<status>\d{3})\s(?P<size>[0-9]*)\s'\
                             r'"(?P<http_referer>.*)"\s'\
                             r'"(?P<http_user_agent>.*)".*$'

        self.assertEquals(nginx_parser.compiled_log_format, control_re_pattern)
        for x in nginx_parser.apply_func(nginx_parser.parse_re.match):
            self.assertEquals(len(x.groupdict()), 9)

        for x in nginx_parser.get_fields():
            self.assertEquals(len(x), 9)
        ## with self.assertRaises(RuntimeError):
        ##     for x in nginx_parser.field_map('not_valid_field', str):
        ##         print x

        log = nginx_parser.field_map('status', lambda x: "bbb")
        for x in log:
            self.assertEquals(x['status'], "bbb")

        for x in nginx_parser.map_fn('status', lambda x: (x, 1)):
            self.assertEquals(x[1], 1)

        def sort_fn(i_list):
            new = defaultdict(list)
            map(lambda x: new[x[0]].append(x[1]), i_list)
            return new.items()

        for x in sort_fn(nginx_parser.map_fn('status', lambda x: (x, 1))):
            pass

        ## for x in nginx_parser.reduce_fn('status', lambda x: (x, 1), lambda x: [x[0], sum([x[1]])]):
        ##     print x

        ## for x in nginx_parser.reduce_fn('status', lambda x: (x, 1), lambda i: [i[0], sum(i[1])]):
        ##     print(x)

    def test_re(self):
        log_line = '66.249.73.219 - - [07/May/2012:16:50:48 -0400] "GET /users/791/ HTTP/1.1" 200 3318 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
        pattern = r'^(?P<remote_addr>(?:\d{1,3}\.){3}\d{1,3}).*'\
                  r'\[(?P<time_local>.+)\].*'\
                  r'"(?P<http_method>POST|GET)\s'\
                  r'(?P<url>.*)\s'\
                  r'(?P<http_protocol>.*)"\s'\
                  r'(?P<status>\d{3})\s(?P<size>[0-9]*)\s'\
                  r'"(?P<http_referer>.*)"\s'\
                  r'"(?P<http_user_agent>.*)".*$'
        pattern_re = re.compile(pattern, re.U)
        matched = pattern_re.match(log_line)
        self.assertTrue(matched)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilsTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultT='suite')
