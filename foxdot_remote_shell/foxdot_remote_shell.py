#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO, StringIO
from contextlib import redirect_stdout

class FoxDotRemoteConsole(BaseHTTPRequestHandler):
    verbose = False

    def log_message(self, format, *args):
        if self.verbose: super().log_message(format, *args)

    def log_request(self, code='-', size='-'):
        self.log_message('"%s" %s %s', self.requestline, str(code), str(size))

    def do_GET(self):
        self.send_error(501)
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()

        output = StringIO()
        with redirect_stdout(output):
            if not hasattr(self, 'execute'):
                from FoxDot import execute
                self.execute = execute

            self.execute(body, verbose=self.verbose, verbose_error=self.verbose)

        output = output.getvalue()

        if self.verbose: print(output);

        response = BytesIO()
        response.write(bytes(output + '\n', encoding='UTF-8'))
        self.wfile.write(response.getvalue())

def get_args():
    parser = ArgumentParser(description='FoxDot remote shell')
    parser.add_argument('--host', type=str, default='', help='sets server host')
    parser.add_argument('--port', type=int, default=8000, help='sets server port')
    parser.add_argument('--verbose', action='store_true', help='displays incoming data')
    return parser.parse_args()

def main():
    args = get_args()

    if (args.verbose):
        FoxDotRemoteConsole.verbose = True

    server = HTTPServer((args.host, args.port), FoxDotRemoteConsole)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
