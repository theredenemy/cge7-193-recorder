# cge7-193-recorder : main.py Copyright (C) 2025  TheRedEnemy
import ipaddress
import socket
import pyautogui
import pydirectinput
import os
import a2s
import time
import consolelogger
import source_functions
import listfindlib
import fileinuse_functions
import configparser
import traceback
import uptime_functions
import sys
import win32_functions
import configHelper
from config_defaults import *
from makeConfig import makeConfig
from source_functions import start_game
pydirectinput.FAILSAFE = False
pyautogui.FAILSAFE = False
config = configparser.ConfigParser()
# Start of Script
if os.path.isfile("SOURCETV.ini") == False:
    makeConfig()

configfile = "SOURCETV.ini"
gamedir = configHelper.read_config(configfile, "SOURCETV", "gamedir", gamedir_default)
logfilename = configHelper.read_config(configfile, "SOURCETV", "logfilename", logfilename_default)
serverip = configHelper.read_config(configfile, "SOURCETV", "serverip", serverip_default)
serverport = configHelper.read_config(configfile, "SOURCETV", "serverport", serverport_default, True)
demosdirname = configHelper.read_config(configfile, "SOURCETV", "demosdirname", demosdirname_default)
appid = configHelper.read_config(configfile, "SOURCETV", "appid", appid_default)
process_name = configHelper.read_config(configfile, "SOURCETV", "process_name", process_name_default)
server_version = configHelper.read_config(configfile, "SOURCETV", "server_version", server_version_default)
uptime_days = configHelper.read_config(configfile, "SOURCETV", "uptime_days", uptime_days_default, True)
fastdl = configHelper.read_config(configfile, "SOURCETV", "fastdl", fastdl_default)
maps_dir = configHelper.read_config(configfile, "SOURCETV", "maps_dir", maps_dir_default)
download_dir = configHelper.read_config(configfile, "SOURCETV", "download_dir", download_dir_default)
mapdatafile = configHelper.read_config(configfile, "SOURCETV", "mapdatafile", mapdatafile_default)
demofilesdirname = configHelper.read_config(configfile, "SOURCETV", "demofilesdirname", demofilesdirname_default)
endloop1 = 0
endloop2 = 0
endloop3 = 0
do_check = 0
nextlinelook = 0
nextline = 0
mtime = 0
connected_to_server = False
joined_server = False
game_disconnect = False
host_disconnect = False

try:
    if ipaddress.ip_address(serverip):
        ip = serverip
except ValueError:
    try:
        ip = socket.gethostbyname(serverip)
    except socket.gaierror:
        ip = serverip
print("Getting Server Version")
if server_version == "None":
    print(f"Fetching Server Version From Server: {ip}:{serverport}")
    endloop4 = 0
    while (endloop4 < 1):
        try:
            address = serverip, serverport
            info = a2s.info(address)
        except Exception as e:
            if not type(e).__name__ == "TimeoutError":
                if type(e).__name__ == "ConnectionResetError":
                    print("ConnectionReset")
                    continue
                error = traceback.format_exc()
                print(error)
            info = False
        if not info == False:
            server_version = info.version
            config.read(configfile)
            config.set("SOURCETV", "server_version", server_version)
            with open(configfile, 'w') as f:
                config.write(f)
            print("Done")
            endloop4 = 1
            info = False
os.system(f"taskkill /f /im {process_name}")
info = False
time.sleep(3)
logfile = f"{gamedir}\\{logfilename}"
while(fileinuse_functions.is_file_in_use(logfile) == True):
    pass
consolelogger.logstart(gamedir, logfilename)
lastmodtime = os.path.getmtime(logfile)
time.sleep(3)
source_functions.move_demos(gamedir, demosdirname, demofilesdirname=demofilesdirname)
time.sleep(3)
source_functions.check_for_map_updates(gamedir, os.path.join(gamedir, download_dir, maps_dir), fastdl, mapdatafile)
time.sleep(3)
start_game(gamedir, logfilename, appid, process_name)
lastmodtime = os.path.getmtime(logfile)
conlist = consolelogger.consolelog(gamedir, logfilename)
nextline = conlist[-1]
while (endloop3 < 1):
    time.sleep(4.5)
    connected_to_server = False
    joined_server = False
    game_disconnect = False
    if not uptime_days == 0:
        if uptime_functions.get_uptime_days() >= uptime_days:
            source_functions.set_focus(process_name)
            source_functions.run_cmd("quit")
            time.sleep(3)
            source_functions.move_demos(gamedir, demosdirname, demofilesdirname=demofilesdirname)
            time.sleep(2)
            print("REBOOT")
            if win32_functions.reboot() == True:
                exit()
            else:
                os.system("shutdown -r -f -t 2")
                exit()
            


    try:
        address = serverip, serverport
        info = a2s.info(address)
    except Exception as e:
        if not type(e).__name__ == "TimeoutError":
            if type(e).__name__ == "ConnectionResetError":
                print("ConnectionReset")
                continue
            error = traceback.format_exc()
            print(error)
        
        info = False
    if do_check == 1:
        maxlinescon = consolelogger.getmaxlines(logfile)
        if maxlinescon >= 5000:
            print("RESET GAME")
            source_functions.reset_game(gamedir, logfilename, appid, process_name, logfile)
            do_check = 0
        else:
            do_check = 0

    if not info == False:
        #print("server up")
        if not info.version == server_version:
            print("RESET GAME")
            server_version = info.version
            config.read(configfile)
            config.set("SOURCETV", "server_version", server_version)
            with open(configfile, 'w') as f:
                config.write(f)
            # RESET GAME AND LOGS BREAK
            source_functions.reset_game(gamedir, logfilename, appid, process_name, logfile)
            inserver = 0
            continue

            
            
        if info.player_count >= info.max_players:
            print("Server is full")
            inserver = 0
            continue
        else:
            source_functions.set_focus(process_name)
            server_join = source_functions.connect_to_server(server_ip=serverip, server_port=serverport, source_tv=True)
            if server_join == True:
                # Bug Fix
                print("Connecting to Server")
                for i in range(20):
                    conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                    if listfindlib.findword(conlist, "Connected") == True:
                        print("Connected To Server")
                        inserver = 1
                        connected_to_server = True
                        break
                    else:
                        connected_to_server = False
                        time.sleep(5)
            else:
                #print("server is down")
                inserver = 0
                continue
        if connected_to_server == False:
            print("Cannot connect to Server. RESET GAME")
            # RESET GAME AND LOGS BREAK
            source_functions.reset_game(gamedir, logfilename, appid, process_name, logfile)
            inserver = 0
            connected_to_server = False
            joined_server = False
            continue
        if server_join == True:
            print("Joining Server")
            for i in range(60):
                print(f"{i}:", end='\r')
                conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                if listfindlib.findtext(conlist, "Disconnect") == True:
                    joined_server = False
                    game_disconnect = True
                    break
                if "The server you are trying to connect to is running" in conlist:
                    joined_server = False
                    game_disconnect = True
                    break
                if "Client reached server_spawn" in conlist:
                    print("\nJoined Server")
                    joined_server = True
                    break
                else:
                    joined_server = False
                    time.sleep(5)
        if game_disconnect == True:
            print("Disconnect")
            pydirectinput.press("enter")
            source_functions.set_focus(process_name)
            time.sleep(1)
            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
            pydirectinput.press("enter")
            pydirectinput.press("enter")
            inserver = 0
            do_check = 1
            nextline = conlist[-1]
            continue
        if joined_server == False:
            print("Cannot join Server. RESET GAME")
            # RESET GAME AND LOGS BREAK
            source_functions.reset_game(gamedir, logfilename, appid, process_name, logfile)
            inserver = 0
            connected_to_server = False
            joined_server = False
            continue
           
        source_functions.set_focus(process_name)     
                
        
        while (inserver >= 1):
            if not nextline == nextlinelook:
                print(nextline, end='\r')
                nextlinelook = nextline
            mtime = os.path.getmtime(logfile)
            if not lastmodtime == mtime:
                lastmodtime = mtime
                time.sleep(3)
                for i in range(5):
                    time.sleep(1)
                    conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                    if "Connection failed after 4 retries" in conlist:
                        print("\nDisconnect")
                        print("FUCK")
                        time.sleep(5)
                        source_functions.set_focus(process_name)
                        pydirectinput.press("enter")
                        time.sleep(1)
                        source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
                        pydirectinput.press("enter")
                        pydirectinput.press("enter")
                        inserver = 0
                        do_check = 1
                        break
                    if "Server is full" in conlist:
                        print("\nDisconnect")
                        print("Server is full")
                        time.sleep(3)
                        source_functions.set_focus(process_name)
                        pydirectinput.press("enter")
                        time.sleep(1)
                        source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
                        pydirectinput.press("enter")
                        pydirectinput.press("enter")
                        inserver = 0
                        do_check = 1
                        break
                    if "The server you are trying to connect to is running" in conlist:
                        time.sleep(2)
                        source_functions.run_cmd("echo in-server")
                        conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                        if "in-server" in conlist:
                            nextline = conlist[-1]
                            source_functions.run_cmd("status")
                            conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                            nextline = conlist[-1]
                            if listfindlib.findword(conlist, "hostname") == True:
                                host_disconnect = False
                            elif listfindlib.findword(conlist, "SourceTV") == True:
                                host_disconnect = False
                            else:
                                host_disconnect = True
                        else:
                            host_disconnect = True
                        conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                        if host_disconnect == True:
                            print("\nDisconnect")
                            if host_disconnect == True:
                                host_disconnect = False
                            source_functions.set_focus(process_name)
                            time.sleep(2)
                            pydirectinput.press("enter")
                            pydirectinput.press("enter")
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
                            source_functions.run_cmd("disconnect")
                            source_functions.move_demos(gamedir, demosdirname, demofilesdirname=demofilesdirname)
                            inserver = 0
                            print("RESET GAME")
                            print(f"Fetching Server Version From Server: {serverip}:{serverport}")
                            endloop4 = 0
                            while (endloop4 < 1):
                                try:
                                    address = serverip, serverport
                                    info = a2s.info(address)
                                except Exception as e:
                                    if not type(e).__name__ == "TimeoutError":
                                        if type(e).__name__ == "ConnectionResetError":
                                            print("ConnectionReset")
                                            continue
                                        error = traceback.format_exc()
                                        print(error)
                                    info = False
                                if not info == False:
                                    server_version = info.version
                                    config.read(configfile)
                                    config.set("SOURCETV", "server_version", server_version)
                                    with open(configfile, 'w') as f:
                                        config.write(f)
                                    print("Done")
                                    endloop4 = 1
                                    info = False
                            source_functions.reset_game(gamedir, logfilename, appid, process_name, logfile)
                            inserver = 0
                            break
                        else:
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
                            pydirectinput.press('esc')
                            break
                    
                    
                    if listfindlib.findtext(conlist, "Disconnect") == True:
                        time.sleep(5)
                        source_functions.run_cmd("echo in-server")
                        conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                        if "in-server" in conlist:
                            nextline = conlist[-1]
                            source_functions.run_cmd("status")
                            conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                            nextline = conlist[-1]
                            if listfindlib.findword(conlist, "hostname") == True:
                                host_disconnect = False
                            elif listfindlib.findword(conlist, "SourceTV") == True:
                                host_disconnect = False
                            else:
                                host_disconnect = True
                        else:
                            host_disconnect = True
                                
                        if host_disconnect == True:
                            print("\nDisconnect")
                            if host_disconnect == True:
                                host_disconnect = False
                            source_functions.set_focus(process_name)
                            time.sleep(2)
                            pydirectinput.press("enter")
                            pydirectinput.press("enter")
                            # This is a Fix for an Endless Loop What the fuck
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
                            source_functions.run_cmd("disconnect")
                            source_functions.move_demos(gamedir, demosdirname, demofilesdirname=demofilesdirname)
                            inserver = 0
                            do_check = 1
                            break
                        else:
                            # what
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
                            pydirectinput.press('esc')
                            break
                    if "Server connection timed out" in conlist:
                        print("\nDisconnect")
                        print("FUCK")
                        source_functions.set_focus(process_name)
                        time.sleep(3)
                        pydirectinput.press("enter")
                        pydirectinput.press("enter")
                        source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6")
                        source_functions.run_cmd("disconnect")
                        source_functions.move_demos(gamedir, demosdirname, demofilesdirname=demofilesdirname)
                        inserver = 0
                        do_check = 1
                        break
                    if "Host_Error: Map is missing" in conlist:
                        time.sleep(3)
                        source_functions.run_cmd("echo in-server")
                        conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                        if "in-server" in conlist:
                            nextline = conlist[-1]
                            source_functions.run_cmd("status")
                            conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                            nextline = conlist[-1]
                            if listfindlib.findword(conlist, "hostname") == True:
                                host_disconnect = False
                            elif listfindlib.findword(conlist, "SourceTV") == True:
                                host_disconnect = False
                            else:
                                host_disconnect = True
                        else:
                            host_disconnect = True
                        if host_disconnect == True:
                            print("\nDisconnect")
                            if host_disconnect == True:
                                host_disconnect = False
                            print("FUCK")
                            source_functions.set_focus(process_name)
                            time.sleep(3)
                            pydirectinput.press("enter")
                            pydirectinput.press("enter")
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4")
                            source_functions.run_cmd("disconnect")
                            source_functions.move_demos(gamedir, demosdirname, demofilesdirname=demofilesdirname)
                            inserver = 0
                            do_check = 1
                            break
                        else:
                            # what
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4")
                            pydirectinput.press('esc')
                            break
                    if "Host_Error: Client's map differs from the server's" in conlist:
                        time.sleep(3)
                        source_functions.run_cmd("echo in-server")
                        conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                        if "in-server" in conlist:
                            nextline = conlist[-1]
                            source_functions.run_cmd("status")
                            conlist = consolelogger.consolelog(gamedir, logfilename, nextline-3)
                            nextline = conlist[-1]
                            if listfindlib.findword(conlist, "hostname") == True:
                                host_disconnect = False
                            elif listfindlib.findword(conlist, "SourceTV") == True:
                                host_disconnect = False
                            else:
                                host_disconnect = True
                        else:
                            host_disconnect = True
                        if host_disconnect == True:
                            print("\nDisconnect")
                            if host_disconnect == True:
                                host_disconnect = False
                            print("FUCK")
                            source_functions.set_focus(process_name)
                            time.sleep(3)
                            pydirectinput.press("enter")
                            pydirectinput.press("enter")
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4")
                            source_functions.run_cmd("disconnect")
                            source_functions.move_demos(gamedir, demosdirname, demofilesdirname=demofilesdirname)
                            inserver = 0
                            do_check = 1
                            break
                        else:
                            # what
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4")
                            pydirectinput.press('esc')
                            break        
                        
                        
                    if listfindlib.findtext(conlist, "hello") == True:
                        source_functions.chat("hi BREAK")
                        # FUCK
                        for i in range(2):
                            source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6; echo BREAK")
                        time.sleep(1)
                        pydirectinput.press("esc")
                        # How The Fuck Did i forget this
                        break
                        
                    
                    print(f"{conlist[-1]} : {i}", end='\r')
                nextline = conlist[-1]
                


