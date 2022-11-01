from distutils import extension
import re
import os.path
from urllib.parse import urlparse


def make_file_name(url):
    parsed = urlparse(url)
    if parsed.scheme:
        url = parsed.netloc + parsed.path
    path, extension = os.path.splitext(url)
    splitted_name = re.split('[^0-9a-zA-Z]', path)
    if extension:
        return '-'.join(splitted_name) + extension
    return '-'.join(splitted_name) + '.html'


def make_dir_name(url):
    parsed = urlparse(url)
    splitted_link = re.split('[^0-9a-zA-Z]', parsed.netloc + parsed.path)
    dir_name = '-'.join(splitted_link) + '_files'
    return dir_name
