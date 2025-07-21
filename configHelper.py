import configparser

def read_config(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    return config