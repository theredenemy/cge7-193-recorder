import configHelper
from config_defaults import *
from __main__ import configfile


def reload_config():
    import __main__
    __main__.gamedir = configHelper.read_config(configfile, "SOURCETV", "gamedir", gamedir_default)
    __main__.logfilename = configHelper.read_config(configfile, "SOURCETV", "logfilename", logfilename_default)
    __main__.serverip = configHelper.read_config(configfile, "SOURCETV", "serverip", serverip_default)
    __main__.serverport = configHelper.read_config(configfile, "SOURCETV", "serverport", serverport_default, True)
    __main__.demosdirname = configHelper.read_config(configfile, "SOURCETV", "demosdirname", demosdirname_default)
    __main__.appid = configHelper.read_config(configfile, "SOURCETV", "appid", appid_default)
    __main__.process_name = configHelper.read_config(configfile, "SOURCETV", "process_name", process_name_default)
    __main__.server_version = configHelper.read_config(configfile, "SOURCETV", "server_version", server_version_default)
    __main__.uptime_days = configHelper.read_config(configfile, "SOURCETV", "uptime_days", uptime_days_default, True)
    __main__.fastdl = configHelper.read_config(configfile, "SOURCETV", "fastdl", fastdl_default)
    __main__.maps_dir = configHelper.read_config(configfile, "SOURCETV", "maps_dir", maps_dir_default)
    __main__.maps_download_dir = configHelper.read_config(configfile, "SOURCETV", "maps_download_dir", maps_download_dir_default)
    __main__.mapdatafile = configHelper.read_config(configfile, "SOURCETV", "jsonfile", mapdatafile_default)