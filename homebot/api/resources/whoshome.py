import subprocess
import sys
import re


def checkifHome(macAddress):
    output = subprocess.Popen([((sys.path[0]) + '/arpscan.sh')], stdout=subprocess.PIPE, shell=False).communicate()[0]
    # print (output)
    # macAddress = input('Insert MAC address')
    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()):
        if macAddress in str(output):
            print('available')
        else:
            print('absent')
    else:
        print('MAC address invalid')
