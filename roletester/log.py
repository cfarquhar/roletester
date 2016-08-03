import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

logger = logging.getLogger('roletester')
logger.setLevel(logging.DEBUG)
