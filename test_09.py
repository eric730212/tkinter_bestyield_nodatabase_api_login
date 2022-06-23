import configparser

conf = configparser.ConfigParser()

conf.read('config.ini')

print(conf['default']['a'])

conf['default'] = {'a': 20}

print(conf['default']['a'])
