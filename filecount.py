import subprocess
from subprocess import Popen, PIPE
p1 = Popen(["ls", "-alh", "/uscms_data/d3/msaunder/skims2017/mc_TT/"], stdout=subprocess.PIPE)
p2 = Popen(["grep", "root"], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = Popen(["wc", "-l"], stdin=p2.stdout, stdout=subprocess.PIPE)
num = int(p3.communicate()[0])
print num, num+1
