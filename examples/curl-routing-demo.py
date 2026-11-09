#!/usr/bin/env python3
"""Show curl proxy selection using two loopback-only HTTP fixtures."""
import os
import shutil
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def fixture(label):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = (label + '\n').encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    assert server.server_address[0] == '127.0.0.1'
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def main():
    curl = shutil.which('curl')
    if not curl:
        raise SystemExit('curl is required')
    direct, direct_thread = fixture('direct-handler')
    proxy, proxy_thread = fixture('proxy-handler')
    try:
        target = f'http://127.0.0.1:{direct.server_port}/status'
        proxy_url = f'http://127.0.0.1:{proxy.server_port}'
        # Remove only proxy-selection variables from the child process environment.
        env = {k: v for k, v in os.environ.items() if not k.lower().endswith('_proxy')}
        env['NO_PROXY'] = '*'
        command = [curl, '-q', '--silent', '--show-error', '--fail', '--max-time', '3', '--proxy', proxy_url]
        cases = [('NO_PROXY=*', [], 'direct-handler'),
                 ('NO_PROXY=* with --noproxy ""', ['--noproxy', ''], 'proxy-handler')]
        for label, options, expected in cases:
            result = subprocess.run(command + options + [target], env=env,
                                    capture_output=True, text=True, timeout=5, check=True)
            actual = result.stdout.strip()
            if actual != expected:
                raise AssertionError(f'{label}: expected {expected}, received {actual}')
            print(f'{label}: {actual}')
        print('PASS: both routing decisions matched the expected handler.')
        print('This HTTP fixture does not forward traffic or test real proxy authentication.')
    finally:
        for server, thread in [(direct, direct_thread), (proxy, proxy_thread)]:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == '__main__':
    main()
