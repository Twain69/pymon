"""
Created on 18.05.2020

@author: Oliver Flegler
"""
from scapy.sendrecv import sr1

import notification
from scapy.layers.inet import IP, ICMP
import os


def checkDestinationAvailable(config):
    notification.printHeader("Checking network destinations")

    try:
        destinations = config['network']
    except (KeyError, TypeError):
        notification.printVerbose("No network destinations configured to be checked. Skipping!")
        return

    for dest in destinations:
        ip = dest['ip']
        startCommand = dest['startCommand']

        notification.printVerbose("Checking if destination '" + ip + "' is reachable")
        icmp = IP(dst=ip) / ICMP()

        response = sr1(icmp, timeout=5, verbose=config['verbose'])
        if response is None:
            notification.error(config, "Destination '" + ip + "' not reachable")
            os.system(startCommand)
        else:
            notification.printVerbose("Destination '" + ip + "' reached")
