import os
import os.path
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader.url import make_file_name, make_dir_name


TAGS = {'link': 'href',
        'img': 'src',
        'script': 'src'}


def make_request(link):
    r = requests.get(link)
    logging.debug(f'Response from server: {r}')
    r.raise_for_status()
    return r


def modify_html_and_get_data(link):
    dir_name = make_dir_name(link)
    netloc = urlparse(link)[1]
    r = make_request(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = {}
    for key in TAGS:
        tags = soup.find_all(key)
        for tag in tags:
            if tag.get(TAGS[key])[0] == '/':
                another_link = urljoin(link, tag[TAGS[key]])
                name = make_file_name(netloc + tag.get(TAGS[key]))
                another_path = os.path.join(dir_name, name)
                data[another_link] = another_path
                tag[TAGS[key]] = another_path
            else:
                another_netloc = urlparse(tag.get(TAGS[key]))[1]
                parts = os.path.splitext(tag[TAGS[key]])
                if netloc == another_netloc and parts[1]:
                    name = make_file_name(tag.get(TAGS[key]))
                    another_path = os.path.join(dir_name, name)
                    data[tag[TAGS[key]]] = another_path
                    tag[TAGS[key]] = another_path
    return soup.prettify(), data
