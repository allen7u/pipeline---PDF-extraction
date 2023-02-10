







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
import pyperclip

output_dir = "F:\Anaconda_Cache"

def quote_path(path):
    print('checking path {} ...'.format(path))
    # check if pdf path quoted
    if not (path.startswith('"') and path.endswith('"')):
        print('Quoting path...')
        # quote the path in case it contains spaces
        print('before inner quote: ', path)
        path = '"{}"'.format(path)
        print('after inner quote: ', path)
        # save path to a file
        with open('path_after inner quote.txt', 'w', encoding='utf-8') as f:
            f.write(path)
    else:
        print('Path already quoted')
    print(path)
    return path

def pdf_to_text(pdf_path):
    # create output dir if not exists
    if not os.path.exists(st.session_state['output_dir']):
        os.makedirs(st.session_state['output_dir'])
    print('before strip: ', pdf_path)
    # pdf_path = pdf_path.lstrip('"')
    pdf_path = pdf_path.replace('"', '')
    print('after strip: ', pdf_path)
    base_name = os.path.basename(pdf_path).strip('.pdf')
    print('before quote: ', pdf_path)
    pdf_path = quote_path(pdf_path)
    print('after quote: ', pdf_path)
    text_path = os.path.join(st.session_state['output_dir'], base_name + '.txt')
    # check if text file already exists
    if os.path.exists(text_path):
        print('text file already exists')
        # read text file
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    text_path = quote_path(text_path)
    json_path = os.path.join(st.session_state['output_dir'], base_name + '.json')
    json_path = quote_path(json_path)
    # replace backslashes with double backslashes
    pdf_path = pdf_path.replace('\\', '\\\\')
    text_path = text_path.replace('\\', '\\\\')
    print('before format: ', pdf_path)
    print('before format: ', text_path)
    # translate the pdf_path to wsl
    cmd = 'wsl wslpath -u {}'.format(pdf_path)
    print('cmd: ', cmd)
    # save cmd to a file
    with open('cmd pdf.txt', 'w', encoding='utf-8') as f:
        f.write(cmd)
    pdf_path_u = sp.check_output(cmd).decode('utf-8').strip()
    cmd = 'wsl wslpath -u {}'.format(text_path)
    print('cmd: ', cmd)
    # save cmd to a file
    with open('cmd text.txt', 'w', encoding='utf-8') as f:
        f.write(cmd)
    text_path_u = sp.check_output(cmd).decode('utf-8').strip()
    pdf_path_u_quote = quote_path(pdf_path_u)
    text_path_u_quote = quote_path(text_path_u)
    cmd = 'wsl java -jar pdfact.jar  {}  {}'.format(pdf_path_u_quote, text_path_u_quote)
    print(cmd)
    res = sp.check_output(cmd).decode('utf-8').strip()
    print(res)
    # wait for the text file to be created
    text_path = text_path.strip('"')
    while not os.path.exists(text_path):
        # print('waiting for text file to be created...')
        time.sleep(0.1)
    # read text file
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def main():
    st.title('PDF to Text Converter ')
    st.subheader('powered by pdfact')
    container = st.empty()
    if 'pdf_paths' not in st.session_state:
        st.session_state['pdf_paths'] = container.text_area('Please paste the paths you want to convert, typing not supported for now', 
        value = '', key = 1, height = 150)
    col1, col2, col3 = st.columns(3)
    with col1:
        convert_button = st.button('Convert')
    with col2:
        paste_button = st.button('Paste')
    with col3:
        clear_button = st.button('Clear')
    # show_button = st.button('Show')
    output_dir = st.text_input('Please select the folder where you want to save the JSON files', 
    value = 'F:\Anaconda_Cache')  
    if output_dir:
        st.session_state['output_dir'] = output_dir
    print('output_dir ', st.session_state['output_dir'])
    if convert_button:
        display = st.container()
        display.write('Converting...')
        print('before convert ++++++++ ', st.session_state['pdf_paths'])
        print('before split ', st.session_state['pdf_paths'])
        print('after split ', st.session_state['pdf_paths'].splitlines())
        for pdf_file in st.session_state['pdf_paths'].splitlines():
            print('pdf_file ', pdf_file)
            text  = pdf_to_text(pdf_file)
            display.write(text[:100])
            display.write('=============================')
        display.write('Done')
        # st.balloons()
    if clear_button:
        st.session_state['pdf_paths'] = container.text_area('Please paste the paths you want to convert, typing not su for now', 
        value = '', key = 2, height = 150)
        print('after clear ', st.session_state['pdf_paths'])
    if paste_button:
        # read from clipboard 
        print('before ', st.session_state['pdf_paths'])
        st.session_state['pdf_paths'] = st.session_state['pdf_paths'] + '\n' + pyperclip.paste()
        st.session_state['pdf_paths'] = st.session_state['pdf_paths'].strip()
        print('after ', st.session_state['pdf_paths'])
        st.session_state['pdf_paths'] = container.text_area('Please paste the paths you want to convert, typing not su for now',
        value = st.session_state['pdf_paths'], key = 3, height = 150)
    #     print('final ', st.session_state['pdf_paths'])
    # if show_button:
    #     st.session_state['pdf_paths'] = container.text_area('Please paste the paths you want to convert, typing not su for now',
    #     value = st.session_state['pdf_paths'], key = 4, height = 150)
    #     print('show ',st.session_state['pdf_paths'])       


if __name__ == '__main__':
    # check if this is the main thread
    if threading.current_thread() is threading.main_thread():
        # run streamlit app without opening browser
        sp.Popen(["streamlit", "run", "main.py", "--server.port", "8501", "--browser.serverAddress", "localhost", "--server.headless", "true"])
        # Create a webview and display the Streamlit app
        webview.create_window("Pdfact - PDF to Text Converter", "http://localhost:8501")
        # start the webview
        webview.start()
    else:
        main()




