import os
import os.path
import logging
from progress.bar import Bar
from page_loader.url import make_file_name, make_dir_name
from page_loader.html import modify_html_and_get_data, make_request


def download_resources(data, path, url):
    bar = Bar('Processing', max=len(data))
    dir_name = make_dir_name(url)
    os.mkdir(os.path.join(path, dir_name))
    for resource_url, resource_path in data.items():
        file_name = os.path.join(path, resource_path)
        with open(file_name, 'wb') as result:
            r = make_request(resource_url)
            logging.debug(f'Downloading: {resource_url}')
            result.write(r.content)
            bar.next()
    bar.finish()


def download(url, path):
    if not os.path.isdir(path):
        raise FileNotFoundError('The specified directory does not exist. '
                                'Please, specify an existing directory')
    html_content, data = modify_html_and_get_data(url)
    download_resources(data, path, url)
    html_name = make_file_name(url)
    path_to_html = os.path.join(path, html_name)
    with open(path_to_html, 'w') as file:
        file.write(html_content)
    return path_to_html
