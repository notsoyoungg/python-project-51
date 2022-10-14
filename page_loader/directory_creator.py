import re
import os
import os.path


def build_dir(link, file_path):
    link_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_parts[1])
    dir_name = '-'.join(splitted_link) + '_files'
    path_to_dir = os.path.join(file_path, dir_name)
    os.mkdir(path_to_dir)
    return dir_name