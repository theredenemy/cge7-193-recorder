# cge7-193-recorder : consolelogger.py Copyright (C) 2025  TheRedEnemy
import time
import os
import shutil
def getmaxlines(filename):
    linenum = 0
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            linenum += 1
        return linenum
def logstart(gamedir, logfilename):
    logfile = f"{gamedir}\\{logfilename}"
    if os.path.isdir("gamelogs") == False:
        os.mkdir("gamelogs")
    if os.path.isfile(logfile) == True:
        maxlines = getmaxlines(logfile)
        if not maxlines > 1:
            print("Log Already Started")
            return
    if os.path.isfile(logfile) == True:
        try:
            os.rename(logfile, f"gamelogs\\tf2log_{time.strftime("%Y-%m-%d-%H-%M-%S")}.txt")
        except PermissionError:
            print("gameopened")
    if os.path.isfile(logfile) == False:
        logstart = open(logfile, 'w', encoding='utf-8', errors='ignore')
        time.sleep(2)
        txt = "HELLO WORLD\n"
        logstart.write(txt)
        logstart.close
def consolelog(gamedir, logfilename, startline=1):
    e = 0
    logfile = f"{gamedir}\\{logfilename}"
    lastmodtime = os.path.getmtime(logfile)
    lastline = 0
    lastlinenum = startline
    linelist = []
    
    try:    
        maxlines = getmaxlines(logfile)
       
        
        lastlineprint = lastlinenum
        thelinenum = lastlineprint
        linenum = startline
        with open(logfile, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.readlines()
            linecount = maxlines-startline
            for i in range(linecount):
                linelist.append(content[linenum])
                linenum = linenum + 1
                newlines = i
        lastlinenum = maxlines + 1
        #print("New Lines:", newlines)
        for i, item in enumerate(linelist):
            linelist[i] = item.replace('\n', '')
            linelist[i] = item.strip()
        linelist.append(lastlinenum)
        for i in range(len(linelist)):
            if isinstance(linelist[i], str):
                linelist[i] = linelist[i].replace('.', '')
        return linelist
                
    except IndexError:
        logstart = open(logfile, 'w', encoding='utf-8', errors='ignore')
        txt = "HELLO WORLD"
        logstart.write(txt)
        logstart.close
    
if __name__ == '__main__':
    if os.path.isfile("SOURCETV.ini") == True:
        import configHelper
        config = configHelper.read_config('SOURCETV.ini')
        gamedir = config['SOURCETV']['gamedir']
        logfilename = config['SOURCETV']['logfilename']
        data = consolelog(gamedir, logfilename)
        print(data)
    