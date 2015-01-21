// -*- C++ -*-
// $RCSfile: contour.C,v $
// $Revision: 1.24.18.7 $
// $Author: fyc $
// $Date: 2014/08/01 21:10:36 $

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

#include "common/threadstate.h"
#include "common/printvec.h"
#include "common/tostring.h"
#include "engine/IO/contour.h"
#include "engine/contourcell.h"
#include "engine/mastercoord.h"
#include "engine/masterelement.h"
#include "engine/ooferror.h"
#include <algorithm>		// for std::sort
#include <map>
#include <utility>		// for std::pair

// Memory Allocation Note: Contours are made up of CCurves, which
// contain pointers to MasterCoords.  The EdgeData structures also
// contain pointers to the same MasterCoords, which are the
// intersection points of the contour with an edge of a ContourCell.
// It's the EdgeData structure that "owns" the MasterCoords, and which
// is in charge of allocating and deleting them.  The only contour
// points which are *not* in an EdgeData structure are the corners of
// the MasterElement, which are added to contours by
// MasterElement::perimeterSection.  The MasterCoord*s returned by
// perimeterSection are pointers to static data, and shouldn't be
// deleted.  So there's no memory leak if EdgeData does all the
// allocation and deletion.

class EdgeData {
private:
  // Intercepts are stored as MasterCoords instead of ContourCoords
  // since we don't need to store contour values in them. 
  std::vector<MasterCoord*> intercepts;
  void clear(int);
public:
  EdgeData(const ContourCoord *pt0, const ContourCoord *pt1)
    :  intercepts(0), pt0(pt0), pt1(pt1)
  {}
  virtual ~EdgeData();
  virtual void print(std::ostream&) const = 0;
  void findIntercepts(const std::vector<double> *cvalues);
  MasterCoord *getIntercept(int i) const { return intercepts[i]; }
  // ContourCoord *otherpoint(const ContourCoord*) const;
  const ContourCoord * const pt0, *pt1;
};

class BoundaryEdgeData : public EdgeData {
public:
  BoundaryEdgeData(const ContourCoord *pt0, const ContourCoord *pt1,
		   ContourCell *cell)
    : EdgeData(pt0, pt1), next(0), cell(cell)
  {}
  virtual void print(std::ostream&) const;
  BoundaryEdgeData *next; 
  ContourCell *cell;
};

class InteriorEdgeData : public EdgeData {
public:
  InteriorEdgeData(const ContourCoord *pt0, const ContourCoord *pt1)
    : EdgeData(pt0, pt1)
  {}
  virtual void print(std::ostream&) const;
};


EdgeData::~EdgeData() {
  clear(intercepts.size());
}

void EdgeData::clear(int n) {
  for(std::vector<MasterCoord*>::size_type i=0; i<intercepts.size(); i++) {
    delete intercepts[i];
    intercepts[i] = 0;
  }
  intercepts.resize(n, 0);
}

std::ostream &operator<<(std::ostream &os, const EdgeData &edge) {
  edge.print(os);
  return os;
}

void InteriorEdgeData::print(std::ostream &os) const {
  os << "InteriorEdgeData(" << *pt0 << ", " << *pt1 << ")";
}

void BoundaryEdgeData::print(std::ostream &os) const {
  os << "BoundaryEdgeData(" << *pt0 << ", " << *pt1 << ")";
}

void EdgeData::findIntercepts(const std::vector<double> *cvalues)
{
  int n = cvalues->size();
  clear(n);
  if(pt0->value == pt1->value) {
    intercepts.resize(n, 0);
  }
  else {
    MasterCoord vec = (*pt1 - *pt0)*(1./(pt1->value - pt0->value));
    double fmin, fmax;
    if(pt0->value < pt1->value) {
      fmin = pt0->value;
      fmax = pt1->value;
    }
    else {
      fmin = pt1->value;
      fmax = pt0->value;
    }
    intercepts.reserve(n);
    for(int i=0; i<n; i++) {
      double cval = (*cvalues)[i];
      if((fmin < cval) && (cval < fmax)) {
	intercepts[i] = new MasterCoord(*pt0 + vec*(cval - pt0->value));
      }
    }
  }
}

// ContourCoord *EdgeData::otherpoint(const ContourCoord *pt) const {
//   if(pt == pt0)
//     return pt1;
//   return pt0;
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// ContourCells store the address of their corners, instead of the
// coordinates themselves, to avoid roundoff when comparing points
// from different cells.  The ContourCellSet constructor makes sure to
// use pointers to the same ContourCoord objects when constructing
// cells.

ContourCell::ContourCell(const std::vector<ContourCoord*> &c)
  : checked_(false)
{
  corners[0] = c[0];
  corners[1] = c[1];
  corners[2] = c[2];
  for(int i=0; i<3; i++) {
    nbrs[i] = 0;
    edges[i] = 0;
  }
}

std::ostream &operator<<(std::ostream &os, const ContourCell &cell) {
  os << "ContourCell("
     << *cell.corners[0] << " [" << cell.corners[0]->value-1.0 << "], "
     << *cell.corners[1] << " [" << cell.corners[1]->value-1.0 << "], "
     << *cell.corners[2] << " [" << cell.corners[2]->value-1.0 << "])";
  return os;
}

void ContourCell::set_nbr(const ContourCoord *pt0, const ContourCoord *pt1,
			  ContourCell *othercell, EdgeData *edge)
{
  for(int i=0; i<3; i++) {
    int j = (i+1)%3;
    if(corners[i] == pt0 && corners[j] == pt1) {
      // nbrs[i] and edges[i] are opposite corner[i]
      int k = 3 - i - j;
      nbrs[k] = othercell;
      edges[k] = edge;
      return;
    }
  }
  throw ErrProgrammingError("Error in ContourCell::set_nbr", __FILE__,__LINE__);
}

int ContourCell::cornerno(const ContourCoord *pt) const {
  for(int i=0; i<3; i++)
    if(pt == corners[i])
      return i;
  // The error message will be evaluated by Python as a string in
  // single quotes, so the apostrophe needs to be protected (in
  // Python) with a backslash. To get the backslash into the C++
  // string, *it* needs to be protected with a backslash.
  throw ErrProgrammingError("Can\\'t find corner!", __FILE__, __LINE__);
}

void ContourCell::check() {
  checked_ = true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A ContourCellSet is the set of contour cells for an Element. The
// ContourCellSet's constructor takes a list of ContourCellSkeletons
// and creates the ContourCells themselves. The skeletons have only
// the locations of the corners, while the cells also know information
// about their neighbors.  That information is generated in the
// ContourCellSet's constructor.

// There is an operator< for MasterCoord*'s, and MasterCoord is a base
// class for ContourCoord, so an explicit comparison operator isn't
// needed for these maps.
typedef std::pair<const ContourCoord*, const ContourCoord*> CoordPair;
typedef std::map<CoordPair, ContourCell*> EdgeDict;
typedef std::map<const MasterCoord*, BoundaryEdgeData*> BdyMap;

ContourCellSet::ContourCellSet(const std::vector<ContourCellSkeleton*> 
			       &cellskeletons)
{
  // Make a list of the points at the corners of the cells. Points
  // will occur in more than one cell, so we have to check for
  // uniqueness.  Simultaneously, make sure that cells that share
  // points also share ContourCoords (ie refer to the same object),
  // which hopefully will allow faster dictionary lookup in
  // Contour.join.

  // ptlist[i] is the ContourCellCoord object used to construct corners[i].
  std::vector<ContourCellCoord> ptlist;

  for(std::vector<ContourCellSkeleton*>::size_type iskel=0; iskel<cellskeletons.size(); iskel++) {
    const ContourCellSkeleton &skelcell = *cellskeletons[iskel];
    std::vector<ContourCoord*> cellcorners(3);
    for(int j=0; j<3; j++) {	// loop over corners of cell skeleton
      const ContourCellCoord &skelcorner = skelcell.corner[j];
      // See if this point has already been found in another cell.
      // This linear search is inefficient but not done much, since
      // ContourCellSets are cached.
      bool found = 0;
      for(std::vector<ContourCellCoord>::size_type k=0; k<ptlist.size() && !found; k++) {
	if(ptlist[k] == skelcorner) {
	  cellcorners[j] = corners[k];
	  found = 1;
	}
      }
      if(!found) {
	ContourCoord *coord = new ContourCoord(skelcorner.x, skelcorner.y);
	corners.push_back(coord);
	ptlist.push_back(skelcorner);
	cellcorners[j] = coord;
      }
    }
    cellList.push_back(ContourCell(cellcorners));
  }

  // Assign neighbors and create EdgeData structures to hold contour
  // intercepts.  A cell stores a reference to itself in a dictionary,
  // edgedict, whose keys are the pairs of points that delineate each
  // edge of the cell.  When a second cell is found with the same
  // edge, it retrieves the first cell from the dictionary and they
  // joyfully identify themselves as neighbors.  Then they remove
  // their common edge from the dictionary.  Note that when stored in
  // the edgedict, the key is a pair of corners in counterclockwise
  // order, but when retrieved, the pair is in clockwise order.
  // That's because the pair is stored by one cell and retrieved by
  // the cell on the other side of the edge.

  EdgeDict edgedict; 

  for(std::vector<ContourCell>::size_type cellno=0; cellno<cellList.size(); cellno++) {
    ContourCell *cell = &cellList[cellno];
    for(int i=0; i<3; i++) {
      int j = (i+1)%3;
      ContourCoord *crnri = cell->corners[i];
      ContourCoord *crnrj = cell->corners[j];
      EdgeDict::iterator dictkey = edgedict.find(CoordPair(crnrj, crnri));
      if(dictkey == edgedict.end()) {
	// Didn't find the pair of corners in the dictionary
	edgedict[CoordPair(crnri, crnrj)] = cell;
      }
      else {
	ContourCell *nbr = (*dictkey).second;
	EdgeData *edgedata = new InteriorEdgeData(crnri, crnrj);
	edges.push_back(edgedata);
	nbr->set_nbr(crnrj, crnri, cell, edgedata);
	cell->set_nbr(crnri, crnrj, nbr, edgedata);
	edgedict.erase(dictkey);
      }
    }
  }

  // Any edges still in edgedict are exterior edges.  They have to be
  // linked up to define the element's perimeter.
  BdyMap startptdict;		// BoundaryEdgeData keyed by starting point
  for(EdgeDict::iterator i=edgedict.begin(); i!=edgedict.end(); ++i) {
    const ContourCoord *pt0 = (*i).first.first;
    const ContourCoord *pt1 = (*i).first.second;
    ContourCell *cell = (*i).second;
    BoundaryEdgeData *edgedata = new BoundaryEdgeData(pt0, pt1, cell);
    cell->set_nbr(pt0, pt1, 0, edgedata); // no neighbor
    edges.push_back(edgedata);
    startptdict[pt0] = edgedata;
  }
  for(BdyMap::iterator i=startptdict.begin(); i!=startptdict.end(); ++i) {
    BoundaryEdgeData *edata = (*i).second;
    edata->next = startptdict[edata->pt1];
  }
}

ContourCellSet::~ContourCellSet() {
  for(std::vector<ContourCoord*>::iterator i=corners.begin(); i<corners.end();
      ++i)
    delete *i;
  for(std::vector<EdgeData*>::iterator i=edges.begin(); i<edges.end(); ++i)
    delete *i;
}

void ContourCellSet::new_contour() {
  for(std::vector<ContourCell>::size_type i=0; i<cellList.size(); i++)
    cellList[i].uncheck();
}

void ContourCellSet::findIntercepts(const std::vector<double> *clevels) {
  for(std::vector<EdgeData*>::size_type i=0; i<edges.size(); i++)
    edges[i]->findIntercepts(clevels);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A ContourCellSet is a set of ContourCells for a particular element
// geometry and subdivision level.  It's used to store contour values
// and intercepts during a contour calculation.  Since it's moderately
// expensive to create, ContourCellSets are cached and reused.  That
// creates a thread-safety issue, since two simultaneous threads
// shouldn't use the same ContourCellSet.  Therefore ContourCellSets
// are only reused within a thread, and when the thread is done
// contouring, it has to clear the cache.

// The ContourCellCacheID identifies a ContourCellSet by element
// geometry, subdivision level, and thread.  It's used to retrieve
// ContourCellSets from the cache.

class ContourCellCacheID {
public:
  const int threadno;
  const int ncells;
  const MasterElement *element;
  ContourCellCacheID(const MasterElement *element, int ncells);
  ~ContourCellCacheID(); 
};

std::ostream &operator<<(std::ostream &os, const ContourCellCacheID &id) {
  os << "ContourCellCacheID(" << id.threadno << ", " << id.ncells << ", "
     << id.element << ")";
  return os;
}

ContourCellCacheID::ContourCellCacheID(const MasterElement *element, int ncells)
  : threadno(findThreadNumber()), ncells(ncells), element(element)
{}

ContourCellCacheID::~ContourCellCacheID() {}


// Less-than function for ContourCellCacheID objects allows them to be
// used as std::map keys.
bool operator<(const ContourCellCacheID &a, const ContourCellCacheID &b) {
  if(a.threadno < b.threadno) return 1;
  if(a.threadno > b.threadno) return 0;
  if(a.ncells < b.ncells) return 1;
  if(a.ncells > b.ncells) return 0;
  if(a.element < b.element) return 1;
  return 0;
}

typedef std::map<ContourCellCacheID, ContourCellSet*> ContourCellCache;

static ContourCellCache cache;
static Lock cacheLock;

// Retrieve the set of (2)n^2 contour cells for the given master
// element, and create the set if necessary.

ContourCellSet *contourCellCache(MasterElement *master, int n) {
  ContourCellCacheID id(master, n);
  ContourCellCache::iterator i = cache.find(id);
  if(i == cache.end()) {
    // contourcells returns a "new" pointer, so SWIG will not make
    // extra copies -- this is slightly ugly for us here.
    //* TODO 3.1: that comment is obsolete.  contourcells isn't swigged
    //* anymore.  If the ContourCellSet constructor took master and n
    //* as args, then we wouldn't need skel here at all.
    cacheLock.acquire();
    ContourCellSet *cset = 0;
    try {
      std::vector<ContourCellSkeleton*> *skel = master->contourcells(n);
      cset = new ContourCellSet( *skel );
      for(std::vector<ContourCellSkeleton*>::iterator s=skel->begin();
	  s<skel->end(); ++s)
	delete *s;
      delete skel;
      cache[id] = cset;
    }
    catch (...) {
      cacheLock.release();
      throw;
    }
    cacheLock.release();
    return cset;
  }
  return (*i).second;
}

// Remove all cached contour cells for this thread id.

void clearCache() {
  int threadno = findThreadNumber();
  std::vector<ContourCellCache::iterator> erasures;
  cacheLock.acquire();
  try {
    for(ContourCellCache::iterator i=cache.begin(); i!=cache.end(); ++i) {
      if((*i).first.threadno == threadno) {
	delete (*i).second;
	// We used to call cache.erase(i) here, on the presumption
	// that because erasing data from a std::map doesn't
	// invalidate iterators other than the iterator being erased,
	// it was ok to erase an item and then increment its iterator.
	// That doesn't seem to be true with clang++ in OS X 10.9, so
	// now we keep a list of the iterators to be erased and erase
	// them in a separate loop.
	erasures.push_back(i);
      }
    }
    for(unsigned int i=0; i<erasures.size(); i++) {
      cache.erase(erasures[i]);
    }
  }
  catch (...) {
    cacheLock.release();
    throw;
  }
  cacheLock.release();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// EmbryonicContours are passed from ContourState object to
// ContourState object as the contour is constructed.  They may be
// only part of a full contour.

class EmbryonicContour {
public:
  EmbryonicContour(const MasterCoord *start, const CContour &contour,
		   const ContourCellSet &cells, bool close)
    : contourValue(contour.value),
      contourIndex(contour.index),
      cellset(cells),
      close(close)
  {
    curve.push_back(start);
  }
  CCurve curve;
  const double contourValue;
  const int contourIndex;
  const ContourCellSet &cellset;
  const bool close;
};

std::ostream &operator<<(std::ostream &os, const EmbryonicContour &ebc) {
  os << "EmbryonicContour:";
  for(CCurve::const_iterator i=ebc.curve.begin(); i<ebc.curve.end(); ++i)
    os << " " << *(*i);
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int nContourStates = 0;
int nDeleted = 0;
int nCreated = 0;


ContourState::ContourState() : embryo(0) {
  ++nContourStates;
  ++nCreated;
}

ContourState::ContourState(EmbryonicContour *embryo)
  : embryo(embryo)
{
  ++nContourStates;
  ++nCreated;
}

ContourState::~ContourState() {
  --nContourStates;
  ++nDeleted;
}

bool ContourState::loopy() const {
  return embryo && embryo->curve.size() > 1 &&
    *embryo->curve.begin() == *embryo->curve.rbegin();
}


ContourState *ContourState::evolve() const {
  ContourState *state = next();
  while(!state->done() && !state->loopy()) {
    ContourState *lastState = state;
    state = lastState->next();
    delete lastState;
  }
  return state;
}

CCurve *ContourState::curve() const {
  if(embryo)
    return &(embryo->curve);
  return 0;
}

void ContourState::cleanup() {
  delete embryo;
}

// -----------

class Contour_Finished : public ContourState {
public:
  Contour_Finished() {}
  Contour_Finished(EmbryonicContour *mbrio) {
    embryo = mbrio;		
  }
  virtual bool done() const { return true; }
};

class Contour_StartOnEdge : public ContourState {
private:
  const EdgeData * const edge;
  ContourCell &cell;
public:
  Contour_StartOnEdge(ContourCell &cell, 
		      CContour &contour, const EdgeData * const edge,
		      const ContourCellSet &cells, bool close);
  virtual ContourState *next() const;
  bool loopy() const { return false; }
};

class Contour_StartAlongEdge : public ContourState {
private:
  ContourCell &cell;
  const ContourCellSet &cells;	// This is being initialized in the constructor and passed to EmbryonicContour.
  int endno;
public:
  Contour_StartAlongEdge(ContourCell &cell, const ContourCellSet &cells,
			 CContour &contour, bool close);
  virtual ContourState *next() const;
  virtual bool loopy() const { return false; }
};

class Contour_EnterViaEdge : public ContourState {
private:
  const EdgeData *edge;
  ContourCell &cell;
public:
  Contour_EnterViaEdge(ContourCell&, const EdgeData*, EmbryonicContour*);
  virtual ContourState *next() const;
};

class Contour_LeaveViaEdge : public ContourState {
private:
  ContourCell &cell;
  const int edgeno;
public:
  Contour_LeaveViaEdge(ContourCell&, int edgeno,
		       EmbryonicContour *embryo);
  virtual ContourState *next() const;
};

class Contour_LeaveViaCorner : public ContourState {
private:
  ContourCell &cell;
  const int cornerno;
public:
  Contour_LeaveViaCorner(ContourCell &cell, int cornerno,
			 EmbryonicContour *embryo);
  virtual ContourState *next() const;
};

// ---------------

Contour_StartOnEdge::Contour_StartOnEdge(ContourCell &cell, 
					 CContour &contour,
					 const EdgeData * const edge,
					 const ContourCellSet &cells,
					 bool close)
  : edge(edge), cell(cell)
{
  // At this point, we know that edge->getIntercept() will return a
  // non-null pointer.
  embryo = new EmbryonicContour(edge->getIntercept(contour.index),
				contour, cells, close);
}

ContourState *Contour_StartOnEdge::next() const {
  // which edge are we?
  for(int i=0; i<3; i++) {
    if(cell.edges[i] == edge) {	// pointer comparison
      // we're edge i
      if(cell.corners[i]->value == embryo->contourValue) {
	// Point on the opposite corner is on the contour.  See if
	// we're headed the right direction.  We want to keep the
	// higher values on the left.
	if(cell.corners[(i+1)%3]->value > embryo->contourValue) {
	  embryo->curve.push_back(cell.corners[i]);
	  return new Contour_LeaveViaCorner(cell, i, embryo);
	}
	else {			// going the wrong way
	  embryo->curve.push_front(cell.corners[i]);
	  return new Contour_LeaveViaEdge(cell, i, embryo);
	}
      }	// end if(cell.corners[i]->value == embryo.contourValue)
      // Leave through one of the other sides
      //     --------------  corner i
      //     \            /
      //      \          /
      //       \        /
      //        *- - - >
      // edge i  \    /    edge k
      //          \  /
      //           \/
      for(int k=(i+1)%3; k!=i; k=(k+1)%3) {
	EdgeData *otheredge = cell.edges[k];
	MasterCoord *intercept = otheredge->getIntercept(embryo->contourIndex);
	if(intercept) {
	  // Check direction, keeping higher values on the left
	  if(cell.corners[(i+1)%3]->value > embryo->contourValue) {
	    embryo->curve.push_back(intercept);
	    return new Contour_LeaveViaEdge(cell, k, embryo);
	  }
	  else {		// going the wrong way
	    embryo->curve.push_front(intercept);
	    return new Contour_LeaveViaEdge(cell, i, embryo);
	  }
	} // end if(intercept)
      } // end loop over k
    } // end if(cell.edges[i] == edge)
  } // end loop over edges i
  throw ErrProgrammingError("Contour_StartOnEdge couldn\\'t find a way out!",
			    __FILE__, __LINE__);
};

// -----------

Contour_StartAlongEdge::Contour_StartAlongEdge(ContourCell &cell,
					       const ContourCellSet &cells,
					       CContour &contour, bool close)
  : cell(cell), cells(cells)
{
  // First, check to see if we can really start here.  We know a
  // priori that exactly two of the cells corners are at the contour
  // value.  If the third corner is above the contour value, then the
  // "stay to the right" rule means that we should have been
  // considering the cell's neighbor instead.  See the comment in
  // Contour_LeaveViaCorner::next().

  // TODO OPT: Is this check already done by CContour::compute(), before
  // creating Contour_StartAlongEdge?  compute() could pass in the
  // correct corner and this routine wouldn't need to think at all.

  for(int i=0; i<3; i++) {
    if(cell.corners[i]->value != contour.value) {
      // OK to start here. Because corner i is below the contour, if
      // the contour goes clockwise (ie from i+2 to i+1) it will have
      // the high ground on the left.
      int startno = (i+2)%3;
      endno = (i+1)%3;
      embryo = new EmbryonicContour(cell.corners[startno],contour,cells,close);
      embryo->curve.push_back(cell.corners[endno]);
      return;
    }
  }
  throw ErrProgrammingError("Contour_StartAlongEdge can\'t get started!",
			    __FILE__, __LINE__);
}

ContourState *Contour_StartAlongEdge::next() const {
  return new Contour_LeaveViaCorner(cell, endno, embryo);
}

// ------------

Contour_EnterViaEdge::Contour_EnterViaEdge(ContourCell &cell,
					   const EdgeData *edge,
					   EmbryonicContour *embryo)
  : ContourState(embryo), edge(edge), cell(cell)
{}

ContourState *Contour_EnterViaEdge::next() const {
  if(cell.checked())
    return new Contour_Finished(embryo);
  cell.check();
  // Which edge are we?
  for(int i=0; i<3; i++) {
    if(cell.edges[i] == edge) {	// we're edge i
      if(cell.corners[i]->value == embryo->contourValue) {
	// Point on the opposite corner is on the contour
	embryo->curve.push_back(cell.corners[i]);
	return new Contour_LeaveViaCorner(cell, i, embryo);
      }
      // We'd better leave through another edge
      for(int j=1; j<3; j++) {
	int k = (i+j)%3;
	EdgeData *otheredge = cell.edges[k];
	MasterCoord *intercept = otheredge->getIntercept(embryo->contourIndex);
	if(intercept) {
	  embryo->curve.push_back(intercept);
	  return new Contour_LeaveViaEdge(cell, k, embryo);
	}
      }	// end loop over other edges j
    } // end if(cell.edges[i] == edge)
  } // end loop over edges i
  throw ErrProgrammingError("Can\'t find way out of ContourCell",
			    __FILE__, __LINE__);
}

// --------------

Contour_LeaveViaEdge::Contour_LeaveViaEdge(ContourCell &cell, int edgeno,
					   EmbryonicContour *embryo)
  : ContourState(embryo), cell(cell), edgeno(edgeno)
{}

ContourState *Contour_LeaveViaEdge::next() const {
  ContourCell *nextcell = cell.nbrs[edgeno];
  if(!nextcell)
    return new Contour_Finished(embryo);
//     return new Contour_HitBdy(cell, edgeno, embryo);
  return new Contour_EnterViaEdge(*nextcell, cell.edges[edgeno], embryo);
}

// -------------

Contour_LeaveViaCorner::Contour_LeaveViaCorner(ContourCell &cell,
					       int cornerno,
					       EmbryonicContour *embryo)
  : ContourState(embryo), cell(cell), cornerno(cornerno)
{}

ContourState *Contour_LeaveViaCorner::next() const {
  // Here we invoke the "stay to the right" rule, by going around the
  // corner counterclockwise from the cell we're leaving, looking for
  // the first possible way out.  The cell was entered either from
  // point a or point 1, and now we're at point 0.  If we entered at
  // 1, then there's no need to check for an exit at 2, since the
  // stay-to-the-right rule says that we'd have gone from 1 to 2
  // directly.  If we entered at a, then 2 can't be on the contour, so
  // we still don't need to check it.  When we get back around to cell
  // Z, it's ok to check for an exit at 1, *even if* we entered there,
  // since that will pick up the correct degenerate contour loop.
  //
  //      \   /           Leaving cell A via corner 0,
  //       \ /   C        first look at cell B, which is nbr[1] of A.
  //   -----x--------c    The two possible cases are leaving B via point
  //   Z   /0\  B   /     b, or leaving via the BC edge at point c.
  //      /   \    /b     (Point 2 can't be on the contour, so we don't
  // \   /  A  \  /       have to check the edge between A and B.)
  //  \ /1     2\/
  //    ----a----q         After checking B, check C, and so on.

  ContourCell *othercell = cell.nbrs[(cornerno+1)%3]; // ie, cell B

  while(othercell != &cell) {
    if(!othercell) {		// At a boundary
	return new Contour_Finished(embryo);
    }
    else {			// othercell is not null 
      // Which corner of othercell is node 0 of this cell?
      int othercornerno = othercell->cornerno(cell.corners[cornerno]);
      if(!othercell->checked()) {
	othercell->check();
	// Can we go out through the far edge of the cell?
	EdgeData *faredge = othercell->edges[othercornerno];
	MasterCoord *intercept = faredge->getIntercept(embryo->contourIndex);
	if(intercept) {
	  embryo->curve.push_back(intercept);
	  return new Contour_LeaveViaEdge(*othercell, othercornerno, embryo);
	}
	// Can we go out along the edge between this cell and the next
	// one?  ptc is point c in the diagram.
	ContourCoord *ptc = othercell->corners[(othercornerno+2)%3];
	ContourCoord *ptq = othercell->corners[(othercornerno+1)%3];
	if(ptc->value==embryo->contourValue && ptq->value<embryo->contourValue){
	  embryo->curve.push_back(ptc);
	  return new Contour_LeaveViaCorner(*othercell, (othercornerno+2)%3,
					    embryo);
	}
      }	// end if(!othercell->checked())
      // No luck, go to next cell counterclockwise around the corner
      othercell = othercell->nbrs[(othercornerno+1)%3];
    } // end if(othercell)
  } // end while(othercell != cell)
  // If we got here, there's no place left to go.
  return new Contour_Finished(embryo);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CContour::CContour(double value, int index)
  : value(value), index(index)
{
  curves = new std::vector<CCurve>;
  loops = new std::vector<CCurve>;
}

CContour::~CContour() {
  delete curves;
  delete loops;
}

void CContour::compute(ContourCellSet *cells, MasterElement *master, bool close)
{
  cells->new_contour();		// resets "checked" flag
  for(int i=0; i<cells->size(); i++) { // look at all cells...
    ContourCell &cell = (*cells)[i];
    if(!cell.checked()) {	// ... that haven't been checked yet
      cell.check();
      bool done = false;
      // Does this contour cross an edge of the cell?
      for(int edgeno=0; edgeno<3 && !done; edgeno++) {
	EdgeData *edge = cell.edges[edgeno];
	MasterCoord *intercept = edge->getIntercept(index);
	if(intercept) {
	  evolve(new Contour_StartOnEdge(cell, *this, edge, *cells, close));
	  done = true;
	}
      }	// end loop over edges
      if(!done) {
	// Contour doesn't cross an edge. Does it cross two nodes?  If
	// it crosses one node but no edges, then it doesn't really
	// cross the cell.  If it crosses three nodes, the cell is
	// entirely on the contour and the neighboring cells will take
	// care of the drawing.
	int ncoincidences = 0;
	for(int icorn=0; icorn<3; icorn++) {
	  if(cell.corners[icorn]->value == value)
	    ncoincidences++;
	}
	if(ncoincidences == 2) {
	  // If the third corner is above the contour value, then the
	  // "stay to the right" rule means that we should have been
	  // considering the cells's neighbor instead.  See comment in
	  // Contour_LeaveViaCorner::next().
	  bool ok = true;
	  for(int i=0; i<3 && ok; i++) {
	    if(cell.corners[i]->value != value) {
	      if(cell.corners[i]->value > value) {
		ok = false;
	      }
	    }
	  }
	  if(ok) {
	    evolve(new Contour_StartAlongEdge(cell, *cells, *this, close));
	    done = true;
	  }
	}
      }	// end if(!done)
    } // end if(!cell.checked())
  } // end loop over cells
  join();
  if(close) {
    closealongboundary(master);
    checkperimeter(master);
  }
}
  
void CContour::evolve(const ContourState *state) {
  const ContourState *firststate = state;
  ContourState *finalstate = state->evolve();
  CCurve *curve = finalstate->curve();
  if(curve) {
    add_curve(curve);		// copies curve
  }
  finalstate->cleanup();
  delete finalstate;
  delete firststate;
}

void CContour::add_curve(const CCurve *curve) {
  // Make sure to copy the curve. Up to now it's been living in the
  // EmbryonicContour, which will be deleted.
  if(curve->front() == curve->back()) {
    if(curve->size() > 2)
      loops->push_back(CCurve(curve->begin(), --curve->end()));
  }
  else if(curve->size() > 1) {
    curves->push_back(CCurve(*curve));
  }
}

void CContour::join() {
  // Examine curves one by one, seeing if each can connect to a
  // previously examined curve.  It it can, it is.  Attaching a curve
  // can change the list of examined curves, since one curve can join
  // two others or close a loop (in which case the loop is removed
  // from further consideration), so we have to be careful not to
  // modify the list while looping over it.
  std::vector<CCurve> *newcurves = new std::vector<CCurve>;
  for(std::vector<CCurve>::iterator ic=curves->begin(); ic<curves->end(); ++ic){
    // Look for possible connections in the list of examined curves,
    // without modifying the list yet.
    CCurve &curve = *ic;
    std::vector<CCurve>::iterator the_end = newcurves->end();
    std::vector<CCurve>::iterator headconnector = the_end;
    std::vector<CCurve>::iterator tailconnector = the_end;
    for(std::vector<CCurve>::iterator i=newcurves->begin();
	i<the_end && (headconnector==the_end || tailconnector==the_end);
	++i)
      {
	CCurve &othercurve = *i;
	if(*curve.rbegin() == *othercurve.begin()) // compares MasterCoord*'s
	  tailconnector = i;
	if(*curve.begin() == *othercurve.rbegin())
	  headconnector = i;
    }
    // Now make the connections, if any.
    if(headconnector != the_end && tailconnector != the_end) {
      // connection at both ends
      if(headconnector == tailconnector) { // curve closes a loop
	CCurve &othercurve = *headconnector;
	othercurve.insert(othercurve.end(), ++curve.begin(), --curve.end());
	loops->push_back(othercurve);
	newcurves->erase(headconnector);
      }
      else {			// curve links two others without looping
	CCurve &headcurve = *headconnector;
	CCurve tailcurve = *tailconnector;
	headcurve.insert(headcurve.end(), ++curve.begin(), curve.end());
	headcurve.insert(headcurve.end(), ++tailcurve.begin(), tailcurve.end());
	newcurves->erase(tailconnector);
      }
    }
    else if(tailconnector != the_end) {
      // Curve connects at its end, but not its beginning.
      CCurve &othercurve = *tailconnector;
      curve.insert(curve.end(), ++othercurve.begin(), othercurve.end());
      newcurves->erase(tailconnector);
      newcurves->push_back(curve);
    }
    else if(headconnector != the_end) {
      // Curve connects at its beginning, but not its end.
      CCurve &othercurve = *headconnector;
      othercurve.insert(othercurve.end(), ++curve.begin(), curve.end());
    }
    else {
      // Curve doesn't connect to any previously examined curve.
      newcurves->push_back(curve);
    }
  }
  delete curves;
  curves = newcurves;
}

void CContour::closealongboundary(const MasterElement *master) {
  // Look for endpoints that are on the element boundary and join them
  // up with new curve segments.
  if(curves->size() == 0)
    return;

  // Make a list of endpoints on the boundary.
  std::vector<MasterEndPoint> endpts;
  endpts.reserve(2*curves->size());
  for(std::vector<CCurve>::const_iterator i=curves->begin();i<curves->end();++i)
    {
      endpts.push_back(MasterEndPoint((*i).front(), true));
      endpts.push_back(MasterEndPoint((*i).back(), false));
    }
  // Sort the list in counter clockwise order.  The ordering for
  // MasterEndPoints puts the ends of curves before the beginnings, if
  // the points conincide.
  std::sort(endpts.begin(), endpts.end(), master->bdysorter());
  unsigned int j = 0;
  if(endpts[0].start) j = 1;
  while(j < endpts.size()) {
    const MasterCoord *start = endpts[j].mc;
    const MasterCoord *end = endpts[(j+1)%endpts.size()].mc;
    CCurve *newcurve = master->perimeterSection(start, end);
    add_curve(newcurve);
    delete newcurve;
    j += 2;
  }
  join();
}

double area(const CCurve &loop) {
  double a = cross(*loop.back(), *loop[0]);
  for(CCurve::size_type i=1; i<loop.size(); i++) {
    a += cross(*loop[i-1], *loop[i]);
  }
  return 0.5*a;
}

void CContour::checkperimeter(const MasterElement *master) {
  // If the contour consists of backward loops in the middle of the
  // element, surround the whole element with a forward loop.  This
  // happens if there is a depression in the middle of the element.
  double totalarea = 0.0;
  for(std::vector<CCurve>::size_type i=0; i<loops->size(); i++)
    totalarea += area((*loops)[i]);
  if(totalarea < 0) {
    const std::vector<const MasterCoord*> &perimeter(master->perimeter());
    loops->push_back(CCurve(perimeter.begin(), perimeter.end()));
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const CCurve &curve) {
  os << "CCurve(";
  if(curve.size() > 0) {
    os << *curve[0];
    for(CCurve::size_type i=1; i<curve.size(); i++)
      os << ", " << *curve[i];
  }
  os << ")";
  return os;
}
