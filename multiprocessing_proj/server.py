from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import time

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(10)
        self.send_response(200)
        self.end_headers()

def run(server_class=ThreadingHTTPServer, handler_class=MyHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
