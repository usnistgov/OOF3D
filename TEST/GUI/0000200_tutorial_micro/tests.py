# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:21 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

import os
from generics import *

# This tutorial (as recorded) overwrites a data file, so we have to
# make sure that there's a file to overwrite.

datafilename = 'tutorial3.mic'          # name of the file as written in the log

if not os.path.exists(datafilename):
    dfile = open(datafilename, 'w')
    print >> dfile, "dummy"
    dfile.close()

def imagePageSensitizationCheck0():
    # before undoing image modifications
    return sensitizationCheck(
        {
        'Prev' : 1,
        'OK' : 1,
        'Next' : 0,
        'Undo' : 1,
        'Redo' : 0
        },
        base='OOF2:Image Page:Pane')

def imagePageSensitizationCheck1():
    # after undoing one image modification
    return sensitizationCheck(
        {
        'Prev' : 1,
        'OK' : 1,
        'Next' : 0,
        'Undo' : 1,
        'Redo' : 1
        },
        base='OOF2:Image Page:Pane')

def imagePageSensitizationCheck2():
    # after undoing all image modifications
    return sensitizationCheck(
        {
        'Prev' : 1,
        'OK' : 1,
        'Next' : 0,
        'Undo' : 0,
        'Redo' : 1
        },
        base='OOF2:Image Page:Pane')

def newPixelGroupSensitizationCheck0():
    return sensitizationCheck(
        {
        "gtk-ok" : 1,
        "gtk-cancel" : 1,
        "name:Auto" : 1,
        "name:Text" : 1
        },
        base="Dialog-Create new pixel group")

def newPixelGroupSensitizationCheck1():
    return sensitizationCheck(
        {
        "gtk-ok" : 0,
        "gtk-cancel" : 1
        },
        base="Dialog-Create new pixel group")

def newPixelGroupSensitizationCheck2():
    # When Auto is clicked
    return sensitizationCheck(
        {
        'gtk-ok' : 1,
        'gtk-cancel' : 1,
        'name:Auto' : 1,
        'name:Text' : 0
        },
        base="Dialog-Create new pixel group")

def newPixelGroupSensitizationCheck3():
    # When Auto is not clicked, but Text is empty
    return sensitizationCheck(
        {
        'gtk-ok' : 0,
        'gtk-cancel' : 1,
        'name:Auto' : 1,
        'name:Text' : 1
        },
        base="Dialog-Create new pixel group")
