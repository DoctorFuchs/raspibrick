# KillIdleProc.py

import SharedConstants
import os, subprocess, sys
import ConfigParser

print "Starting KillIdleProc"
num = ['0','1','2','3','4','5','6','7','8','9']
cmd = 'ps -ef | grep "sudo PYTHONPATH=/home/pi/raspibrick/lib python2.7 -Qnew /home/pi/raspibrick/IdleProcess.py"'
f = os.popen(cmd)
out = f.read()
line = out.splitlines()[0]
#print line
startpos = 0
for c in line:
    if c in num:
        break
    startpos += 1
endpos = startpos
for c in line[startpos:]:
    if c not in num:
        break
    endpos += 1
#print startpos, endpos
id = line[startpos:endpos]
#print id
os.system("sudo kill " + id)
