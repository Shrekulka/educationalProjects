import logging

from utils.config import Config

# Create a formatter for the log messages with a specific format
formatter = logging.Formatter('%(asctime)s |%(filename)s |%(lineno)04d-%(levelname)-5s| - | %(message)s |')

# Create a logger named 'hunter'
logger = logging.getLogger('hunter')

# Set the logging level for the logger to DEBUG
logger.setLevel(logging.DEBUG)

# Create a file handler for logging, specifying the log file path from the Config class
file_handler = logging.FileHandler(Config.LOG_FILE_PATH)

# Set the formatter for the file handler
file_handler.setFormatter(formatter)

# Create a stream handler for logging to the console
stream_handler = logging.StreamHandler()

# Set the formatter for the stream handler
stream_handler.setFormatter(formatter)

# Add the file handler and stream handler to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
