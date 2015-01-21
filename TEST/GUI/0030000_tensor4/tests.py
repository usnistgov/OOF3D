# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

base = "Dialog-Parametrize Mechanical;Elasticity"

removefile('aniso.dat')
removefile('cubics.dat')
removefile('isomat.dat')

def testcij(widgetname, **cijs):
    dct = {}
    for i in range(1, 7):
        for j in range(i, 7):
            cijname = "c%d%d" % (i, j)
            wijname = "%d,%d" % (i-1, j-1)
            try:
                dct[wijname] = cijs[cijname]
            except KeyError:
                dct[wijname] = 0.0
    return gtkMultiFloatCompare(dct, widgetbase=base+";"+widgetname)

def sensitivecij(widgetname, **cijs):
    for i in range(1, 7):
        for j in range(i, 7):
            cijname = "c%d%d" % (i, j)
            wijname = "%d,%d" % (i-1, j-1)
            try:
                nominal = cijs[cijname]
            except KeyError:
                nominal = 0
            fullwname = base + ";" + widgetname + ":" + wijname
            actual = is_sensitive(fullwname)
            if actual != nominal:
                print >> sys.stderr, "Sensitization test failed for", fullwname
                return 0
    return 1

def convertibleCij(widgetname, **cijs):
    return testcij(widgetname+":cijkl:Cij", **cijs)

def sensitiveConvCij(widgetname, **cijs):
    return sensitivecij(widgetname+":cijkl:Cij", **cijs)

def anisoCij(anisoclass, **cijs):
    return testcij("Anisotropic;"+anisoclass, **cijs)

def sensitiveAnisoCij(anisoclass, **cijs):
    return sensitivecij("Anisotropic;"+anisoclass, **cijs)

def other(widgetname, version, **vals):
    ## tests a non-Cij widget for cijkl
    return gtkMultiFloatCompare(
        vals, widgetbase=base+";"+widgetname+":cijkl:"+version)
