import streamlit as st
from .utils import read_json,save_image_attachment
import os 
from pathlib import Path

def image_file_upload():
    uploaded_files = st.file_uploader("Choose a image file", accept_multiple_files=True)
    return uploaded_files


def image_file_save(uploaded_files):
    files =[]
    config = read_json("config","./")
    for uploaded_file in uploaded_files:
        file_name = str(len(os.listdir(Path(config["attachments_path"]))))
        save_image_attachment(uploaded_file,file_name)
        files.append(file_name)
    return files

