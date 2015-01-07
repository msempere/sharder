'''
Copyright (c) 2014, Young King
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

"""Internal module for Python 2 backwards compatibility."""
import sys


if sys.version_info[0] < 3:
    from urlparse import urlparse
    from itertools import imap, izip
    from string import letters as ascii_letters
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

    iteritems = lambda x: x.iteritems()
    dictkeys = lambda x: x.keys()
    dictvalues = lambda x: x.values()
    nativestr = lambda x: \
        x if isinstance(x, str) else x.encode('utf-8', 'replace')
    u = lambda x: x.decode()
    b = lambda x: x
    next = lambda x: x.next()
    byte_to_chr = lambda x: x
    unichr = unichr
    xrange = xrange
    basestring = basestring
    unicode = unicode
    bytes = str
    long = long
else:
    from urllib.parse import urlparse
    from io import BytesIO
    from string import ascii_letters

    iteritems = lambda x: x.items()
    dictkeys = lambda x: list(x.keys())
    dictvalues = lambda x: list(x.values())
    byte_to_chr = lambda x: chr(x)
    nativestr = lambda x: \
        x if isinstance(x, str) else x.decode('utf-8', 'replace')
    u = lambda x: x
    b = lambda x: x.encode('iso-8859-1') if not isinstance(x, bytes) else x
    next = next
    unichr = chr
    imap = map
    izip = zip
    xrange = range
    basestring = str
    unicode = str
    bytes = bytes
    long = int

try: # Python 3
    from queue import LifoQueue, Empty, Full
except ImportError:
    from Queue import Empty, Full
    try: # Python 2.6 - 2.7
        from Queue import LifoQueue
    except ImportError: # Python 2.5
        from Queue import Queue
        # From the Python 2.7 lib. Python 2.5 already extracted the core
        # methods to aid implementating different queue organisations.
        class LifoQueue(Queue):
            """Override queue methods to implement a last-in first-out queue."""

            def _init(self, maxsize):
                self.maxsize = maxsize
                self.queue = []

            def _qsize(self, len=len):
                return len(self.queue)

            def _put(self, item):
                self.queue.append(item)

            def _get(self):
                return self.queue.pop()

