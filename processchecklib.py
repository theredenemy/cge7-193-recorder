def process_check(process):
    import subprocess
    import re
    tasklistoutput = subprocess.getoutput('tasklist.exe')
    findpro = re.search(process, tasklistoutput)
    if findpro:
        return True
    else:
        return False
