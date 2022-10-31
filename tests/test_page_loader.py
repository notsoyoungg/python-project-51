import os
from os.path import abspath
from os.path import join
from page_loader.page_loader import download
from tests import FIXTURES_PATH
import requests_mock
import pytest


def build_fixture_path(file_name):
    return FIXTURES_PATH + file_name


DIR_NAME1 = 'localhost-blog-about_files'
DIR_NAME2 = 'site-com-blog-about_files'
ASSETS1 = [('http://localhost/blog/about', 'localhost-blog-about.html'),
           ('http://localhost/photos/me.jpg', 'expected/localhost-blog-about_files/localhost-photos-me.jpg'),
           ('http://localhost/assets/scripts.js', 'expected/localhost-blog-about_files/localhost-assets-scripts.js'),
           ('http://localhost/blog/about/assets/styles.css', 'expected/localhost-blog-about_files/localhost-blog-about-assets-styles.css')]
ASSETS2 = [('http://site.com/blog/about', 'site-com-blog-about.html'),
           ('http://site.com/photos/me.jpg', 'expected/site-com-blog-about_files/site-com-photos-me.jpg'),
           ('https://site.com/assets/scripts.js', 'expected/site-com-blog-about_files/site-com-assets-scripts.js'),
           ('http://site.com/blog/about/assets/styles.css', 'expected/site-com-blog-about_files/site-com-blog-about-assets-styles.css')]


def test_page_loader(tmpdir):
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('expected/localhost-blog-about.html')), 'r') as expected_html_file:
            for link, path in ASSETS1:
                with open(build_fixture_path(path), 'rb') as file:
                    m.get(link, content=file.read())
            result = download('http://localhost/blog/about', tmpdir)
            downloaded_html = open(join(tmpdir, 'localhost-blog-about.html')).read()
            assert result == join(tmpdir, 'localhost-blog-about.html')
            assert downloaded_html == expected_html_file.read()
            assert len(os.listdir(tmpdir)) == 2
            assert len(os.listdir(join(tmpdir, DIR_NAME1))) == 4


def test_page_loader_again(tmpdir):
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('expected/site-com-blog-about.html')), 'r') as expected_html_file:
            for link, path in ASSETS2:
                with open(build_fixture_path(path), 'rb') as file:
                    m.get(link, content=file.read())
            result = download('http://site.com/blog/about', tmpdir)
            downloaded_html = open(join(tmpdir, 'site-com-blog-about.html')).read()
            assert result == join(tmpdir, 'site-com-blog-about.html')
            assert downloaded_html == expected_html_file.read()
            assert len(os.listdir(tmpdir)) == 2
            assert len(os.listdir(join(tmpdir, DIR_NAME2))) == 4


def test_exception_1():
    with pytest.raises(Exception) as e:
        download('https://localhost/blog/about', 'dsfjsjsgj')
    assert str(e.value) == 'The specified directory does not exist. '\
                           'Please, specify an existing directory'


def test_exception_2(tmpdir):
    with pytest.raises(Exception) as e:
        download('https://google.com/images/branding/googleeruadfj', tmpdir)
        assert str(e.value) == 'That’s an error. Status code: 404'
