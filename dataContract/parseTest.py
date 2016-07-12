import yaml

file = '/root/Container_Test/dataContract/services.json'

with open(file) as data_file:
    data = yaml.safe_load(data_file)
    if data:
        for i in data.values():
            print i
