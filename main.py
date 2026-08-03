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

if __name__ == "__main__":
    cge.load_config(configfile=default_configfile)
    cge.main()


