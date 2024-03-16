#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Sun Mar 03 2024
#
# Copyright (c) 2024 Abolfazl Danayi
# adanayidet@gmail.com
#

import http.server
import socketserver

class StaticServer:
    def __init__(self, directory, port=8000):
        self.directory = directory
        self.__port = port
        self.httpd = None

    @property
    def port(self) -> int:
        if self.httpd is None:
            return None
        return self.httpd.server_address[1]

    def serve_forever(self):
        handler = self._get_handler()
        with socketserver.TCPServer(("", self.__port), handler) as httpd:
            self.httpd = httpd
            print(f"Serving the development server at port {self.port}")
            httpd.serve_forever()

    def _get_handler(self):
        dir = self.directory
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                nonlocal dir
                super().__init__(*args, directory=dir, **kwargs)

        return CustomHandler
