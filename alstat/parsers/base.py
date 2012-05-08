#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
loganalyzer.base
~~~~~~~~~~~~~~~~~

Base logs parser

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""
import bz2
import fnmatch
import gzip
import os
import re


class BaseParser(object):
    """
    Base log parser
    """

    LOG_FORMAT = r'^{remote_addr}.*'\
                 r'\[{time_local}\].*'\
                 r'"{http_method}\s'\
                 r'{url}\s'\
                 r'{http_protocol}"\s'\
                 r'{status}\s{size}\s'\
                 r'"{http_referer}"\s'\
                 r'"{http_user_agent}".*$'

    PATTERNS_MAP = {
        "url": r".*",
        "http_protocol": r".*",
        "http_method": r"POST|GET",
        "remote_addr": r"(?:\d{1,3}\.){3}\d{1,3}",
        "remote_user": r"\S+",
        "time_local": r".+",
        "size": r'[0-9]*',
        "status": r'\d{3}',
        "http_referer": r".*",
        "http_user_agent": r".*",
        }

    def __init__(self, root_path, file_name_pattern):
        self.root_path = root_path
        self.file_name_pattern = file_name_pattern
        self._compiled_log_format = None
        self._compiled_log_format_re = None

    @property
    def compiled_log_format(self):
        if self._compiled_log_format:
            return self._compiled_log_format
        else:
            log_format = self.LOG_FORMAT.format(**dict([(k, r"(?P<{0}>{1})".format(k, v)) for k, v in self.PATTERNS_MAP.iteritems()]))
            self._compiled_log_format = log_format
        return self._compiled_log_format

    def setup_log_format(self, log_format):
        self.LOG_FORMAT = log_format

    def open_file(self, filename):
        """Analyze filename and open it if it's have gzip format
        """
        if filename.endswith(".gz"):
            return gzip.open(filename)
        elif filename.endswith(".bz2"):
            return bz2.BZ2File(filename)
        else:
            return open(filename)

    def get_files(self):
        """Open all files in ``root_path`` matche by ``file_name_pattern``
        and return generator
        """
        for path, dirlist, filelist in os.walk(self.root_path):
            for name in fnmatch.filter(filelist, self.file_name_pattern):
                yield self.open_file(os.path.join(path, name))

    def get_lines(self):
        """Read file lines in generator with files concatenation
        """
        for source in self.get_files():
            for item in source:
                yield item

    def grep(self, pattern):
        """
        Find all lines matched by ``pattern``
        """
        compiled_pattern = re.compile(pattern)
        for line in self.get_lines():
            if compiled_pattern.search(line):
                yield line

    def apply_func(self, func):
        """Read lines and apply ``func``
        """
        for line in self.get_lines():
            yield func(line)

    @property
    def parse_re(self):
        """Parse lines and return generator of dicts
        """
        if self._compiled_log_format_re:
            return self._compiled_log_format_re

        self._compiled_log_format_re = re.compile(self.compiled_log_format)

        return self._compiled_log_format_re

    def get_fields(self):
        """Get generator of fields
        """
        for item in self.apply_func(self.parse_re.match):
            if not item:
                continue
            yield item.groupdict()


    def field_map(self, field_name, func):
        """Apply func to ``name`` field

        Arguments:
        - `name` - field name
        - `func` - function applyed to item field value
        """
        if field_name not in self.PATTERNS_MAP.keys():
            raise RuntimeError("Not a valid field name")

        for d in self.get_fields():
            d[field_name] = func(d[field_name])
            yield d

    def map_fn(self, field_name, map_func):
        if field_name not in self.PATTERNS_MAP.keys():
            raise RuntimeError("Not a valid field name")

        for item in self.get_fields():
            yield map_func(item[field_name])

    def reduce_fn(self, field_name, map_func, reduce_func):
        if field_name not in self.PATTERNS_MAP.keys():
            raise RuntimeError("Not a valid field name")

        result = {}
        for x in self.map_fn(field_name, map_func):
            #result[field_name] = reduce_func(x[field_name])
            yield reduce_func(x)
