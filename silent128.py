import subprocess
import os

def modify(s):
    ms=s.replace("\\","\\\\")
    return ms

def runcmd(command):
    command = os.path.normpath(command)

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()
    output = output.decode("utf-8")
    print(output)
    if error:
        error = error.decode("utf-8")
        print(f"Error: {error}")

# 12.8 :

'''_______NEW VERSION_______'''

# c1223=r"\\rdlservnt\cdimage\OpenEdge\122\nt64\untested\SP_Jul21\setup.exe -psc_s -psc_f1=C:\Users\sazar\Documents\response122.ini -psc_f2=C:\result122-13.log"
c128=r"\\rdlservnt\cdimage\OpenEdge\128\nt64\artifactory\Jul25_1907\setup.exe -psc_s -psc_f1=C:\Users\sazar\Documents\response128.ini -psc_f2=C:\res128.log"
command=r"{}".format(modify(c128))
runcmd(command[2:])

print("\nautomation part--\n")
# RUN Automation.py
autoFile="C:/Users/sazar/AppData/Local/Programs/Python/Python311/vsc/AUTOmation.py"
# autoFile=r"{}".format(modify(autoFile))
try:
    process = subprocess.run(["python", autoFile], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(e.stderr)



'''
_______UNINSTALLING________
'''

unins="C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Progress/OpenEdge 12.8ALPHA (64-bit)/Uninstall OpenEdge 12.8ALPHA (64-bit).lnk"

runcmd(unins)
# unins="C:/Program Files (x86)/InstallShield Installation Information/{2f029b3e-4a73-4d79-874a-28f38a94baac}/setup.exe -psc_s -runfromtemp -l0x0009 -removeonly"
# unins="C:/Users/sazar/Desktop/setup.exe -psc_s -runfromtemp -l0x0009 -removeonly"
# uninsCmd=r"{}".format(modify(unins))




'''_______OLD VERSION_______'''

c127=r"\\rdlservnt\cdimage\OpenEdge\127\nt64\artifactory\Apr21_1256\setup.exe -psc_s -psc_f1=C:\Users\sazar\Documents\response127.ini -psc_f2=C:\\res127.log"
command=r"{}".format(modify(c127))

runcmd(command[2:])

# RUN Automation.py
autoFile="C:/Users/sazar/AppData/Local/Programs/Python/Python311/vsc/AUTOmation2.py"
try:
    process = subprocess.run(["python", autoFile], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(e.stderr)


'''_______DIFF________'''

diffFile="C:/Users/sazar/AppData/Local/Programs/Python/Python311/vsc/DIFFauto.py"
try:
    process = subprocess.run(["python", diffFile], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(e.stderr)








# import subprocess
# import os

# # ---- 128
# # cmd=r"\\rdlservnt\\cdimage\\OpenEdge\\128\\nt64\\artifactory\\Jul12_1900\setup.exe -psc_s -psc_f1=C:\\response.ini -psc_f2=C:\\res2.log"
# #cmd=r"\\rdlservnt\\cdimage\\OpenEdge\\128\\nt64\\perf\\Jun8\setup.exe -psc_s -psc_f1=C:\\response.ini -psc_f2=C:\\res3.log"

# # ---- 122
# cmd =r"\\rdlservnt\\cdimage\\OpenEdge\\122\\nt64\\untested\\SP_Jun30\\setup.exe -psc_s -psc_f1=C:\\response122.ini -psc_f2=C:\\res122.log"


# # cmd=r"C:\\ProgramData\\Microsoft\Windows\Start Menu\\Programs\\Progress\\OpenEdge 12.8ALPHA (64-bit)\\Uninstall OpenEdge 12.8ALPHA (64 bit).lnk"
# cmd = os.path.normpath(cmd)

# process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# op, error = process.communicate()
# op = op.decode("utf-8")
# print(op)
# if error:
#     error = error.decode("utf-8")
#     print(f"Error: {error}")
