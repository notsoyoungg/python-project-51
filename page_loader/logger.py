import logging
from logging import StreamHandler, Formatter
import sys


logger = logging.getLogger('logger')
handler = StreamHandler(stream=sys.stderr)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
