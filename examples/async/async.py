#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Appier Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import time
import mimetypes
import threading

import appier

class AsyncApp(appier.App):

    def __init__(self, *args, **kwargs):
        appier.App.__init__(
            self,
            name = "async",
            *args, **kwargs
        )

    @appier.route("/async", "GET")
    @appier.route("/async/hello", "GET")
    def hello(self):
        partial = self.field("partial", True, cast = bool)
        handler = self.handler_partial if partial else self.handler
        yield from appier.header_a()
        yield "before\n"
        yield from appier.ensure_a(handler)
        yield "after\n"

    @appier.route("/async/callable", "GET")
    def callable(self):
        yield from appier.header_a()
        yield "before\n"
        yield from appier.ensure_a(lambda: time.sleep(30.0))
        yield "after\n"

    @appier.route("/async/file", "GET")
    def file(self):
        file_path = self.field("path", None)
        delay = self.field("delay", 0.0, cast = float)
        thread = self.field("thread", False, cast = bool)
        type, _encoding = mimetypes.guess_type(file_path, strict = True)
        type = type or "application/octet-stream"
        self.request.content_type = type
        yield from appier.header_a()
        yield from appier.ensure_a(
            self.read_file,
            args = [file_path],
            kwargs = dict(delay = delay),
            thread = thread
        )

    @appier.route("/async/http", "GET")
    def http(self):
        url = self.field("url", "https://www.flickr.com/")
        delay = self.field("delay", 0.0, cast = float)
        self.request.content_type = "text/html"
        yield from appier.header_a()
        yield from appier.sleep(delay)
        yield from appier.get_a(url)

    @appier.coroutine
    def handler(self, future):
        thread = threading.current_thread()
        print("executing in %s" % thread)
        message = "hello world\n"
        timeout = yield from appier.sleep(3.0)
        message += "timeout: %.2f\n" % timeout
        result = yield from self.calculator(2, 2)
        message += "result: %d\n" % result
        future.set_result(message)

    @appier.coroutine
    def handler_partial(self, future):
        yield "hello world\n"
        timeout = yield from appier.sleep(3.0)
        yield "timeout: %.2f\n" % timeout
        result = yield from self.calculator(2, 2)
        yield "result: %d\n" % result

    @appier.coroutine
    def calculator(self, *args, **kwargs):
        thread = threading.current_thread()
        print("executing in %s" % thread)
        print("computing...")
        yield from appier.sleep(3.0)
        print("finished computing...")
        return sum(args)

    @appier.coroutine
    def read_file(self, future, file_path, chunk = 65536, delay = 0.0):
        count = 0
        file = open(file_path, "rb")
        try:
            while True:
                data = file.read(chunk)
                if not data: break
                count += len(data)
                if delay: yield from appier.sleep(delay)
                yield data
        finally:
            file.close()
        return count

app = AsyncApp()
app.serve()
