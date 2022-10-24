import os
import os.path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import validators
from page_loader.names_maker import make_file_name, make_html_name


def complete_the_lists(tags, atribute, links, paths, link, dir_name):
    scheme = urlparse(link)[0]
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
                    tag[atribute] = path
                    paths.append(path)
            elif tag.get(atribute)[0] == '/':
                links.append(scheme + '://' + netloc + tag[atribute])
                url_parts = urlparse(tag[atribute])
                new_part = url_parts._replace(query='')
                name = make_file_name(netloc + urlunparse(new_part))
                path = os.path.join(dir_name, name)
                tag[atribute] = path
                paths.append(path)


def edit_html(content, link, dir_name, main_path):
    soup = BeautifulSoup(content, 'html.parser')
    tags1 = soup.find_all(['img', 'script'])
    tags2 = soup.find_all('link')
    links = []
    paths = []
    complete_the_lists(tags2, 'href', links, paths, link, dir_name)
    complete_the_lists(tags1, 'src', links, paths, link, dir_name)
    html_file = make_html_name(link)
    path_to_html = os.path.join(main_path, html_file)
    with open(path_to_html, 'w') as edited_html:
        edited_html.write(soup.prettify())
    return dict(zip(links, paths))
