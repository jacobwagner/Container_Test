import yaml
import os


class ServicesParser(object):
    @staticmethod
    def getServiceDic():
        inventory = os.path.dirname(__file__) + '/services.json'
        serviceDic = {}

        try:
            with open(inventory) as data_file:
                data = yaml.safe_load(data_file)
                if data:
                    for key, value in data.iteritems():
                        tmpList = []
                        for service in value['services'].keys():
                            tmpList.append(service)
                        serviceDic[key] = tmpList
            return serviceDic
        except Exception as inst:
            print "getServiceDic Error"
            print type(inst)
            print inst.args
