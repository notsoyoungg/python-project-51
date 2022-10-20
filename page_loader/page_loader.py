import requests
import os
import os.path
import logging
import sys
from logging import StreamHandler, Formatter
from progress.bar import Bar
from page_loader.names_maker import make_html_name
from page_loader.directory_creator import build_dir
from page_loader.html_editor import edit_html


logger = logging.getLogger('logger')
handler = StreamHandler(stream=sys.stderr)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


EXTENSIONS = ['.jpg', '.png', '.svg', '.css']
bar = Bar('Processing', max=100500)


def make_request(link):
    r = requests.get(link)
    logger.debug(f'Response from server: {r}')
    logger.debug(r.raise_for_status())
    return r


def download(main_link, main_path):
    if not os.path.isdir(main_path):
        raise FileNotFoundError('The specified directory does not exist. '
                                'Please, specify an existing directory')
    r = make_request(main_link)
    content = r.text
    dir_name = build_dir(main_link, main_path)
    data = edit_html(content, main_link, dir_name, main_path)
    html_file = make_html_name(main_link)
    for img_link, path in data.items():
        file_name = os.path.join(main_path, path)
        parts = os.path.splitext(file_name)
        if parts[1] in EXTENSIONS:
            with open(file_name, 'wb') as result:
                r = make_request(img_link)
                result.write(r.content)
                bar.next()
        else:
            with open(file_name, 'w') as result:
                r = make_request(img_link)
                result.write(r.text)
                bar.next()
    bar.finish()
    return os.path.join(main_path, html_file)
