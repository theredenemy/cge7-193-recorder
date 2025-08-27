# cge7-193-recorder : source_functions.py Copyright (C) 2025  TheRedEnemy
import consolelogger
import processchecklib
import os
import time

def run_cmd(cmd):
    import os
    import pydirectinput
    import pyautogui
    import time
    pydirectinput.FAILSAFE = False
    pyautogui.FAILSAFE = False
    time.sleep(3)
    pydirectinput.press('F7')
    time.sleep(1)
    pyautogui.write(cmd)
    time.sleep(1)
    pydirectinput.press('enter')
    pydirectinput.press('F6')

def chat(msg):
    import os
    import pydirectinput
    import pyautogui
    import time
    pydirectinput.FAILSAFE = False
    pyautogui.FAILSAFE = False
    time.sleep(3)
    pydirectinput.press('y')
    time.sleep(1)
    pyautogui.write(msg)
    time.sleep(1)
    pydirectinput.press('enter')
    
def move_demos(gamedir, demosdirname):
    import os
    import time
    import shutil
    import pathlib
    maindir = os.getcwd()
    demofilesdirname = "demofiles"
    allowed_extensions = ['.dem', '.json']
    demosdir = os.path.join(gamedir, demosdirname)
    dircheck = os.listdir(demosdir)
    if len(dircheck) == 0:
        return False


    if os.path.isdir(demofilesdirname) == False:
        os.mkdir(demofilesdirname)
    if os.path.isdir(demosdir) == True:
        for filename in os.listdir(demosdir):
            filepath = f"{demosdir}\\{filename}"
            if os.path.isfile(filepath) == True:
                fileext = pathlib.Path(filepath).suffix
                if fileext in allowed_extensions:
                    file_time = os.path.getctime(filepath)
                    file_ti_c = time.ctime(file_time)
                    file_c = time.strptime(file_ti_c)
                    date = time.strftime("%Y-%m-%d", file_c)
                    hour = time.strftime("%H", file_c)
                    datedir = f"{demofilesdirname}\\{date}"
                    hourdir = f"{demofilesdirname}\\{date}\\hour-{hour}"
                    if os.path.isdir(datedir) == False:
                        os.mkdir(datedir)
                    if os.path.isdir(hourdir) == False:
                        os.mkdir(hourdir)
                    if os.path.isfile(f"{hourdir}\\{filename}") == True:
                        os.remove(f"{hourdir}\\{filename}")
                    shutil.move(filepath, f"{hourdir}\\" )
                    print(f"Moved {filename} to {hourdir}\\{filename} ")
                else:
                    print(f"skip {filename}")
    else:
        print("nope")
                    
def get_pid(process_name):
    import psutil
    pid = None
    
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']
            return pid

def set_focus(process_name):
    from pywinauto import Application
    pid = get_pid(process_name)
    app = Application().connect(process=pid)
    app.top_window().set_focus()


def start_game(gamedir, logfilename, appid, process_name):
    logfile = f"{gamedir}\\{logfilename}"
    consolelogger.logstart(gamedir, logfilename)
    lastmodtime = os.path.getmtime(logfile)
    endloop1 = 0
    endloop2 = 0
    os.system(f"taskkill /f /im {process_name}")
    time.sleep(3)
    print(f"Starting AppID: {appid}")
    os.system(f"start steam://rungameid/{appid}")
    print("wait")
    while (endloop1 < 1):
        if processchecklib.process_check(process_name) == True:
            endloop1 = 1
    while (endloop2 < 1):
        if not lastmodtime == os.path.getmtime(logfile):
            conlist = consolelogger.consolelog(gamedir, logfilename)
            nextline = conlist[-1]
            lastmodtime = os.path.getmtime(logfile)
            if "GAME START" in conlist:
                print('Game Has Started')
                time.sleep(3)
                endloop2 = 1
            conlist = consolelogger.consolelog(gamedir, logfilename, nextline)
            nextline = conlist[-1]
            lastmodtime = os.path.getmtime(logfile)

def connect_to_server(server_ip, server_port, source_tv=True):
    import socket
    import ipaddress
    import a2s
    import traceback
    try:
        if ipaddress.ip_address(server_ip):
            ip = server_ip
    except ValueError:
        try:
            ip = socket.gethostbyname(server_ip)
        except socket.gaierror:
            return False
    try:
        address = ip, server_port
        info = a2s.info(address)
    except Exception as e:
        if not type(e).__name__ == "TimeoutError":
            if type(e).__name__ == "ConnectionResetError":
                print("ConnectionReset")
                return False
            error = traceback.format_exc()
            print(error)
        return False
    if source_tv == True:
        port = info.stv_port
        if port == None:
            return False
    else:
        port = server_port
    print(f"join {ip}:{port}")
    run_cmd(f"connect {ip}:{port}")
    return True

def reset_game(gamedir, logfilename, appid, process_name, logfile):
    import fileinuse_functions
    import __main__
    # RESET GAME AND LOGS BREAK
    os.system(f"taskkill /f /im {process_name}")
    while(fileinuse_functions.is_file_in_use(logfile) == True):
        pass
    time.sleep(5)
    consolelogger.logstart(gamedir, logfilename)
    lastmodtime = os.path.getmtime(logfile)
    start_game(gamedir, logfilename, appid, process_name)
    set_focus(process_name)
    __main__.lastmodtime = os.path.getmtime(logfile)
    conlist = consolelogger.consolelog(gamedir, logfilename)
    __main__.nextline = conlist[-1]
    __main__.inserver = 0
    
    
        
        
      
    
    
    
    

                               
                
            