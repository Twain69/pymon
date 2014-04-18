#!/usr/bin/python
'''
Created on 18.04.2014

@author: Oliver Flegler
'''

import os
import subprocess

if __name__ == '__main__':
    df = subprocess.Popen(["df -P -l | tail -n+2 | cut -d " " -f 1"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
    print device