import requests
import os
import os.path
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import validators
import logging
import sys
from logging import StreamHandler, Formatter
from progress.bar import Bar


logger = logging.getLogger('logger')
handler = StreamHandler(stream=sys.stderr)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


SCHEME = 'https://'
EXTENSIONS = {'html': '.html', 'jpg': '.jpg', 'png': '.png'}
EXTENSIONS2 = ['.jpg', '.png', '.svg', '.css']
bar = Bar('Processing', max=100500)


def make_html_name(link):
    link_two_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_two_parts[1])
    if splitted_link[-1] == 'html':
        return '-'.join(splitted_link[0:-1]) + '.html'
    return '-'.join(splitted_link) + '.html'


def build_dir(link, file_path):
    link_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_parts[1])
    dir_name = '-'.join(splitted_link) + '_files'
    path_to_dir = os.path.join(file_path, dir_name)
    os.mkdir(path_to_dir)
    return dir_name


# принимает имя-путь, состоящее из нетлока и ссылки
# возвращает имя файла без полного пути до него
def make_file_name(name):
    if 'http' in name:
        name = name.split('//')[1]
    parts = os.path.splitext(name)
    splitted_name = re.split('[^0-9a-zA-Z]', parts[0])
    if parts[1]:
        return '-'.join(splitted_name) + parts[1]
    return '-'.join(splitted_name) + '.html'


def complete_the_lists(tags, atribute, links, paths, link, dir_name):
    netloc = urlparse(link)[1]
    for tag in tags:
        if tag.get(atribute):
            if validators.url(tag.get(atribute)):
                another_netloc = urlparse(tag.get(atribute))[1]
                parts = os.path.splitext(tag[atribute])
                if netloc == another_netloc and parts[1]:
                    links.append(tag[atribute])
                    parsed = urlparse(tag.get(atribute))
                    parsed_new = parsed._replace(query='')
                    name = make_file_name(urlunparse(parsed_new))
                    path = os.path.join(dir_name, name)
                    # вот тут происходит замена путей в тексте html,
                    # который далее нужно будет записать в файл
                    tag[atribute] = path
                    paths.append(path)
            elif tag.get(atribute)[0:2] != '//':
                links.append(SCHEME + netloc + tag[atribute])
                url_parts = urlparse(tag[atribute])
                new_part = url_parts._replace(query='')
                name = make_file_name(netloc + urlunparse(new_part))
                path = os.path.join(dir_name, name)
                tag[atribute] = path
                paths.append(path)


# принимает изначальную ссылку
# тут еще нужно обработать тэг 'link'
# как-то сделать через рекурсию ?
# возврачает словарь со ссылками в качестве ключей
# в переменной soup после вызова функции хранится переписанный html
# который далее нужно записать в файл

# походу надо распарсить url, потом заменить его
# часть на новую и собрать url снова
def edit_html(content, link, dir_name, main_path):
    soup = BeautifulSoup(content, 'html.parser')
    tags1 = soup.find_all(['img', 'script'])
    tags2 = soup.find_all('link')
    links = []
    paths = []
    complete_the_lists(tags1, 'src', links, paths, link, dir_name)
    complete_the_lists(tags2, 'href', links, paths, link, dir_name)
    html_file = make_html_name(link)
    path_to_html = os.path.join(main_path, html_file)
    with open(path_to_html, 'w') as edited_html:
        edited_html.write(soup.prettify())
        bar.next()
    return dict(zip(links, paths))


def make_request(link):
    r = requests.get(link)
    logger.debug(f'Response from server: {r}')
    if r.status_code != 200 and r.status_code != 111:
        raise Exception(f'That’s an error. Status code: {r.status_code}')
    return r


# data - это словарик с именами и ссылками
def download(main_link, main_path):
    if not os.path.isdir(main_path):
        raise Exception('The specified directory does not exist. '
                        'Please, specify an existing directory')
    r = make_request(main_link)
    content = r.text
    dir_name = build_dir(main_link, main_path)
    data = edit_html(content, main_link, dir_name, main_path)
    html_file = make_html_name(main_link)
    for img_link, path in data.items():
        file_name = os.path.join(main_path, path)
        parts = os.path.splitext(file_name)
        if parts[1] in EXTENSIONS2:
            with open(file_name, 'wb') as result:
                r = make_request(img_link)
                logger.debug(f'Response from server: {r}')
                result.write(r.content)
                bar.next()
        else:
            with open(file_name, 'w') as result:
                r = make_request(img_link)
                result.write(r.text)
                bar.next()
    bar.finish()
    return os.path.join(main_path, html_file)
