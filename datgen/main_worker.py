import argparse
from http.server import HTTPServer
from io import BytesIO
from sauth import SimpleHTTPAuthHandler
import pickle
from pathlib import Path

from datgen.image_match.match import match
from datgen.image_generation.generate_image import generate_image


class Handler(SimpleHTTPAuthHandler):
    def do_POST(self):
        """
            Overrides the handling of POST HTTP request
        """
        auth_header = self.headers.get('Authorization', '').encode('ascii')
        # authentication
        if auth_header is None:
            self.do_authhead()
            self.wfile.write(b'no auth header received')
        elif auth_header == self.valid_header:
            file_content = self.rfile.read(int(self.headers['Content-Length']))
            data = pickle.loads(file_content)

            if data['action'] == 'generate':
                # handles the generation
                self.send_response(200)
                self.end_headers()
                prompt = data['content']
                print('Generating: ' + prompt)
                bytes_img = BytesIO()
                pil_img = generate_image(prompt)
                pil_img.save(bytes_img, 'PNG')
                self.wfile.write(bytes_img.getvalue())
            elif data['action'] == 'match':
                # handles the match
                self.send_response(200)
                self.end_headers()
                print('Matching...')
                print(data['content'])
                match_results = match(data['content'])
                self.wfile.write(pickle.dumps(match_results))
            else:
                # handles the retrieval
                path = Path('../data/datgen_data/') / data['content']
                print('Retrieving :' + str(path))
                if path.is_file():
                    self.send_response(200)
                    self.end_headers()
                    with open(path, 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    self.send_response(404)
                    self.end_headers()

        else:
            # authentication failed
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
