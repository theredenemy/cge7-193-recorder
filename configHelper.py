import configparser
import os

def read_config(configfile, section, option, default_value, is_int=False):
    config = configparser.ConfigParser()
    if os.path.isfile(configfile) == False:
        config.add_section(section)
        config.set(section, option, str(default_value))
        with open(configfile, 'w') as f:
            config.write(f)
    config.read(configfile)
    if not config.has_section(section):
        config.add_section(section)
    if not config.has_option(section, option):
        config.set(section, option, str(default_value))
        with open(configfile, 'w') as f:
            config.write(f)
    # get value
    if is_int == True:
        value = config.getint(section, option)
    else:
        value = config[section][option]
    
    return value