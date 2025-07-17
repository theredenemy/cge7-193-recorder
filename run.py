import os
venvdir = "venv"
if os.path.isdir(venvdir) == False:
    
    f = open("make_venv.bat", "w")
    makevenvbat = f'''python -m venv {venvdir}
    cls
    call {venvdir}/Scripts/activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt'''
    f.write(makevenvbat)
    f.close()
    os.system("make_venv.bat")

f = open("load_venv.bat", "w" )
loadvenvbat = f'''call {venvdir}/Scripts/activate.bat
python main.py'''
f.write(loadvenvbat)
f.close()
os.system("load_venv.bat")
    