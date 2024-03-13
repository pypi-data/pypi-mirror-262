#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from future import standard_library

standard_library.install_aliases()
import gzip
import http.server
import os
import shutil
from subprocess import call


class ForwardHTTPHandler(http.server.SimpleHTTPRequestHandler):
    forward_url = None

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith("/"):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)

        ctype = self.guess_type(path)

        if not os.path.exists(path):
            path = ".cache" + self.path
            if not os.path.exists(path):
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                cmd = ["curl", "-k", self.forward_url + self.path, "-o", path]
                self.log_message("forward request: %s", cmd)
                call(cmd)
                try:
                    with gzip.open(path) as f:
                        data = f.read()
                    with open(path, "wb") as f:
                        f.write(data)
                except IOError:
                    pass

        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, "rb")
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f


if __name__ == "__main__":
    webapp = os.path.join(os.path.dirname(__file__), "dashboard")
    baseurl = "https://lhcb-nightlies.web.cern.ch"
    import sys

    if "-h" in sys.argv or "--help" in sys.argv:
        print("Usage: %s [WebApp-dir [forward-url [port]]" % sys.argv[0])
        print("\nCalled without arguments is equivalent to")
        print("\t%s %s %s 8000" % (sys.argv[0], webapp, baseurl))
        sys.exit(0)

    if sys.argv[1:]:
        webapp = sys.argv.pop(1)

    print("Entering", webapp)
    os.chdir(webapp)

    if os.path.isdir(".cache"):
        print("Cleaning cache...")
        shutil.rmtree(".cache")

    if sys.argv[1:]:
        baseurl = sys.argv.pop(1)
    ForwardHTTPHandler.forward_url = baseurl
    print("Set up to forward calls to", ForwardHTTPHandler.forward_url)

    http.server.test(HandlerClass=ForwardHTTPHandler)
