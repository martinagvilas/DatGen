from ftplib import FTP
import os
from PIL import Image
import numpy as np


def get_ftp_client(address, port, username, passwd):
    ftp = FTP()
    ftp.set_pasv(False)
    ftp.connect(address, port)
    ftp.login(username, passwd)
    return ftp


def save_temp_img(img_bin, temp_directory):
    with open(temp_directory, 'ab') as f:
        f.write(img_bin)


def retrieve_image(ftp_client, image_path):
    temp_directory = 'datgen/dataset_assembly/img_temp'
    if os.path.exists(temp_directory):
        os.remove(temp_directory)
    resp = ftp_client.retrbinary(f'RETR {image_path}', lambda x : save_temp_img(x, temp_directory))
    img = np.asarray(Image.open(temp_directory)) if 'complete' in resp else None
    if os.path.exists(temp_directory):
        os.remove(temp_directory)
    return img


if __name__ == '__main__':
    ftp_client = get_ftp_client('128.0.145.146', 60666, 'xiaxu', '12345')
    img = retrieve_image(ftp_client, 'conceptual_captions/my_cat.png')
