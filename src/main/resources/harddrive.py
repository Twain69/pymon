'''
Created on 19.04.2014

@author: Oliver Flegler
'''

import subprocess
import notification

def checkFreeSpace(config):
    notification.printHeader("Checking harddrive free space")
    
    try:
        defaultMinFreePercent = config['harddrive']['minFreeSpace']
    except (KeyError, TypeError):
        defaultMinFreePercent = 80
    
    df = subprocess.Popen(["df", "-P"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    lines = output.split("\n")[1:-1]
    for line in lines:
        
        device = line.split()[0]
        percent = line.split()[4]
        mountpoint = line.split()[5]
        
        minFreePercent = defaultMinFreePercent
        
        try:
            for override in config['harddrive']['override']:
                if mountpoint == override['mountPoint']:
                    minFreePercent = override['minFreeSpace']
                    break
        except (KeyError, TypeError):
            pass
        
        percentClean = int(percent.split("%")[0])
        if percentClean >= minFreePercent:
            notification.error(config, "device " + str(device) + " usage: " + str(percentClean) + "% (min " + str(minFreePercent) + "%) mountpoint: " + mountpoint)
        else:
            notification.printVerbose("checked {0:20s} usage: {1:3d}% (min: {2:3d}%, device: {3:10s})".format(mountpoint, percentClean, minFreePercent, device))
                
                
def checkRaidStatus(config):
    notification.printHeader("Checking RAID status")
    
    try:
        raid = config['raid']
    except (KeyError, TypeError):
        notification.printVerbose("No raid devices have been configured. Skipping!")
        return
    
    try:
        status = raid['status']
    except (KeyError, TypeError):
        status = "disabled"
        
    if status == "enabled":
        for device in raid['devices']:
            deviceName = device['name']
            notification.printVerbose("Checking RAID " + deviceName)
            
            mdadm = subprocess.Popen(["mdadm", "--detail", deviceName], stdout=subprocess.PIPE)
            output = mdadm.communicate()[0]
            lines = output.split("\n")
            
            totalDevices = None        
            activeDevices = None
            
            for row in lines:
                if "Total Devices" in row:
                    totalDevices = int(row.split(":")[1])
                if "Active Devices" in row:
                    activeDevices = int(row.split(":")[1])
            
            if totalDevices is not None and activeDevices is not None:
                totalDevices = int(totalDevices)
                activeDevices = int(activeDevices)
                if totalDevices != activeDevices:
                    notification.error(config, "RAID {0:0s} is degraded. {1:0d} disks total, {2:0d} disks active ".format(deviceName, totalDevices, activeDevices))
                else:
                    notification.printVerbose("RAID " + deviceName + " is OK")
            else:
                notification.error(config, "Could not determine details of RAID " + deviceName)
    else:
        notification.printVerbose("RAID status check is disabled")