import configparser
import os

def read_data(mapdatafile, map, readdata):
    config = configparser.ConfigParser()
    if os.path.isfile(mapdatafile) == False:
        return False
    config.read(mapdatafile)
    if not config.has_section(map):
        return False
    if not config.has_option(map, readdata):
        return False
    data = config[map][readdata]
    return data

def set_data(mapdatafile, map, option, data):
    config = configparser.ConfigParser()
    if os.path.isfile(mapdatafile) == False:
        return False
    config.read(mapdatafile)
    if not config.has_section(map):
        config.add_section(map)
    config.set(map, option, data)
    with open(mapdatafile, 'w') as f:
        config.write(f)
    return True