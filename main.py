from dataContract.infoParser import InfoParser
from dataContract.logLevel import LogLevel
from log import logging
import sys
import argparse


if __name__ == '__main__':

    logger = logging.getLogger()

    parser = argparse.ArgumentParser(description='Process Chaos creation.')
    parser.add_argument('--act', type=str, default='container', choices=['container', 'service'], help='Usage for act on container/service level, default=container')
    parser.add_argument('--log', type=str, default='debug', choices=['critical', 'error', 'warning', 'debug', 'info', 'notest' ], help='Usage for log level, default=debug')
    parser.add_argument('--min', type=int, default=30, help='Usage for min sec, should be > 30 sec')
    parser.add_argument('--max', type=int, default=50, help='Usage for max sec, should be > 50 sec')
    
    args = parser.parse_args()

    act = args.act
    log_level = args.log 
    min_sec = args.min 
    max_sec = args.max 

    level_name = log_level
    level = LogLevel.LEVELS.get(level_name, logging.DEBUG)
    logger.setLevel(level)


    infoParser = InfoParser()
    stack = infoParser.getStackInstance()
    #stack.printStack()
    #stack.getHostList()
    
    #stack.updateServicesState()
    #stack.printServiceState()

    #stack.updateHostState()
    #stack.printHostState()
    stack.createChaos(act, min_sec, max_sec)
