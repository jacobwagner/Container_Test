import logging
import sys

logging.basicConfig(filename='chaos.log', filemode='w', level=logging.INFO)

logger = logging.getLogger('chaos')
logger.setLevel(logging.INFO)
