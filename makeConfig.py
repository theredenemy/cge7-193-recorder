from config_defaults import (
    gamedir_default,
    logfilename_default,
    serverip_default,
    serverport_default,
    demosdirname_default,
    appid_default,
    process_name_default,
    server_version_default
)


import configparser


def makeConfig():
  import configparser
  config_file = configparser.ConfigParser()


  config_file.add_section("SOURCETV")

  config_file.set("SOURCETV", "gamedir", gamedir_default)
  config_file.set("SOURCETV", "logfilename", logfilename_default)
  config_file.set("SOURCETV", "serverip", serverip_default)
  config_file.set("SOURCETV", "serverport", serverport_default)
  config_file.set("SOURCETV", "demosdirname", demosdirname_default)
  config_file.set("SOURCETV", "appid", appid_default)
  config_file.set("SOURCETV", "process_name", process_name_default)
  config_file.set("SOURCETV", "server_version", server_version_default)

  with open(r"SOURCETV.ini", 'w') as configfileObj:
     config_file.write(configfileObj)
     configfileObj.flush()
     configfileObj.close()

  print("Config file 'SOURCETV.ini' created")