'''
Created on 19.04.2014

@author: Oliver Flegler
'''

import pymon
import smtplib
import socket

def error(config, msg):

    if config['notification']['status'] == "enabled":   
        sender = config['notification']['sender']
        subject = "Error on " + socket.gethostname() + " (pymon)"
        
        for recipient in config['notification']['recipients']:
            recipient = recipient['recipient']
            message = """From: %s
To:  %s
Subject: %s

%s
""" % (sender, recipient, subject, msg) 
            
            s = smtplib.SMTP('localhost')
            s.sendmail(sender, [recipient], message)
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