import configparser
import os

def read_data(mapdatafile, map, readdata, is_int=False, is_float=False):
    config = configparser.ConfigParser()
    if os.path.isfile(mapdatafile) == False:
        return False
    config.read(mapdatafile)
    if not config.has_section(map):
        return False
    if not config.has_option(map, readdata):
        return False
    if is_int == True:
        data = config.getint(map, readdata)
    elif is_float == True:
        data = config.getfloat(map, readdata)
    else:
        data = config[map][readdata]
    return data

def set_data(mapdatafile, map, option, data):
    config = configparser.ConfigParser()
    if os.path.isfile(mapdatafile) == True:
        config.read(mapdatafile)
    if not config.has_section(map):
        config.add_section(map)
    config.set(map, option, str(data))
    with open(mapdatafile, 'w') as f:
        config.write(f)
    return True