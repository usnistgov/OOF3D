# -*- python -*-
# $RCSfile: tsl.py,v $
# $Revision: 1.12.2.3 $
# $Author: fyc $
# $Date: 2014/07/29 21:24:04 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import corientation
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import progress
from ooflib.SWIG.orientationmap import orientmapdata
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import utils
from ooflib.common.IO import reporter

import math, os, string, re


class DataPoint:
    def __init__(self, position, angletuple, phasename):
        self.position = position
        self.angle = corientation.COrientBunge(*angletuple)
        self.phasename = phasename
    def euler(self):
        return self.angle.abg()
    def __repr__(self):
        return "(%g, %g)" % (self.position[0], self.position[1])


## getrows() splits a list of DataPoints into lists in which x is
## monotonically increasing.
    
def getrows(datapts):
    row = [datapts[0]]
    for pt in datapts[1:]:
        if pt.position[0] > row[-1].position[0]:
            row.append(pt)
        else:
            yield row
            row = [pt]
    yield row

class TSLreader(orientmapdata.OrientMapReader):
    def __init__(self):
        self.phaselists = {}
        orientmapdata.OrientMapReader.__init__(self)

    if config.dimension() == 2:
        def read(self, filename):
            prog = progress.getProgress(os.path.basename(filename),
                                        progress.DEFINITE)
            rows, npts = self.readfile(filename, prog)
            
            try:

                nx = len(rows[0])
                ny = len(rows)
                count = 0
                for row in rows:
                    count += 1
                    if len(row) != nx:
                        raise ooferror.ErrUserError(
                            "Orientation map data appears to be incomplete")

                # pixel size
                dx = rows[0][1].position[0] - rows[0][0].position[0]
                dy = rows[1][0].position[1] - rows[0][0].position[1]
                pxlsize = primitives.Point(dx, dy)

                # If we assume that the points are in the centers of the
                # pixels, then the actual physical size is one pixel bigger
                # than the range of the xy values.
                size = rows[-1][-1].position + pxlsize

                debug.fmsg("nx=", nx, "ny=", ny, "size=", size, "pxlsize=", pxlsize)

                if config.dimension() == 2:
                    od = orientmapdata.OrientMap(primitives.iPoint(nx, ny), size)
                else:
                    od = orientmapdata.OrientMap(primitives.iPoint(nx, ny, 1), size)
                count = 0
                for row in rows:
                    for datum in row:
                        self.addDatum(od, datum, pxlsize, ny, count, npts, prog)

            finally:
                prog.finish()
            return od


    elif config.dimension() == 3:
        def read(self, filepattern):
            dirname = os.path.dirname(filepattern)
            items = os.listdir(dirname)
            escaped_pattern = string.replace(re.escape(os.path.basename(filepattern)),"\\*",".*?")
            files = []
            for item in items:
                match = re.match(escaped_pattern, item)
                if match != None:
                    span = match.span()
                    if span[0]==0 and span[1] == len(item):
                        files.append(os.path.join(dirname,item))


            prog = progress.getProgress(os.path.basename(filepattern),
                                        progress.DEFINITE)

            try:
                # Look at the just the first file to get some info
                z = 0
                rows, npts = self.readfile(files[0],prog,z)
                nx = len(rows[0])
                ny = len(rows)
                nz = len(files)
                dx = rows[0][1].position[0] - rows[0][0].position[0]
                dy = rows[1][0].position[1] - rows[0][0].position[1]
                dz = 1
                pxlsize = primitives.Point(dx, dy, dz)
                size = rows[-1][-1].position + pxlsize
                od = orientmapdata.OrientMap(primitives.iPoint(nx, ny, nz), size)
                count = 0
                for row in rows:
                    count +=1
                    for datum in row:
                        self.addDatum(od, datum, pxlsize, ny, count, npts, prog, nz)

                # now look at the rest of the files
                for file in files[1:]:
                    z = z+dz
                    rows, nrowpts = self.readfile(file,prog,z)
                    npts = npts + nrowpts
                    count = 0
                    for row in rows:
                        count += 1
                        if len(row) != nx:
                            raise ooferror.ErrUserError(
                                "Orientation map data appears to be incomplete")

                        for datum in row:
                            self.addDatum(od, datum, pxlsize, ny, count, npts, prog, nz)

            finally: 
                prog.finish()

            return od

            

    def readfile(self, filename, prog, z=0):
        tslfile = file(filename, "r")
        prog.setMessage("Reading " + filename)
        count = 1                       # line counter
        lines = tslfile.readlines()
        nlines = len(lines)
        data = utils.ReservableList(nlines)
        angletype = None
        for line in lines:
            if line[0] == '#':
                if line.startswith("Column 1-3", 2):
                    if "radians" in line:
                        angletype = "radians"
                    else:
                        angletype = "degrees"
                    debug.fmsg("Angles are in %s." % angletype)
            else:                       # line[0] != '#'
                substrings = line.split()
                if len(substrings) < 5:
                    raise ooferror.ErrUserError(
                        "Too few numbers in line %d of %s" % (count, filename))
                values = map(float, substrings[:5])
                if angletype == "radians":
                    angles = values[:3]
                elif angletype == "degrees":
                    angles = map(math.radians, values[:3])
                else:
                    raise ooferror.ErrDataFileError(
                        "Angle type not specified in TSL data file")
                orientation = corientation.COrientBunge(*angles)
                if config.dimension() == 2:
                    point = primitives.Point(values[3], values[4])
                elif config.dimension() == 3:
                    point = primitives.Point(values[3], values[4], z)
                data.append(DataPoint(point, # position
                    angles,
                    ' '.join(substrings[10:])))    # phase name
            count += 1      # count actual file lines, comments and all
            prog.setMessage("read %d/%d lines" % (count, nlines))
            prog.setFraction(float(count)/nlines)
        npts = len(data)
        debug.fmsg("read %d lines, %d data points" % (count, npts))

        # We don't yet know if the points are on a rectangular or a
        # hexagonal lattice, so split the data up into rows.
        # getrows() is a generator, but we need an actual list so that
        # we can index into it.
        rows = list(getrows(data))

        if len(rows) < 2:
            raise ooferror.ErrUserError(
                "Orientation map data has too few rows.")
        if rows[0][0].position[0] != rows[1][0].position[0]:
            # Must be a hexagonal lattice.  Throw out every other row.
            reporter.warn("Converting hexagonal lattice to rectangular by discarding alternate rows.")
            rows = rows[::2]            # discard odd numbered rows

        return rows, npts

    def addDatum(self, od, datum, pxlsize, ny, count, npts, prog, nz=0):
        prog.setMessage("Processing orientations %d/%d" % (count,npts))
        if config.dimension() == 2:
            ij = primitives.iPoint(
                int(round(datum.position[0]/pxlsize[0])),
                ny-1-int(round(datum.position[1]/pxlsize[1])))
        elif config.dimension() == 3:
            ij = primitives.iPoint(
                int(round(datum.position[0]/pxlsize[0])),
                ny-1-int(round(datum.position[1]/pxlsize[1])),
                nz-1-int(round(datum.position[2]/pxlsize[2])))
        try:
            self.phaselists[datum.phasename].append(ij)
        except KeyError:
            self.phaselists[datum.phasename] = [ij]
        self.set_angle(od, ij, datum.euler())
        prog.setMessage("%d/%d orientations" % (count,npts))
        prog.setFraction(float(count)/npts)
        count += 1
        if prog.stopped():
            return None


    ## postProcess is called after the orientation data has been
    ## assigned to a Microstructure.
    # TODO 3.1: We should have a progress bar here
    def postProcess(self, microstructure):
        phasenames = self.phaselists.keys()
        phasenames.sort()
        for phasename in phasenames:
            orientmapdata.addPixelsToGroup(microstructure, phasename,
                                           self.phaselists[phasename])

orientmapdata.registerOrientMapReaderClass('TSL', TSLreader,
                                           help='TSL .ang file')
        
