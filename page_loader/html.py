import os
import os.path
import sys
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader.url import make_file_name, make_dir_name


logging.basicConfig(format='[%(asctime)s: %(levelname)s] %(message)s',
                    level=logging.DEBUG,
                    force=True,
                    stream=sys.stderr)


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
    media_resources = {}
    for current_tag, attr in TAGS.items():
        tags = soup.find_all(current_tag)
        for tag in tags:
            if tag.get(attr)[0] == '/':
                link_to_asset = urljoin(link, tag[attr])
                name = make_file_name(netloc + tag.get(attr))
                file_path = os.path.join(dir_name, name)
                media_resources[link_to_asset] = file_path
                tag[attr] = file_path
            else:
                another_netloc = urlparse(tag.get(attr))[1]
                parts = os.path.splitext(tag[attr])
                if netloc == another_netloc and parts[1]:
                    name = make_file_name(tag.get(attr))
                    file_path = os.path.join(dir_name, name)
                    media_resources[tag[attr]] = file_path
                    tag[attr] = file_path
    return soup.prettify(), media_resources
