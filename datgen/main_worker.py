from image_generation.generate_image import generate_image
from http.server import HTTPServer
from io import BytesIO
from sauth import SimpleHTTPAuthHandler
import argparse


class Handler(SimpleHTTPAuthHandler):
    def do_POST(self):
        auth_header = self.headers.get('Authorization', '').encode('ascii')
        if auth_header is None:
            self.do_authhead()
            self.wfile.write(b'no auth header received')
        elif auth_header == self.valid_header:
            self.send_response(200)
            self.end_headers()

            prompt = self.rfile.read(int(self.headers['Content-Length'])).decode()
            print('Generating: ' + prompt)
            bytes_img = BytesIO()
            pil_img = generate_image(prompt)
            pil_img.save(bytes_img, 'PNG')
            self.wfile.write(bytes_img.getvalue())
        else:
            self.do_authhead()
            self.wfile.write(auth_header)
            self.wfile.write(b'not authenticated')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    args = parser.parse_args()

    Handler.username = args.username
    Handler.password = args.password
    server = HTTPServer(('', 60666), Handler)
    server.serve_forever()
