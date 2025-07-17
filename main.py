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
pydirectinput.FAILSAFE = False
pyautogui.FAILSAFE = False
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
# Start of Script
gamedir = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Team Fortress 2\\tf"
logfilename = "datalogtf2.txt"
serverip = "79.127.217.197"
serverport = 22913
demosdirname = "demos"
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
                if listfindlib.findtext(conlist, "Disconnect") == True:
                    source_functions.chat("in-server")
                    if listfindlib.findtext(conlist, "in-server") == False:
                        pydirectinput.press("enter")
                        pydirectinput.press("enter")
                        source_functions.move_demos(gamedir, demosdirname)
                        inserver = 0
                        do_check = 1
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
                


