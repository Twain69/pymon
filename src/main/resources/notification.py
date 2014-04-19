'''
Created on 19.04.2014

@author: Oliver Flegler
'''

import pymon


def error(msg):
    #TODO: send mail!
    printVerbose("**** ERROR: " + msg)

def printMessage(offset, msg):
    if pymon.verbose == True:
        print " "*offset + msg

def printVerbose(msg):
    printMessage(2, msg)
        
def printHeader(msg):
    printMessage(0, "\n" + msg)
        
def setVerbose(verbose):
    pymon.verbose = verbose