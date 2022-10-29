import re
import os.path


def make_html_name(link):
    link_two_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_two_parts[1])
    if splitted_link[-1] == 'html':
        return '-'.join(splitted_link[0:-1]) + '.html'
    return '-'.join(splitted_link) + '.html'


def make_file_name(name):
    if 'http' in name:
        name = name.split('//')[1]
    parts = os.path.splitext(name)
    splitted_name = re.split('[^0-9a-zA-Z]', parts[0])
    if parts[1]:
        return '-'.join(splitted_name) + parts[1]
    return '-'.join(splitted_name) + '.html'


def make_dir_name(link):
    link_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_parts[1])
    dir_name = '-'.join(splitted_link) + '_files'
    return dir_name
