import os
import os.path
import logging
from progress.bar import Bar
from page_loader.url import make_html_name, make_dir_name
from page_loader.html_editor import modify_html_and_get_data
from page_loader.html_editor import make_request


def download_resources(data, path, link):
    bar = Bar('Processing', max=len(data))
    dir_name = make_dir_name(link)
    os.mkdir(os.path.join(path, dir_name))
    for img_link, path_to_file in data.items():
        file_name = os.path.join(path, path_to_file)
        with open(file_name, 'wb') as result:
            r = make_request(img_link)
            logging.debug(img_link)
            result.write(r.content)
            bar.next()
    bar.finish()


def download(link, path):
    if not os.path.isdir(path):
        raise FileNotFoundError('The specified directory does not exist. '
                                'Please, specify an existing directory')
    html_content, data = modify_html_and_get_data(link)
    download_resources(data, path, link)
    html_name = make_html_name(link)
    path_to_html = os.path.join(path, html_name)
    with open(path_to_html, 'w') as edited_html:
        edited_html.write(html_content)
    return path_to_html
