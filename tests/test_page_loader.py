import os
from os.path import abspath
from os.path import join
from page_loader.page_loader import download
from tests import FIXTURES_PATH
import tempfile
import requests_mock
import pytest


def build_fixture_path(file_name):
    return FIXTURES_PATH + file_name


IMGFILE1 = 'localhost-photos-me.jpg'
IMGFILE2 = 'site-com-photos-me.jpg'
JSFILE1 = 'localhost-assets-scripts.js'
CSSFILE1 = 'localhost-blog-about-assets-styles.css'
JSFILE2 = 'site-com-assets-scripts.js'
CSSFILE2 = 'site-com-blog-about-assets-styles.css'
DIR_NAME1 = 'localhost-blog-about_files'
DIR_NAME2 = 'site-com-blog-about_files'


@pytest.fixture
def tmpdir():
    return tempfile.mkdtemp()


# тут я так и не догадался как сделать так, чтобы всё мокалось через цикл
def test_page_loader(tmpdir):
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('localhost-blog-about.html')), 'r') as source, \
             open(abspath(build_fixture_path('expected/localhost-blog-about.html')), 'r') as expected_html_file, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-photos-me.jpg')), 'rb') as expected_img, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-assets-scripts.js')), 'r') as expected_jsfile, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-blog-about-assets-styles.css')), 'rb') as expected_cssfile:
            source = source.read()
            expected_img = expected_img.read()
            expected_jsfile = expected_jsfile.read()
            expected_cssfile = expected_cssfile.read()
            m.get('http://localhost/blog/about', text=source)
            m.get('http://localhost/photos/me.jpg', content=expected_img)
            m.get('http://localhost/assets/scripts.js', text=expected_jsfile)
            m.get('http://localhost/blog/about/assets/styles.css', content=expected_cssfile)
            result = download('http://localhost/blog/about', tmpdir)
            downloaded_html = open(join(tmpdir, 'localhost-blog-about.html')).read()
            assert result == join(tmpdir, 'localhost-blog-about.html')
            assert downloaded_html == expected_html_file.read()
            assert len(os.listdir(tmpdir)) == 2
            assert len(os.listdir(join(tmpdir, DIR_NAME1))) == 4


def test_page_loader_again(tmpdir):
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('site-com-blog-about.html')), 'r') as source, \
             open(abspath(build_fixture_path('expected/site-com-blog-about.html')), 'r') as expected_html_file, \
             open(abspath(build_fixture_path('expected/site-com-blog-about_files/site-com-photos-me.jpg')), 'rb') as expected_img, \
             open(abspath(build_fixture_path('expected/site-com-blog-about_files/site-com-assets-scripts.js')), 'r') as expected_jsfile, \
             open(abspath(build_fixture_path('expected/site-com-blog-about_files/site-com-blog-about-assets-styles.css')), 'rb') as expected_cssfile:
            source = source.read()
            expected_img = expected_img.read()
            expected_jsfile = expected_jsfile.read()
            expected_cssfile = expected_cssfile.read()
            m.get('http://site.com/blog/about', text=source)
            m.get('http://site.com/photos/me.jpg', content=expected_img)
            m.get('https://site.com/assets/scripts.js', text=expected_jsfile)
            m.get('http://site.com/blog/about/assets/styles.css', content=expected_cssfile)
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
