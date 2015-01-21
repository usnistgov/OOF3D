// -*- C++ -*-
// $RCSfile: contour.h,v $
// $Revision: 1.9.18.3 $
// $Author: langer $
// $Date: 2013/11/08 20:44:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// OBSOLETE IN 3D

#include <oofconfig.h>

#ifndef CONTOUR_H
#define CONTOUR_H

// These objects mostly manipulate lists of pointers to MasterCoords
// or ContourCoords.  ContourCoords are MasterCoords with an
// additional "value" member to store the contour value.  They live on
// the corners of the ContourCells and are owned by the ContourCells.
// The intersection points of contours and ContourCell edges are
// stored in a list of MasterCoord*'s that lives in each EdgeData
// object.

#include "engine/mastercoord.h"
#include <deque>
#include <string>
#include <vector>
class MasterElement;
class EdgeData;

// Forward declarations for things in this file.
class ContourCell;
class ContourCellSkeleton;
class EmbryonicContour;

std::ostream &operator<<(std::ostream&, const CCurve&);

class ContourCoord : public MasterCoord {
public:
  ContourCoord(double x, double y) : MasterCoord(x, y), value(0.0) {}
  ContourCoord(const MasterCoord &mc) : MasterCoord(mc), value(0.0) {}
  double value;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ContourState objects form the state machine for creating contours.

class ContourState {
protected:
  EmbryonicContour *embryo;
public:
  ContourState();
  ContourState(EmbryonicContour *embryo);
  virtual ~ContourState();
  virtual bool done() const { return false; }
  bool loopy() const;
  virtual CCurve *curve() const;
  virtual ContourState *next() const { return 0; }
  ContourState *evolve() const;
  void cleanup();
};


// A ContourCell is a triangular cell within an Element.  The function
// being plotted is evaluated at the corners of the cell and contours
// are determined by linearly interpolating within the cell.

class ContourCell {
private:
  bool checked_;
public:
  ContourCell(const std::vector<ContourCoord*> &);
  ContourCoord *corners[3];
  ContourCell *nbrs[3];
  EdgeData *edges[3];
  void set_nbr(const ContourCoord*, const ContourCoord*,
	       ContourCell*, EdgeData*);
  int cornerno(const ContourCoord*) const;
  void check(); // { checked_ = true; }
  void uncheck() { checked_ = false; }
  bool checked() const { return checked_; }
  friend class ContourCellSet;
};

std::ostream &operator<<(std::ostream&, const ContourCell&);

// A ContourCellSet is the set of contour cells for an Element. The
// ContourCellSet's constructor takes a list of ContourCellSkeletons
// and creates the ContourCells themselves. The skeletons have only
// the locations of the corners, while the cells also know information
// about their neighbors.  That information is generated in the
// ContourCellSet's constructor.

class ContourCellSet {
private:
  std::vector<ContourCell> cellList;
  std::vector<ContourCoord*> corners;
  std::vector<EdgeData*> edges;
public:
  ContourCellSet(const std::vector<ContourCellSkeleton*> &skeletons);
  ~ContourCellSet();
  void new_contour();
  std::vector<ContourCoord*> *getCorners() { return &corners; }
  void findIntercepts(const std::vector<double> *clevels);
  int size() const { return cellList.size(); }
  ContourCell &operator[](int i) { return cellList[i]; }
};

ContourCellSet *contourCellCache(MasterElement *master, int n);
void clearCache();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CContour {
private:
  std::vector<CCurve> *curves;
  std::vector<CCurve> *loops;
  void evolve(const ContourState*);
  void add_curve(const CCurve *curve);
  void join();
  void checkperimeter(const MasterElement*);
  void closealongboundary(const MasterElement*);
public:
  CContour(double value, int index);
  ~CContour();
  const double value;
  const int index;
  void compute(ContourCellSet*, MasterElement*, bool);
  std::vector<CCurve> *getCurves() const { return curves; }
  std::vector<CCurve> *getLoops() const { return loops; }
};

#endif // CONTOUR_H
