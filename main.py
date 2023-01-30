







import threading
import webview
import streamlit as st
import subprocess as sp

import os
import json
import time
import sys
import re
import glob
import shutil
import pandas as pd

output_dir = "F:\Anaconda_Cache"

def quote_path(path):
    print('checking path {} ...'.format(path))
    # check if pdf path quoted
    if not (path.startswith('"') and path.endswith('"')):
        print('Quoting path...')
        # quote the path in case it contains spaces
        path = '"{}"'.format(path)
    else:
        print('Path already quoted')
    print(path)
    return path

def pdf_to_text(pdf_path):
    pdf_path = pdf_path.strip('"')
    base_name = os.path.basename(pdf_path).strip('.pdf')
    pdf_path = quote_path(pdf_path)
    text_path = os.path.join(output_dir, base_name + '.txt')
    text_path = quote_path(text_path)
    json_path = os.path.join(output_dir, base_name + '.json')
    json_path = quote_path(json_path)
    cmd = 'java -jar F:\\Anaconda_Play\\PDF_extract_without_python\\pdfact\\bin\\pdfact.jar  {}  {}'.format(pdf_path, text_path)
    print(cmd)
    sp.call(cmd, shell=True)
    # wait for the text file to be created
    text_path = text_path.strip('"')
    while not os.path.exists(text_path):
        # print('waiting for text file to be created...')
        time.sleep(0.1)
    # read text file
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # save text to json file
    # with open(json_path, 'w', encoding='utf-8') as f:
    #     json.dump(text, f)
    return text

def main():
    st.title('PDF to Text Converter')
    convert_button = st.button('Convert')
    pdf_paths = st.text_area('Please select the PDF files you want to convert', 
    value = '', height = 150)
    output_dir = st.text_input('Please select the folder where you want to save the JSON files', 
    value = 'F:\Anaconda_Cache')  
    if convert_button:
        st.write('Converting...')
        for pdf_file in pdf_paths.split('\n'):
            text  = pdf_to_text(pdf_file)
            st.write(text[:100])
            st.write('=============================')
        st.write('Done')
        # st.balloons()

if __name__ == '__main__':
    # check if this is the main thread
    if threading.current_thread() is threading.main_thread():
        # run streamlit app without opening browser
        sp.Popen(["streamlit", "run", "main.py", "--server.port", "8502", "--browser.serverAddress", "localhost", "--server.headless", "true"])
        # Create a webview and display the Streamlit app
        webview.create_window("PDF to Text Converter", "http://localhost:8502")
        # start the webview
        webview.start()
    else:
        main()




