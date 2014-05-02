#!/usr/bin/python
'''
Created on 18.04.2014

@author: Oliver Flegler
'''

#TODO List:
# checkRaidStatus has to be tested
# add pymon.conf as sample to rpm deployment
# Override of harddrive min free percent per partition
#
# Functions needed:
#   ping_destination with script running when destination is not available
#   check hetzner backup space

import argparse
import yaml

import harddrive
import process
import hardware
import notification

verbose = False

def parseArguments():
    parser = argparse.ArgumentParser(description='Check the local system')
    parser.add_argument('-c', '--configFile', help="The location of the config file", default="/etc/pymon.conf")
    parser.add_argument('-v', '--verbose', help="Print verbose output", action="store_true")
    args=parser.parse_args()
    return args

if __name__ == '__main__':
    args = parseArguments()
    notification.setVerbose(args.verbose)
    
    try:
        f = open(args.configFile)
        config = yaml.safe_load(f)
        f.close()
    except IOError:
        config = None
    
    notification.printVerbose("\n **** verbose mode ****")
    
    harddrive.checkFreeSpace(config)
    
    process.checkProcessRunning(config)
    
    harddrive.checkRaidStatus(config)
    
    hardware.checkCPUTemperatur(config)
    
    hardware.checkFanSpeed(config)