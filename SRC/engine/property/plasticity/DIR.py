# -*- python -*-
# $RCSfile: DIR.py,v $
# $Revision: 1.1.66.1 $
# $Author: langer $
# $Date: 2013/11/08 20:46:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'plasticity'

clib = 'oof3dengine'

subdirs = ['constitutive']

cfiles =      ['plasticity.C','plasticity_data.C']
hfiles =      ['plasticity.h','plasticity_data.h','constitutive_base.h']
swigfiles =   ['plasticity.swg']
swigpyfiles = ['plasticity.spy']
