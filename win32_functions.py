def reboot():
    import win32api
    import win32con
    import win32security
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

    
    
    
