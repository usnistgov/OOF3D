# -*- python -*-
# $RCSfile: typename.py,v $
# $Revision: 1.5.18.1 $
# $Author: langer $
# $Date: 2014/04/16 18:44:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Used by TypeChecker.__repr__() in parameter.py.

import types

reversetypedir = {}

for name, tipe in types.__dict__.items():
    if type(tipe) is types.TypeType:
        reversetypedir[tipe] = name


def typename(tipe):
    if isinstance(tipe, (types.ClassType, types.TypeType)):
        return tipe.__name__
    if isinstance(tipe, types.InstanceType):
        return tipe.__class__.__name__
    return reversetypedir[tipe]
