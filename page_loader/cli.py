import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='Downloads the page to the specified directory.'
    )
    parser.add_argument('-o', '--output', type=str, default=os.getcwd())
    parser.add_argument('page_link', type=str)
    return parser.parse_args()
