import pyautogui
import pydirectinput
import os
import a2s
import processchecklib
import time
import multiprocessing
import consolelogger
import source_functions
import re
import listfindlib
import fileinuse_functions
import configparser
import configHelper
pydirectinput.FAILSAFE = False
pyautogui.FAILSAFE = False
gamedir_default = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Team Fortress 2\\tf"
logfilename_default = "datalogtf2.txt"
serverip_default = "79.127.217.197"
serverport_default = "22913"
demosdirname_default = "demos"
def start_tf2(gamedir, logfilename):
    logfile = f"{gamedir}\\{logfilename}"
    consolelogger.logstart(gamedir, logfilename)
    lastmodtime = os.path.getmtime(logfile)
    endloop1 = 0
    endloop2 = 0
    os.system("taskkill /f /im tf_win64.exe")
    time.sleep(3)
    os.system("start steam://rungameid/440")
    print("wait")
    while (endloop1 < 1):
        if processchecklib.process_check("tf_win64.exe") == True:
            endloop1 = 1
    while (endloop2 < 1):
        if not lastmodtime == os.path.getmtime(logfile):
            conlist = consolelogger.consolelog(gamedir, logfilename)
            nextline = conlist[-1]
            lastmodtime = os.path.getmtime(logfile)
            if "GAME START" in conlist:
                print('hi')
                time.sleep(3)
                endloop2 = 1
            conlist = consolelogger.consolelog(gamedir, logfilename, nextline)
            nextline = conlist[-1]
            lastmodtime = os.path.getmtime(logfile)
def makeConfig():
  import configparser
  config_file = configparser.ConfigParser()


  config_file.add_section("SOURCETV")

  config_file.set("SOURCETV", "gamedir", gamedir_default)
  config_file.set("SOURCETV", "logfilename", logfilename_default)
  config_file.set("SOURCETV", "serverip", serverip_default)
  config_file.set("SOURCETV", "serverport", serverport_default)
  config_file.set("SOURCETV", "demosdirname", demosdirname_default)

  with open(r"SOURCETV.ini", 'w') as configfileObj:
     config_file.write(configfileObj)
     configfileObj.flush()
     configfileObj.close()

  print("Config file 'SOURCETV.ini' created")
# Start of Script
if os.path.isfile("SOURCETV.ini") == False:
    makeConfig()
config = "SOURCETV.ini"
gamedir = configHelper.read_config(config, "SOURCETV", "gamedir", gamedir_default)
logfilename = configHelper.read_config(config, "SOURCETV", "logfilename", logfilename_default)
serverip = configHelper.read_config(config, "SOURCETV", "serverip", serverip_default)
serverport = configHelper.read_config(config, "SOURCETV", "serverport", serverport_default, True)
demosdirname = configHelper.read_config(config, "SOURCETV", "demosdirname", demosdirname_default)
endloop1 = 0
endloop2 = 0
endloop3 = 0
do_check = 0
os.system("taskkill /f /im tf_win64.exe")
time.sleep(3)
logfile = f"{gamedir}\\{logfilename}"
consolelogger.logstart(gamedir, logfilename)
lastmodtime = os.path.getmtime(logfile)
time.sleep(3)
source_functions.move_demos(gamedir, demosdirname)
time.sleep(3)
start_tf2(gamedir, logfilename)
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
            # RESET GAME AND LOGS BREAK
            os.system("taskkill /f /im tf_win64.exe")
            while(fileinuse_functions.is_file_in_use(logfile) == True):
                pass
            time.sleep(5)
            consolelogger.logstart(gamedir, logfilename)
            lastmodtime = os.path.getmtime(logfile)
            start_tf2(gamedir, logfilename)
            lastmodtime = os.path.getmtime(logfile)
            conlist = consolelogger.consolelog(gamedir, logfilename)
            nextline = conlist[-1]
            do_check = 0
        else:
            do_check = 0

    if not info == False:
        print("server up")
        if info.player_count >= info.max_players:
            print("Server is full")
            inserver = 0
        else:
            print(f"join {serverip}:{serverport}")
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
                    pydirectinput.press("enter")
                    pydirectinput.press("enter")
                    inserver = 0
                    do_check = 1
                if "Server is full" in conlist:
                    print("Server is full")
                    time.sleep(3)
                    pydirectinput.press("enter")
                    pydirectinput.press("enter")
                    inserver = 0
                    do_check = 1
                if "The server you are trying to connect to is running" in conlist:
                    time.sleep(2)
                    source_functions.run_cmd("echo in-server")
                    if listfindlib.findtext(conlist, "in-server") == False:
                        pydirectinput.press("enter")
                        pydirectinput.press("enter")
                        source_functions.move_demos(gamedir, demosdirname)
                        inserver = 0
                        # RESET GAME AND LOGS BREAK
                        os.system("taskkill /f /im tf_win64.exe")
                        while(fileinuse_functions.is_file_in_use(logfile) == True):
                            pass
                        time.sleep(5)
                        consolelogger.logstart(gamedir, logfilename)
                        lastmodtime = os.path.getmtime(logfile)
                        start_tf2(gamedir, logfilename)
                        lastmodtime = os.path.getmtime(logfile)
                        conlist = consolelogger.consolelog(gamedir, logfilename)
                        nextline = conlist[-1]
                        inserver = 0
                    
                    
                if listfindlib.findtext(conlist, "Disconnect") == True:
                    time.sleep(2)
                    source_functions.run_cmd("echo in-server")
                    if listfindlib.findtext(conlist, "in-server") == False:
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
                    time.sleep(3)
                    pydirectinput.press("enter")
                    pydirectinput.press("enter")
                    source_functions.move_demos(gamedir, demosdirname)
                    inserver = 0
                    do_check = 1
                if listfindlib.findtext(conlist, "hello") == True:
                    source_functions.chat("hello")
                


