import yaml
import os
import inspect

from log import logging

class ServicesParser(object):
    @staticmethod
    def getServiceDic():
        inventory = os.path.dirname(__file__) + '/services.json'
        serviceDic = {}

        #parse the service json file and generate a dic which key is component, values is services name.
        try:
            with open(inventory) as data_file:
                data = yaml.safe_load(data_file)
                if data:
                    for key, value in data.iteritems():
                        tmpList = []
                        for service in value['services'].keys():
                            tmpList.append(service)
                        serviceDic[key] = tmpList
        except Exception as inst:
            logger.error(str(inspect.stack()[0][3]))
            logger.info('calling func : '+str(inspect.stack()[1][3]) + '() from ' + str(inspect.stack()[1][1]))
            logger.error(type(inst))
            logger.error(inst.args)
        finally:
            return serviceDic
            
