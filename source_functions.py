# cge7-193-recorder : source_functions.py Copyright (C) 2025  TheRedEnemy
import consolelogger
import processchecklib
import os
import time
import hashlib
import dateutil
def download_file(url, filename):
    import requests
    file_data = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(file_data.content)
    return filename

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
    print("\nMoving Demos")
    maindir = os.getcwd()
    demosint = 0
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
                if fileext == ".dem":
                    demosint += 1
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
    print(f"Done Moving Demos: {demosint} New Demos")
    
                    
def get_pid(process_name):
    import psutil
    pid = None
    
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']
            return pid

def set_focus(process_name):
    from pywinauto import Application
    import time
    pid = get_pid(process_name)
    endloop = 0
    while (endloop <= 0):
        try:
            app = Application().connect(process=pid)
            app.top_window().set_focus()
            endloop = 1
        except RuntimeError:
            print("Game Not Responding")
            time.sleep(3)


def start_game(gamedir, logfilename, appid, process_name):
    import fileinuse_functions
    logfile = f"{gamedir}\\{logfilename}"
    os.system(f"taskkill /f /im {process_name}")
    while(fileinuse_functions.is_file_in_use(logfile) == True):
        pass
    consolelogger.logstart(gamedir, logfilename)
    lastmodtime = os.path.getmtime(logfile)
    endloop1 = 0
    endloop2 = 0
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
                set_focus(process_name)
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
    run_cmd(f"echo 1; echo 2; echo 3; echo 4; connect {ip}:{port}")
    time.sleep(5)
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
    check_for_map_updates(__main__.gamedir, os.path.join(__main__.gamedir, __main__.download_dir, __main__.maps_dir), __main__.fastdl, __main__.mapdatafile)
    lastmodtime = os.path.getmtime(logfile)
    start_game(gamedir, logfilename, appid, process_name)
    set_focus(process_name)
    __main__.lastmodtime = os.path.getmtime(logfile)
    conlist = consolelogger.consolelog(gamedir, logfilename)
    __main__.nextline = conlist[-1]
    __main__.inserver = 0
def move_file(filepath, dir):
    import shutil
    file_time = os.path.getctime(filepath)
    file_ti_c = time.ctime(file_time)
    file_c = time.strptime(file_ti_c)
    date = time.strftime("%Y-%m-%d", file_c)
    hour = time.strftime("%H", file_c)
    datedir = f"{dir}\\{date}"
    hourdir = f"{dir}\\{date}\\hour-{hour}"
    filename = os.path.basename(filepath)
    if os.path.isdir(datedir) == False:
        os.mkdir(datedir)
    if os.path.isdir(hourdir) == False:
            os.mkdir(hourdir)
    if os.path.isfile(f"{hourdir}\\{filename}") == True:
        number = 0
        while True:
            if os.path.isdir(number) == False:
                break
            else:
                number = number + 1
        os.mkdir(number)
        shutil.move(f"{hourdir}\\{filename}", f"{hourdir}\\{number}\\" )
        print(f"Moved {filename} to {hourdir}\\{number}\\{filename} ")
    else:
        shutil.move(filepath, f"{hourdir}\\" )
        print(f"Moved {filename} to {hourdir}\\{filename} ")
def check_for_map_updates(gamedir, maps_dir, fastdl, mapdatafile):
    import pathlib
    import requests
    import map_data_functions
    import shutil
    import traceback
    cgemaps_dir = "cgemaps"
    tempdir = f"{cgemaps_dir}\\temp"
    if os.path.isdir(cgemaps_dir) == False:
        os.mkdir(cgemaps_dir)
    if fastdl == "False":
        return False
    allowed_extensions = ['.bsp', '.nav']
    if os.path.isdir(maps_dir) == False:
        return False
    mapsdir1 = os.path.join(gamedir, maps_dir)
    dircheck = os.listdir(mapsdir1)
    if len(dircheck) == 0:
        return False
    try:
        for filename in os.listdir(mapsdir1):
            print(filename)
            filepath = f"{mapsdir1}\\{filename}"
            fileext = pathlib.Path(filepath).suffix
            map = pathlib.Path(filepath).stem
        
            if fileext in allowed_extensions:
                #time.sleep(0.1)
                url = f"{fastdl}/maps/{filename}"
                header = requests.head(url)
                if header.status_code == 200:
                    date_string = header.headers.get('Last-Modified')
                    dt = dateutil.parser.parse(date_string)
                    unix_time = dt.timestamp()
                    last_updated = map_data_functions.read_data(mapdatafile, map, "last_updated", is_float=True)
                    checksum = map_data_functions.read_data(mapdatafile, map, "checksum")
                    if last_updated == False or checksum == False:
                        if os.path.isdir(tempdir) == True:
                            shutil.rmtree(tempdir)
                        os.mkdir(tempdir)
                        map_download_temp = f"{tempdir}\\{map}_download{fileext}"
                        download_file(url, map_download_temp)
                        basename = os.path.basename(map_download_temp)
                        map_download_md5 = hashlib.md5(open(map_download_temp, 'rb').read()).hexdigest()
                        map_md5 = hashlib.md5(open(filepath, 'rb').read()).hexdigest()
                        if not map_md5 == map_download_md5:
                            map_data_functions.set_data(mapdatafile, map, "last_updated", unix_time)
                            map_data_functions.set_data(mapdatafile, map, "checksum", map_download_md5)
                            move_file(filepath, cgemaps_dir)
                        else:
                            map_data_functions.set_data(mapdatafile, map, "last_updated", unix_time)
                            map_data_functions.set_data(mapdatafile, map, "checksum", map_md5)
                        last_updated = map_data_functions.read_data(mapdatafile, map, "last_updated", is_float=True)
                        checksum = map_data_functions.read_data(mapdatafile, map, "checksum")
                        continue
                else:
                    print(header.status_code)
                    continue
                

                        
                if not last_updated == unix_time:
                    print(f"UPDATE: {filename}")
                    tempdir = f"{cgemaps_dir}\\temp"
                    if os.path.isdir(tempdir) == True:
                        shutil.rmtree(tempdir)
                    os.mkdir(tempdir)
                    map_download_temp = f"{tempdir}\\{map}_download.{fileext}"
                    download_file(url, map_download_temp)
                    basename = os.path.basename(map_download_temp)
                    map_download_md5 = hashlib.md5(open(map_download_temp, 'rb').read()).hexdigest()
                    if not checksum == map_download_md5:
                        map_data_functions.set_data(mapdatafile, map, "last_updated", unix_time)
                        map_data_functions.set_data(mapdatafile, map, "checksum", map_download_md5)
                        move_file(filepath, cgemaps_dir)
                    else:
                        map_data_functions.set_data(mapdatafile, map, "last_updated", unix_time)
            else:
                print(f"skip {filename}")
    except Exception as e:
        print(type(e).__name__)
        error = traceback.format_exc()
        print(error)
        return False
    if os.path.isdir(tempdir) == True:
        shutil.rmtree(tempdir)
    return True



    
    
        
        
      
    
    
    
    

                               
                
            