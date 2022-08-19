from paramiko.client import SSHClient
import os
from PIL import Image
import numpy as np


def get_sftp_client(address, port, username, passwd):
    ssh_client = SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(address, port=port, username=username, password=passwd)
    sftp_client = ssh_client.open_sftp()
    sftp_client.chdir('/Users/xuxia/projects/data/')
    return sftp_client


def retrieve_image(sftp_client, image_path):
    temp_directory = 'datgen/dataset_assembly/img_temp'
    if os.path.exists(temp_directory):
        os.remove(temp_directory)
    sftp_client.get(image_path, temp_directory)
    if os.path.exists(temp_directory):
        try:
            pil_img = Image.open(temp_directory)
            img = np.asarray(pil_img)
            pil_img.close()
        except:
            img = None
        os.remove(temp_directory)
    else:
        img = None
    return img


if __name__ == '__main__':
    sftp_client = get_sftp_client('128.0.145.146', 60666, input('Username:'), input('Password:'))
    img = retrieve_image(sftp_client, 'conceptual_captions/my_cat.png')
