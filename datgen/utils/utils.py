import io
import socket
from PIL import Image

def read_img_from_socket(s):
    file_size = int(s.recv(2048).decode())
    img = b''
    while len(img) < file_size:
        img += s.recv(2048)
    pil_img = Image.open(io.BytesIO(img))
    return pil_img


def create_server_socket(port=60666):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    return s

def get_client_socket():
    server_socket = create_server_socket()
    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f'{addr} connected!')
            break
        except:
            pass
    return client_socket