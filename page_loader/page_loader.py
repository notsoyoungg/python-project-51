import requests
import os, os.path
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urlunsplit


SCHEME = 'https://'


def build_file_name(link):
    link_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_parts[1])
    print(f'заспличенная ссылка: {splitted_link}')
    file_name = '-'.join(splitted_link) + '.html'
    if splitted_link[-1] == 'png':
        print(splitted_link[-1])
        file_name = '-'.join(splitted_link[0:-1]) + '.png'
    if splitted_link[-1] == 'jpg':
        print(splitted_link[-1])
        file_name = '-'.join(splitted_link[0:-1]) + '.jpg'
    else:
        file_name = '-'.join(splitted_link) + '.html'
    return file_name


def build_dir_name(link, file_path=None):
    link_parts = link.split('//')
    splitted_link = re.split('[^0-9a-zA-Z]', link_parts[1])
    dir_name = '-'.join(splitted_link) + '_files'
    if file_path:
        os.mkdir(os.path.join(file_path, dir_name))
    return dir_name


def parser(html, link, file_path):
    url = urlparse(link)
    soup = BeautifulSoup(html, 'html.parser')
    images_list = soup.find_all('img')
    file_name = build_file_name(link)
    dir_name = build_dir_name(link, file_path)
    output_file = os.path.join(file_path, file_name)
    links = []
    names = []
    for image in images_list:
        name = build_file_name(link + image['src'])
        if image['src'][0] == '/':
            links.append(SCHEME + url[1] + image['src'])
        else:
            links.append(image['src'])
            name = build_file_name(image['src'])
        names.append(name)
        local_path = os.path.join(dir_name, name)
        image['src'] = local_path
    with open(output_file, 'w') as result:
        result.write(soup.prettify())
    print(dict(zip(links, names)))
    return dict(zip(links, names))


def download(file_path, link):
    r = requests.get(link)
    content = parser(r.text, link, file_path)
    file_name = build_file_name(link)
    print(f'имя штмла: {file_name}')
    dir_name = build_dir_name(link)
    output_file = os.path.join(file_path, file_name)
    output_dir = os.path.join(file_path, dir_name)
    for img_link, name in content.items():
        print(f'это ссылка: {img_link}')
        print(f'это имя: {name}')
        file_name2 = os.path.join(output_dir, name)
        with open(file_name2, 'wb') as result:
            r = requests.get(img_link)
            result.write(r.content)
    return output_file


def download_imgs(file_path, link):
    r = requests.get(link)
    img_links = parser(r.text)
    file_name, dir_name = build_file_name(link)
    output_file = os.path.join(file_path, file_name)
    with open(output_file, 'wb') as result:
        result.write(r.content)
    return output_file

download('python-project-51', 'https://habr.com/ru/post/190154/')
#download_imgs('python-project-51', 'https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png')

# directory = os.getcwd()
# print(directory)


# print(build_file_name('https://google.com/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png'))
site = requests.get('https://progler.ru/blog/sozdanie-i-prosmotr-faylov-html-s-pomoschyu-python')
soup = BeautifulSoup(site.text, 'html.parser')
# print(soup.prettify())
images_list = soup.find_all('img')
links = []
names = []
for image in images_list:
    print(image['src'])


url = urlparse('https://progler.ru/blog/sozdanie-i-prosmotr-faylov-html-s-pomoschyu-python')
url2 = urlparse('https://ru.hexlet.io/courses')
print(url)
print(url2)
print(url[1])
