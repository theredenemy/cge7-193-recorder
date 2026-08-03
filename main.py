# cge7-193-recorder : main.py Copyright (C) 2025  TheRedEnemy
import pyautogui
import pydirectinput
import os
from cge_recorder import CGE_RECORDER
import configparser
import sys
from config_defaults import *
from makeConfig import makeConfig
pydirectinput.FAILSAFE = False
pyautogui.FAILSAFE = False
cge = CGE_RECORDER()
# Start of Script
if os.path.isfile("SOURCETV.ini") == False:
    makeConfig()

default_configfile = "SOURCETV.ini"
# # Init Vars
# gamedir = None
# logfilename = None
# serverip = None
# serverport = None
# demosdirname = None
# appid = None
# process_name = None
# server_version = None
# uptime_days = None
# fastdl = None
# maps_dir = None
# download_dir = None
# mapdatafile = None
# demofilesdirname = None
# gamelogs_dir = None
# join_sourcetv = None
# use_server_password = None
# password = None
# endloop1 = 0
# endloop2 = 0
# endloop3 = 0
# do_check = 0
# nextlinelook = 0
# nextline = 0
# mtime = 0
# connected_to_server = False
# joined_server = False
# game_disconnect = False
# host_disconnect = False
if __name__ == "__main__":
    cge.load_config(configfile=default_configfile)
    cge.main()


