// -*- C++ -*-
// $RCSfile: contourcell.h,v $
// $Revision: 1.9.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CONTOURCELL_H
#define CONTOURCELL_H

// Classes used to support contour plotting on the finite element
// mesh.  These are low level objects actually used by the
// MasterElements. The more advanced things used by the contouring
// code itself (such as the real ContourCell class) are in
// engine/IO/contour.h and related files.

#include "mastercoord.h"
#include "common/coord.h"
#include <iostream>
#include <vector>

class ContourCellCoord {
public:
  ContourCellCoord(double x, double y, int ix, int iy)
    : x(x), y(y), ix(ix), iy(iy)
  {}
  ContourCellCoord() {}
  double x, y;
  int ix, iy;			// used for identification.
};

std::ostream &operator<<(std::ostream &os, const ContourCellCoord&);

bool operator==(const ContourCellCoord&, const ContourCellCoord&);

class ContourCellSkeleton {
public:
  ContourCellCoord corner[3];
  ContourCellSkeleton() {}
  ContourCellCoord &operator[](int i) { return corner[i]; }
  const ContourCellCoord &operator[](int i) const { return corner[i]; }
};

std::ostream &operator<<(std::ostream &os, const ContourCellSkeleton&);

#endif // CONTOURCELL_H
