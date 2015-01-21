# -*- python -*-
# $RCSfile: hkl.py,v $
# $Revision: 1.6.2.2 $
# $Author: fyc $
# $Date: 2014/07/29 21:23:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import corientation
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import progress
from ooflib.SWIG.orientationmap import orientmapdata
from ooflib.common import debug
from ooflib.common import primitives
import math
import os.path
import string

class HKLreader(orientmapdata.OrientMapReader):
    def __init__(self):
        self.phaselists = {}
        orientmapdata.OrientMapReader.__init__(self)
    def read(self, filename):
        hklfile = file(filename, "r")
        ## TODO  OPT: Use lineiter = iter(hklfile) instead of iter(lines).
        ## Then it's not necessary to create an array of lines.
        lines = hklfile.readlines()
        lineiter = iter(lines)
        line = lineiter.next()
        while not line.startswith('XCells'):
            line = lineiter.next()
        xcells = string.atoi(string.split(line)[1])
        line = lineiter.next()
        ycells = string.atoi(string.split(line)[1])
        line = lineiter.next()
        xstep = string.atof(string.split(line)[1])
        line = lineiter.next()
        ystep = string.atof(string.split(line)[1])
        line = lineiter.next()


        od = orientmapdata.OrientMap(
            primitives.iPoint(xcells, ycells),
            primitives.Point(xcells*xstep, ycells*ystep))
        
        while not string.split(line)[0] == 'Phase':
            line = lineiter.next()
        prog = progress.getProgress(os.path.basename(filename),
                                    progress.DEFINITE)
        try:
            count = 0
            npts = xcells*ycells
            for line in lineiter:
                vals = string.split(line)
                phase = vals[0]
                x = string.atof(vals[1])
                y = string.atof(vals[2])
                angles = map(string.atof, vals[5:8])
                mad = string.atof(vals[8])  # mean angular deviation
                ij = primitives.iPoint(
                    int(round(x/xstep)),
                    ycells-1-int(round(y/ystep)))
                try:
                    self.phaselists[phase].append(ij)
                except KeyError:
                    self.phaselists[phase] = [ij]
                self.set_angle(
                    od, ij, 
                    corientation.COrientBunge(*map(math.radians, angles)))
                prog.setFraction(float(count)/npts)
                prog.setMessage("%d/%d orientations" % (count, npts))
                count += 1
                if pbar.stopped():
                    return None
        finally:
            prog.finish()
        return od

    ## postProcess is called after the orientation data has been
    ## assigned to a Microstructure.
    def postProcess(self, microstructure):
        phasenames = self.phaselists.keys()
        phasenames.sort()
        for phasename in phasenames:
            orientmapdata.addPixelsToGroup(microstructure, 'Phase_' + phasename,
                                           self.phaselists[phasename])

orientmapdata.registerOrientMapReaderClass('HKL', HKLreader,
                                           help='HKL channel text file')
