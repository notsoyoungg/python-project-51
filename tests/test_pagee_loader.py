from os.path import abspath
from os.path import join
from page_loader.page_loader import download
import tests
import tempfile
import requests_mock
import pytest


def build_fixture_path(file_name):
    return tests.FIXTURES_PATH + file_name


IMGFILE1 = 'localhost-photos-me.jpg'
IMGFILE2 = 'site-com-photos-me.jpg'
JSFILE1 = 'localhost-assets-scripts.js'
CSSFILE1 = 'localhost-blog-about-assets-styles.css'
JSFILE2 = 'site-com-assets-scripts.js'
CSSFILE2 = 'site-com-blog-about-assets-styles.css'
DIR_NAME1 = 'localhost-blog-about_files'
DIR_NAME2 = 'site-com-blog-about_files'


def test_page_loader():
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('localhost-blog-about.html')), 'r') as source, \
             open(abspath(build_fixture_path('expected/localhost-blog-about.html')), 'r') as expected_html_file, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-photos-me.jpg')), 'rb') as expected_img, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-assets-scripts.js')), 'r') as expected_jsfile, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-blog-about-assets-styles.css')), 'rb') as expected_cssfile:
            with tempfile.TemporaryDirectory() as tmp:
                source = source.read()
                expected_img = expected_img.read()
                expected_jsfile = expected_jsfile.read()
                expected_cssfile = expected_cssfile.read()
                m.get('http://localhost/blog/about', text=source)
                m.get('http://localhost/photos/me.jpg', content=expected_img)
                m.get('http://localhost/assets/scripts.js', text=expected_jsfile)
                m.get('http://localhost/blog/about/assets/styles.css', content=expected_cssfile)
                result = download('http://localhost/blog/about', tmp)
                downloaded_html = open(join(tmp, 'localhost-blog-about.html')).read()
                downloade_img = open(join(tmp, DIR_NAME1, IMGFILE1), 'rb').read()
                downloaded_js = open(join(tmp, DIR_NAME1, JSFILE1), 'r').read()
                downloaded_css = open(join(tmp, DIR_NAME1, CSSFILE1), 'rb').read()
                assert result == join(tmp, 'localhost-blog-about.html')
                assert downloaded_html == expected_html_file.read()
                assert downloade_img == expected_img
                assert downloaded_js == expected_jsfile
                assert downloaded_css == expected_cssfile


def test_page_loader_again():
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('site-com-blog-about.html')), 'r') as source, \
             open(abspath(build_fixture_path('expected/site-com-blog-about.html')), 'r') as expected_html_file, \
             open(abspath(build_fixture_path('expected/site-com-blog-about_files/site-com-photos-me.jpg')), 'rb') as expected_img, \
             open(abspath(build_fixture_path('expected/site-com-blog-about_files/site-com-assets-scripts.js')), 'r') as expected_jsfile, \
             open(abspath(build_fixture_path('expected/site-com-blog-about_files/site-com-blog-about-assets-styles.css')), 'rb') as expected_cssfile:
            with tempfile.TemporaryDirectory() as tmp:
                source = source.read()
                expected_img = expected_img.read()
                expected_jsfile = expected_jsfile.read()
                expected_cssfile = expected_cssfile.read()
                m.get('http://site.com/blog/about', text=source)
                m.get('http://site.com/photos/me.jpg', content=expected_img)
                m.get('https://site.com/assets/scripts.js', text=expected_jsfile)
                m.get('http://site.com/blog/about/assets/styles.css', content=expected_cssfile)
                result = download('http://site.com/blog/about', tmp)
                downloaded_html = open(join(tmp, 'site-com-blog-about.html')).read()
                downloade_img = open(join(tmp, DIR_NAME2, IMGFILE2), 'rb').read()
                downloaded_js = open(join(tmp, DIR_NAME2, JSFILE2), 'r').read()
                downloaded_css = open(join(tmp, DIR_NAME2, CSSFILE2), 'rb').read()
                assert result == join(tmp, 'site-com-blog-about.html')
                assert downloaded_html == expected_html_file.read()
                assert downloade_img == expected_img
                assert downloaded_js == expected_jsfile
                assert downloaded_css == expected_cssfile


def test_error1():
    with pytest.raises(Exception) as e:
        download('https://localhost/blog/about', 'dsfjsjsgj')
    assert str(e.value) == 'The specified directory does not exist. '\
                           'Please, specify an existing directory'


def test_error2():
    with pytest.raises(Exception) as e:
        with tempfile.TemporaryDirectory() as tmp:
            download('https://google.com/images/branding/googleeruadfj', tmp)
        assert str(e.value) == 'That’s an error. Status code: 404'
