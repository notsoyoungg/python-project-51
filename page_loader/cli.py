import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='Downloads the page to the specified directory.'
    )
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', type=str, default=os.getcwd())
    return parser.parse_args()
