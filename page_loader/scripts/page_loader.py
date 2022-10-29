from page_loader.page_loader import download
from page_loader.cli import parse_args
import sys
import logging


logging.basicConfig(format='[%(asctime)s: %(levelname)s] %(message)s',
                    level=logging.DEBUG,
                    force=True,
                    stream=sys.stderr)


def main():
    args = parse_args()
    try:
        print(download(args.page_link, args.output))
    except Exception as e:
        logging.debug(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
