import json
import yaml
from os.path import abspath


def parse(content, format):
    if format == 'json':
        return json.load(content)
    if format in ('yaml', 'yml'):
        return yaml.safe_load(content)
    raise Exception(f"Unrecognized format: {format}")


def get_content(filepath):
    with open(abspath(filepath)) as content:
        extension = filepath.split('.')[-1]
        return parse(content, extension)
