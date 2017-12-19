#Check if enth. is available

import subprocess
import time
from time import localtime, strftime
import os
import sys
import re


def firmwareUp():
    os.system('echo "a" > /dev/'+port)
    cmd_tab=['a','e2p --boot_mode=DOWNLOAD','e2p --dl_firmware_url=https://195.116.227.11/FW_02_00_00/SAGEM_194_test_FAKE.as3','reboot -f']
    for element in cmd_tab:
        os.system('echo "'+element+'" > /dev/'+port)
        time.sleep(1)


def cmd_output(to_find,lines):
    cmd = ('tail -n'+str(lines)+' /home/pi/Desktop/output.txt | grep -i "'+to_find+'"')
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    result = output.stdout.read()
    if to_find in result:
        writeToFile(result)
        return True
    else:
        return False

def writeToFile(msg):
    with open('/home/pi/Desktop/enth0.txt','a+') as file:
        file.write(str(msg))
        file.write('\n')


def to_send(cmd):
    os.system('echo "a" > /dev/'+port)
    time.sleep(1)
    os.system('echo "'+cmd+'" > /dev/'+port)
    time.sleep(2)


def main():
    global port
    port = 'ttyUSB0'
    for i in range(0,1000):
        firmwareUp()
        time.sleep(120)
        canCheckIP = cmd_output('app.live> BaseBanner > updateProgramInfoAfter() - lcn: 3 - serviceIndex: 0',200)
        while canCheckIP is not True:
            time.sleep(10)
            canCheckIP = cmd_output('app.live> BaseBanner > updateProgramInfoAfter() - lcn: 3 - serviceIndex: 0',100)
        to_send('ifconfig')
        isIPseen = cmd_output('inet addr',100)
        writeToFile(isIPseen)
    
main()  

