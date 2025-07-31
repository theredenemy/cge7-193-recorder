import pyautogui
import pydirectinput
import os
import a2s
import time
import consolelogger
import source_functions
import listfindlib
import fileinuse_functions
import configHelper
from makeConfig import makeConfig
from config_defaults import (
    gamedir_default,
    logfilename_default,
    serverip_default,
    serverport_default,
    demosdirname_default,
    appid_default,
    process_name_default
)
from source_functions import start_game
pydirectinput.FAILSAFE = False
pyautogui.FAILSAFE = False
# Start of Script
if os.path.isfile("SOURCETV.ini") == False:
    makeConfig()
config = "SOURCETV.ini"
gamedir = configHelper.read_config(config, "SOURCETV", "gamedir", gamedir_default)
logfilename = configHelper.read_config(config, "SOURCETV", "logfilename", logfilename_default)
serverip = configHelper.read_config(config, "SOURCETV", "serverip", serverip_default)
serverport = configHelper.read_config(config, "SOURCETV", "serverport", serverport_default, True)
demosdirname = configHelper.read_config(config, "SOURCETV", "demosdirname", demosdirname_default)
appid = configHelper.read_config(config, "SOURCETV", "appid", appid_default)
process_name = configHelper.read_config(config, "SOURCETV", "process_name", process_name_default)
endloop1 = 0
endloop2 = 0
endloop3 = 0
do_check = 0
print("Getting Server Version")
endloop4 = 0
while (endloop4 < 1):
    try:
        address = serverip, serverport
        infover = a2s.info(address)
    except TimeoutError:
        info = False
    if not infover == False:
        server_version = infover.version
        print("Done")
        endloop4 = 1
os.system(f"taskkill /f /im {process_name}")
time.sleep(3)
logfile = f"{gamedir}\\{logfilename}"
consolelogger.logstart(gamedir, logfilename)
lastmodtime = os.path.getmtime(logfile)
time.sleep(3)
source_functions.move_demos(gamedir, demosdirname)
time.sleep(3)
start_game(gamedir, logfilename, appid, process_name)
lastmodtime = os.path.getmtime(logfile)
conlist = consolelogger.consolelog(gamedir, logfilename)
nextline = conlist[-1]
while (endloop3 < 1):
    time.sleep(3)
    try:
        address = serverip, serverport
        info = a2s.info(address)
    except TimeoutError:
        info = False
    if do_check == 1:
        maxlinescon = consolelogger.getmaxlines(logfile)
        if maxlinescon >= 5000:
            print("RESET GAME")
            # RESET GAME AND LOGS BREAK
            os.system(f"taskkill /f /im {process_name}")
            while(fileinuse_functions.is_file_in_use(logfile) == True):
                pass
            time.sleep(5)
            consolelogger.logstart(gamedir, logfilename)
            lastmodtime = os.path.getmtime(logfile)
            start_game(gamedir, logfilename, appid, process_name)
            source_functions.set_focus(process_name)
            lastmodtime = os.path.getmtime(logfile)
            conlist = consolelogger.consolelog(gamedir, logfilename)
            nextline = conlist[-1]
            do_check = 0
        else:
            do_check = 0

    if not info == False:
        print("server up")
        if not info.version == server_version:
            print("RESET GAME")
            server_version = info.version
            # RESET GAME AND LOGS BREAK
            os.system(f"taskkill /f /im {process_name}")
            while(fileinuse_functions.is_file_in_use(logfile) == True):
                pass
            time.sleep(5)
            consolelogger.logstart(gamedir, logfilename)
            lastmodtime = os.path.getmtime(logfile)
            start_game(gamedir, logfilename, appid, process_name)
            source_functions.set_focus(process_name)
            lastmodtime = os.path.getmtime(logfile)
            conlist = consolelogger.consolelog(gamedir, logfilename)
            nextline = conlist[-1]
            inserver = 0
            
        if info.player_count >= info.max_players:
            print("Server is full")
            inserver = 0
        else:
            print(f"join {serverip}:{serverport}")
            source_functions.set_focus(process_name)
            source_functions.run_cmd(f"connect {serverip}:{serverport}")
            inserver = 1
        while (inserver >= 1):
            if not lastmodtime == os.path.getmtime(logfile):
                conlist = consolelogger.consolelog(gamedir, logfilename, nextline)
                nextline = conlist[-1]
                lastmodtime = os.path.getmtime(logfile)
                if "Connection failed after 4 retries" in conlist:
                    print("FUCK")
                    time.sleep(3)
                    source_functions.set_focus(process_name)
                    pydirectinput.press("enter")
                    pydirectinput.press("enter")
                    inserver = 0
                    do_check = 1
                if "Server is full" in conlist:
                    print("Server is full")
                    time.sleep(3)
                    source_functions.set_focus(process_name)
                    pydirectinput.press("enter")
                    pydirectinput.press("enter")
                    inserver = 0
                    do_check = 1
                if "The server you are trying to connect to is running" in conlist:
                    time.sleep(2)
                    source_functions.run_cmd("echo in-server")
                    if listfindlib.findtext(conlist, "in-server") == False:
                        source_functions.set_focus(process_name)
                        time.sleep(2)
                        pydirectinput.press("enter")
                        pydirectinput.press("enter")
                        source_functions.move_demos(gamedir, demosdirname)
                        inserver = 0
                        print("RESET GAME")
                        server_version = info.version
                        # RESET GAME AND LOGS BREAK
                        os.system(f"taskkill /f /im {process_name}")
                        while(fileinuse_functions.is_file_in_use(logfile) == True):
                            pass
                        time.sleep(5)
                        consolelogger.logstart(gamedir, logfilename)
                        lastmodtime = os.path.getmtime(logfile)
                        start_game(gamedir, logfilename, appid, process_name)
                        source_functions.set_focus(process_name)
                        lastmodtime = os.path.getmtime(logfile)
                        conlist = consolelogger.consolelog(gamedir, logfilename)
                        nextline = conlist[-1]
                        inserver = 0
                    
                    
                if listfindlib.findtext(conlist, "Disconnect") == True:
                    time.sleep(2)
                    source_functions.run_cmd("echo in-server")
                    if listfindlib.findtext(conlist, "in-server") == False:
                        source_functions.set_focus(process_name)
                        time.sleep(2)
                        pydirectinput.press("enter")
                        pydirectinput.press("enter")
                        source_functions.move_demos(gamedir, demosdirname)
                        inserver = 0
                        do_check = 1
                    else:
                        # what
                        pydirectinput.press('esc')
                if "Server connection timed out" in conlist:
                    print("FUCK")
                    source_functions.set_focus(process_name)
                    time.sleep(3)
                    pydirectinput.press("enter")
                    pydirectinput.press("enter")
                    source_functions.move_demos(gamedir, demosdirname)
                    inserver = 0
                    do_check = 1
                if listfindlib.findtext(conlist, "hello") == True:
                    source_functions.chat("hello")
                


