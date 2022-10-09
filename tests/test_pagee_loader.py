from os.path import abspath
from os.path import join
from page_loader.page_loader import download
import tests
import tempfile
import requests_mock
import pytest


# чтобы отображались логи, тусты запускать с флагом -s: 'poetry run pytest -s'
def build_fixture_path(file_name):
    return tests.FIXTURES_PATH + file_name


IMG1_NAME = 'google-com-images-branding-googlelogo-1x-googlelogo-white-background-color-272x92dp.png'
IMG2_NAME = 'google-com-textinputassistant-tia.png'
IMG3_NAME = 'localhost-photos-me.jpg'
FILE1_NAME = 'localhost-assets-scripts.js'
FILE2_NAME = 'localhost-blog-about-assets-styles.css'
DIR_NAME = 'google-com_files'
DIR_NAME2 = 'localhost-blog-about_files'


def test_page_loader():
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('source.html')), 'r') as source, \
             open(abspath(build_fixture_path('edited.html')), 'r') as edited, \
             open(abspath(build_fixture_path('img1.png')), 'rb') as img1, \
             open(abspath(build_fixture_path('img2.png')), 'rb') as img2:
                with tempfile.TemporaryDirectory() as tmp:
                    source = source.read()
                    img1 = img1.read()
                    img2 = img2.read()
                    m.get('https://google.com', text=source)
                    m.get('https://google.com/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png', content=img1)
                    m.get('https://google.com/textinputassistant/tia.png', content=img2)
                    result = download('https://google.com', tmp)
                    expected = open(join(tmp, 'google-com.html')).read()
                    expected_img1 = open(join(tmp, DIR_NAME, IMG1_NAME), 'rb').read()
                    expected_img2 = open(join(tmp, DIR_NAME, IMG2_NAME), 'rb').read()
                    assert result == join(tmp, 'google-com.html')
                    assert expected == edited.read()
                    assert expected_img1 == img1
                    assert expected_img2 == img2


def test2_page_loader():
    with requests_mock.Mocker() as m:
        with open(abspath(build_fixture_path('localhost-blog-about.html')), 'r') as source, \
             open(abspath(build_fixture_path('expected/localhost-blog-about.html')), 'r') as edited, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-photos-me.jpg')), 'rb') as img, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-assets-scripts.js')), 'r') as jsfile, \
             open(abspath(build_fixture_path('expected/localhost-blog-about_files/localhost-blog-about-assets-styles.css')), 'r') as cssfile:
                with tempfile.TemporaryDirectory() as tmp:
                    source = source.read()
                    img = img.read()
                    jsfile = jsfile.read()
                    cssfile = cssfile.read()
                    m.get('https://localhost/blog/about', text=source)
                    m.get('https://localhost/photos/me.jpg', content=img)
                    m.get('http://localhost/assets/scripts.js', text=jsfile)
                    m.get('https://localhost/blog/about/assets/styles.css', text=cssfile)
                    result = download('https://localhost/blog/about', tmp)
                    expected = open(join(tmp, 'localhost-blog-about.html')).read()
                    expected_img = open(join(tmp, DIR_NAME2, IMG3_NAME), 'rb').read()
                    expected_js = open(join(tmp, DIR_NAME2, FILE1_NAME), 'r').read()
                    expected_css = open(join(tmp, DIR_NAME2, FILE2_NAME), 'r').read()
                    assert result == join(tmp, 'localhost-blog-about.html')
                    assert expected == edited.read()
                    assert expected_img == img
                    assert expected_js == jsfile
                    assert expected_css == cssfile


def test3_error():
    with pytest.raises(Exception) as e:
        download('https://localhost/blog/about', 'dsfjsjsgj')
    assert str(e.value) == 'The specified directory does not exist. '\
                           'Please, specify an existing directory'


def test4_error():
    with pytest.raises(Exception) as e:
        with tempfile.TemporaryDirectory() as tmp:
            download('https://google.com/images/branding/googleeruadfj', tmp)
        assert str(e.value) == 'That’s an error. Status code: 404'