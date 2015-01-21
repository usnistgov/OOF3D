# -*- python -*- 
# $RCSfile: DIR.py,v $
# $Revision: 1.5.6.2 $
# $Author: langer $
# $Date: 2014/01/18 04:41:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

dirname = 'elements'
if not DIM_3:
    clib = 'oof2engine'
else:
    clib = 'oof3dengine'

cfiles = ['quad4.C', 'quad4_8.C', 'quad8.C',
          #               'quad8_4.C',
          'quad9.C',
          'tri3.C', 'tri3_6.C', 'tri6.C', 'tri6_3.C',
          'quad4shapefunction.C', 'quad8shapefunction.C',
          'quad9shapefunction.C', 'tri3shapefunction.C',
          'tri6shapefunction.C',
          'edge2.C','edge2shapefunction.C',
          'edge3.C','edge3shapefunction.C',
          'edge3sub.C','edge3super.C']#Interface branch

hfiles = ['quad4shapefunction.h', 'quad8shapefunction.h',
          'quad9shapefunction.h', 'tri3shapefunction.h',
          'tri6shapefunction.h',
          'edge2shapefunction.h','edge3shapefunction.h']#Interface branch

swigfiles = ['quad4.swg', 'quad4_8.swg', 'quad8.swg',
             #                  'quad8_4.swg',
             'quad9.swg',
             'tri3.swg', 'tri3_6.swg', 'tri6.swg', 'tri6_3.swg']

swigpyfiles = ['quad4.spy', 'quad4_8.spy', 'quad8.spy', 'quad8_4.spy',
               'quad9.swg', 
               'tri3.spy', 'tri3_6.spy', 'tri6.spy', 'tri6_3.spy']

if DIM_3:
    cfiles.extend(['tet4.C','tet4shapefunction.C'])
    hfiles.extend(['tet4shapefunction.h'])
    swigfiles.extend(['tet4.swg'])
    swigpyfiles.extend(['tet4.spy'])

pyfiles = ['initialize.py']


