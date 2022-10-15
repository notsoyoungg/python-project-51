from page_loader.page_loader import download
from page_loader.cli import parse_args
from urllib3 import HTTPConnectionPool
from page_loader.logger import logger
import sys


def main():
    args = parse_args()
    try:
        result = download(args.page_link, args.output)
        print(result)
        sys.exit(0)
    except ConnectionRefusedError as e:
        logger.debug(f'дратути дратути дратути {e}')
        sys.exit(0)
    except Exception as e:
        logger.debug(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
