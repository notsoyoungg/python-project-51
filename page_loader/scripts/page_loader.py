from page_loader.page_loader import download
from page_loader.cli import parse_args
import sys


def main():
    args = parse_args()
    try:
        print(download(args.page_link, args.output))
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
