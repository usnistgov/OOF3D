# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:28 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import os

def skeletonPageSensitivityCheck0():
    return (sensitizationCheck({'Microstructure' : 1,
                                'Skeleton' : 1,
                                'New' : 1,
                                'Simple' : 1,
                                'Rename' : 1,
                                'Copy' : 1,
                                'Delete' : 1,
                                'Save' : 1,
                                },
                               base='OOF2:Skeleton Page')
            and 
            sensitizationCheck({'Method:Chooser' : 1,
                                'OK' : 1,
                                'Prev' : 0,
                                'Next' : 0,
                                'Undo' : 1,
                                'Redo' : 0
                                },
                               base='OOF2:Skeleton Page:Pane:Modification'))

def skeletonPageSensitivityCheck1():
    return (sensitizationCheck({'Microstructure' : 1,
                                'Skeleton' : 1,
                                'New' : 1,
                                'Simple' : 1,
                                'Rename' : 1,
                                'Copy' : 1,
                                'Delete' : 1,
                                'Save' : 1,
                                },
                               base='OOF2:Skeleton Page')
            and 
            sensitizationCheck({'Method:Chooser' : 1,
                                'OK' : 1,
                                'Prev' : 1,
                                'Next' : 0,
                                'Undo' : 1,
                                'Redo' : 0
                                },
                               base='OOF2:Skeleton Page:Pane:Modification'))

def skeletonPageSensitivityCheck2():
    return (sensitizationCheck({'Microstructure' : 1,
                                'Skeleton' : 1,
                                'New' : 1,
                                'Simple' : 1,
                                'Rename' : 1,
                                'Copy' : 1,
                                'Delete' : 1,
                                'Save' : 1,
                                },
                               base='OOF2:Skeleton Page')
            and
            sensitizationCheck({'Method:Chooser' : 1,
                                'OK' : 1,
                                'Prev' : 1,
                                'Next' : 0,
                                'Undo' : 1,
                                'Redo' : 1
                                },
                               base='OOF2:Skeleton Page:Pane:Modification'))

def skeletonPageSensitivityCheck3():
    return (sensitizationCheck({'Microstructure' : 1,
                                'Skeleton' : 1,
                                'New' : 1,
                                'Simple' : 1,
                                'Rename' : 1,
                                'Copy' : 1,
                                'Delete' : 1,
                                'Save' : 1,
                                },
                               base='OOF2:Skeleton Page')
            and
            sensitizationCheck({'Method:Chooser' : 1,
                                'OK' : 1,
                                'Prev' : 1,
                                'Next' : 0,
                                'Undo' : 0,
                                'Redo' : 1
                                },
                               base='OOF2:Skeleton Page:Pane:Modification'))

def skeletonPageSensitivityCheck4():
    # After loading a new Skeleton, but before modifying it.  A
    # previous Skeleton had been modified.
    return (sensitizationCheck({'Microstructure' : 1,
                                'Skeleton' : 1,
                                'New' : 1,
                                'Simple' : 1,
                                'Rename' : 1,
                                'Copy' : 1,
                                'Delete' : 1,
                                'Save' : 1,
                                },
                               base='OOF2:Skeleton Page')
            and 
            sensitizationCheck({'Method:Chooser' : 1,
                                'OK' : 1,
                                'Prev' : 1,
                                'Next' : 0,
                                'Undo' : 0,
                                'Redo' : 0
                                },
                               base='OOF2:Skeleton Page:Pane:Modification'))

def microstructurePageSensitivityCheck0():
    # Existing MS, with a selected pixel group
    return (sensitizationCheck({'Microstructure' : 1,
                                'New' : 1,
                                'NewFromImage' : 1,
                                'NewFromFile' : 1,
                                'Rename' : 1,
                                'Copy' : 1,
                                'Delete' : 1,
                                'Save' : 1
                                },
                               base='OOF2:Microstructure Page')
            and 
            sensitizationCheck({'New' : 1,
                                'Rename' : 1,
                                'Copy' : 1,
                                'Delete' : 1,
                                'Meshable' : 1,
                                'Add': 0,
                                'Remove': 0,
                                'Clear': 1,
                                'Info': 1
                                },
                               base='OOF2:Microstructure Page:Pane:PixelGroups')
            )

def microstructurePageSensitivityCheck1():
    # No existing MS
    return (sensitizationCheck({'Microstructure' : 0,
                                'New' : 1,
                                'NewFromImage' : 0,
                                'NewFromFile' : 1,
                                'Rename' : 0,
                                'Copy' : 0,
                                'Delete' : 0,
                                'Save' : 0
                                },
                               base='OOF2:Microstructure Page')
            and 
            sensitizationCheck({'New' : 0,
                                'Rename' : 0,
                                'Copy' : 0,
                                'Delete' : 0,
                                'Meshable' : 0,
                                'Add': 0,
                                'Remove': 0,
                                'Clear': 0,
                                'Info': 0
                                },
                               base='OOF2:Microstructure Page:Pane:PixelGroups')
            )


def activeAreaPageSensitivityCheck0():
    return (sensitizationCheck({'OOF2:Active Area Page:Microstructure' : 1})
            and
            sensitizationCheck({"Store" : 1,
                                "Rename" : 0,
                                "Delete" : 0,
                                "Restore" : 0,
                                "Modify:Method" : 1,
                                "Modify:Prev" : 0,
                                "Modify:OK" : 1,
                                "Modify:Next" : 0,
                                "Modify:Undo" : 0,
                                "Modify:Redo" : 0,
                                "Modify:Override" : 1
                                },
                               base="OOF2:Active Area Page:Pane"))
            
def activeAreaPageSensitivityCheck1():
    return (sensitizationCheck({'OOF2:Active Area Page:Microstructure' : 1})
           and 
           sensitizationCheck({"Store" : 1,
                               "Rename" : 0,
                               "Delete" : 0,
                               "Restore" : 0,
                               "Modify:Method" : 1,
                               "Modify:Prev" : 0,
                               "Modify:OK" : 1,
                               "Modify:Next" : 0,
                               "Modify:Undo" : 1,
                               "Modify:Redo" : 0,
                               "Modify:Override" : 1
                               },
                              base="OOF2:Active Area Page:Pane"))


def activeAreaStatusCheck(nactive, ntotal, override=False):
    status = gtklogger.findWidget('OOF2:Active Area Page:Pane:Status')
    if override:
        return status.get_text()=="OVERRIDE: all %d pixels are active" % ntotal
    return status.get_text() == '%d of %d pixels are active' % (nactive, ntotal)

def pixelInfoTBCheck(windowname, x, y):
    xtext = gtklogger.findWidget('%s:Pane0:Pane1:Pane2:TBScroll:Pixel Info:X'
                                 % windowname)
    ytext = gtklogger.findWidget('%s:Pane0:Pane1:Pane2:TBScroll:Pixel Info:Y'
                                 % windowname)
    return int(xtext.get_text()) == x and int(ytext.get_text()) == y

def cleanup():
    os.remove('movenode.log')
