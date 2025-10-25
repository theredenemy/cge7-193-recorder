from config_defaults import *


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
  config_file.set("SOURCETV", "uptime_days", uptime_days_default)
  config_file.set("SOURCETV", "fastdl", fastdl_default)
  config_file.set("SOURCETV", "maps_dir", maps_dir_default)
  config_file.set("SOURCETV", "download_dir", download_dir_default)
  config_file.set("SOURCETV", "demofilesdirname", demofilesdirname_default)

  with open(r"SOURCETV.ini", 'w') as configfileObj:
     config_file.write(configfileObj)
     configfileObj.flush()
     configfileObj.close()

  print("Config file 'SOURCETV.ini' created")

if __name__ == "__main__":
   makeConfig()