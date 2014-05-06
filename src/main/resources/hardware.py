'''
Created on 19.04.2014

@author: Oliver Flegler
'''

import notification
import subprocess

def checkCPUTemperatur(config):
    pass

def checkFanSpeed(config):
    notification.printHeader("Checking fan speeds")
    
    try:
        defaultMinSpeed = config['hardware']['fanSpeed']['minSpeed']
    except (KeyError, TypeError):
        defaultMinSpeed = 500
    
    try:
        p1 = subprocess.Popen(["sensors"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["egrep", "^fan"], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0]
        fans = output.split("\n")[0:-1]
    except (OSError):
        notification.error(config, "Sensors not installed")
        
    if len(fans) == 0:
        notification.error(config, "Could not find any fans")
        
    
    for fan in fans:
        
        fanname = fan.split()[0]
        speed = int(fan.split()[1])
        fanname = fanname.split(":")[0]
        minSpeed = defaultMinSpeed
        
        try:
            for override in config['hardware']['fanSpeed']['override']:
                if fanname in override['name']:
                    minSpeed = override['minSpeed']
                    break
        except (KeyError, TypeError):
            pass
        
        if speed < minSpeed:
            notification.error(config, "Fan speed to low for fan " + fanname + ". Current speed: " + str(speed) + " (minSpeed: " + str(minSpeed) + ")")
        else:
            notification.printVerbose("Fan speed for fan " + fanname + " currently " + str(speed) + " (minSpeed: " + str(minSpeed) + ")")