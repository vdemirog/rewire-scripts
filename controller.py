import os
import subprocess
import time

#content = subprocess.run("nc -l -p 7998", shell=True)
content = "/temp2"
print(content)

iplist = ["10.10.10.29","10.10.10.4", "10.10.10.19"]

for i in range(len(iplist)-1):
    print(iplist[i])

    #create face
    addfacecmd = 'echo "ndnaddface tcp4://%s" | nc -q 1 %s 8000 &'%(iplist[i+1], iplist[i])
    subprocess.run(addfacecmd, shell=True)

    time.sleep(1)
    #register content to the next face
    registercmd = 'echo "ndnregister %s tcp4://%s" | nc -q 1 %s 8000 &'%(content, iplist[i+1], iplist[i])
    subprocess.run(registercmd, shell=True)

    time.sleep(1)

