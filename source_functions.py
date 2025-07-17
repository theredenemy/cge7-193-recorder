def run_cmd(cmd):
    import os
    import pydirectinput
    import pyautogui
    import time
    pydirectinput.FAILSAFE = False
    pyautogui.FAILSAFE = False
    time.sleep(3)
    pydirectinput.press('F7')
    print("f7")
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
                    
                        
                
            