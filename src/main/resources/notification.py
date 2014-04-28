'''
Created on 19.04.2014

@author: Oliver Flegler
'''

import pymon
import smtplib
import socket

from email.mime.text import MIMEText


def error(config, msg):
    msg = MIMEText()
    
    msg['Subject'] = "Error on " + socket.gethostname() + " (pymon)"
    msg['From'] = "servermaster@flegler.com"
    #msg['To'] = 
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