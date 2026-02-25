import win32api
import win32con
import win32security
import win32gui
import win32process
import ctypes
import psutil
import time
def reboot():
    
    # What The Fuck
    id = win32security.LookupPrivilegeValue(None, win32security.SE_SHUTDOWN_NAME)
    handle =  win32api.GetCurrentProcess()
    token = win32security.OpenProcessToken(handle, win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY)

    if token is None:
        print("Could not get token")
        return False
    # Get Token Privileges
    win32security.AdjustTokenPrivileges(token, False, ((id, win32security.SE_PRIVILEGE_ENABLED),))

    win32api.ExitWindowsEx(win32con.EWX_REBOOT | win32con.EWX_FORCE, 0)
    win32api.CloseHandle(token)
    return True

def get_pid(process_name):
    
    pid = None
    
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']
            return pid
    if pid is None:
        return False

def GetHwndsFromPID(pid):
    hwnds = []
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            #print(hwnd)
            found = win32process.GetWindowThreadProcessId(hwnd)
            for id in found:
                #print("pid", id, pid)
                if id == pid:
                    # print(id, hwnd)
                    hwnds.append(hwnd)
                    break
            return True
    
    win32gui.EnumWindows(callback, hwnds)
    return hwnds
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
            print("Window Not Responding")
            time.sleep(3)
def set_focus_win32(process_name):
    pid = get_pid(process_name)
    if pid is False:
        return False
    while True:
        try:
            hwnds = GetHwndsFromPID(pid)
            hwnd = hwnds[0]

            if hwnd:
                while ctypes.windll.user32.IsHungAppWindow(hwnd):
                    pass
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                

                win32gui.SetForegroundWindow(hwnd)
            
                return True
            else:
                return False
        except Exception as e:
            print("Window Not Responding")
            time.sleep(3)

    
    
    
