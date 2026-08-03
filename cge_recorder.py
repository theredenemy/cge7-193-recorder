# cge7-193-recorder : cge_recorder.py Copyright (C) 2026  TheRedEnemy
import configparser

import configHelper
from config_defaults import *
import consolelogger
import fileinuse_functions
import listfindlib
import source_functions
import uptime_functions
import win32_functions
from source_functions import start_game


import a2s
import pydirectinput


import ctypes
import ipaddress
import os
import socket
import time
import traceback
import winsound
class CGE_RECORDER:

    def __init__(self):
        self.main_configfile = None
        self.gamedir = None
        self.logfilename = None
        self.serverip = None
        self.serverport = None
        self.demosdirname = None
        self.appid = None
        self.process_name = None
        self.server_version = None
        self.uptime_days = None
        self.fastdl = None
        self.maps_dir = None
        self.download_dir = None
        self.mapdatafile = None
        self.demofilesdirname = None
        self.gamelogs_dir = None
        self.join_sourcetv = None
        self.use_server_password = None
        self.password = None
        
    def check_vars(self):
        return {self.gamedir, self.logfilename, self.serverip, self.serverport, self.demosdirname, self.appid, self.process_name, self.server_version, self.uptime_days, self.fastdl, self.maps_dir, self.download_dir, self.mapdatafile, self.demosdirname, self.demofilesdirname, self.gamelogs_dir, self.join_sourcetv, self.use_server_password, self.password}

    def load_config(self, configfile):
            self.main_configfile = configfile
            self.gamedir = configHelper.read_config(configfile, "SOURCETV", "gamedir", gamedir_default)
            self.logfilename = configHelper.read_config(configfile, "SOURCETV", "logfilename", logfilename_default)
            self.serverip = configHelper.read_config(configfile, "SOURCETV", "serverip", serverip_default)
            self.serverport = configHelper.read_config(configfile, "SOURCETV", "serverport", serverport_default, True)
            self.demosdirname = configHelper.read_config(configfile, "SOURCETV", "demosdirname", demosdirname_default)
            self.appid = configHelper.read_config(configfile, "SOURCETV", "appid", appid_default)
            self.process_name = configHelper.read_config(configfile, "SOURCETV", "process_name", process_name_default)
            self.server_version = configHelper.read_config(configfile, "SOURCETV", "server_version", server_version_default)
            self.uptime_days = configHelper.read_config(configfile, "SOURCETV", "uptime_days", uptime_days_default, True)
            self.fastdl = configHelper.read_config(configfile, "SOURCETV", "fastdl", fastdl_default)
            self.maps_dir = configHelper.read_config(configfile, "SOURCETV", "maps_dir", maps_dir_default)
            self.download_dir = configHelper.read_config(configfile, "SOURCETV", "download_dir", download_dir_default)
            self.mapdatafile = configHelper.read_config(configfile, "SOURCETV", "mapdatafile", mapdatafile_default)
            self.demofilesdirname = configHelper.read_config(configfile, "SOURCETV", "demofilesdirname", demofilesdirname_default)
            self.gamelogs_dir = configHelper.read_config(configfile, "SOURCETV", "gamelogs_dir", default_value=gamelogs_dir_default)
            self.join_sourcetv = configHelper.read_config(configfile, "SOURCETV", "join_sourcetv", default_value=join_sourcetv_default, is_bool=True)
            self.use_server_password = configHelper.read_config(configfile, "SOURCETV", "use_server_password", default_value=use_server_password_default, is_bool=True)
            self.password = configHelper.read_config(configfile, "SOURCETV", "password", default_value=password_default)
    def main(self):
        config = configparser.ConfigParser()
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
        print(self.check_vars())
        if None in self.check_vars():
            return
        try:
            if ipaddress.ip_address(self.serverip):
                ip = self.serverip
        except ValueError:
            try:
                ip = socket.gethostbyname(self.serverip)
            except socket.gaierror:
                ip = self.serverip
        winsound.Beep(frequency=590, duration=500)
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        print("Hello")
        print("Getting Server Version")
        if self.server_version == "None":
            print(f"Fetching Server Version From Server: {ip}:{self.serverport}")
            endloop4 = 0
            while (endloop4 < 1):
                try:
                    address = self.serverip, self.serverport
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
                    self.server_version = info.version
                    configHelper.set_config(self.main_configfile, "SOURCETV", "self.server_version", self.server_version)
                    print("Done")
                    endloop4 = 1
                    info = False
        os.system(f"taskkill /f /im {self.process_name}")
        info = False
        time.sleep(3)
        logfile = f"{self.gamedir}\\{self.logfilename}"
        while(fileinuse_functions.is_file_in_use(logfile) == True):
            pass
        consolelogger.logstart(self.gamedir, self.logfilename, self.gamelogs_dir)
        lastmodtime = os.path.getmtime(logfile)
        time.sleep(3)
        source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
        time.sleep(3)
        source_functions.check_for_map_updates(self.gamedir, os.path.join(self.gamedir, self.download_dir, self.maps_dir), self.fastdl, self.mapdatafile)
        time.sleep(3)
        start_game(self.gamedir, self.logfilename, self.appid, self.process_name, self.gamelogs_dir)
        lastmodtime = os.path.getmtime(logfile)
        conlist = consolelogger.consolelog(self.gamedir, self.logfilename)
        nextline = conlist[-1]
        while True:
            time.sleep(4.5)
            connected_to_server = False
            joined_server = False
            game_disconnect = False
            if not self.uptime_days == 0:
                if uptime_functions.get_uptime_days() >= self.uptime_days:
                    source_functions.set_focus(self.process_name)
                    source_functions.run_cmd("quit", self.process_name)
                    time.sleep(3)
                    source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
                    time.sleep(2)
                    print("REBOOT")
                    if win32_functions.reboot() == True:
                        exit()
                    else:
                        os.system("shutdown -r -f -t 2")
                        exit()



            try:
                address = self.serverip, self.serverport
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
                    source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                    do_check = 0
                else:
                    do_check = 0

            if not info == False:
                #print("server up")
                if not info.version == self.server_version:
                    print("RESET GAME")
                    self.server_version = info.version
                    configHelper.set_config(self.main_configfile, "SOURCETV", "self.server_version", self.server_version)
                    # RESET GAME AND LOGS BREAK
                    source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                    inserver = 0
                    continue



                if info.player_count >= info.max_players:
                    print("Server is full")
                    inserver = 0
                    continue
                else:
                    source_functions.set_focus(self.process_name)
                    server_join = source_functions.connect_to_server(process_name=self.process_name, server_ip=self.serverip, server_port=self.serverport, source_tv=self.join_sourcetv, use_server_password=self.use_server_password, password=self.password)
                    if server_join == True:
                        # Bug Fix
                        print("Connecting to Server")
                        for i in range(20):
                            conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                            if "The server you are trying to connect to is running" in conlist:
                                joined_server = False
                                game_disconnect = True
                                break
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
                    source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                    inserver = 0
                    connected_to_server = False
                    joined_server = False
                    continue
                if server_join == True:
                    print("Joining Server")
                    for i in range(60):
                        print(f"{i}:", end='\r')
                        conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                        if listfindlib.findtext(conlist, "Disconnect") == True:
                            joined_server = False
                            game_disconnect = True
                            break
                        if "Client reached server_spawn" in conlist:
                            print("\nJoined Server")
                            winsound.Beep(600, 500)
                            joined_server = True
                            break
                        else:
                            joined_server = False
                            time.sleep(5)
                if game_disconnect == True:
                    print("Disconnect")
                    pydirectinput.press("enter")
                    source_functions.set_focus(self.process_name)
                    time.sleep(1)
                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                    pydirectinput.press("enter")
                    pydirectinput.press("enter")
                    inserver = 0
                    do_check = 1
                    nextline = conlist[-1]
                    continue
                if joined_server == False:
                    print("Cannot join Server. RESET GAME")
                    # RESET GAME AND LOGS BREAK
                    source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                    inserver = 0
                    connected_to_server = False
                    joined_server = False
                    continue

                source_functions.set_focus(self.process_name)


                while (inserver >= 1):
                    if not win32_functions.get_pid(self.process_name):
                        print("GAME IS NOT OPEN")
                        time.sleep(10)
                        print("GAME CRASH")
                        print("RESET GAME")
                        source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                        inserver = 0
                        break
                    try:
                        if ctypes.windll.user32.IsHungAppWindow(win32_functions.GetHwndsFromPID(win32_functions.get_pid(self.process_name))[0]):
                            print("Game Not Responding")
                            for i in range(100):
                                if ctypes.windll.user32.IsHungAppWindow(win32_functions.GetHwndsFromPID(win32_functions.get_pid(self.process_name))[0]):
                                    hung = True
                                    print("Game Not Responding")
                                    time.sleep(3)
                                else:
                                    hung = False
                                    break
                            if hung:
                                print("GAME CRASH")
                                print("RESET GAME")
                                source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                                inserver = 0
                                break
                    except IndexError:
                        print("GAME CRASH")
                        print("RESET GAME")
                        source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                        inserver = 0
                        break

                    if not self.process_name == win32_functions.GetForegroundWindowProcessName():
                        time.sleep(5)
                        win32_functions.set_focus_win32(self.process_name)
                    if not nextline == nextlinelook:
                        print(nextline, end='\r')
                        nextlinelook = nextline
                    mtime = os.path.getmtime(logfile)
                    if not lastmodtime == mtime:
                        lastmodtime = mtime
                        time.sleep(3)
                        for i in range(5):
                            time.sleep(1)
                            conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                            if "Connection failed after 4 retries" in conlist:
                                print("\nDisconnect")
                                print("FUCK")
                                time.sleep(5)
                                source_functions.set_focus(self.process_name)
                                pydirectinput.press("enter")
                                time.sleep(1)
                                source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                pydirectinput.press("enter")
                                pydirectinput.press("enter")
                                inserver = 0
                                do_check = 1
                                break
                            if "Server is full" in conlist:
                                print("\nDisconnect")
                                print("Server is full")
                                time.sleep(3)
                                source_functions.set_focus(self.process_name)
                                pydirectinput.press("enter")
                                time.sleep(1)
                                source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                pydirectinput.press("enter")
                                pydirectinput.press("enter")
                                inserver = 0
                                do_check = 1
                                break
                            if "The server you are trying to connect to is running" in conlist:
                                time.sleep(2)
                                source_functions.run_cmd("echo in-server")
                                conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                                if "in-server" in conlist:
                                    nextline = conlist[-1]
                                    source_functions.run_cmd("status")
                                    conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                                    nextline = conlist[-1]
                                    if listfindlib.findword(conlist, "hostname") == True:
                                        host_disconnect = False
                                    elif listfindlib.findword(conlist, "SourceTV") == True:
                                        host_disconnect = False
                                    else:
                                        host_disconnect = True
                                else:
                                    host_disconnect = True
                                conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                                if host_disconnect == True:
                                    print("\nDisconnect")
                                    if host_disconnect == True:
                                        host_disconnect = False
                                    source_functions.set_focus(self.process_name)
                                    time.sleep(2)
                                    pydirectinput.press("enter")
                                    pydirectinput.press("enter")
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    source_functions.run_cmd("disconnect", self.process_name)
                                    source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
                                    inserver = 0
                                    print("RESET GAME")
                                    print(f"Fetching Server Version From Server: {self.serverip}:{self.serverport}")
                                    endloop4 = 0
                                    while (endloop4 < 1):
                                        try:
                                            address = self.serverip, self.serverport
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
                                            self.server_version = info.version
                                            configHelper.set_config(self.main_configfile, "SOURCETV", "self.server_version", self.server_version)
                                            print("Done")
                                            endloop4 = 1
                                            info = False
                                    source_functions.reset_game(self.gamedir, self.logfilename, self.appid, self.process_name, logfile, self.gamelogs_dir)
                                    inserver = 0
                                    break
                                else:
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    pydirectinput.press('esc')
                                    break


                            if listfindlib.findtext(conlist, "Disconnect") == True:
                                time.sleep(5)
                                source_functions.run_cmd("echo in-server", self.process_name)
                                conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                                if "in-server" in conlist:
                                    nextline = conlist[-1]
                                    source_functions.run_cmd("status", self.process_name)
                                    conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
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
                                    source_functions.set_focus(self.process_name)
                                    time.sleep(2)
                                    pydirectinput.press("enter")
                                    pydirectinput.press("enter")
                                    # This is a Fix for an Endless Loop What the fuck
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    source_functions.run_cmd("disconnect", self.process_name)
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
                                    inserver = 0
                                    do_check = 1
                                    break
                                else:
                                    # what
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    pydirectinput.press('esc')
                                    break
                            if "Server connection timed out" in conlist:
                                print("\nDisconnect")
                                print("FUCK")
                                source_functions.set_focus(self.process_name)
                                time.sleep(3)
                                pydirectinput.press("enter")
                                pydirectinput.press("enter")
                                source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                source_functions.run_cmd("disconnect")
                                source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
                                inserver = 0
                                do_check = 1
                                break
                            if "Host_Error: Map is missing" in conlist:
                                time.sleep(3)
                                source_functions.run_cmd("echo in-server", self.process_name)
                                conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                                if "in-server" in conlist:
                                    nextline = conlist[-1]
                                    source_functions.run_cmd("status", self.process_name)
                                    conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
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
                                    source_functions.set_focus(self.process_name)
                                    time.sleep(3)
                                    pydirectinput.press("enter")
                                    pydirectinput.press("enter")
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4", self.process_name)
                                    source_functions.run_cmd("disconnect", self.process_name)
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
                                    inserver = 0
                                    do_check = 1
                                    break
                                else:
                                    # what
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4", self.process_name)
                                    pydirectinput.press('esc')
                                    break
                            if "Host_Error: Client's map differs from the server's" in conlist:
                                time.sleep(3)
                                source_functions.run_cmd("echo in-server", self.process_name)
                                conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                                if "in-server" in conlist:
                                    nextline = conlist[-1]
                                    source_functions.run_cmd("status", self.process_name)
                                    conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
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
                                    source_functions.set_focus(self.process_name)
                                    time.sleep(3)
                                    pydirectinput.press("enter")
                                    pydirectinput.press("enter")
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4", self.process_name)
                                    source_functions.run_cmd("disconnect", self.process_name)
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
                                    inserver = 0
                                    do_check = 1
                                    break
                                else:
                                    # what
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4", self.process_name)
                                    pydirectinput.press('esc')
                                    break


                            if listfindlib.findtext(conlist, "hello") == True:
                                source_functions.chat("hi BREAK")
                                # FUCK
                                source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6; echo BREAK", self.process_name)
                                time.sleep(1)
                                nextline = conlist[-1]
                                source_functions.run_cmd("status", self.process_name)
                                conlist = consolelogger.consolelog(self.gamedir, self.logfilename, nextline-3)
                                nextline = conlist[-1]
                                if listfindlib.findword(conlist, "hostname") == True:
                                    host_disconnect = False
                                elif listfindlib.findword(conlist, "SourceTV") == True:
                                    host_disconnect = False
                                else:
                                    host_disconnect = True
                                if host_disconnect == True:
                                    print("\nDisconnect")
                                    if host_disconnect == True:
                                        host_disconnect = False
                                    print("FUCK")
                                    source_functions.set_focus(self.process_name)
                                    time.sleep(3)
                                    pydirectinput.press("enter")
                                    pydirectinput.press("enter")
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4", self.process_name)
                                    source_functions.run_cmd("disconnect", self.process_name)
                                    source_functions.run_cmd("echo 1; echo 2; echo 3; echo 4; echo 5; echo 6", self.process_name)
                                    source_functions.move_demos(self.gamedir, self.demosdirname, demofilesdirname=self.demofilesdirname)
                                    inserver = 0
                                    do_check = 1
                                    break
                                pydirectinput.press("esc")
                                # How The Fuck Did i forget this
                                break


                            print(f"{conlist[-1]} : {i}", end='\r')
                        nextline = conlist[-1]


    