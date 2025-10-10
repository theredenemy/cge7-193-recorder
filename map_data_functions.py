import configparser
import os

def read_data(mapdatafile, map):
    config = configparser.ConfigParser()
    if os.path.isfile(mapdatafile) == False:
        return False
    config.read(mapdatafile)
    
    if not config.has_option(map, "last_updated"):
        return False
    if not config.has_option(map, "checksum"):
        return False
    last_updated = config[map]["last_updated"]
    checksum = config[map]["checksum"]
    data = []
    data.append(last_updated)
    data.append(checksum)
    return data

def set_data(mapdatafile, map, last_updated, checksum):
    config = configparser.ConfigParser()
    if os.path.isfile(mapdatafile) == False:
        return False
    config.read(mapdatafile)
    if not config.has_section(map):
        config.add_section(map)
    config.set(map, "last_updated", last_updated)
    config.set(map, "checksum", checksum)
    return True