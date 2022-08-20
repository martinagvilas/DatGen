from image_generation.generate_image import generate_image
import socket
import os


def send_file_trough_socket(file_path, s):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            file_size = os.path.getsize(file_path)
            s.send(str(file_size).encode())
            bytes_sent = s.sendfile(f)
        print(f'Sent: {file_path}, {bytes_sent} bytes')
    else:
        raise FileNotFoundError('File NOT found!')


def connect_to_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def handle_request(request, s):
    if request.startswith('Retrieve:'):
        send_file_trough_socket(request[9:], s)
    elif request.startswith('Generate:'):
        img = generate_image(request[9])
        if os.path.exists('temp_image.png'):
            os.remove('temp_image.png')
        img.save('temp_image.png')
        send_file_trough_socket('temp_image.png', s)
    else:
        raise NotImplementedError('Bad luck.')


if __name__ == '__main__':
    while True:
        try:
            s = connect_to_socket('108.61.211.18', 60666)
            break
        except:
            pass
    while True:
        request = s.recv(1024).decode()
        print('handling request: ' + request)
        handle_request(request, s)
