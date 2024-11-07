import logging

# Package-wide logger setup
logger = logging.getLogger('injectr')

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.ERROR)
