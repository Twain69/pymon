#!/usr/bin/python3
'''
Created on 18.04.2014

@author: Oliver Flegler
'''

#TODO List:
# Functions needed:
#   ping_destination with script running when destination is not available
#   check hetzner backup space
#   check cpu temperatur

import argparse
import yaml

import harddrive
import process
import hardware
import notification
import network

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
        config['verbose'] = args.verbose
        f.close()
    except IOError:
        config = None
        config['verbose'] = 0

    notification.printVerbose("\n **** verbose mode ****")

    harddrive.checkFreeSpace(config)

    process.checkProcessRunning(config)

    harddrive.checkRaidStatus(config)

    hardware.checkCPUTemperatur(config)

    hardware.checkFanSpeed(config)

    network.checkDestinationAvailable(config)
