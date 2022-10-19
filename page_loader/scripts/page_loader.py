from page_loader.page_loader import download
from page_loader.cli import parse_args
from urllib3 import HTTPConnectionPool
from page_loader.logger import logger
import sys


def main():
    args = parse_args()
    try:
        print(download(args.page_link, args.output))
        sys.exit(0)
    except ConnectionRefusedError as e:
        logger.debug(f'RefusedError RefusedError RefusedError {e}')
        sys.exit(0)
    except Exception as e:
        logger.debug(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
