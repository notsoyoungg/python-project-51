from os.path import abspath
from os.path import join
from page_loader.page_loader import download
import tests
import tempfile
import requests_mock


def build_fixture_path(file_name):
    return tests.FIXTURES_PATH + file_name


def test_page_loader():
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('source.html')), 'r') as source:
            with tempfile.TemporaryDirectory() as tmp:
                source = source.read()
                m.get('https://google.com', text=source)
                result = download(tmp, 'https://google.com')
                expected = open(join(tmp, 'google-com.html')).read()
                assert result == join(tmp, 'google-com.html')
                assert expected == source