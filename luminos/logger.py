from logging import getLogger, StreamHandler, INFO
from colorlog import ColoredFormatter

# Create a logger instance
logger = getLogger(__name__)

# Define color styles for different log levels
log_colors = {
    'DEBUG': 'green',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}

# Setup ColoredFormatter with color styles
color_formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s: %(message)s",
    log_colors=log_colors
)

# Create a stream handler with color formatter
console = StreamHandler()
console.setFormatter(color_formatter)

# Add the handler to the logger
logger.addHandler(console)
logger.setLevel(INFO)
