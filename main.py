from dataContract.infoParser import InfoParser
from dataContract.logLevel import LogLevel
from log import logging
import sys


if __name__ == '__main__':
    level = ["critical", "error", "warning", "info", "debug", "notest"]
    act = ["container", "service"]

    logger = logging.getLogger()

    # set log level(default DEBUG):
    # critical > error > warning > info > debug
    if len(sys.argv) != 3:
        print "Usage : python main.py [container | service] [loglevel]"
    else:
        if not sys.argv[1].lower() in act or not sys.argv[2].lower() in level:
            print "Usage : python main.py [container | service] [loglevel]"
        else:
            level_name = sys.argv[2]
            level = LogLevel.LEVELS.get(level_name, logging.DEBUG)
            logger.setLevel(level)

            act_name = sys.argv[1]

   

            infoParser = InfoParser()
            stack = infoParser.getStackInstance()
            #stack.printStack()
            #stack.getHostList()
            
            #stack.updateServicesState()
            #stack.printServiceState()

            #stack.updateHostState()
            #stack.printHostState()
            stack.createChaos(act_name)
