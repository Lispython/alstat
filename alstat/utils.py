#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
loganalyzer.utils
~~~~~~~~~~~~~~~~~

Utils to analyze logfiles

:copyright: (c) 2012 by David M. Beazley, Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""

import fnmatch
import gzip, bz2
import os
import re


def open_files(filenames):
    """Open given filenames

    Attributes:
    - `filenames` - list of filenames with full path

    """
    for name in filenames:
        if name.endswith(".gz"):
            yield gzip.open(name)
        elif name.endswith(".bz2"):
            yield bz2.BZ2File(name)
        else:
            yield open(name)


def find_files(file_pattern, top):
    """Find logfiles by pattern
    Attributes:
    - `file_pattern` - filename pattern
    - `top` - parent directory to search files
    Usage:
        files = find_files("access-log*", '/var/log/nginx/')
    """
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, file_pattern):
            yield os.path.join(path, name)


def grep(pattern, lines):
    """Grep a sequence of lines that match a re pattern

    Attributes:
    - `pattern` - pattern to match
    - `lines` - iterable seq with lines

    Usage:
        matched_lines = grep(r'ply-.*\.gz', lines)


    """
    compiled_pattern = re.compile(pattern)
    for line in lines:
        if compiled_pattern.search(line):
            yield line


def parse_line(func, lines):
    """Parse lines by given function

    Attributes:
    - `lines` - iterable seq with lines
    - `func` - function to parse line
    """
    for line in lines:
        yield func(line)


def field_map(dictseq, name, func):
    """Take a sequence of dictionaries and remap one of the fields

    Attributes:
    - `dictseq` - sequence of parsed lines
    - `name` - field to apply ``func``
    - `func` - map function
    """
    for d in dictseq:
        d[name] = func(d[name])
        yield d


def build_log_re(patterns_dict, log_format):
    """Build re by given patterns_dict with format

    Attributes:
    - `patterns_dict` - dict of names and re patterns
    - `format` - string format to replace

    """
    for name, pattern in patterns_dict.iteritems():
        log_format = log_format.replace(name, r"(?P<%s>%s)" % (name, pattern))

    return re.compile(log_format)
