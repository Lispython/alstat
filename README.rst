Welcome to alstat's documentation!
==================================================

alstat is advances logs statistics.
It's collection of utils to analyze logs.

Features
--------

- Unpack gzipped logfiles
- Fast


Usage
-----

This commant print all lines from all log files in directory /var/log/nginx
if format `http_method status http_referer`::

    alstat -d /var/log/nginx/ -p "*access*" -f "base" http_method status http_referer

    GET 200 http://google.com
    .... to many lines
    GET 404 http://ya.ru/
    PUT 200 http://yandex.com/


You can view fields list that you can use to display::

    alstat -d /var/log/nginx/ -p "*access*" -l

    Alstat v0.0.1 start at Tue May  8 23:25:24 2012
    You can use fieldnames: status, http_protocol, http_method, http_referer, remote_addr, url, time_local, http_user_agent, remote_user, size



INSTALLATION
------------

To use alstat use pip or easy_install:

`pip install alstat`

or

`easy_install alstat`


TODO
----
- Add group by fields and count
- Web interface with reports


CONTRIBUTE
----------

Fork https://github.com/Lispython/alstat/ , create commit and pull request.

THANKS
------

To David M. Beazley for `generators`_ examples.


SEE ALSO
--------

-  `python pypi`_.

.. _`python pypi`: http://pypi.python.org

.. _`generators`: http://www.dabeaz.com/generators/
