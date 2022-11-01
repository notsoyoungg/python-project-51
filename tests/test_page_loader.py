import os
from os.path import abspath
from os.path import join
from page_loader.page_loader import download
from tests import FIXTURES_PATH
import requests_mock
import pytest


def build_fixture_path(file_name):
    return FIXTURES_PATH + file_name


ASSETS1 = [('http://localhost/blog/about', 'localhost-blog-about.html'),
           ('http://localhost/photos/me.jpg', 'expected/photo.jpg'),
           ('http://localhost/assets/scripts.js', 'expected/script.js'),
           ('http://localhost/blog/about/assets/styles.css', 'expected/styles.css')]
ASSETS2 = [('http://site.com/blog/about', 'site-com-blog-about.html'),
           ('http://site.com/photos/me.jpg', 'expected/photo.jpg'),
           ('https://site.com/assets/scripts.js', 'expected/script.js'),
           ('http://site.com/blog/about/assets/styles.css', 'expected/styles.css')]


@pytest.mark.parametrize("url,file_path,file_name,dir_name,assets", [
                        ('http://localhost/blog/about', 'expected/localhost-blog-about.html', 'localhost-blog-about.html', 'localhost-blog-about_files', ASSETS1),
                        ('http://site.com/blog/about', 'expected/site-com-blog-about.html', 'site-com-blog-about.html', 'site-com-blog-about_files', ASSETS2)])
def test_page_loader(url, file_path, file_name, dir_name, assets, tmpdir):
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path(file_path)), 'r') as expected_html_file:
            for link, path in assets:
                with open(build_fixture_path(path), 'rb') as file:
                    m.get(link, content=file.read())
            result = download(url, tmpdir)
            downloaded_html = open(join(tmpdir, file_name)).read()
            assert result == join(tmpdir, file_name)
            assert downloaded_html == expected_html_file.read()
            assert len(os.listdir(tmpdir)) == 2
            assert len(os.listdir(join(tmpdir, dir_name))) == 4


def test_exception_1():
    with pytest.raises(Exception) as e:
        download('https://localhost/blog/about', 'dsfjsjsgj')
    assert str(e.value) == 'The specified directory does not exist. '\
                           'Please, specify an existing directory'


def test_exception_2(tmpdir):
    with pytest.raises(Exception) as e:
        download('https://google.com/images/branding/googleeruadfj', tmpdir)
        assert str(e.value) == 'That’s an error. Status code: 404'
