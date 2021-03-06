import logging

#logging levels
# CRITICAL 50
# ERROR    40
# WARNING  30
# INFO     20
# DEBUG    10
# NOTEST    0
# set basic log file name and default log level to INFO
logging.basicConfig(filename='chaos.log', filemode='w', level=logging.ERROR)

logger = logging.getLogger()

# create console handler and set default level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler 
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)
