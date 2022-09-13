from unittest import result
import requests
import os.path
import re

def build_file_name(link):
    link_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_parts[1])
    file_name = '-'.join(splitted_link) + '.html'
    return file_name

directory = os.getcwd()

def download(file_path, link):
    r = requests.get(link)
    file_name = build_file_name(link)
    output_file = os.path.join(file_path, file_name)
    with open(output_file, 'w') as result:
        result.write(r.text)
    print(output_file)
    return result


# download('python-project-51', 'https://google.com')

directory = os.getcwd()
print(directory)