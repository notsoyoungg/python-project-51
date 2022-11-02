import os
import requests_mock
import pytest
from os.path import abspath
from os.path import join
from urllib.parse import urljoin
from page_loader.page_loader import download
from tests import FIXTURES_PATH
from page_loader.url import make_dir_name


def build_fixture_path(file_name):
    return FIXTURES_PATH + file_name


ASSETS = [('/photos/me.jpg', 'expected/photo.jpg'), ('/assets/scripts.js', 'expected/script.js'), ('/blog/about/assets/styles.css', 'expected/styles.css')]


@pytest.mark.parametrize("url,expected_html_path,mocked_html", [
                        ('http://localhost/blog/about', 'expected/localhost-blog-about.html', 'localhost-blog-about.html'),
                        ('http://site.com/blog/about', 'expected/site-com-blog-about.html', 'site-com-blog-about.html')])
def test_page_loader(url, expected_html_path, mocked_html, tmpdir):
    with requests_mock.Mocker() as m:
        with open(build_fixture_path(mocked_html), 'rb') as file:
            m.get(url, content=file.read())
        with open(build_fixture_path(expected_html_path), 'r') as expected_html_file:
            for url_part, path in ASSETS:
                with open(build_fixture_path(path), 'rb') as file:
                    print(build_fixture_path(path))
                    print(urljoin(url, url_part))
                    m.get(urljoin(url, url_part), content=file.read())
            result = download(url, tmpdir)
            downloaded_html = open(join(tmpdir, mocked_html)).read()
            assert result == join(tmpdir, mocked_html)
            assert downloaded_html == expected_html_file.read()
            assert len(os.listdir(tmpdir)) == 2
            assert len(os.listdir(join(tmpdir, make_dir_name(url)))) == 4


def test_exception_directory_not_found():
    with pytest.raises(Exception) as e:
        download('https://localhost/blog/about', 'dsfjsjsgj')
    assert str(e.value) == 'The specified directory does not exist. '\
                           'Please, specify an existing directory'


def test_exception_http404(tmpdir):
    with pytest.raises(Exception) as e:
        download('https://google.com/images/branding/googleeruadfj', tmpdir)
        assert str(e.value) == 'That’s an error. Status code: 404'
