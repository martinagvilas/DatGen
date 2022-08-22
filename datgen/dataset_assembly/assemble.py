import streamlit as st
from zipfile import ZipFile
import os
from os.path import basename, exists





def create_download_button():
    if exists('dataset.zip'):
        os.remove('dataset.zip')
    with ZipFile('dataset.zip', 'w') as zipped_data:
        for folderName, subfolders, filenames in os.walk('datgen/temp'):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipped_data.write(filePath, basename(filePath))
    zipped_data.close()
    file_size = os.path.getsize('dataset.zip') / 1e6
    with open('dataset.zip', 'rb') as f:
        dataset = f.read()
    st.download_button(f'Download Dataset! Dataset Size:{file_size:>8.4f}', dataset,
                       file_name='dataset.zip', mime='application/zip')
