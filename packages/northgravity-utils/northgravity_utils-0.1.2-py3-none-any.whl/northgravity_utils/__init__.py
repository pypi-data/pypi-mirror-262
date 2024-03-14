import logging
import sys

# Set logger with proper format for backend parsing to status page
from .constants import LOGGER_NAME

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.Logger(LOGGER_NAME)
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(logger_handler)


# Import the methods
from .BackTest import *
from .DataHandler import *
from .FileHandler import *
from .StatTests import *
from .TaskExecUtils import *
from .utils import *
