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


def make_request(url):
    r = requests.get(url)
    logging.debug(f'Response from server: {r}')
    r.raise_for_status()
    return r


def modify_html_and_get_data(url):
    dir_name = make_dir_name(url)
    domain = urlparse(url)[1]
    r = make_request(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    media_resources = {}
    for current_tag, attr in TAGS.items():
        tags = soup.find_all(current_tag)
        for tag in tags:
            if tag.get(attr)[0] == '/':
                link_to_asset = urljoin(url, tag[attr])
                name = make_file_name(domain + tag.get(attr))
                file_path = os.path.join(dir_name, name)
                media_resources[link_to_asset] = file_path
                tag[attr] = file_path
            else:
                another_netloc = urlparse(tag.get(attr))[1]
                parts = os.path.splitext(tag[attr])
                if domain == another_netloc and parts[1]:
                    name = make_file_name(tag.get(attr))
                    file_path = os.path.join(dir_name, name)
                    media_resources[tag[attr]] = file_path
                    tag[attr] = file_path
    return soup.prettify(), media_resources
