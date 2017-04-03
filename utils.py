#! /usr/bin/env python

import os
import sys
import subprocess
import time 


def dprint(s, debug=False):
    if debug: print s

def syscall(cmd, debug=False):
    if debug:
        print("cmd={}".format(cmd))
    else:
        os.system(cmd)

def chkcall(cmd, wait=False):
    cmdl = cmd.split(' ')
    p1 = subprocess.Popen(cmdl, stdout=subprocess.PIPE)
    out, err = p1.communicate()
    if wait: p1.wait()
    return out.rstrip('\r\n')

def chkcall2(cmd1, cmd2, wait=False):
    cmd1l = cmd1.split(' ')
    cmd2l = cmd2.split(' ')
    p1 = subprocess.Popen(cmd1l, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2l, stdin=p1.stdout, stdout=subprocess.PIPE)
    out, err = p2.communicate()
    if wait: p2.wait()
    return out.rstrip('\r\n')

def get_tstamp():
    timestr = time.strftime("%Y%m%d-%H%M%S") 
    return timestr
