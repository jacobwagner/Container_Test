from dataContract.infoParser import InfoParser
from dataContract.logLevel import LogLevel
from log import logging
import sys

if __name__ == '__main__':

    logger = logging.getLogger()

    # set log level(default DEBUG):
    # critical > error > warning > info > debug
    if len(sys.argv) > 1:
        level_name = sys.argv[1]
        level = LogLevel.LEVELS.get(level_name, logging.DEBUG)
        logger.setLevel(level)

    infoParser = InfoParser()
    stack = infoParser.getStackInstance()
    #stack.printStack()
    #stack.getHostList()
    
    #stack.updateServicesState()
    #stack.printServiceState()

    stack.updateHostState()
    stack.printHostState()
    #stack.createChaos()
