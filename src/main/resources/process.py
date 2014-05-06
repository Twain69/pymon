'''
Created on 19.04.2014

@author: Oliver Flegler
'''

import notification
import subprocess, os

def checkProcessRunning(config):
    notification.printHeader("Checking running processes")
    
    ps = subprocess.Popen(["ps", "auxwww"], stdout=subprocess.PIPE)
    output = ps.communicate()[0]
    processList = output.split("\n")[1:-1]
    
    try:
        checkprocesses = config['processes']
    except (KeyError, TypeError):
        notification.printVerbose("No processes configured to be checked. Skipping!")
        return
    
    for process in checkprocesses:
        
        processName = process['name']
        startCommand = process['startCommand']
        try:
            processOwner = process['processOwner']
        except KeyError:
            processOwner = ""
        try:
            status = process['status']
        except KeyError:
            status = "enabled"
        
        if status == "enabled":
            notification.printVerbose("Checking for process '" + processName + "'")
        
            found = False
            
            for line in processList:
                if found:
                    break
                elements = line.split()
                # $ ps auxwww | head -n1
                # USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
                # -> command is starting at position 10
                combinedProcessName = ""
                for row in elements[10:]:
                    combinedProcessName = combinedProcessName + " " + row
                combinedProcessName = combinedProcessName.strip()
                    
                if processName in combinedProcessName:
                    user = elements[0]
                    found = True
            
            if found is False:
                notification.error(config, "Process '" + processName + "' not found, trying to start")
                os.system(startCommand)
            else:
                if processOwner is not "" and processOwner != user:
                    notification.error(config, "Process '" + processName + "' found, but process owner is wrong: " + user + " instead of " + processOwner)
                else:
                    notification.printVerbose(" Process '" + processName + "' running, process owner: " + user)
        
        else:
            notification.printVerbose("Check for process '" + processName + "' is disabled, skipping")
            
        #notification.printVerbose("")