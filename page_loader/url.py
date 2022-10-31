import re
import os.path
from urllib.parse import urlparse


def make_file_name(name):
    parsed = urlparse(name)
    if parsed.scheme:
        name = parsed.netloc + parsed.path
    parts = os.path.splitext(name)
    splitted_name = re.split('[^0-9a-zA-Z]', parts[0])
    if parts[1]:
        return '-'.join(splitted_name) + parts[1]
    return '-'.join(splitted_name) + '.html'


def make_dir_name(link):
    parsed = urlparse(link)
    splitted_link = re.split('[^0-9a-zA-Z]', parsed.netloc + parsed.path)
    dir_name = '-'.join(splitted_link) + '_files'
    return dir_name
