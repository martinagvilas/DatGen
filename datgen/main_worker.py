from image_generation.generate_image import generate_image
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        prompt = self.rfile.read(int(self.headers['Content-Length'])).decode()
        print('Generating: ' + prompt)
        bytes_img = BytesIO()
        pil_img = generate_image(prompt)
        pil_img.save(bytes_img, 'PNG')
        self.wfile.write(bytes_img.getvalue())


server = HTTPServer(('', 60666), Handler)
server.serve_forever()
