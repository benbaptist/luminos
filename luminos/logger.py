import logging
import os

LOG_DIRECTORY = os.path.expanduser('~/.config/luminos/logs')
LOG_FILE = os.path.join(LOG_DIRECTORY, 'luminos.log')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)
