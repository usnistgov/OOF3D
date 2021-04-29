// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/ghostoofcanvas.h"
#include "common/IO/oofcerr.h"
#include "common/IO/vtkutils.h"
#include "common/VSB/vsb.h"
#include "common/cdebug.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/geometry.h"
#include "common/printvec.h"
#include "common/progress.h"
#include "common/timestamp.h"
#include "common/tostring.h"
#include "common/voxelsetboundary.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletongroups.h"
#include "engine/femesh.h"
#include "engine/homogeneity.h"
#include "engine/masterelement.h"
#include "engine/material.h"
#include "engine/skeletonfilter.h"

#include <algorithm>
#include <limits>
#include <math.h>
#include <set>
#include <map>
#include <vtkCellLocator.h>
#include <vtkDataArray.h>
#include <vtkGenericCell.h>
#include <vtkIntArray.h>
#include <vtkMergePoints.h>
#include <vtkPointData.h>
#include <vtkTetra.h>
#include <vtkUnstructuredGrid.h>
#include <vtkVersionMacros.h>

// Names needed for PythonExportable base class
const std::string CSkeletonBase::modulename_("ooflib.SWIG.engine.cskeleton2");
const std::string CSkeleton::classname_("CSkeleton");
const std::string CDeputySkeleton::classname_("CDeputySkeleton");

unsigned long CSkeletonBase::uidbase = 0;

// Values used when setting the size of the bins used in
// VoxelSetBoundary construction.  The nominal linear size of the bins
// is the cube root of average element volume time VSB_FUDGE, but not
// less than MIN_VSB_BINSIZE.  The size is set to DEFAULT_VSB_BIN if
// no other information is available with which to make a better
// choice.
#define VSB_FUDGE 8.0
#define DEFAULT_VSB_BIN 20
#define MIN_VSB_BINSIZE 5


CSkeletonBase::CSkeletonBase()
  : illegal_(false),
    defaultVSBbin(DEFAULT_VSB_BIN, DEFAULT_VSB_BIN, DEFAULT_VSB_BIN)
{
  // oofcerr << "CSkeletonBase::ctor: " << this << std::endl;
  uid = uidbase;
  ++uidbase;
  illegal_ = false;
  illegalCount = 0;
  suspectCount = 0;
  homogeneityIndex = 0;
  unweightedHomogIndex = 0;
  unweightedShapeEnergy = 0;
  weightedShapeEnergy = 0;
  homogeneity_index_computation_time.backdate();
  unweighted_homogeneity_computation_time.backdate();
  unweighted_shape_energy_computation_time.backdate();
  weighted_shape_energy_computation_time.backdate();
  illegality_computation_time.backdate();
  
  illegal_count_computation_time.backdate();
  suspect_count_computation_time.backdate();
  vsbTimeStamp.backdate();
}

CSkeletonBase::~CSkeletonBase() {
  // oofcerr << "CSkeletonBase::dtor: " << this << std::endl;
  clearVSBs();
}

const TimeStamp &CSkeletonBase::getTimeStamp() const {
  const TimeStamp &mts = getMicrostructure()->getTimeStamp();
  if(mts > geometry_timestamp)
    return mts;
  return geometry_timestamp;
}

void CSkeletonBase::incrementTimestamp() {
  ++geometry_timestamp;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeleton::CSkeleton(CMicrostructure *ms, bool prdcty[DIM])
  : CSkeletonBase(),
    grid(vtkSmartPointer<vtkUnstructuredGrid>::New()),
    points(vtkSmartPointer<vtkPoints>::New()),
    zombie(false)
{
  // oofcerr << "CSkeleton::ctor: this=" << *this << " " << this << std::endl;
  MS = ms;
  size = Coord(MS->size());
  volume_ = 1;
  for(int i=0; i<DIM; ++i)
    volume_ *= size[i];
  periodicity = prdcty;
  
  grid->SetPoints(points);

  deputy = NULL;		// the currently active deputy

  washMe = false;
  numDefunctNodes = 0;
  // oofcerr << "CSkeleton::ctor: done" << std::endl;
}

// Creating a new CSkeleton from Python should always be done by
// calling newCSkeleton.  The CSkeleton constructor isn't swigged, so
// that Python won't have ownership of any CSkeletons.

CSkeleton *newCSkeleton(CMicrostructure *ms, bool prdcty[DIM]) {
  return new CSkeleton(ms, prdcty);
}

CSkeleton::~CSkeleton() {
  // oofcerr << "CSkeleton::dtor: this=" << this << std::endl;
  grid->SetPoints(0);		// not sure that this is necessary...

  // Clearing deputy_list is not necessary because the deputies should
  // all be destroyed before the sheriff.
  assert(deputy_list.empty());

  for(CSkeletonNodeIterator nit=nodes.begin(); nit!=nodes.end(); ++nit)
    delete (*nit);
  nodes.clear();

  for(CSkeletonElementIterator eit = elements.begin(); eit!=elements.end();
      ++eit)
    delete (*eit);
  elements.clear();

  for(CSkeletonSegmentMap::iterator sit=segments.begin();
      sit!=segments.end(); ++sit)
    delete (*sit).second;
  segments.clear();

  for(CSkeletonFaceMap::iterator fit=faces.begin(); fit!=faces.end(); ++fit)
    delete (*fit).second;
  faces.clear();

  for(CSkeletonPointBoundaryMap::iterator pbit = pointBoundaries.begin(); 
      pbit != pointBoundaries.end(); ++pbit)
    delete (*pbit).second;

  for(CSkeletonEdgeBoundaryMap::iterator ebit = edgeBoundaries.begin(); 
      ebit != edgeBoundaries.end(); ++ebit)
    delete (*ebit).second;

  for(CSkeletonFaceBoundaryMap::iterator fbit = faceBoundaries.begin(); 
      fbit != faceBoundaries.end(); ++fbit)
    delete (*fbit).second;
}

void CSkeleton::destroy() {
  // oofcerr << "CSkeleton::destroy: this=" << this << " nDeputies=" << nDeputies()
  //  	  << std::endl;
  if(nDeputies() == 0) {
    // oofcerr << "CSkeleton::destroy: deleting " << this << std::endl;
    delete this;
  }
  else {
    // oofcerr << "CSkeleton::destroy: zombifying " << this << std::endl;
    zombie = true;
  }
}

void CSkeleton::destroyZombie() {
  if(zombie && nDeputies() == 0) {
    // oofcerr << "CSkeleton::destroyZombie: deleting " << this << std::endl;
    delete this;
  }
}

void CSkeleton::createPointGrid(int m, int n, int l) {
  // Called by SkeletonGeometry.__call__.  See TetraSkeleton in
  // cskeleton2.spy.
  double dx = size[0]/(double) m;
  double dy = size[1]/(double) n;
  double dz = size[2]/(double) l;
  int total = (m+1)*(n+1)*(l+1), i, j, k;
  Coord x;

  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("Allocating nodes", DEFINITE));

  try {
    points->Allocate(total, total);
    nodes.reserve(total);

    CSkeletonPointBoundary *blf = getPointBoundary("XminYminZmax", true);
    CSkeletonPointBoundary *brf = getPointBoundary("XmaxYminZmax", true);
    CSkeletonPointBoundary *tlf = getPointBoundary("XminYmaxZmax", true);
    CSkeletonPointBoundary *trf = getPointBoundary("XmaxYmaxZmax", true);
    CSkeletonPointBoundary *blb = getPointBoundary("XminYminZmin", true);
    CSkeletonPointBoundary *brb = getPointBoundary("XmaxYminZmin", true);
    CSkeletonPointBoundary *tlb = getPointBoundary("XminYmaxZmin", true);
    CSkeletonPointBoundary *trb = getPointBoundary("XmaxYmaxZmin", true);
  
    // TODO 3.1: Why are these loops in this order?  It probably doesn't
    // matter.  Changing it may break many of the tests...
    for(i=0; i<n+1; ++i) { // y dimension
      for(j=0; j<m+1; ++j) {  // x dimension
	for(k=0; k<l+1; ++k) {  // z dimension
	  // TODO OPT: There's no need to treat the i,j,k==0 cases explicitly.
	  if(j==m)
	    x[0] = size[0];
	  else if(j==0)
	    x[0] = 0.0;
	  else
	    x[0] = j*dx;
	  if(i==n)
	    x[1] = size[1];
	  else if(i==0)
	    x[1] = 0.0;
	  else
	    x[1] = i*dy;
	  if(k==l)
	    x[2] = size[2];
	  else if(k==0)
	    x[2] = 0.0;
	  else
	    x[2] = k*dz;
	
	  CSkeletonNode *node = addNode(x);

	  // TODO OPT: need way of storing partnerships

	  // Add nodes to default point boundaries
	  if(i==0 and j==0 and k==0)
	    blb->addNode(node);
	  if(i==0 and j==m and k==0)
	    brb->addNode(node);
	  if(i==n and j==0 and k==0)
	    tlb->addNode(node);
	  if(i==n and j==m and k==0)
	    trb->addNode(node);                   
	  if(i==0 and j==0 and k==l)
	    blf->addNode(node);
	  if(i==0 and j==m and k==l)
	    brf->addNode(node);
	  if(i==n and j==0 and k==l)
	    tlf->addNode(node);
	  if(i==n and j==m and k==l)
	    trf->addNode(node);

	  if(progress->stopped()) {
	    progress->finish();
	    return;
	  }
	  int ndone = (i*(m+1) + j)*(l+1) + k+1;
	  progress->setFraction(ndone/float(total));
	  progress->setMessage(to_string(ndone) + "/" + to_string(total)
			       + " nodes");
	}
      }
    }
  }
  catch (...) {
    progress->finish();
    throw;
  }
  progress->finish();
}

CSkeletonNode *CSkeleton::addNode(const Coord &x) {
  int nidx = points->InsertNextPoint(x.xpointer());
  CSkeletonNode *node = new CSkeletonNode(nidx, points);
  if(x[0] == 0.0 || x[0] == size[0]) node->setMobilityX(0);
  if(x[1] == 0.0 || x[1] == size[1]) node->setMobilityY(0);
#if DIM==3
  if(x[2] == 0.0 || x[2] == size[2]) node->setMobilityZ(0);
#endif
  nodes.push_back(node);
  return node;
}

void CSkeleton::createTetra(const TetArrangement *arrangement,
			    int m, int n, int l)
{
  int total = 5*m*n*l;
  grid->Allocate(total, total);
  elements.reserve(total);

  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("Creating elements from nodes",
						DEFINITE));
  try {
    // arrangement is a pointer so that it can be swigged.
    bool flip = (*arrangement == MIDDLING_ARRANGEMENT);
    // if(*arrangement == MODERATE_ARRANGEMENT) 
    //   flip = 0;
    // else if(*arrangement == MIDDLING_ARRANGEMENT)
    //   flip = 1;

    ICoord lim = ICoord(n,m,l);

    for(int i=0; i<n; ++i) { // y dimension
      for(int j=0; j<m; ++j) {  // x dimension
	for(int k=0; k<l; ++k) {  // z dimension

	  int element_count = 5*(i*m*l+j*l+k);

	  int ulf = (i+1)*(m+1)*(l+1)+j*(l+1)+k+1;      // upper left front
	  int urf = (i+1)*(m+1)*(l+1)+(j+1)*(l+1)+k+1;  // upper right front
	  int lrf = i*(m+1)*(l+1)+(j+1)*(l+1)+k+1;      // lower right front
	  int llf = i*(m+1)*(l+1)+j*(l+1)+k+1;          // lower left front 
	  int ulb = (i+1)*(m+1)*(l+1)+j*(l+1)+k;        // upper left back
	  int urb = (i+1)*(m+1)*(l+1)+(j+1)*(l+1)+k;    // upper right back 
	  int lrb = i*(m+1)*(l+1)+(j+1)*(l+1)+k;        // lower right back
	  int llb = i*(m+1)*(l+1)+j*(l+1)+k;            // lower left back

	  if(!flip) {
	    vtkIdType ids1[4] = {llf, urf, lrf, lrb};
	    createElement(VTK_TETRA, 4, ids1);
	    vtkIdType ids2[4] = {llf, ulf, urf, ulb};
	    createElement(VTK_TETRA, 4, ids2);
	    vtkIdType ids3[4] = {lrb, urf, urb, ulb};
	    createElement(VTK_TETRA, 4, ids3);
	    vtkIdType ids4[4] = {llf, lrb, llb, ulb};
	    createElement(VTK_TETRA, 4, ids4);
	    vtkIdType ids5[4] = {llf, ulb, urf, lrb};
	    createElement(VTK_TETRA, 4, ids5);
	  }
	  else {
	    vtkIdType ids1[4] = {llf, ulf, lrf, llb};
	    createElement(VTK_TETRA, 4, ids1);
	    vtkIdType ids2[4] = {ulf, urf, lrf, urb};
	    createElement(VTK_TETRA, 4, ids2);
	    vtkIdType ids3[4] = {ulf, ulb, urb, llb};
	    createElement(VTK_TETRA, 4, ids3);
	    vtkIdType ids4[4] = {lrf, urb, lrb, llb};
	    createElement(VTK_TETRA, 4, ids4);
	    vtkIdType ids5[4] = {ulf, urb, lrf, llb};
	    createElement(VTK_TETRA, 4, ids5);
	  }

	  ICoord idx = ICoord(i,j,k);
	  addGridSegmentsToBoundaries(idx,lim);
	  addGridFacesToBoundaries(idx,lim,flip);

	  flip = !flip;

	  if(progress->stopped()) return;
	  progress->setFraction(float(element_count)/float(total));
	  progress->setMessage(to_string(element_count) + "/"
			       + to_string(total) + " elements");

	}	// end loop over z
	if(l%2==0) flip = !flip;
      } // end loop over x
      if(m%2==0) flip = !flip;
    } // end loop over y
    incrementTimestamp();
  }
  catch (...) {
    progress->finish();
    throw;
  }
  progress->finish();
}

void CSkeleton::addElement(CSkeletonElement *element, vtkIdType *ids) {
  elements.push_back(element);
  for(int i=0; i<6; ++i) {
    const IDTYPE *ptIds = vtkTetra::GetEdgeArray(i);
    CSkeletonSegment *s = getOrCreateSegment(nodes[ids[ptIds[0]]],
					     nodes[ids[ptIds[1]]]);
    s->increment_nelements();
  }
  for(int i=0; i<4; ++i) {
    const IDTYPE *ptIds = vtkTetra::GetFaceArray(i);
    CSkeletonFace *f = getOrCreateFace(nodes[ids[ptIds[0]]],
				       nodes[ids[ptIds[1]]],
				       nodes[ids[ptIds[2]]]);
    f->increment_nelements();
  }
  // ++geometry_timestamp;
}

void CSkeleton::createElement(vtkIdType type, vtkIdType numpts, vtkIdType* ids) 
{
  CSkeletonNodeVector *ns = new CSkeletonNodeVector;
  for(int i=0; i<numpts; ++i)
    ns->push_back(nodes[ids[i]]);
  int eidx = grid->InsertNextCell(type,numpts,ids);
  CSkeletonElement *el = new CSkeletonElement(eidx, ns);
  el->connectToNodes();
  addElement(el, ids);
}

void CSkeleton::acceptProvisionalElement(CSkeletonElement *el) {
  VTKCellType type = el->getCellType();
  vtkIdType n = el->getNumberOfNodes();
  vtkIdType *ids = new vtkIdType[n];
  el->getPointIds(ids);
  int eidx = grid->InsertNextCell(type, n, ids);
  el->promote(eidx);
  addElement(el, ids);
  delete [] ids;
}

// The nodes in segments and faces are sorted by UID, not topological order.
CSkeletonSegment *CSkeleton::getOrCreateSegment(CSkeletonNode *n1,
						CSkeletonNode *n2) 
{
  CSkeletonMultiNodeKey h(n1,n2);
  CSkeletonSegmentMap::iterator segIt = segments.find(h);
  if(segIt == segments.end()) {
    // the segment is not already in the map
    CSkeletonNodeVector *nds = new CSkeletonNodeVector;
    nds->push_back(n1);
    nds->push_back(n2);
    std::sort(nds->begin(), nds->end(), CSkeletonSelectable::ltUid);
    CSkeletonSegment *seg = new CSkeletonSegment(nds);
    segments[h] = seg;
  }
  return segments[h];
}

CSkeletonFace *CSkeleton::getOrCreateFace(CSkeletonNode *n1, CSkeletonNode *n2,
					  CSkeletonNode *n3)
{
  CSkeletonMultiNodeKey h(n1,n2,n3);
  CSkeletonFaceMap::iterator faceIt = faces.find(h); // don't deny it
  if(faceIt == faces.end()) {
    // the face is not already in the map
    CSkeletonNodeVector *nds = new CSkeletonNodeVector;
    nds->push_back(n1);
    nds->push_back(n2);
    nds->push_back(n3);
    std::sort(nds->begin(), nds->end(), CSkeletonSelectable::ltUid);
    CSkeletonFace *face = new CSkeletonFace(nds);
    faces[h] = face;
  }
  return faces[h];
}

void CSkeleton::addGridSegmentsToBoundaries(const ICoord &idx,
					    const ICoord &nml)
{
  // idx holds what is referred to as i,j,k above in the functions
  // that create the initial skeleton. nml holds n,m,l.

  // If you search the code for the names of the edge boundaries,
  // possibly to see where and how they're created, you won't find
  // them.  The names are constructed here and not spelled out
  // anywhere in the code.  This comment remedies the problem.  The
  // edge boundaries names are XminYmax, XminZmin, XminYmin,
  // XmaxYmin, YmaxZmax, XminZmax, XmaxYmax, YmaxZmin, XmaxZmin,
  // YminZmax, YminZmin, and XmaxZmax.
  std::string names[3][2] = {{"Ymin","Ymax"}, 
			     {"Xmin","Xmax"}, 
			     {"Zmin","Zmax"}};
  // index formula = i*(m+1)*(l+1)+j*(l+1)+k
  int multiplier[3] = {(nml[1]+1)*(nml[2]+1), nml[2]+1, 1};
  int lim[3][2] = {{0,nml[0]-1}, {0,nml[1]-1}, {0,nml[2]-1}};
  ICoord coords[3];
  coords[0] = ICoord(0,1,2);
  coords[1] = ICoord(1,2,0);
  coords[2] = ICoord(2,0,1);

  for(int c=0; c<3; ++c) { // rotates the coordinates;
    for(int a=0; a<2; ++a) { // the high or low for the first coordinate
      for(int b=0; b<2; ++b) { // the high or low for the second coordinate
	if(idx[coords[c][0]] == lim[coords[c][0]][a] &&
	   idx[coords[c][1]] == lim[coords[c][1]][b]) 
	  {
	    int n0 = (idx[coords[c][0]]+a)*multiplier[coords[c][0]]
	      + (idx[coords[c][1]]+b)*multiplier[coords[c][1]]
	      + idx[coords[c][2]]*multiplier[coords[c][2]];
	    // coords[c][2] is the direction that this propagates in
	    int n1 = n0 + multiplier[coords[c][2]];
	    const std::string &name_a = names[coords[c][0]][a];
	    const std::string &name_b = names[coords[c][1]][b];
	    const std::string bdyname = (name_a < name_b?
					 name_a + name_b : name_b + name_a);
	    CSkeletonEdgeBoundary *boundary = getEdgeBoundary(bdyname, true);
	    //	      names[coords[c][0]][a]+names[coords[c][1]][b], true);
	    CSkeletonSegment *seg = findExistingSegment(nodes[n0], nodes[n1]);
	    // The default direction becomes the positive direction for
	    // every edge. The directions of the segments here don't
	    // have the same meaning they have in 2D.
	    OrientedCSkeletonSegment *oriented_seg =
	      new OrientedCSkeletonSegment(seg);
	    oriented_seg->set_direction(nodes[n0], nodes[n1]);
	    boundary->addOrientedSegment(oriented_seg);
	  }
      }
    }
  }

}

// void CSkeleton::createOrientedFaceForBoundary(int n[4], int flip, int half,
// 					      int up,
// 					      CSkeletonFaceBoundary *boundary) 
// {
//   // flip tells us which way the diagonal segment goes, half tells us
//   // whether it's the upper half or the lower half of the triangle,
//   // and up tells us whether it's the upper or lower (left or right,
//   // front or back) boundary.
//   int triangles[2][2][3] = { { {0,1,2}, {0,2,3} }, { {1,2,3}, {0,1,3} } };
//   int *idx = triangles[flip][half];
//   if(!up) std::reverse(idx, idx+3);
//   CSkeletonFace *face = findExistingFace(nodes[n[idx[0]]], nodes[n[idx[1]]],
// 					 nodes[n[idx[2]]]);
//   OrientedCSkeletonFace *oriented_face = new OrientedCSkeletonFace(face);
//   oriented_face->set_direction(nodes[n[idx[0]]], nodes[n[idx[1]]],
// 			       nodes[n[idx[2]]]);
//   boundary->addOrientedFace(oriented_face);
// }

void CSkeleton::addGridFacesToBoundaries(const ICoord &idx, const ICoord &nml,
					 bool flip) 
{
  std::string names[3][2] = {{"Ymin", "Ymax"},
			     {"Xmin", "Xmax"},
			     {"Zmin", "Zmax"}};
  // index formula = i*(m+1)*(l+1)+j*(l+1)+k
  int multiplier[3] = {(nml[1]+1)*(nml[2]+1), nml[2]+1, 1};
  int lim[3][2] = {{0,nml[0]-1}, {0,nml[1]-1}, {0,nml[2]-1}};
  int n[4]; //n0, n1, n2, n3;
  ICoord coords[3];
  coords[0] = ICoord(0,1,2);
  coords[1] = ICoord(1,2,0);
  coords[2] = ICoord(2,0,1);
  ICoord triangles[2][2];
  triangles[0][0] = ICoord(0,1,2);
  triangles[0][1] = ICoord(0,2,3);
  triangles[1][0] = ICoord(1,2,3);
  triangles[1][1] = ICoord(0,1,3);
  ICoord diagonal_segs[2];
  diagonal_segs[0] = ICoord(0,2,0);
  diagonal_segs[1] = ICoord(1,3,0);

  for(int c=0; c<3; ++c) { // rotates through the three coordinate planes
    for(int a=0; a<2; ++a) { // y / x / z
      if(idx[coords[c][0]] == lim[coords[c][0]][a]) { // if we are on a boundary
	// the indices in n form a CCW quad in the coords[1],
	// coords[2] plane with respect to the positive direction of
	// coords[0]
	n[0] = (idx[coords[c][0]]+a)*multiplier[coords[c][0]]
	  + idx[coords[c][1]]*multiplier[coords[c][1]]
	  + idx[coords[c][2]]*multiplier[coords[c][2]];
	n[1] = n[0] + multiplier[coords[c][2]]; 
	n[2] = n[1] + multiplier[coords[c][1]];
	n[3] = n[0] + multiplier[coords[c][1]];
	CSkeletonFaceBoundary *boundary = getFaceBoundary(
						  names[coords[c][0]][a], 
						  0,
						  true);
	//loop through the two possible diagonals in the quad
	for(int diag=0; diag<2; ++diag) {
	  CSkeletonSegment *seg = 
	    findExistingSegment(nodes[n[diagonal_segs[diag][0]]], 
				nodes[n[diagonal_segs[diag][1]]]);
	  if(seg != NULL) {
	    // loop through the two triangular halves of the quad
	    for(int half=0; half<2; ++half) {
	      ICoord idx = triangles[diag][half];
	      if(!a) 
		std::reverse(idx.xpointer(), idx.xpointer()+3);
	      CSkeletonFace *face = findExistingFace(
		     nodes[n[idx[0]]], nodes[n[idx[1]]], nodes[n[idx[2]]]);
	      OrientedCSkeletonFace *oriented_face =
		new OrientedCSkeletonFace(face);
	      oriented_face->set_direction(nodes[n[idx[0]]], nodes[n[idx[1]]],
					   nodes[n[idx[2]]]);
	      boundary->addOrientedFace(oriented_face);
	    }
	  }
	}
      }
    }
  }
} // end addGridFacesToBoundaries

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// checkIllegality does a quick check, stopping after it finds one
// illegal element.  Therefore it does *not* set
// CSkeletonBase::illegalCount.

bool CSkeletonBase::checkIllegality() {
  if(illegality_computation_time > geometry_timestamp)
    return illegal_;
  for(CSkeletonElementIterator el=beginElements(); el!=endElements(); ++el) {
    if((*el)->illegal()) {
      illegal_ = true;
    }
  }
  illegal_ = false;
  ++illegality_computation_time;
  return illegal_;
}

// getIllegalCount checks all elements.  It sets
// CSkeletonBase::illegal_ as well as CSkeletonBase::illegalCount.

int CSkeletonBase::getIllegalCount() {
  if(illegal_count_computation_time < geometry_timestamp)
    return illegalCount;
  illegalCount = 0;
  for(CSkeletonElementIterator el=beginElements(); el!=endElements(); ++el) {
    if((*el)->illegal())
      ++illegalCount;
  }
  illegal_ = illegalCount > 0;
  ++illegal_count_computation_time;	  
  ++illegality_computation_time;
  return illegalCount;
}

void CSkeletonBase::backdateIllegalityTimeStamp() {
  // Force illegal element count to be repeated.
  illegal_count_computation_time.backdate();
  illegality_computation_time.backdate();
}

int CSkeletonBase::getSuspectCount() {
  if(suspect_count_computation_time < geometry_timestamp) {	
    suspectCount = 0;
    for(CSkeletonElementIterator el=beginElements(); el!=endElements(); ++el) {
      if((*el)->suspect()) {
	++suspectCount;
      } 
    }
    ++suspect_count_computation_time;	  
  }
  return suspectCount;
}

void CSkeletonBase::getIllegalElements(CSkeletonElementVector &baddies) const {
  baddies.clear();
  for(CSkeletonElementIterator el=beginElements(); el!=endElements(); ++el) {
    if((*el)->illegal())
      baddies.push_back(*el);
  }
}


void CSkeletonBase::getSuspectElements(CSkeletonElementVector &baddies) const {
  baddies.clear();
  for(CSkeletonElementIterator el=beginElements(); el!=endElements(); ++el) {
    if((*el)->suspect())
      baddies.push_back(*el);
  }
}

const std::string &CSkeletonBase::getElementType(int eidx) {
  static std::string s("tetra");
  return s;

//   cleanUp();

//   switch(getGrid()->GetCellType(eidx)) {
//   case VTK_TETRA:
//     return "tetra";

//   case VTK_TRIANGLE:
//     return "triangle";
    
//   case VTK_QUAD:
//     return "quad";

//   case VTK_HEXAHEDRON:
//     return "brick";

//   default:
//     return "unknown";

//   }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const OuterFaceID OUTERFACE_XMIN(0, 0, "xmin");
const OuterFaceID OUTERFACE_XMAX(0, 1, "xmax");
const OuterFaceID OUTERFACE_YMIN(1, 2, "ymin");
const OuterFaceID OUTERFACE_YMAX(1, 3, "ymax");
const OuterFaceID OUTERFACE_ZMIN(2, 4, "zmin");
const OuterFaceID OUTERFACE_ZMAX(2, 5, "zmax");
const OuterFaceID OUTERFACE_NONE(-1, -1, "none");

const OuterEdgeID OUTEREDGE_NONE(OUTERFACE_NONE, OUTERFACE_NONE);
const OuterEdgeID OUTEREDGE_XMINYMIN(OUTERFACE_XMIN, OUTERFACE_YMIN);
const OuterEdgeID OUTEREDGE_XMINYMAX(OUTERFACE_XMIN, OUTERFACE_YMAX);
const OuterEdgeID OUTEREDGE_XMINZMIN(OUTERFACE_XMIN, OUTERFACE_ZMIN);
const OuterEdgeID OUTEREDGE_XMINZMAX(OUTERFACE_XMIN, OUTERFACE_ZMAX);
const OuterEdgeID OUTEREDGE_XMAXYMIN(OUTERFACE_XMAX, OUTERFACE_YMIN);
const OuterEdgeID OUTEREDGE_XMAXYMAX(OUTERFACE_XMAX, OUTERFACE_YMAX);
const OuterEdgeID OUTEREDGE_XMAXZMIN(OUTERFACE_XMAX, OUTERFACE_ZMIN);
const OuterEdgeID OUTEREDGE_XMAXZMAX(OUTERFACE_XMAX, OUTERFACE_ZMAX);
const OuterEdgeID OUTEREDGE_YMINZMIN(OUTERFACE_YMIN, OUTERFACE_ZMIN);
const OuterEdgeID OUTEREDGE_YMINZMAX(OUTERFACE_YMIN, OUTERFACE_ZMAX);
const OuterEdgeID OUTEREDGE_YMAXZMIN(OUTERFACE_YMAX, OUTERFACE_ZMIN);
const OuterEdgeID OUTEREDGE_YMAXZMAX(OUTERFACE_YMAX, OUTERFACE_ZMAX);

OuterEdgeID::OuterEdgeID(const OuterFaceID &f0, const OuterFaceID &f1)
  : face0(f0.id < f1.id? f0 : f1),
    face1(f0.id < f1.id? f1 : f0)
{}

OuterFaceID outerFaceNameFromID(int id) {
  switch(id) {
  case 0:
    return OUTERFACE_XMIN;
  case 1:
    return OUTERFACE_XMAX;
  case 2:
    return OUTERFACE_YMIN;
  case 3:
    return OUTERFACE_YMAX;
  case 4:
    return OUTERFACE_ZMIN;
  case 5:
    return OUTERFACE_ZMAX;
  }
  return OUTERFACE_NONE;
}

std::ostream &operator<<(std::ostream &os, const OuterFaceID &fn) {
  return os << fn.name;
}

bool OuterFaceID::contains(const Coord &position, const CSkeletonBase *skel)
  const
{
  Coord size = skel->getMicrostructure()->size();
  switch(id) {
  case 0:
    return position[0] == 0.0;
  case 1:
    return position[0] == size[0];
  case 2:
    return position[1] == 0.0;
  case 3:
    return position[1] == size[1];
  case 4:
    return position[2] == 0.0;
  case 5:
    return position[2] == size[2];
  }
  return false;
}

std::ostream &operator<<(std::ostream &os, const OuterEdgeID &ed) {
  return os << "(" << ed.face0 << ", " << ed.face1 << ")";
}

// onOuterFace tells whether all the given nodes are on the same
// exterior boundary.  It returns an OuterFaceID which identifies
// the boundary.  OUTERFACE_NONE is numerically 0, so the return value
// can be used as a boolean.  Note that it's possible that all the
// nodes are on more than one boundary, in which case onOuterFace
// returns one but not both boundaries.

OuterFaceID CSkeletonBase::onOuterFace(const CSkeletonNodeVector *nodes)
  const 
{
  bool bdyflags[2*DIM];
  return onOuterFace_(nodes, bdyflags);
}

OuterFaceID CSkeletonBase::onOuterFace_(const CSkeletonNodeVector *nodes,
					  bool *bdyflags) 
  const
{
  // TODO 3.1: Make nodes const.  

  // TODO 3.1 Check that skeleton construction and refinement doesn't
  // introduce round off error for boundary node positions, which
  // could make the comparisons below fail.

  // TODO 3.1: Using node positions to determine externality may be
  // subject to round off error.  If this is rewritten to use some
  // other information instead, some of the skeleton rationalization
  // routines may need to be rewritten.
  Coord _size = getMicrostructure()->size();
  for(int i=0; i<2*DIM; ++i)
    bdyflags[i] = true;
  for(CSkeletonNodeIterator it = nodes->begin(); it != nodes->end(); ++it) {
    Coord x;
    x = (*it)->position();

    // The value in bdyflag[i] is for the OuterFaceID with id=i.
    for(int c=0; c<DIM; ++c) {
      bdyflags[2*c] &= (x[c]==0.0);
      bdyflags[2*c+1] &= (x[c]==_size[c]);
    }
  }
  for(int i=0; i<2*DIM; i++)
    if(bdyflags[i]) {
      return outerFaceNameFromID(i);
    }
  return OUTERFACE_NONE;
}

bool CSkeletonBase::onOuterFace(const OuterFaceID face, 
				const CSkeletonNodeVector *nodes) 
  const
{
  for(CSkeletonNodeVector::const_iterator n=nodes->begin(); n!=nodes->end();
      ++n)
    {
      if(!face.contains((*n)->position(), this))
	return false;
    }
  return true;
}

// TODO 3.1: onSameOuterFace(n1, n2) is the same as
// onOuterFace(union(n1, n2)). If it were written that way, then
// onOuterFace and onOuterFace_ could be just one function, with no
// ugly bdyflags argument.

OuterFaceID CSkeletonBase::onSameOuterFace(const CSkeletonNodeVector *nodes1, 
					     const CSkeletonNodeVector *nodes2)
  const
{
  bool b1[2*DIM], b2[2*DIM];
  OuterFaceID fn1 = onOuterFace_(nodes1, b1);
  OuterFaceID fn2 = onOuterFace_(nodes2, b2);
  if(fn1 && fn2) {
    for(int i=0; i<2*DIM; ++i) {
      if(b1[i] && b2[i])
	return outerFaceNameFromID(i);
    }
  }
  return OUTERFACE_NONE;
}

OuterEdgeID CSkeletonBase::onOuterEdge(const CSkeletonNodeVector *nodes) const {
  bool bdyflags[2*DIM];
  onOuterFace_(nodes, bdyflags);
  std::vector<int> which;	// which flags are set in bdyflags
  for(int i=0; i<2*DIM; i++)
    if(bdyflags[i])
      which.push_back(i);
  if(which.size() < 2)
    return OUTEREDGE_NONE;
  // If which.size() == 3, then the points are on a corner.  This will
  // just return one of the edges that meets at the corner. But if the
  // points are distinct, they can't all be on one corner, so this
  // shouldn't be a big problem.
  return OuterEdgeID(outerFaceNameFromID(which[0]),
		     outerFaceNameFromID(which[1]));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool CSkeletonBase::checkExteriorSegments(const CSkeletonSegmentVector *segs)
  const
{
  for(CSkeletonSegmentVector::const_iterator i=segs->begin(); i!=segs->end();
      ++i)
    {
      if(!onOuterFace((*i)->getNodes()))
	return false;
    }
  return true;
}

bool CSkeletonBase::checkExteriorFaces(const CSkeletonFaceVector *faces)
  const
{
  for(CSkeletonFaceVector::const_iterator i=faces->begin(); i!=faces->end();
      ++i)
    {
      if(!onOuterFace((*i)->getNodes()))
	return false;
    }
  return true;
}


//Returns (weighted) homogeneity index, which is the default
double CSkeletonBase::getHomogeneityIndex() const {
//Only recalculate if skeleton has changed since last time it was calculated
  if(homogeneity_index_computation_time < getTimeStamp()) {
    try {
      calculateHomogeneityIndex();
    }
    catch (...) {
      throw ErrHomogeneityNotCalculable();
    }
  }
  return homogeneityIndex;
}

// Handles the calculation for (weighted) homogeneity index

void CSkeletonBase::calculateHomogeneityIndex() const {
  // Keep track of element homogeneities and bad elements
  homogeneityIndex = 0.0;
  illegalCount = 0;
  suspectCount = 0;
  // Creates progress bar since this can be a long calculation
  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("Calculating homogeneity index",
						DEFINITE));
  try {
    buildVSBs();
    double vtot = 0.0;		// total volume
    for(CSkeletonElementIterator elit = beginElements(); 
	elit != endElements(); ++elit)
      {
	//If element isn't illegal, add its info to the homogeneity calculation
	if(!(*elit)->illegal()) {
	  homogeneityIndex += (*elit)->volume()*(*elit)->homogeneity(this);
	  vtot += (*elit)->volume();
	  //If it is legal but suspect, increment the suspect counter
	  if((*elit)->suspect()) 
	    ++suspectCount;
	}
	//If it's not legal, increment the illegal counter
	else {
	  ++illegalCount;
	}
	//Progress bar shows how many elements we've gotten through
	progress->setFraction(float((*elit)->getIndex())/nelements());
	progress->setMessage(to_string((*elit)->getIndex()) + "/" +
			     to_string(nelements()));
      }
    // Using the sum of the volumes of the legal elements, instead of
    // the total volume of the microstructure, in the denominator of
    // the homogeneity index avoids a round-off error problem that
    // makes the index be slightly greater than 1 in some tests (eg,
    // OOF_ElasticTimeSteppers("SS22") in solver_test.py).  The index
    // isn't actually used for computation, so this fudge isn't
    // crucial.  The problem isn't due to the presence of illegal
    // elements.
    // homogeneityIndex /= volume();
    homogeneityIndex /= vtot;
    ++homogeneity_index_computation_time;
    ++illegal_count_computation_time;
    ++suspect_count_computation_time;
  }
  catch (...) {
    progress->finish();
    throw;
  }
  progress->finish();
}

// Gets average homogeneity, not weighted by volume
double CSkeletonBase::getUnweightedHomogeneity() const {
  //Only recalculate if the skeleton has changed since last time
  if(unweighted_homogeneity_computation_time < getTimeStamp()) {
    try {
      calculateUnweightedHomogeneity();
    }
    catch (...) {
      throw ErrHomogeneityNotCalculable();
    }
  }
  return unweightedHomogIndex;
}

// Calculates average homogeneity, not weighted by volume
void CSkeletonBase::calculateUnweightedHomogeneity() const {
  //Keep track of homogeneity data and bad elements
  unweightedHomogIndex = 0.0;
  illegalCount = 0;
  suspectCount = 0;
  //Create progress bar since this can be a long calculation
  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(
			    getProgress("Calculating unweighted homogeneity",
					DEFINITE));
  try {
    for (CSkeletonElementIterator elit = beginElements();
	 elit != endElements(); ++elit)
      {
	//If an element isn't illegal, get its homogeneity data
	if(!(*elit)->illegal()) {
	  unweightedHomogIndex += (*elit)->homogeneity(this);
	  //If it is suspect, increment the suspect counter
	  if((*elit)->suspect()) {++suspectCount;}
	}
	//If it is illegal, increment the illegal counter
	else {
	  ++illegalCount;
	}
	//Set progress bar to show how many elements we've gotten through
	progress->setFraction(float((*elit)->getIndex())/nelements());
	progress->setMessage(to_string((*elit)->getIndex()) + "/" +
			     to_string(nelements()));
      }
    //Divide by number of elements instead of total volume
    //because this is an unweighted average
    unweightedHomogIndex /= nelements();
    ++unweighted_homogeneity_computation_time;
    ++illegal_count_computation_time;
    ++suspect_count_computation_time;
  }
  catch(...) {
    progress->finish();
    throw;
  }
  progress->finish();
}

// Returns the current value of the energy functional, which depends
// on the alpha level used in skeleton modifiers Alpha = 0 gives only
// shape energy, while alpha = 1 gives only homogeneity energy

double CSkeletonBase::energyTotal(double alpha) const {
  double total = 0;
  for(unsigned int i=0; i<nelements(); ++i) {
    total += getElement(i)->energyTotal(this, alpha);
  }
  return total;
}

//Gets the unweighted average shape energy
double CSkeletonBase::getUnweightedShapeEnergy() const {
  //Only recalculate if skeleton has changed since last time
  if (unweighted_shape_energy_computation_time < getTimeStamp()) {
    //Divide total shape energy by number of elements to get unweighted average
    unweightedShapeEnergy = energyTotal(0) / nelements();
    ++unweighted_shape_energy_computation_time;
  }
  return unweightedShapeEnergy;
}

//Gets the weighted average shape energy
double CSkeletonBase::getWeightedShapeEnergy() const {
  //Only recalculate if skeleton has changed since last time
  if (weighted_shape_energy_computation_time < getTimeStamp()) {
    //Keep track of element shape energies and volumes
    weightedShapeEnergy = 0.0;
    double vtot = 0.0;
    for (CSkeletonElementIterator elit = beginElements();
	 elit != endElements(); ++elit)
      {
	//Add each element's shape energy, scaled by its volume
	weightedShapeEnergy +=
	  (*elit)->energyTotal(this, 0) * (*elit)->volume();
	vtot += (*elit)->volume();
      }
    //Divide running total by total volume to get weighted average
    weightedShapeEnergy /= vtot;
    ++weighted_shape_energy_computation_time;
  }
  return weightedShapeEnergy;
}


const CSkeletonElement* CSkeletonBase::enclosingElement(Coord *point) {
  vtkIdType cellId = get_element_locator()->FindCell(point->xpointer());
  if(cellId != -1)
    return getElement(cellId);
  // FindCell sometimes fails, for some reason.  Maybe roundoff error
  // is putting the point outside the element.  In that case, use
  // FindClosestPoint instead.
  Coord q;
  double dist2;
  int subId = 0;
  vtkSmartPointer<vtkGenericCell> cell = vtkSmartPointer<vtkGenericCell>::New();
  get_element_locator()->FindClosestPoint(point->xpointer(),q.xpointer(),cell,cellId,subId,dist2);
  assert(cellId != -1);
  return getElement(cellId);
}

CSkeletonElement* CSkeletonBase::findElement(vtkSmartPointer<vtkCell> cell)
  const
{
  assert(cell.GetPointer() != 0);
  // get points from cell
  std::vector<CSkeletonNode*> cellnodes;
  vtkSmartPointer<vtkPoints> pts = cell->GetPoints();
  for(vtkIdType n=0; n<cell->GetNumberOfPoints(); n++) {
    // CSkeletonNode::index is the value returned by points->InsertNextPoint
    vtkIdType ptid = cell->GetPointId(n);
    cellnodes.push_back(getNode(ptid));
  }
  CSkeletonMultiNodeKey key(cellnodes[0], cellnodes[1], cellnodes[2],
			    cellnodes[3]);
  // TODO OPT: Keep a map and avoid linear search here?
  for(CSkeletonElementIterator i=beginElements(); i!=endElements(); ++i) {
    if(key == (*i)->key())
      return *i;
  }
  return 0;
}

const Coord CSkeleton::nodePositionForSkeleton(CSkeletonNode *n) {
  // Gets the position of the node in this skeleton even if a deputy
  // is active.
  if(deputy != NULL)
    return deputy->originalPosition(n);
  else 
    return n->position();
} 

vtkSmartPointer<vtkCellLocator> CSkeleton::get_element_locator() {
  cleanUp();
  if(!element_locator.GetPointer()) {
    element_locator = vtkSmartPointer<vtkCellLocator>::New();
    element_locator->SetDataSet(grid);
    element_locator->BuildLocator();
  }
  return element_locator;
}

const CSkeletonNode* CSkeletonBase::nearestNode(Coord *point) {
  int idx = get_point_locator()->FindClosestPoint(point->xpointer());
#ifdef DEBUG
  if(idx < 0 || (unsigned int) idx >= nnodes()) {
    throw ErrProgrammingError("FindClosestPoint failed", __FILE__, __LINE__);
  }
#endif	// DEBUG
  return getNode(idx);
}

vtkSmartPointer<vtkMergePoints> CSkeleton::get_point_locator() {
  cleanUp();
  if(!point_locator.GetPointer()) {
    point_locator = vtkSmartPointer<vtkMergePoints>::New();
    point_locator->SetDataSet(grid);
    point_locator->SetDivisions(8,8,8); // TODO OPT: Don't hard-code divisons.
  }
  return point_locator;
}

void CSkeleton::getVtkCells(SkeletonFilter *filter,
			    vtkSmartPointer<vtkUnstructuredGrid> grd)
{
  // oofcerr << "CSkeleton::getVtkCells" << std::endl;
  cleanUp();
  // std::cerr << "CSkeleton::getVtkCells: before initializing, CellData="
  // 	    << *grd->GetCellData() << std::endl;
  grd->Initialize();
  // std::cerr << "CSkeleton::getVtkCells:  after initializing, CellData="
  // 	    << *grd->GetCellData() << std::endl;
  filter->resetMap();
  // Allocate() args are the initial size and the increment to use
  // when expanding.
  // TODO OPT: SkeletonFilter should be able to estimate the size and
  // provide a better guess than we're using here.
  grd->Allocate(elements.size()/2, elements.size()/2);
  grd->SetPoints(points); 
  for(CSkeletonElementIterator it=elements.begin(); it!=elements.end(); ++it) {
    CSkeletonElement *el = *it;
    if(filter->acceptable(el, this)) {
      VTKCellType type = el->getCellType();
      vtkIdType ids[4];
      el->getPointIds(ids);
      vtkIdType cellID = grd->InsertNextCell(type, 4, ids);
      // Keep track of the correspondence between element indices and
      // vtk cell IDs.  This information is used by
      // findClickedCellID() in ghostgfxwindow.py.
      filter->mapCellIndex(cellID, el->getIndex());
    }
  }
}

#ifdef DEBUG
void CSkeleton::getVtkSegments(SkeletonFilter *filter,
			       vtkSmartPointer<vtkUnstructuredGrid> grd)
{
  cleanUp();
  grd->Initialize();
  filter->resetMap();
  grd->Allocate(elements.size()/2, elements.size()/2);
  grd->SetPoints(points);
  for(CSkeletonSegmentIterator sit=beginSegments(); sit!=endSegments(); ++sit) {
    const CSkeletonSegment *seg = (*sit).second;
    if(filter->acceptable(seg, this)) {
      VTKCellType type = seg->getCellType();
      vtkIdType ids[2];
      seg->getPointIds(ids);
      /*vtkIdType cellID = */ grd->InsertNextCell(type, 2, ids);
      // filter->mapCellIndex(cellID, seg->getIndex());
    }
  }
}

void CSkeleton::getExtraVtkSegments(CSkeletonBase *other,
				    vtkSmartPointer<vtkUnstructuredGrid> grd)
{
  // Display segments in this Skeleton that aren't in that one.
  cleanUp();
  CSkeleton *that = other->sheriffSkeleton();
  that->cleanUp();
  // First make sets of all segments in the two Skeletons,
  // representing them by Coords because node indexing may
  // not be the same.
  typedef std::pair<Coord3D, Coord3D> CoordPair;
  std::set<CoordPair> thatSegs, thisSegs;
  std::map<CoordPair, const CSkeletonSegment*> segMap;
  for(CSkeletonSegmentIterator i=beginSegments(); i!=endSegments(); i++)
    {
      CSkeletonSegment *seg = i->second;;
      Coord3D p0 = seg->getNode(0)->position();
      Coord3D p1 = seg->getNode(1)->position();
      if(p0 < p1) {
	thisSegs.emplace(p0, p1);
	segMap[CoordPair(p0, p1)] = seg;
      }
      else {
	thisSegs.emplace(p1, p0);
	segMap[CoordPair(p1, p0)] = seg;
      }
    }
  for(CSkeletonSegmentIterator i=that->beginSegments(); i!=that->endSegments();
      i++)
    {
      CSkeletonSegment *seg = i->second;
      Coord3D p0 = seg->getNode(0)->position();
      Coord3D p1 = seg->getNode(1)->position();
      if(p0 < p1)
	thatSegs.emplace(p0, p1);
      else
	thatSegs.emplace(p1, p0);
    }
  std::set<CoordPair> diff;
  std::set_difference(thisSegs.begin(), thisSegs.end(),
		      thatSegs.begin(), thatSegs.end(),
		      std::inserter(diff, diff.end()));
  grd->Initialize();
  grd->Allocate(diff.size(), diff.size());
  grd->SetPoints(points);
  for(auto &ptpair : diff) {
    const CSkeletonSegment *seg = segMap[ptpair];
    vtkIdType ids[2];
    seg->getPointIds(ids);
    grd->InsertNextCell(seg->getCellType(), 2, ids);
  }
}
#endif // DEBUG

vtkSmartPointer<vtkDataArray> CSkeleton::getMaterialCellData(
					    const SkeletonFilter *filter)
  const 
{
  // TODO 3.1: Test filters.
  vtkSmartPointer<vtkIntArray> intCellData = 
    vtkSmartPointer<vtkIntArray>::New();
  for(CSkeletonElementIterator it=elements.begin(); it!=elements.end(); ++it) {
    CSkeletonElement *el = *it;
    if(filter->acceptable(el, this)) {
      int cat = el->dominantPixel(this);
      intCellData->InsertNextValue(cat);
    }
  }
  return vtkSmartPointer<vtkDataArray>(intCellData.GetPointer());
}

vtkSmartPointer<vtkDataArray> CSkeleton::getEnergyCellData(
			     double alpha, const SkeletonFilter *filter)
const
{
  // double min = std::numeric_limits<double>::max();
  // double max = -min;
  vtkSmartPointer<vtkDoubleArray> data = vtkSmartPointer<vtkDoubleArray>::New();
  for(CSkeletonElementIterator it=elements.begin(); it!=elements.end(); ++it) {
    CSkeletonElement *el = *it;
    if(filter->acceptable(el, this)) {
      double energy = el->energyTotal(this, alpha);
      // if(energy > max)
      // 	max = energy;
      // if(energy < min)
      // 	min = energy;
      data->InsertNextValue(energy);
    }
  }
  // oofcerr << "CSkeleton::getEnergyCellData: min=" << min
  // 	  << " max=" << max << std::endl;
  return vtkSmartPointer<vtkDataArray>(data.GetPointer());
}

CSkeletonNode *CSkeleton::getNode(unsigned int nidx) const {
  assert(nidx < nodes.size());
  return nodes[nidx];
}

uidtype CSkeleton::getNodeUid(int nidx) const {
  return nodes[nidx]->uid;
}

bool CSkeleton::hasNode(CSkeletonNode *n) const {
  return std::find_if(nodes.begin(), nodes.end(), FindUid(n->getUid()))
    != nodes.end();
  // for(CSkeletonNodeIterator it=nodes.begin(); it!=nodes.end(); ++it)
  //   if( **it == *n ) return true;
  // return false;
}

bool CSkeleton::hasElement(CSkeletonElement *e) const {
  return std::find_if(elements.begin(), elements.end(), FindUid(e->getUid()))
    != elements.end();
  // for(CSkeletonElementIterator it=elements.begin(); it!=elements.end(); ++it)
  //   if( **it == *e ) return true;
  // return false;
}

CSkeletonElement *CSkeleton::getElement(unsigned int eidx) const {
  assert(eidx < elements.size());
  return elements[eidx];
}

uidtype CSkeleton::getElementUid(int eidx) const {
  return elements[eidx]->uid;
}

CSkeletonSegment* CSkeletonBase::findExistingSegment(const CSkeletonNode *n1,
						     const CSkeletonNode *n2)
  const
{
  CSkeletonMultiNodeKey h(n1,n2);
  return getSegment(h);
}

CSkeletonSegment *CSkeletonBase::findExistingSegmentByIds(
					  const std::vector<int> *pointIds)
  const
{
  CSkeletonNode *n0 = getNode((*pointIds)[0]);
  CSkeletonNode *n1 = getNode((*pointIds)[1]);
  return findExistingSegment(n0, n1);
}

CSkeletonSegment* CSkeleton::getSegment(const CSkeletonMultiNodeKey &h) const {
  CSkeletonSegmentMap::const_iterator it;
  it = segments.find(h);
  if(it != segments.end())
    return (*it).second;
  else
    return NULL;
}

CSkeletonSegment* CSkeleton::getSegmentByUid(uidtype i) const {
  // This is inefficient, but it's only used by the Skeleton Info
  // toolbox.  If it's used elsewhere, the linear search should be
  // eliminated somehow.
  for(CSkeletonSegmentMap::const_iterator it=segments.begin();
      it!=segments.end(); ++it) 
    {
      CSkeletonSegment *seg = (*it).second;
      if(seg->getUid() == i)
	return seg;
    }
  return 0;
}


bool CSkeletonBase::doesSegmentExist(const CSkeletonNode *n1, 
				     const CSkeletonNode *n2)
  const
{
  CSkeletonMultiNodeKey h(n1,n2);
  return inSegmentMap(h);
}

bool CSkeleton::inSegmentMap(const CSkeletonMultiNodeKey &h) const {
  CSkeletonSegmentMap::const_iterator it = segments.find(h);
  return (it != segments.end());
}

const CSkeletonSegment* CSkeletonBase::nearestSegment(Coord *point) {
  cleanUp();
  vtkIdType cellId = enclosingElement(point)->getIndex();
  double bcoords[4];
  Coord x[4];
#if VTK_MAJOR_VERSION < 9
  vtkIdType *ptIds;
  vtkIdType num=4;
  getGrid()->GetCellPoints(cellId, num, ptIds);
  for(int i=0; i<num; ++i)
    getPoints()->GetPoint(ptIds[i],x[i].xpointer());
#else // VTK_MAJOR_VERSION >= 9
  auto ptIds = vtkSmartPointer<vtkIdList>::New();
  getGrid()->GetCellPoints(cellId, ptIds);
  int i=0;
  for(auto ptId : *ptIds)
    getPoints()->GetPoint(ptId, x[i++].xpointer());
#endif // VTK_MAJOR_VERSION >= 9
  vtkTetra::BarycentricCoords(point->xpointer(), x[0].xpointer(),
			      x[1].xpointer(), x[2].xpointer(), x[3].xpointer(),
			      bcoords);
  double max1=bcoords[0];
  double max2=0;
  int maxIdx1=0;
  int maxIdx2=0;
  for(int i=1; i<4; ++i) {
    if(bcoords[i]>max1){
      max1=bcoords[i];
      maxIdx1=i;
    }
  }
  for(int i=0; i<4; ++i) {
    if(bcoords[i]>max2 && i!=maxIdx1) {
      max2=bcoords[i];
      maxIdx2=i;
    }
  }
#if VTK_MAJOR_VERSION < 9
  return findExistingSegment(getNode(ptIds[maxIdx1]), getNode(ptIds[maxIdx2]));
#else // VTK_MAJOR_VERSION >= 9
  return findExistingSegment(getNode(ptIds->GetId(maxIdx1)),
			     getNode(ptIds->GetId(maxIdx2)));
				     
#endif // VTK_MAJOR_VERSION >= 9
}

CSkeletonFace* CSkeletonBase::findExistingFace(CSkeletonNode *n1,
					       CSkeletonNode *n2,
					       CSkeletonNode *n3)
  const 
{
  CSkeletonMultiNodeKey h(n1,n2,n3);
  return getFace(h);
}

CSkeletonFace *CSkeletonBase::findExistingFaceByIds(
					    const std::vector<int> *pointIds)
  const
{
  CSkeletonNode *n0 = getNode((*pointIds)[0]);
  CSkeletonNode *n1 = getNode((*pointIds)[1]);
  CSkeletonNode *n2 = getNode((*pointIds)[2]);
  return findExistingFace(n0, n1, n2);
}

OrientedCSkeletonFace* CSkeletonBase::createOrientedFace(CSkeletonNode *n1,
							 CSkeletonNode *n2,
							 CSkeletonNode *n3)
  const 
{
  CSkeletonFace* f = findExistingFace(n1,n2,n3);
  OrientedCSkeletonFace *of = new OrientedCSkeletonFace(f);
  of->set_direction(n1,n2,n3);
  return of;
}

CSkeletonFace* CSkeleton::getFace(const CSkeletonMultiNodeKey &h) const {
  CSkeletonFaceMap::const_iterator it;
  it = faces.find(h);
  if(it != faces.end())
    return (*it).second;
  else
    return NULL;
}

CSkeletonFace* CSkeleton::getFaceByUid(uidtype i) const {
  // This is inefficient, but it's only used by the Skeleton Info
  // toolbox.  If it's used elsewhere, the linear search should be
  // eliminated somehow.
  for(CSkeletonFaceMap::const_iterator it=faces.begin(); it!=faces.end(); ++it)
    {
      CSkeletonFace *face = (*it).second;
      if(face->getUid() == i) {
	return face;
      }
    }
  return 0;
}

const CSkeletonFace* CSkeletonBase::nearestFace(Coord *point) {
  cleanUp();
  vtkIdType cellId = enclosingElement(point)->getIndex();
  vtkIdType num=4;
  double bcoords[4]/*, p[3]*/;
  Coord x[4];
  //point->writePointer(p);
  // TODO 3.1: See vtk docs about the thread-safety of
  // vtkUnstructuredGrid::GetCellPoints().
#if VTK_MAJOR_VERSION < 9
  vtkIdType *ptIds;
  getGrid()->GetCellPoints(cellId,num,ptIds);
  for(int i=0; i<num; ++i)
    getPoints()->GetPoint(ptIds[i],x[i].xpointer());
#else // VTK_MAJOR_VERSION >= 9
  auto ptIds = vtkSmartPointer<vtkIdList>::New();
  getGrid()->GetCellPoints(cellId, ptIds);
  int ii=0;
  for(auto ptId : *ptIds)
    getPoints()->GetPoint(ptId, x[ii++].xpointer());
#endif // VTK_MAJOR_VERSION >= 9
  vtkTetra::BarycentricCoords(
      point->xpointer(),
      x[0].xpointer(), x[1].xpointer(), x[2].xpointer(), x[3].xpointer(),
      bcoords);
  double min=bcoords[0];
  int minIdx=0;
  for(int i=1; i<4; ++i) {
    if(bcoords[i]<min){
      min=bcoords[i];
      minIdx=i;
    }
  }
  int j, idxs[3];
  for(int i=0, j=0; i<4; ++i) {
    if(i!=minIdx) {
      idxs[j]=i;
      ++j;
    }
  }
#if VTK_MAJOR_VERSION < 9
  return findExistingFace(getNode(ptIds[idxs[0]]),
			  getNode(ptIds[idxs[1]]),
			  getNode(ptIds[idxs[2]]));
#else // VTK_MAJOR_VERSION >= 9
  return findExistingFace(getNode(ptIds->GetId(idxs[0])),
			  getNode(ptIds->GetId(idxs[1])),
			  getNode(ptIds->GetId(idxs[2])));
#endif // VTK_MAJOR_VERSION >= 9
}

// std::set_intersection doesn't work with unsorted vectors of
// pointers.  We want to compare the Uids.
//* TODO OPT: This could be sped up with sorted containers and
//* set_intersection.  Would it be possible to use sets instead of
//* vectors whereever selectable_vector_intersection is called?

template <class VECTORTYPE>	// any std::container of CSkeletonSelectables
static void selectable_vector_intersection(VECTORTYPE *v1,
					   VECTORTYPE *v2,
					   VECTORTYPE *r)
{
  for(typename VECTORTYPE::size_type i=0; i<v1->size(); ++i) {
    for(typename VECTORTYPE::size_type j=0; j<v2->size(); ++j) {
      if((*v1)[i]->getUid() == (*v2)[j]->getUid()) {
	r->push_back((*v1)[i]);
	// TODO OPT: If the vectors don't contain duplicate entries, put a
	// "break" here.
      }
    }
  }
}


void CSkeletonBase::getSegmentElements(const CSkeletonSegment *segment,
				       CSkeletonElementVector &result)
const 
{
  result.clear();
  const CSkeletonNodeVector *nodes = segment->getNodes();
  CSkeletonElementVector *els0 = (*nodes)[0]->getElements();
  CSkeletonElementVector *els1 = (*nodes)[1]->getElements();
  selectable_vector_intersection(els0, els1, &result);
}

// TODO OPT: Why isn't this simply named getSegmentElements?  The const
// and non-const versions of getFaceElements don't have different
// names.
void CSkeletonBase::getConstSegmentElements(const CSkeletonSegment *segment,
					    ConstCSkeletonElementVector &result)
  const
{
  result.clear();
  const CSkeletonNodeVector *nodes = segment->getNodes();
  ConstCSkeletonElementVector els0, els1;
  (*nodes)[0]->getElements(this, els0);
  (*nodes)[1]->getElements(this, els1);
  selectable_vector_intersection(&els0, &els1, &result);
}

CSkeletonElementVector CSkeletonBase::getSegmentElements(
					 const CSkeletonSegment *segment)
  const
{
  CSkeletonElementVector elems;
  const CSkeletonNodeVector *nodes = segment->getNodes();
  CSkeletonElementVector *els0 = (*nodes)[0]->getElements();
  CSkeletonElementVector *els1 = (*nodes)[1]->getElements();
  selectable_vector_intersection(els0, els1, &elems);
  return elems;
}

void CSkeletonBase::getSegmentFaces(const CSkeletonSegment *segment,
				    CSkeletonFaceVector &result) 
  const
{
  result.clear();
  const CSkeletonNodeVector *nodes = segment->getNodes();
  CSkeletonFaceSet f1, f2;
  getNodeFaces((*nodes)[0], f1);
  getNodeFaces((*nodes)[1], f2);

  CSkeletonFaceSet::iterator it1 = f1.begin();
  CSkeletonFaceSet::iterator it2 = f2.begin();
  while (it1!=f1.end() && it2!=f2.end())
  {
    if(**it1 < **it2)
      ++it1;
    else if(**it2 < **it1)
      ++it2;
    else { 
      result.push_back(*it1);
      it2++; 
    }
  }

}

void CSkeletonBase::getFaceElements(const CSkeletonFace *face,
				    CSkeletonElementVector &result)
  const
{
  result.clear();
  const CSkeletonNodeVector *nodes = face->getNodes();
  CSkeletonElementVector *els0 = (*nodes)[0]->getElements();
  CSkeletonElementVector *els1 = (*nodes)[1]->getElements();
  CSkeletonElementVector *els2 = (*nodes)[2]->getElements();
  CSkeletonElementVector temp;
  selectable_vector_intersection(els0, els1, &temp);
  selectable_vector_intersection(&temp, els2, &result);
}

void CSkeletonBase::getFaceElements(const CSkeletonFace *face,
				    ConstCSkeletonElementVector &result)
  const
{
  result.clear();
  const CSkeletonNodeVector *nodes = face->getNodes();
  ConstCSkeletonElementVector els[3];
  for(int i=0; i<3; i++)
    (*nodes)[i]->getElements(this, els[i]);
  ConstCSkeletonElementVector temp;
  selectable_vector_intersection(&els[0], &els[1], &temp);
  selectable_vector_intersection(&temp, &els[2], &result);
}


// TODO: Use C++11 move constructors and return the CSkeletonNodeSet
// instead of passing it as an argument.
void CSkeletonBase::getNeighborNodes(const CSkeletonNode *node,
				     CSkeletonNodeSet &result)
  const
{
  CSkeletonElementVector *els = node->getElements();
  for(CSkeletonElementIterator it = els->begin();
      it != els->end(); ++it) {
    const CSkeletonNodeVector *ns = (*it)->getNodes();
    for(unsigned int j=0; j < ns->size(); ++j) {
      if(*((*ns)[j]) != *node) {
	if(doesSegmentExist((*ns)[j],node)) {
	  result.insert((*ns)[j]);
	}
      }
    }     
  }
}

void CSkeletonBase::getNodeSegments(const CSkeletonNode *node,
				    CSkeletonSegmentSet &segs) 
  const
{
  CSkeletonElementVector *els = node->getElements();
  for(CSkeletonElementIterator it = els->begin();
      it != els->end(); ++it) {
    const CSkeletonNodeVector *ns = (*it)->getNodes();
    for(CSkeletonNodeVector::size_type j=0; j < ns->size(); ++j) {
      if(*((*ns)[j]) != *node) {
	CSkeletonSegment *seg = findExistingSegment(node, (*ns)[j]);
	if(seg != NULL)
	  segs.insert(seg);
      }
    }
  }
}
  
void CSkeletonBase::getNodeFaces(const CSkeletonNode *node, 
				 CSkeletonFaceSet &faces) 
  const
{
  // This assumes that we have only triangular faces.
  CSkeletonElementVector *els = node->getElements();
  for(CSkeletonElementIterator it = els->begin(); it != els->end(); ++it) {
    for(int i=0; i<4; ++i) {
      const IDTYPE *ptIds = vtkTetra::GetFaceArray(i);
      if((*(*it)->getNode(ptIds[0])) == *node || 
	 (*(*it)->getNode(ptIds[1])) == *node ||
	 (*(*it)->getNode(ptIds[2])) == *node)
	{
	  CSkeletonFace *face = findExistingFace((*it)->getNode(ptIds[0]),
						 (*it)->getNode(ptIds[1]),
						 (*it)->getNode(ptIds[2]));
	  if(face != NULL)
	    faces.insert(face);
	}
    }
  }
}

CSkeletonSegment *CSkeletonBase::getFaceSegment(const CSkeletonFace *face,
						int idx)
  const 
{
  // This assumes that we have only triangular faces.
  return findExistingSegment(face->getNode(idx), face->getNode((idx+1)%3));
}

void CSkeletonBase::getFaceSegments(const CSkeletonFace *face,
				    CSkeletonSegmentSet &segset)
  const 
{
  //  oofcerr << "CSkeletonBase::getFaceSegments: face=" << *face << std::endl;
  for(int i=0; i<3; i++) {
    // oofcerr << "CSkeletonBase::getFaceSegments: calling getFaceSegment("
    // 	    << i << ")" << std::endl;
    CSkeletonSegment *seg = getFaceSegment(face, i);
    if(!seg) {
      oofcerr << "CSkeletonBase::getFaceSegments: seg(" << i <<") = " << seg
	      << std::endl;
      oofcerr << "    nodes are: " << *face->getNode(i) << " " 
	      << *face->getNode((i+1)%3) << std::endl;
      throw ErrProgrammingError("getFaceSegments failed!", __FILE__, __LINE__);
    }
    segset.insert(seg);
    // oofcerr << "CSkeletonBase::getFaceSegments: inserted" << std::endl;
    //segset.insert(getFaceSegment(face, i));

  }
}

CSkeletonSegment *CSkeletonBase::getElementSegment(const CSkeletonElement *el,
						   int idx)
  const 
{
  const IDTYPE *ptIds = vtkTetra::GetEdgeArray(idx);
  return findExistingSegment(el->getNode(ptIds[0]), el->getNode(ptIds[1]));
}

CSkeletonSegmentVector *CSkeletonBase::getElementSegments(
						  const CSkeletonElement *el)
  const
{
  CSkeletonSegmentVector *vec =
    new CSkeletonSegmentVector(el->getNumberOfSegments());
  for(unsigned int idx=0; idx<el->getNumberOfSegments(); idx++) {
    const IDTYPE *ptIds = vtkTetra::GetEdgeArray(idx);
    (*vec)[idx] = findExistingSegment(el->getNode(ptIds[0]), 
				      el->getNode(ptIds[1]));
  }
  return vec;
}

CSkeletonFace *CSkeletonBase::getElementFace(const CSkeletonElement *el,
					     int idx) 
  const 
{
  // TODO 3.1: This assumes triangular faces.
  const IDTYPE *ptIds = vtkTetra::GetFaceArray(idx);
  return findExistingFace(el->getNode(ptIds[0]), el->getNode(ptIds[1]),
			  el->getNode(ptIds[2]));
}

CSkeletonFaceVector *CSkeletonBase::getElementFaces(const CSkeletonElement *el)
  const
{
  // TODO 3.1: This assumes triangular faces.
  CSkeletonFaceVector *vec = new CSkeletonFaceVector(el->getNumberOfFaces());
  for(unsigned int idx=0; idx<el->getNumberOfFaces(); idx++) {
    const IDTYPE *ptIds = vtkTetra::GetFaceArray(idx);
    (*vec)[idx] = findExistingFace(el->getNode(ptIds[0]), el->getNode(ptIds[1]),
				el->getNode(ptIds[2]));
  }
  return vec;
}

ConstCSkeletonElementSet *CSkeletonBase::getElementNeighbors(
						const CSkeletonElement *el)
  const
{
  // Get all neighbors, including ones that share just a node or edge.
  const CSkeletonNodeVector *nodes = el->getNodes();
  ConstCSkeletonElementSet *nbrset = new ConstCSkeletonElementSet();
  for(CSkeletonNodeVector::const_iterator n=nodes->begin();n!=nodes->end();++n)
    {
      const CSkeletonNode *node = *n;
      for(int i=0; i<node->nElements(); ++i) {
	nbrset->insert(node->getElement(i));
      }
    }
  nbrset->erase(el);
  return nbrset;
}

CSkeletonElement *CSkeletonBase::getSister(const CSkeletonElement *el,
					   const CSkeletonFace *face)
  const 
{
  if(face != NULL) {
    CSkeletonElementVector vec;
    getFaceElements(face, vec);
    for(CSkeletonElementIterator it = vec.begin(); it != vec.end(); ++it) {
      if((*it)->getUid() != el->getUid())
	return *it;
    }
  }
  return NULL;
}

void CSkeletonBase::getInternalBoundaryNodes(CSkeletonNodeSet &nodes) const {
  nodes.clear();
  CSkeletonElementVector *elvec;
  int cat1, cat2;
  for(CSkeletonNodeIterator nit = beginNodes(); nit != endNodes(); ++nit) {
    elvec = (*nit)->getElements();
    cat1 = (*elvec)[0]->dominantPixel(this);
    for(CSkeletonElementVector::size_type i=1; i<elvec->size(); ++i) {
      cat2 = (*elvec)[i]->dominantPixel(this);
      if(cat1 != cat2 && cat1 != UNKNOWN_CATEGORY && cat2 != UNKNOWN_CATEGORY) {
	nodes.insert(*nit);
	break;
      }
    }
  }
}

CSkeletonElement *CSkeletonBase::getOrientedSegmentElement(
					   OrientedCSkeletonSegment *oseg) 
{
  CSkeletonElementVector els;
  getSegmentElements(oseg->get_segment(), els);
  return els[0];
}

CSkeletonElement *CSkeletonBase::getOrientedFaceElement(
						OrientedCSkeletonFace *face) 
{
  CSkeletonElementVector els;
  getFaceElements(face->get_face(), els);
  return els[0];
}

// There are four versions of averageNeighborPosition.  The ones with
// just one CSkeletonNode* argument return the average position of the
// neighbors of the given node.  The ones with a second
// CSkeletonNodeSet argument return the average position of the nodes
// in the given set, unless the set is empty, in which case the
// position of the node is returned.  The functions called
// averageConstrainedNbrPosition compute the average using only nodes
// that have the same mobility (or less) than the given node, so that,
// for example, a node on a face can be moved to the average position
// of its neighbors on the same face.  (This will fail if the node has
// neighbors on opposing faces, but if the Skeleton has elements that
// span the whole Microstructure, the smoothing methods that use
// averageConstrainedNbrPosition are being applied prematurely.)

Coord CSkeletonBase::averageNeighborPosition(const CSkeletonNode *node)
  const
{
  CSkeletonNodeSet neighborNodes;
  getNeighborNodes(node, neighborNodes);
  return averageNeighborPosition(node, neighborNodes);
}

Coord CSkeletonBase::averageNeighborPosition(const CSkeletonNode *node,
					     const CSkeletonNodeSet &nbrs)
  const
{
  // Compute the average position x of the nodes in the set nbrs.  If
  // nbrs is empty, return the position of the given node.
  //x[0] = x[1] = x[2] = 0.0;
  Coord x;
  if(!nbrs.empty()) {
    for(CSkeletonNodeSet::const_iterator i=nbrs.begin(); i!=nbrs.end(); ++i) {
      Coord y;
      y = (*i)->position();
      x += y;
    }
    double ninv = 1./nbrs.size();
    x *= ninv;
  }
  else
    x = node->position();
  return x;
}

Coord CSkeletonBase::averageConstrainedNbrPosition(const CSkeletonNode *node)
  const
{
  // Just like averageNeighborPosition, except that if the node is
  // constrained to move only on certain planes, only neighbors with
  // at least the same constraints are used.
  bool mobx = node->movable_x();
  bool moby = node->movable_y();
  bool mobz = node->movable_z();
  CSkeletonNodeSet neighborNodes;
  getNeighborNodes(node, neighborNodes);
  if(mobx && moby && mobz)
    return averageNeighborPosition(node, neighborNodes);
  
  CSkeletonNodeSet oknbrs;
  for(CSkeletonNode *nbr : neighborNodes) {
    if((mobx || !nbr->movable_x()) &&
       (moby || !nbr->movable_y()) &&
       (mobz || !nbr->movable_z()))
      {
	oknbrs.insert(nbr);
      }
  }
  return averageNeighborPosition(node, oknbrs);
}

Coord CSkeletonBase::averageConstrainedNbrPosition(const CSkeletonNode *node,
						   const CSkeletonNodeSet &nbrs)
  const
{
  Coord3D x;
  bool mobx = node->movable_x();
  bool moby = node->movable_y();
  bool mobz = node->movable_z();
  if(mobx && moby && mobz)
    return averageNeighborPosition(node, nbrs);
  CSkeletonNodeSet oknbrs;
  for(CSkeletonNode *nbr : nbrs) {
    if((mobx || !nbr->movable_x()) &&
       (moby || !nbr->movable_y()) &&
       (mobz || !nbr->movable_z()))
      {
	oknbrs.insert(nbr);
      }
    }
  return averageNeighborPosition(node, oknbrs);
}

//     // Two versions of neighborNodes are needed for
//     // PeriodicSkeletonNode because in most contexts we want the
//     // neighbors accross the boundary, but in others, such as when
//     // drawing rubber band lines, we don't want the neighbors of the
//     // partners.  Rather than just calling SkeletonNode.neighborNodes
//     // on self and on the partners, we redo everything we do on self
//     // for the partners with the additional condition that the
//     // potential neighbor is neither the self nor the partner node.
//     // This handles pathological cases where neighbors and partners can
//     // overlap.
//     def neighborNodes(self, skeleton):
//         neighborDict = {}
//         for e in self._elements:
//             for nd in e.nodes:
//                 if nd is not self:
//                     if skeleton.findSegment(nd, self) is not None:
//                         neighborDict[nd] = 1

//         for partnerNode in self.getPartners():
//             for e in partnerNode._elements:
//                 for nd in e.nodes:
//                     if nd is not self and nd is not partnerNode:
//                         if skeleton.findSegment(nd, partnerNode) is not None:
//                             neighborDict[nd] = 1

//         return neighborDict.keys()

//     def aperiodicNeighborNodes(self, skeleton):
//         return SkeletonNode.neighborNodes(self, skeleton)

// TODO OPT: memory management
// CSkeletonNodeVector *CSkeleton::activeNodes() {
//   CSkeletonNodeVector *result = new CSkeletonNodeVector;
//   for(unsigned int i=0; i<nodes.size(); ++i)
//     if(nodes[i]->active(this)) result->push_back(nodes[i]);
//   return result;
// }

CSkeletonPointBoundary *CSkeleton::getPointBoundary(const std::string &name,
						    bool exterior) 
{
  CSkeletonPointBoundaryMap::iterator it = pointBoundaries.find(name);
  if(it == pointBoundaries.end()) {
    if(exterior)
      pointBoundaries[name] = new ExteriorCSkeletonPointBoundary(name);
    else
      pointBoundaries[name] = new CSkeletonPointBoundary(name);
  }
  return pointBoundaries[name];
}

void CSkeleton::checkBoundaryNames(const std::string &name) {
  for(CSkeletonPointBoundaryMap::iterator bound_it = pointBoundaries.begin();
      bound_it != pointBoundaries.end(); ++bound_it)
    {
      if(name == (*bound_it).first)
	throw ErrSetupError("Boundary " + name + " already exists.");
    }
  for(CSkeletonEdgeBoundaryMap::iterator bound_it = edgeBoundaries.begin();
      bound_it != edgeBoundaries.end(); ++bound_it)
    {
      if(name == (*bound_it).first)
	throw ErrSetupError("Boundary " + name + " already exists.");
    }
  for(CSkeletonFaceBoundaryMap::iterator bound_it = faceBoundaries.begin();
      bound_it != faceBoundaries.end(); ++bound_it)
    {
      if(name == (*bound_it).first)
	throw ErrSetupError("Boundary " + name + " already exists.");
    }
}

CSkeletonPointBoundary *CSkeleton::makePointBoundary(
     const std::string &name, CSkeletonNodeVector *nodes, bool exterior) 
{
  checkBoundaryNames(name);

  CSkeletonPointBoundary *bdy = getPointBoundary(name, exterior);

  if(nodes != NULL) {
    for(CSkeletonNodeIterator it = nodes->begin(); it != nodes->end(); ++it)
      bdy->addNode(*it);
  }

//   for mctxt in self.meshes:
//   mctxt.newPointBoundary(name, bdy)

  return bdy;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonEdgeBoundary *CSkeleton::getEdgeBoundary(const std::string &name,
						  bool exterior) 
{
  CSkeletonEdgeBoundaryMap::iterator it = edgeBoundaries.find(name);
  if(it == edgeBoundaries.end()) {
    if(exterior)
      edgeBoundaries[name] = new ExteriorCSkeletonEdgeBoundary(name);
    else
      edgeBoundaries[name] = new CSkeletonEdgeBoundary(name);
  }
  return edgeBoundaries[name];
}

CSkeletonEdgeBoundary *CSkeleton::makeEdgeBoundary(
					   const std::string &name,
					   const CSkeletonSegmentVector *segs, 
					   const CSkeletonNode *start_node,
					   bool exterior)
{
  checkBoundaryNames(name);
  
  CSkeletonEdgeBoundary *boundary = getEdgeBoundary(name, exterior);

  if(segs == NULL)
    return boundary;

  if(segs->empty())
    return boundary;

  if(segs->size() == 1) {
    if(start_node != NULL) {
      if(start_node == (*segs)[0]->getNode(0))
	boundary->addOrientedSegment(
			     new OrientedCSkeletonSegment((*segs)[0], 1));
      else
	boundary->addOrientedSegment(
			     new OrientedCSkeletonSegment((*segs)[0], -1));
    }
    else
      throw ErrProgrammingError(
			"Singleton segment boundaries require a starting node!",
			__FILE__, __LINE__);
  }

  else {
    for(CSkeletonSegmentVector::size_type i=0; i<segs->size()-1; ++i) {
      CSkeletonSegment *s1 = (*segs)[i];
      CSkeletonSegment *s2 = (*segs)[i+1];
      // TODO 3.1: update for periodic bc
      std::set<uidtype> nodes_and_partners;
      nodes_and_partners.insert(s2->getNode(0)->getUid());
      nodes_and_partners.insert(s2->getNode(1)->getUid());
      if(nodes_and_partners.count(s1->getNode(0)->getUid()))
	boundary->addOrientedSegment(new OrientedCSkeletonSegment(s1, -1));
      else
	boundary->addOrientedSegment(new OrientedCSkeletonSegment(s1, 1));
    }
    // For the final segment, we need to check the one previous
    int n = segs->size();
    CSkeletonSegment *s1 = (*segs)[n-1];
    CSkeletonSegment *s2 = (*segs)[n-2];
    std::set<uidtype> nodes_and_partners;
    nodes_and_partners.insert(s2->getNode(0)->getUid());
    nodes_and_partners.insert(s2->getNode(1)->getUid());
    if(nodes_and_partners.count(s1->getNode(0)->getUid()))
      boundary->addOrientedSegment(new OrientedCSkeletonSegment(s1, 1));
    else
      boundary->addOrientedSegment(new OrientedCSkeletonSegment(s1, -1));
  }

// # #         # Write this boundary to any meshes we have.
// # #         for mctxt in self.meshes:
// # #             mctxt.newEdgeBoundary(name, bdy)

  return boundary;
}

// The newer 3D code encapsulates the segment and node info for
// constructed boundaries differently.  The old version took a vector
// of unoriented segments and a start node.  The new version receives
// a vector of oriented segments instead.  When the 2D and 3D codes
// are merged, they'll both use the new 3D encapsulation, the args for
// makeEdgeBoundary will be changed to be like makeEdgeBoundary3D, and
// makeEdgeBoundary3D won't be needed.

CSkeletonEdgeBoundary *CSkeleton::makeEdgeBoundary3D(
				     const std::string &name,
				     const SegmentSequence *segSeq,
				     bool exterior)
{
  checkBoundaryNames(name);
  CSkeletonEdgeBoundary *boundary = getEdgeBoundary(name, exterior);
  if(segSeq) {
    // segSeq was allocated by the sequencer and must be deleted here.
    // It contains OrientedCSkeletonSegments which must be copied
    // before the SegmentSequence is deleted, if they're to be used.
    for(OrientedCSkeletonSegmentVector::const_iterator i=segSeq->begin();
	i!=segSeq->end(); ++i) 
      {
	boundary->addOrientedSegment(new OrientedCSkeletonSegment(**i));
      }
    delete segSeq;
  }
  return boundary;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


CSkeletonFaceBoundary *CSkeleton::getFaceBoundary(const std::string &name,
						  OrientedSurface *surface,
						  bool exterior) 
{
  CSkeletonFaceBoundary *bdy;
  CSkeletonFaceBoundaryMap::iterator it = faceBoundaries.find(name);
  if(it == faceBoundaries.end()) {
    if(exterior)
      bdy = new ExteriorCSkeletonFaceBoundary(name);
    else
      bdy = new CSkeletonFaceBoundary(name);
    faceBoundaries[name] = bdy;
    if(!surface)
      surface = new OrientedSurface();
    bdy->setSurface(surface);
  }
  else {
    // If we're finding an existing boundary, we shouldn't be trying
    // to set its surface.
    assert(surface == 0);
    bdy = (*it).second;
  }
  return bdy;
}

CSkeletonFaceBoundary *CSkeleton::makeFaceBoundary(const std::string &name, 
						   OrientedSurface *surface,
						   bool exterior) 
{
  checkBoundaryNames(name);

  CSkeletonFaceBoundary *bdy = getFaceBoundary(name, surface, exterior);

//   for mctxt in self.meshes:
//   mctxt.newFaceBoundary(name, bdy)

  return bdy;
}



void CSkeleton::removeBoundary(const std::string &name) {
  // TODO OPT: This if/else construct is ugly.  Use double dispatch and
  // only search the appropriate list. (Is that possible?  We might
  // only know the name, in which case some kind of search is
  // necessary.)  The same fix, if any, should be applied to
  // renameBoundary(), below.
  CSkeletonPointBoundaryMap::iterator n = pointBoundaries.find(name);
  if(n != pointBoundaries.end()) {
    delete (*n).second;
    pointBoundaries.erase(n);
  }
  else {
    CSkeletonEdgeBoundaryMap::iterator e = edgeBoundaries.find(name);
    if(e != edgeBoundaries.end()) {
      delete (*e).second;
      edgeBoundaries.erase(e);
    }
    else {
      CSkeletonFaceBoundaryMap::iterator f = faceBoundaries.find(name);
      if(f != faceBoundaries.end()) {
	delete (*f).second;
	faceBoundaries.erase(f);
      }
    }
  }
}

void CSkeleton::renameBoundary(const std::string &oldname,
			       const std::string &newname) 
{
  // See TODO OPT in removeBoundary, above.
  CSkeletonPointBoundaryMap::iterator p = pointBoundaries.find(oldname);
  if(p != pointBoundaries.end()) {
    pointBoundaries[newname] = (*p).second;
    (*p).second->rename(newname);
    pointBoundaries.erase(p);
  }
  else {
    CSkeletonEdgeBoundaryMap::iterator e = edgeBoundaries.find(oldname);
    if(e != edgeBoundaries.end()) {
      edgeBoundaries[newname] = (*e).second;
      (*e).second->rename(newname);
      edgeBoundaries.erase(e);
    }
    else {
      CSkeletonFaceBoundaryMap::iterator f = faceBoundaries.find(oldname);
      if(f != faceBoundaries.end()) {
	faceBoundaries[newname] = (*f).second;
	(*f).second->rename(newname);
	faceBoundaries.erase(f);
      }
    }
  }
}



// Geometry comparison function -- returns true if this skeleton has
// the same size, area, elements, segments, and boundaries as the
// other, and if all the nodes are within tolerance of the positions
// of the other; otherwise returns false OR a string describing what went wrong
// (?).  Note that these objects must not only be topologically
// equivalent, but must also be indexed the same for the comparison to
// succeed (?).  Does not care about the skeleton name, or about
// microstructure stuff like pixels, or about group membership or
// selection status.  The former is properly the responsibility of the
// microstructure, and the latter the responsibility of the skeleton
// context.

// TODO 3.1: Why isn't 'other' const?
std::string *CSkeleton::compare(CSkeletonBase* other, double tolerance)
  const
{
  CSkeleton *omar = other->sheriffSkeleton();

#if DIM==2
  if( !(size[0] == omar->size[0] && size[1] == omar->size[1])) {
    return new std::string("Size mismatch");
  }
  if(area_ != omar->area_) {
    return new std::string("Area mismatch");
  }
#elif DIM==3
  if( !(size[0] == omar->size[0] && size[1] == omar->size[1]
	&& size[2] == omar->size[2])) 
    {
      return new std::string("Size mismatch");
    }
  if(volume_ != omar->volume_) {
    return new std::string("Volume mismatch");
  }
#endif

  if(elements.size() != omar->elements.size()) {
    return new std::string("Element count mismatch " 
			   + to_string(elements.size())
			   + " " + to_string(omar->elements.size()));
  }
#if DIM==3
  if(faces.size() != omar->faces.size()) {
    return new std::string("Face count mismatch" + to_string(faces.size())
			   + " " + to_string(omar->faces.size()));
  }
#endif
  if(segments.size() != omar->segments.size()) {
    return new std::string("Segment count mismatch" + to_string(segments.size())
			   + " " + to_string(omar->segments.size()));
  }
  if(nodes.size() != omar->nodes.size()) {
    return new std::string("Node count mismatch" + to_string(nodes.size())
			   + " " + to_string(omar->nodes.size()));
  }

  // Make sure elements have the same node indices.  The elements
  // might not be in the same order in the two Skeletons, so we can't
  // just compare the node indices in the elements one by one.
  // Instead, compare *sorted* lists of lists of node indices, one
  // (inner) list for each element.

  std::vector< NodeIndexVec > enodes, onodes;
  for(CSkeletonElementVector::const_iterator i=elements.begin();
      i!=elements.end(); ++i) 
    {
      NodeIndexVec nidxs;
      (*i)->getNodeIndices(nidxs);
      enodes.push_back(nidxs);
    }
  for(CSkeletonElementVector::const_iterator i=omar->elements.begin(); 
      i!=omar->elements.end(); ++i) 
    {
      NodeIndexVec nidxs;
      (*i)->getNodeIndices(nidxs);
      onodes.push_back(nidxs);
    }
  std::sort(enodes.begin(), enodes.end());
  std::sort(onodes.begin(), onodes.end());
  if(enodes != onodes) {
    return new std::string("Element node indexing mismatch");
  }

  // Make sure segments have the same node indices.
  enodes.clear();
  onodes.clear();
  for(CSkeletonSegmentMap::const_iterator i=segments.begin();
      i!=segments.end(); ++i) 
    {
      NodeIndexVec nidxs;
      (*i).second->getNodeIndices(nidxs);
      enodes.push_back(nidxs);
    }
  for(CSkeletonSegmentMap::const_iterator i=omar->segments.begin();
      i!=omar->segments.end(); ++i) 
    {
      NodeIndexVec nidxs;
      (*i).second->getNodeIndices(nidxs);
      onodes.push_back(nidxs);
    }
  std::sort(enodes.begin(), enodes.end());
  std::sort(onodes.begin(), onodes.end());
  if(enodes != onodes) {
    return new std::string("Segment node indexing mismatch");
  }

#if DIM==3
  // Now the faces
  enodes.clear();
  onodes.clear();
  for(CSkeletonFaceMap::const_iterator i=faces.begin(); i!=faces.end(); ++i) {
    NodeIndexVec nidxs;
    (*i).second->getNodeIndices(nidxs);
    enodes.push_back(nidxs);
  }
  for(CSkeletonFaceMap::const_iterator i=omar->faces.begin(); 
      i!=omar->faces.end(); ++i) 
    {
      NodeIndexVec nidxs;
      (*i).second->getNodeIndices(nidxs);
      onodes.push_back(nidxs);
    }
  std::sort(enodes.begin(), enodes.end());
  std::sort(onodes.begin(), onodes.end());
  if(enodes != onodes) {
    return new std::string("Face node indexing mismatch");
  }
#endif

  // Basic topology is right, now quantitatively check node locations.
  double tol2 = tolerance*tolerance;
  double diff;
  double diff2;
  for(unsigned int i = 0; i < nnodes(); ++i) {
    Coord x1  = getNode(i)->position();
    Coord x2 = omar->getNode(i)->position();
    diff2 = 0;
    for(int c=0; c<DIM; ++c) {
      diff = x1[c] - x2[c];
      diff2 += diff*diff;
    }
    if(diff2 > tol2) {
      std::string *status = new std::string;
      *status = "Node outside of tolerance (" + to_string(x1[0]) + ","
	+ to_string(x1[1]) + "," + to_string(x1[2]);
      *status += ") (" + to_string(x2[0]) + "," + to_string(x2[1]) + ","
	+ to_string(x2[2]) + ")";
      return status;
    }
  }

  if(pointBoundaries.size() != omar->pointBoundaries.size()) {
    return new std::string("Point boundary count mismatch");
  }
  if(edgeBoundaries.size() != omar->edgeBoundaries.size()) {
    return new std::string("Edge boundary count mismatch");
  }
#if DIM==3
  if(faceBoundaries.size() != omar->faceBoundaries.size()) {
    return new std::string("Face boundary count mismatch");
  }
#endif

  // The boundary tests do *not* assume that the boundaries are in the
  // same order in the two skeletons.
  
  for(CSkeletonPointBoundaryMap::const_iterator i=pointBoundaries.begin(); 
      i!=pointBoundaries.end(); ++i) 
    {
      CSkeletonPointBoundaryMap::const_iterator j =
	omar->pointBoundaries.find((*i).first);
      if(j == omar->pointBoundaries.end()) {
	return new std::string("Point boundary name mismatch: " + (*i).first);
      }
      if((*i).second->size() != (*j).second->size())  {
	return new std::string("Point boundary size mismatch: " + (*i).first);
      }
      CSkeletonNodeSet::const_iterator ni = (*i).second->getNodes()->begin();
      CSkeletonNodeSet::const_iterator nj = (*j).second->getNodes()->begin();
      for( ; ni != (*i).second->getNodes()->end() && 
	     nj != (*j).second->getNodes()->end(); ++ni, ++nj) {
	if((*ni)->getIndex() != (*nj)->getIndex()) {
	  return new std::string("Point boundary node index mismatch: " 
				 + (*i).first);
	}
      }
    }  

  for(CSkeletonEdgeBoundaryMap::const_iterator i=edgeBoundaries.begin(); 
      i!=edgeBoundaries.end(); ++i)
    {
      CSkeletonEdgeBoundaryMap::const_iterator j =
	omar->edgeBoundaries.find((*i).first);
      if(j == omar->edgeBoundaries.end()) {
	return new std::string("Edge boundary name mismatch: " + (*i).first);
      }
      if((*i).second->size() != (*j).second->size())  {
	return new std::string("Edge boundary size mismatch: " + (*i).first);
      }
      OrientedCSkeletonSegmentVector::const_iterator si =
	(*i).second->getSegments()->begin();
      OrientedCSkeletonSegmentVector::const_iterator sj =
	(*j).second->getSegments()->begin();
      for( ; si != (*i).second->getSegments()->end() && 
	     sj != (*j).second->getSegments()->end(); ++si, ++sj) 
	{
	  if(**si != **sj) {
	    return new std::string("Edge boundary node index mismatch: "
				   + (*i).first);
	}
      }
    }

#if DIM==3
  for(CSkeletonFaceBoundaryMap::const_iterator i = faceBoundaries.begin(); 
      i != faceBoundaries.end(); ++i)
    {
      CSkeletonFaceBoundaryMap::const_iterator j =
	omar->faceBoundaries.find((*i).first);
      if(j == omar->faceBoundaries.end()) {
	return new std::string("Face boundary name mismatch: " + (*i).first);
      }
      if((*i).second->size() != (*j).second->size())  {
	return new std::string("Face boundary size mismatch: " + (*i).first);
      }
      // sort the oriented faces by MultiNodeKey because they may have
      // been created in a different order
      OrientedCSkeletonFaceVector faces1, faces2;
      faces1.insert(faces1.begin(), (*i).second->getFaces()->begin(),
		    (*i).second->getFaces()->end());
      faces2.insert(faces2.begin(), (*j).second->getFaces()->begin(),
		    (*j).second->getFaces()->end());
      std::sort(faces1.begin(), faces1.end(), OrientedCSkeletonFace::ltKey);
      std::sort(faces2.begin(), faces2.end(), OrientedCSkeletonFace::ltKey);
      OrientedCSkeletonFaceVector::const_iterator si = faces1.begin();
      OrientedCSkeletonFaceVector::const_iterator sj = faces2.begin();
      for( ; si != faces1.end() && sj != faces2.end(); ++si, ++sj) {
	if(**si != **sj) {
	  return new std::string("Face boundary node index mismatch: "
				 + (*i).first);
	}
      }
    }
#endif	// DIM==3

  return new std::string("");
} // CSkeleton::compare

#ifdef DEBUG
std::string *CSkeleton::compare2(const CSkeletonBase *other) const
{
  const CSkeleton *that = other->sheriffSkeleton();
  std::vector<std::string> messages;
  // Node indices may differ between the two skeletons.  Map nodes
  // from one skeleton to the other using positions.
  NodePositionMap nodes0, nodes1;
  NodePositionSet pos0, pos1;
  for(unsigned int i=0; i<nnodes(); ++i) {
    nodes0[getNode(i)->position()] = i;
    pos0.insert(getNode(i)->position());
  }
  for(unsigned int i=0; i<that->nnodes(); ++i) {
    nodes1[that->getNode(i)->position()] = i;
    pos1.insert(that->getNode(i)->position());
  }
  // Find the nodes that aren't partnered.
  NodePositionSet ndiff;
  std::set_difference(pos0.begin(), pos0.end(), pos1.begin(), pos1.end(),
		      std::inserter(ndiff, ndiff.end()));
  for(const Coord3D &missing : ndiff) {
    messages.emplace_back("Node " + to_string(nodes0[missing]) +
			  " at position " + to_string(missing) +
			  " in this Skeleton is missing in that Skeleton");
  }
  ndiff.clear();
  std::set_difference(pos1.begin(), pos1.end(), pos0.begin(), pos0.end(),
		      std::inserter(ndiff, ndiff.end()));
  for(const Coord3D &missing : ndiff) {
    messages.emplace_back("Node " + to_string(nodes1[missing]) +
			  " at position " + to_string(missing) +
			  " in that Skeleton is missing in this Skeleton");
  }
  if(messages.empty()) {	// ie, nodes match up
    // If the nodes have the same positions, look for sets of four
    // elements that may have different common edges in the two
    // Skeletons.  These would correspond to different ways of
    // subdividing an element marked on all six edges, which is a
    // likely source of differences between Skeletons when the
    // roundoff in the homogeneity calculation changed.

    // Find elements in this that aren't in that, and vv.
    std::set<int> unmatchedEl0; // els in this but not in that.
    std::set<int> unmatchedEl1; // els in that but not in this.
    ElNodesMap elMap0, elMap1;
    NodePosSetSet elements0, elements1;
    for(CSkeletonElementIterator elit = beginElements(); elit != endElements();
	++elit)
      {
	NodePositionSet nodes;
	for(unsigned int i=0; i<4; i++)
	  nodes.insert((*elit)->getNode(i)->position());
	elMap0[nodes] = (*elit)->getIndex();
	elements0.insert(nodes);
      }
    for(CSkeletonElementIterator elit = that->beginElements();
	elit != that->endElements(); ++elit)
      {
	NodePositionSet nodes;
	for(unsigned int i=0; i<4; i++)
	  nodes.insert((*elit)->getNode(i)->position());
	elMap1[nodes] = (*elit)->getIndex();
	elements1.insert(nodes);
      }
    NodePosSetSet missing0, missing1;
    // missing0 contains the elements in this that aren't in
    // that. missing1 is the opposite.
    std::set_difference(elements0.begin(), elements0.end(),
			elements1.begin(), elements1.end(),
			std::inserter(missing0, missing0.end()));
    std::set_difference(elements1.begin(), elements1.end(),
			elements0.begin(), elements0.end(),
			std::inserter(missing1, missing1.end()));
    
    if(!missing0.empty() || !missing1.empty()) {
      // For each element that doesn't have a match in the other
      // skeleton, see if it's part of a set of four elements sharing
      // an edge, and if that set of four has a match.
      NodePosSetSet sixNodesSet0 = unmatchedSixNodeGroups(missing0, elMap0);
      NodePosSetSet sixNodesSet1 = that->unmatchedSixNodeGroups(missing1,
								elMap1);
      // If a six node set occurs in both skeletons, then the elements
      // in that set don't really disagree.  Remove them from the
      // sets.
      NodePosSetSet common;
      std::set_intersection(sixNodesSet0.begin(), sixNodesSet0.end(),
			    sixNodesSet1.begin(), sixNodesSet1.end(),
			    std::inserter(common, common.end()));

      // oofcerr << "CSkeletonBase::compare2: found " << common.size()
      // 	      << " common groups of six nodes" << std::endl;
      // for(const NodePositionSet &nds : common) {
      // 	OOFcerrIndent indent(2);
      // 	oofcerr << "CSkeletonBase::compare2: ";
      // 	std::cerr << nds;
      // 	oofcerr << std::endl;
      // }

      // For each unmatched element, see if it's in a shared group of
      // six nodes.
      NodePosSetSet okElements;
      for(const NodePositionSet &nds : missing0) {
	for(const NodePositionSet &sixNodes : common) {
	  if(std::includes(sixNodes.begin(), sixNodes.end(),
			   nds.begin(), nds.end()))
	    {
	      // This set of nodes is part of a common six node group.
	      okElements.insert(nds);
	      break;
	    }
	}
      }
      // Remove the ok elements from the missing element lists
      NodePosSetSet badElements0;
      std::set_difference(missing0.begin(), missing0.end(),
			  okElements.begin(), okElements.end(),
			  std::inserter(badElements0, badElements0.end()));
      okElements.clear();
      for(const NodePositionSet &nds : missing1) {
	for(const NodePositionSet &sixNodes : common) {
	  if(std::includes(sixNodes.begin(), sixNodes.end(),
			   nds.begin(), nds.end()))
	    {
	      okElements.insert(nds);
	      break;
	    }
	}
      }
      NodePosSetSet badElements1;
      std::set_difference(missing1.begin(), missing1.end(),
			  okElements.begin(), okElements.end(),
			  std::inserter(badElements1, badElements1.end()));

      for(const NodePositionSet &nds : badElements0) {
	messages.emplace_back("Element " + to_string(elMap0[nds]) +
			      " in this Skeleton is not in that one");
      }
      for(const NodePositionSet &nds : badElements1) {
	messages.emplace_back("Element " + to_string(elMap1[nds]) +
			      " in that Skeleton is not in this one");
      }
    } // end if there are missing elements in either skeleton
  } // end if nodes match up

  // Consolidate messages and return.
  std::string *result = new std::string();
  for(std::string &msg : messages) {
    if(result->empty())
      *result += msg;
    else {
      *result += "\n";
      *result += msg;
    }
  }
  if(result->empty())
    *result += "OK!";
  return result;
} // end CSkeleton::compare2

NodePosSetSet CSkeletonBase::unmatchedSixNodeGroups(const NodePosSetSet &els,
						    const ElNodesMap &elMap
						    )
  const
{
  NodePosSetSet sixNodesSet;
  for(const NodePositionSet &el0 : els) {
    ElNodesMap::const_iterator it = elMap.find(el0);
    assert(it != elMap.end());
    unsigned int idx = it->second; // element index in Skeleton
    const CSkeletonElement *elem0 = getElement(idx);
    // Look at each segment of the element by looping over pairs of nodes
    for(unsigned int j=0; j<3; j++) {
      const CSkeletonNode *nj = elem0->getNode(j);
      for(unsigned int k=j+1; k<4; k++) {
	const CSkeletonNode *nk = elem0->getNode(k);
	const CSkeletonSegment *seg = findExistingSegment(nj, nk);
	if(seg->num_elements() == 4) {
	  // Do the four elements on this segment use just six nodes?
	  NodePositionSet segnodes({nj->position(), nk->position()});
	  for(unsigned int e=0; e<4; e++) {
	    for(const CSkeletonNode *nl : *seg->getElement(this, e)->getNodes())
	      segnodes.insert(nl->position());
	  }
	  if(segnodes.size() == 6)
	    sixNodesSet.insert(segnodes);
	}
      }
    }
  }
  return sixNodesSet;
}
#endif // DEBUG


  

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeleton *CSkeleton::sheriffSkeleton() {
  return this;
}

const CSkeleton *CSkeleton::sheriffSkeleton() const {
  return this;
}

void CSkeleton::activate() {
  if(deputy != NULL) {
    deputy->deactivate();
    deputy = NULL;
  }
}

void CSkeleton::deputize(CDeputySkeleton* dep) {
  if(deputy)
    deputy->deactivate();
  deputy = dep;
}

void CSkeleton::addDeputy(CDeputySkeleton *dep) {
  deputy_list.push_back(dep);
}

void CSkeleton::removeDeputy(CDeputySkeleton *dep) {
  deputy_list.remove(dep);
}

NodePositionsMap *CSkeleton::getMovedNodes() const {
  return new NodePositionsMap;
}


void CSkeleton::needsHash() {
  point_locator = vtkSmartPointer<vtkMergePoints>();
  element_locator = vtkSmartPointer<vtkCellLocator>();
}


void CSkeleton::populate_femesh(FEMesh *realmesh, const MasterElement *master,
				Material *mat)
{
  DefiniteProgress *progress =
    dynamic_cast<DefiniteProgress*>(getProgress("Building mesh", DEFINITE));
  try {
    // Calling cleanUp() here ensures that node and element indices
    // agree with the objects' positions in the lists, which ensures
    // that that indices of the objects in the FEMesh agree with the
    // indices in the Skeleton.
    cleanUp();

    // The calculation of nfuncnodes and nmapnodes assumes that corner
    // nodes are both funcnodes and mapnodes.
    int nfuncnodes = (nnodes()
		      + nsegments()*(master->fun_order()-1)
		      + nelements()*master->ninteriorfuncnodes());
    realmesh->reserveFuncNodes(nfuncnodes);
    // mapnodes only includes nodes that are only for mapping.  Nodes
    // that have dofs and are mapping nodes are included in funcnodes.
    int nmapnodes = (nsegments()*master->nedgemapnodes_only()
		     + nfaces()*master->nfacemapnodes_only()); 
    realmesh->reserveMapNodes(nmapnodes);
  
    // Make the corner nodes.  Doing it now in this order guarantees
    // that node indices in the Skeleton and FEMesh agree.

    // TODO: This means that in the Mesh's dof list, the corner nodes
    // for all elements precede any of the non-corner nodes.  Does this
    // cause poor cache management or poor matrix block structure?
  
    // TODO OPT: SPLIT NODES When we have split nodes in the Mesh, indices
    // won't agree.  We need a better way of matching mesh nodes and
    // skeleton nodes!  Should each skeleton node keep a std::set of
    // mesh node pointers?

    for(unsigned int i=0; i<nnodes(); ++i) {
      realmesh->newFuncNode(nodes[i]->position());
    }

    // edgeNodeMap and faceNodeMap map edges and faces to the Nodes that
    // have been created on them, so that the nodes will be re-used on
    // neighboring elements.  They're set and used by realElement().
    // They could be FEMesh data, but they're not needed after the mesh
    // is constructed.
    SkelElNodeMap edgeNodeMap;
    SkelElNodeMap faceNodeMap;

    // make the elements
    for(unsigned int i=0; i<nelements(); ++i) {
      // CSkeletonElement::realElement() creates an element from the
      // appropriate MasterElement and calls FEMesh::addElement().
      progress->setMessage(to_string(i) + "/" + to_string(nelements()) +
			   " elements");
      progress->setFraction(i/(float) nelements());
      elements[i]->realElement(realmesh, i, master, this,
			       edgeNodeMap, faceNodeMap, mat);
      if(progress->stopped())
	throw ErrInterrupted();
    }
  }
  catch (...) {
    progress->finish();
    throw;
  }
  progress->finish();
}

CDeputySkeleton *CSkeletonBase::deputyCopy() {
  CDeputySkeleton *dep = new CDeputySkeleton(this);
  dep->setDefaultVSBbinSize(this);
  return dep;
}

void CSkeleton::copyNodes(CSkeleton *result) const {

  int nidx;
  // TODO OPT: Use vtkPoints::DeepCopy?
  for(unsigned int i = 0; i<nodes.size(); ++i) {
    nidx = result->points->InsertNextPoint(nodes[i]->position().xpointer());
    // The dynamic cast is required because copy_child returns a
    // CSkeletonSelectable*.
    result->nodes.push_back(
	    dynamic_cast<CSkeletonNode*>(
			 nodes[i]->copy_child(nidx, result->points)));
  }

//         // rebuild the node partnerships - must be done in separate loop
//         // after all nodes are created
//         for n in self.nodes:
//             for p in n.getPartners():
//                 n.getChildren()[-1].addPartner(p.getChildren()[-1])
}

// formerly known as improper copy
CSkeleton *CSkeleton::nodeOnlyCopy() {
  cleanUp();

  CSkeleton *result = new CSkeleton(MS, periodicity);
  result->setDefaultVSBbinSize(this);

  copyNodes(result);

  result->illegal_ = this->illegal_;

  return result;
}

// formerly known as proper copy

CSkeleton *CSkeleton::completeCopy() {
  // oofcerr << "CSkeleton::completeCopy" << std::endl;
  // This isn't const, because it has to set parent/child pointers.
  cleanUp();
  CSkeleton *result = new CSkeleton(MS, periodicity);
  result->setDefaultVSBbinSize(this);

  copyNodes(result);

  // Create all the segments and faces ahead of time by copying the
  // parents. This is simpler and more efficient than searching for
  // them later.
  int dummy = 0;
  for(CSkeletonSegmentIterator s = segments.begin(); s != segments.end(); ++s) {
    CSkeletonSegment *seg = dynamic_cast<CSkeletonSegment*>
      ((*s).second->copy_child(dummy, result->points));
    CSkeletonMultiNodeKey h(seg->getNode(0), seg->getNode(1));
    result->segments[h] = seg;
  }

  for(CSkeletonFaceIterator f = faces.begin(); f != faces.end(); ++f) {
    CSkeletonFace *face = dynamic_cast<CSkeletonFace*>
      ((*f).second->copy_child(dummy, result->points));
    CSkeletonMultiNodeKey h(face->getNode(0), face->getNode(1),
			    face->getNode(2));
    result->faces[h] = face;
  }

  for(unsigned int i=0; i<elements.size(); ++i) {
    CSkeletonElement *newEl = elements[i]->copy_child(i, result->points);
    VTKCellType type = newEl->getCellType();
    vtkIdType ids[4];
    newEl->getPointIds(ids);
    result->grid->InsertNextCell(type, 4, ids);
    result->addElement(newEl, ids);
  }

  result->illegal_ = this->illegal_;
  result->illegalCount = illegalCount;
  result->suspectCount = suspectCount;
  result->homogeneityIndex = homogeneityIndex;
  result->unweightedHomogIndex = unweightedHomogIndex;
  result->unweightedShapeEnergy = unweightedShapeEnergy;
  result->weightedShapeEnergy = weightedShapeEnergy;
  result->homogeneity_index_computation_time =
    homogeneity_index_computation_time.clone();
  result->unweighted_homogeneity_computation_time =
    unweighted_homogeneity_computation_time.clone();
  result->unweighted_shape_energy_computation_time =
    unweighted_shape_energy_computation_time.clone();
  result->weighted_shape_energy_computation_time =
    weighted_shape_energy_computation_time.clone();
  result->illegality_computation_time =
    illegality_computation_time.clone();
  result->illegal_count_computation_time =
    illegal_count_computation_time.clone();
  result->suspect_count_computation_time =
    suspect_count_computation_time.clone();
  result->geometry_timestamp =
    geometry_timestamp.clone();

  // TODO: Copy voxelSetBdys and vsbBins?
  vsbTimeStamp.backdate();

  // oofcerr << "CSkeleton::completeCopy: done" << std::endl;
  return result;
} // end CSkeleton::completeCopy

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

 // the caller is responsible for deleting this merge
ProvisionalMerge *CSkeleton::mergeNode(CSkeletonNode *n0, CSkeletonNode *n1) {
  ProvisionalMerge *merge = new ProvisionalMerge(this, n0, n1, "mergeNode");
  merge = addElementsToMerge(n0,n1,merge);

  //         partners = node0.getPartnerPair(node1)
  //         if partners is not None:
  //             change = self.addElementsToChange(partners[0], partners[1],
  //                                               change)
  //             if change is None:
  //                 return
  return merge;
}

ProvisionalMerge* CSkeleton::addElementsToMerge(
		 CSkeletonNode *n0, CSkeletonNode *n1, ProvisionalMerge *merge)
{
  if(!n0->canMergeWith(n1)) {
    delete merge;
    return NULL;
  }
  
  CSkeletonSegment *doomedSegment = findExistingSegment(n0, n1);
  if(doomedSegment == NULL) {
    delete merge;
    return NULL;
  }
  
  // elements that contain both nodes - topologically changing elements
  CSkeletonElementVector topElements;
  getSegmentElements(doomedSegment, topElements);
  // elements that contain node0 but not node1
  CSkeletonElementVector isoElements;
  CSkeletonElementVector *node0Elements = n0->getElements();
  for(CSkeletonElementIterator it = node0Elements->begin();
      it != node0Elements->end(); ++it)
    {
      // TODO: Why not just compare CSkeletonNode pointers here?
      if((*it)->getNode(0)->getIndex() != n1->getIndex() && 
	 (*it)->getNode(1)->getIndex() != n1->getIndex() && 
	 (*it)->getNode(2)->getIndex() != n1->getIndex() && 
	 (*it)->getNode(3)->getIndex() != n1->getIndex())
	isoElements.push_back(*it);
    }

  n0->moveTo( n1->position());
  for(CSkeletonElementVector::iterator it=isoElements.begin(); 
      it!=isoElements.end(); ++it) 
    {
      if((*it)->illegal()) {
	n0->moveBack();
	delete merge;
	return NULL;
      }
    }
  n0->moveBack();

  for(CSkeletonElementVector::iterator it=isoElements.begin(); 
      it!=isoElements.end(); ++it) 
    {
      const CSkeletonNodeVector *oldnodes = (*it)->getNodes();
      CSkeletonNodeVector *newnodes = new CSkeletonNodeVector(*oldnodes);
      for(unsigned int i = 0; i<newnodes->size(); ++i) {
	if((*newnodes)[i]->getIndex() == n0->getIndex()) 
	  (*newnodes)[i] = n1;
      }
      merge->substituteElement((*it), new CSkeletonElement(newnodes));
    }
  
  merge->removeElements(topElements);
  return merge;
} // CSkeleton::addElementsToMerge

void CSkeleton::removeElements(const CSkeletonElementSet &defunct_elements)
{
  for(CSkeletonElementSet::const_iterator it=defunct_elements.begin();
      it!=defunct_elements.end(); ++it)
    {
      // oofcerr << "CSkeleton::removeElements: removing " << **it << std::endl;
      removeElement((*it));
    }
  washMe = true;
}

void CSkeleton::removeElement(CSkeletonElement *element) {
  element->set_defunct();
  // Calling removeElement on a node, segment, or face will mark that
  // object as "defunct" when its last element is removed.
  for(CSkeletonNodeIterator it=element->getNodes()->begin(); 
      it!=element->getNodes()->end(); ++it) 
    {
      (*it)->removeElement(element, this);
    }
  for(unsigned int i=0; i<element->getNumberOfSegments(); ++i) {
    getElementSegment(element, i)->decrement_nelements();
  }
  for(unsigned int i=0; i<element->getNumberOfFaces(); ++i) {
    getElementFace(element, i)->decrement_nelements();
  }
  washMe = true;
}

void CSkeleton::removeNode(CSkeletonNode *node) {
  // oofcerr << "CSkeleton::removeNode: node=" << node
  // 	  << " " << node->position() << std::endl;
  node->set_defunct();
  // each of the segments and faces on this node become defunct as well
  CSkeletonSegmentSet segs;
  getNodeSegments(node, segs);
  for(CSkeletonSegmentSet::iterator it = segs.begin(); it != segs.end(); ++it)
    (*it)->set_defunct();
  CSkeletonFaceSet faces;
  getNodeFaces(node, faces);
  for(CSkeletonFaceSet::iterator it = faces.begin(); it != faces.end(); ++it)
    (*it)->set_defunct();
  washMe = true;
  ++numDefunctNodes;
}

bool CSkeleton::moveNodeTo(CSkeletonNode *node, const Coord &position) {
  bool moved = node->moveTo(position);
  //         node.moveTo(position)
  //         for partner in node.getPartners():
  //             partner.moveTo(position)
  return moved;
}

bool CSkeleton::moveNodeBy(CSkeletonNode *node, const Coord &disp) {
  bool moved = node->moveBy(disp);
  //         node.moveTo(position)
  //         for partner in node.getPartners():
  //             partner.moveTo(position)
  return moved;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeleton::cleanUp() {
  if(washMe) {
    // First remove the nodes, rebuilding the whole points object.
    int numNewNodes = nodes.size() - numDefunctNodes;
    CSkeletonNodeVector new_nodes;
    vtkSmartPointer<vtkPoints> newPoints = vtkSmartPointer<vtkPoints>::New();
    newPoints->Allocate(numNewNodes, numNewNodes);
    for(CSkeletonNodeIterator it = nodes.begin(); it!=nodes.end(); ++it) {
      if(!(*it)->is_defunct() && (*it)->nElements() != 0) {
	new_nodes.push_back(*it);
	int nidx = newPoints->InsertNextPoint((*it)->position().xpointer());
	(*it)->setIndex(nidx);
      }
      else {
	// oofcerr << "CSkeleton::cleanUp: deleting node " << *it << " " << **it
	// 	<< " defunct=" << (*it)->is_defunct()
	// 	<< " nElements=" << (*it)->nElements() << std::endl;
 	delete (*it);
      }
    }
    nodes.clear();
    nodes.insert(nodes.end(), new_nodes.begin(), new_nodes.end());
    // Other objects contain pointers to the Skeleton's points, so
    // it's not sufficient to say "points=newPoints" here.  The data
    // must be copied.  (TODO OPT: The copy could be avoided if the
    // other objects contained pointers to pointers to points.)
    // points->Initialize();
    points->DeepCopy(newPoints);

    // Now remove the elements, rebuilding the whole grid.
    vtkIdType eidx, n, ids[4];
    CSkeletonElementVector new_elements;
    grid->Initialize(); // reset to empty state;
    grid->Allocate(elements.size(), elements.size());
    for(CSkeletonElementIterator it=elements.begin(); it!=elements.end();
	++it)
      {
	if(!(*it)->is_defunct()) {
	  new_elements.push_back(*it);
	  VTKCellType type = (*it)->getCellType();
	  n = (*it)->getNumberOfNodes();
	  // this gets the new ids
	  (*it)->getPointIds(ids);
	  eidx = grid->InsertNextCell(type,n,ids);
	  (*it)->setIndex(eidx);
	}
	else
	  delete (*it);
      }
    elements.clear();
    elements.insert(elements.end(), new_elements.begin(),
		    new_elements.end());
    //grid->Squeeze();
    grid->SetPoints(points);

    // Then the segments and faces, which are deleted and erased from
    // their maps.
    std::vector<CSkeletonMultiNodeKey> doomedkeys;
    for(CSkeletonSegmentIterator it=segments.begin(); it!=segments.end();
	++it)
      {
	if((*it).second->is_defunct() || (*it).second->nElements() == 0) {
	  delete (*it).second;
	  doomedkeys.push_back((*it).first);
	}
      }
    for(unsigned int i=0; i<doomedkeys.size(); ++i) 
      segments.erase(doomedkeys[i]);

    doomedkeys.clear();
    for(CSkeletonFaceIterator it=faces.begin(); it!=faces.end(); ++it) {
      if((*it).second->is_defunct() || (*it).second->nElements() == 0) {
	delete (*it).second;
	doomedkeys.push_back((*it).first);
      }
    }
    for(unsigned int i = 0; i<doomedkeys.size(); ++i)
      faces.erase(doomedkeys[i]);

    washMe = false;
    numDefunctNodes = 0;
  } // end if(washMe)
} // CSkeleton::cleanUp

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CDeputySkeleton::CDeputySkeleton(CSkeletonBase *skel)
  : CSkeletonBase(),
    skeleton(skel->sheriffSkeleton()),
    active(false)
{
  // oofcerr << "CDeputySkeleton::ctor: " << *this << " " << this << std::endl;
  skeleton->addDeputy(this);
  illegal_ = skel->illegal();
  // When the DeputySkeleton is active, the positions of its nodes
  // are stored in the actual nodes, and the positions of the
  // reference Skeleton's nodes are stored in the nodePositions
  // dictionary.  When it's inactive, it's the other way around.
  nodePositions = skel->getMovedNodes(); // returns a new NodePositionsMap*.
  try {
    homogeneityIndex = skel->getHomogeneityIndex();
    //unweightedHomogIndex = skel->getUnweightedHomogeneity();
  } catch (ErrHomogeneityNotCalculable) {
    oofcerr << "HomogeneityNotCalculable error occurred when constructing deputy skeleton!" << std::endl;
    throw;
  }
  ++homogeneity_index_computation_time;
  //++unweighted_homogeneity_computation_time;
}

// Creating a new CDeputySkeleton from Python should always be done by
// calling newCDeputySkeleton.  The CDeputySkeleton constructor isn't
// swigged, so that Python won't have ownership of any
// CDeputySkeletons.

CDeputySkeleton *newCDeputySkeleton(CSkeletonBase *skel) {
  return new CDeputySkeleton(skel);
}

CDeputySkeleton::~CDeputySkeleton() {
  // oofcerr << "CDeputySkeleton::dtor: this=" << this << std::endl;
  delete nodePositions;
}

void CDeputySkeleton::destroy() {
  skeleton->removeDeputy(this);
  skeleton->destroyZombie(); // Destroy the sheriff only if it has no deputies.
  // oofcerr << "CDeputySkeleton::destroy: deleting " << this << std::endl;
  delete this;
}

void CDeputySkeleton::activate() {
  if(!active) {
    active = true;
    skeleton->deputize(this);
    swapPositions();
  }
}

void CDeputySkeleton::deactivate() {
  if(active) {
    active = false;
    swapPositions();
  }
}

CSkeleton* CDeputySkeleton::sheriffSkeleton() {
  return skeleton;
}

const CSkeleton* CDeputySkeleton::sheriffSkeleton() const {
  return skeleton;
}

const Coord CDeputySkeleton::nodePositionForSkeleton(CSkeletonNode *n) 
{
  // Gets the position of the node in this skeleton even if a deputy
  // is active.
  if(active)
    return n->position();
  else {
    NodePositionsMap::iterator it = nodePositions->find(n);
    if(it != nodePositions->end()) {
      return (*it).second;
    }
    else {
      return skeleton->nodePositionForSkeleton(n);
    }
  }
} 

const Coord CDeputySkeleton::originalPosition(CSkeletonNode *n) {
  NodePositionsMap::iterator it = nodePositions->find(n);
  if(it != nodePositions->end()) {
    return (*it).second;
  }
  else {
    return n->position();
  }
}

void CDeputySkeleton::swapPositions() {
  // For each moved node, swap the position stored in nodePositions
  // with the position stored in the Skeleton's main data.  Called
  // when a DeputySkeleton is activated or deactivated.

  // The timestamp should *not* be updated.  This operation does not
  // change this Skeleton, it just changes where its data is stored.
  
  for(NodePositionsMap::iterator npmit=nodePositions->begin();
      npmit!=nodePositions->end(); ++npmit) 
    {
      CSkeletonNode *node = (*npmit).first;
      Coord temp = (*npmit).second;
      (*npmit).second = node->getPosition();
      node->unconstrainedMoveTo(temp);
    }
  skeleton->needsHash();
}

NodePositionsMap *CDeputySkeleton::getMovedNodes() const {
  // getMovedNodes() is a virtual function called only when
  // constructing a new CDeputySkeleton for a CSkeleton or a
  // CDeputySkeleton.  The CSkeleton version of getMovedNodes()
  // returns an empty NodePositionsMap.  This one returns a
  // NodePositionsMap containing the positions of the nodes that have
  // been already moved.

  if(active) { 
    // This deputy is active, so the node positions have to be
    // retrieved from the nodes (actually the CSkeleton's points
    // vector).
    NodePositionsMap *npm = new NodePositionsMap;
    for(NodePositionsMap::iterator npmit = nodePositions->begin();
	npmit != nodePositions->end(); ++npmit) 
      {
	// Copy position from CSkeletonNode into nodePositions[node]
	CSkeletonNode *node = (*npmit).first;
	(*npm)[node] = node->getPosition();
      }
    return npm;
  }
  // This deputy is not active.  Just copy the NodePositionsMap.
  return new NodePositionsMap(*nodePositions);
}

bool CDeputySkeleton::moveNodeTo(CSkeletonNode *node, const Coord &position) {
  NodePositionsMap::iterator npmit = nodePositions->find(node);
  if(npmit == nodePositions->end()) {
    (*nodePositions)[node] = node->getPosition();
  }
  bool moved = node->moveTo(position);
//         for partner in node.getPartners():
//             if not self.nodePositions.has_key(partner):
//                 self.nodePositions[partner] = partner.position()
//             partner.moveTo(position)
  return moved;
}

bool CDeputySkeleton::moveNodeBy(CSkeletonNode *node, const Coord &disp) {
  NodePositionsMap::iterator npmit = nodePositions->find(node);
  if(npmit == nodePositions->end()) {
    (*nodePositions)[node] = node->getPosition();
  }
  bool moved = node->moveBy(disp);
//         for partner in node.getPartners():
//             if not self.nodePositions.has_key(partner):
//                 self.nodePositions[partner] = partner.position()
//             partner.moveTo(position)
  return moved;
}

void CDeputySkeleton::moveNodeBack(CSkeletonNode *node) {
  node->moveBack();
  if(node->getPosition() == (*nodePositions)[node]) {
    nodePositions->erase(node);
  }
//         for partner in node.getPartners():
//             partner.moveBack()
//             if partner.position() == self.nodePositions[partner]:
//                 del self.nodePositions[partner]
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string *CSkeletonBase::sanityCheck() const {
#ifndef HAVE_SSTREAM
  std::ostrstream diag;		// "diag" for diagnosis, not diagonal
#else
  std::ostringstream diag;
#endif
  DefiniteProgress *prog =
    dynamic_cast<DefiniteProgress*>(getProgress("Sanity Check", DEFINITE));
  try {
    // Copy the skeletons nodes into a set for fast lookup.
    CSkeletonNodeSet nodeset(beginNodes(), endNodes());

    // Loop over elements
    {
      int i = 0;
      for(CSkeletonElementIterator el=beginElements(); el!=endElements(); ++el)
	{
	  if((*el)->illegal()) {
	    diag << "Illegal element: " << *(*el) << std::endl;
	  }
	  const CSkeletonNodeVector *enodes = (*el)->getNodes();
	  for(CSkeletonNodeIterator n=enodes->begin(); n!=enodes->end(); ++n) {
	    // Check that each of the element's nodes is in the skeleton's
	    // list of nodes.
	    if(nodeset.find(*n) == nodeset.end()) 
	      diag << "Element " << (*el)->getUid()
		   << " contains a node " << (*n)->getUid()
		   << " not in the skeleton" << std::endl;
	    // Check that the element is in each of its nodes' list of elements.
	    const CSkeletonElementVector *nodeEls = (*n)->getElements();
	    if(std::find(nodeEls->begin(), nodeEls->end(), *el)
	       == nodeEls->end())
	      {
		diag << "Element " << (*el)->getUid()
		     << " is missing from node " << (*n)->getUid()
		     << "'s list of elements" << std::endl;
	      }
	    
	  }	// end loop over the element's nodes
	  // Check that the skeleton contains a segment for each pair of
	  // nodes in the element.
	  // TODO: This really should be done by an element method,
	  // because it assumes that the element is tetrahedral.
	  for(CSkeletonNodeIterator n1=enodes->begin(); n1!=enodes->end(); ++n1)
	    {
	      CSkeletonNodeIterator n2 = n1;
	      n2++;
	      for(; n2!=enodes->end(); ++n2) {
		if(!doesSegmentExist(*n1, *n2))
		  diag << "Skeleton segment is missing for nodes "
		       << (*n1)->getUid() << " and " << (*n2)->getUid()
		       << " of element " << (*el)->getUid() << std::endl;
	      }
	    }
	  i++;
	  prog->setMessage("checking " + to_string(i) + "/" +
			   to_string(nelements()) + " elements");
	  prog->setFraction(i/(double) nelements());
	} // end loop over elements in the skeleton
    }	  // end element block

    // Loop over nodes
    {
      int i = 0;
      // Create an element set for fast lookup
      ConstCSkeletonElementSet elset(beginElements(), endElements());
      for(CSkeletonNodeIterator n=beginNodes(); n!=endNodes(); ++n) {
	// TODO: This is really slow for large skeletons, and makes the
	// regression test very slow.  It would probably be faster if we
	// converted the skeleton's std::vector of elements to a
	// std::set and searched it instead of the vector in the call to
	// hasElement() in the inner loop.
	CSkeletonElementVector *els = (*n)->getElements();
	if(els->empty())
	  diag << "Node " << (*n)->getUid() << " has no elements" << std::endl;
	for(CSkeletonElementIterator el=els->begin(); el!=els->end(); ++el) {
	  if(elset.find(*el) == elset.end())
	    //if(!hasElement(*el))
	    diag << "Node " << (*n)->getUid() << " contains an element "
		 << (*el)->getUid() << " not in the skeleton" << std::endl;
	}

	/* TODO: The following python code was not translated to C++
	   with the rest of this function.  When periodicity is
	   included, this code should be translated.

	   # Check that nodes on periodic boundaries have partners
	   #         x = node.position().x
	   #         y = node.position().y
	   #         xmax = self.MS.size().x
	   #         ymax = self.MS.size().y
	   #         if self.x_periodicity and (x == 0.0 or x == xmax):
	   #             p = node.getDirectedPartner('x')
	   #             if not p or ((x == 0.0 and p.position().x != xmax) or
	   #                          (x ==  xmax and p.position().x != 0.0)):
	   #                 reporter.report(node.__class__.__name__, node.index(),
	   #                                 "at", node.position(),
	   #                                 "has no periodic partner in x")
	   #                 reporter.report("   partners are at",
	   #                                 [(ptnr.position(), ptnr.index())
	   #                                  for ptnr in node.getPartners()])
	   #                 sane = False
	   #         if self.y_periodicity and (y == 0.0 or y == ymax):
	   #             p = node.getDirectedPartner('y')
	   #             if not p or ((y == 0.0 and p.position().y != ymax) or
	   #                          (y == ymax and p.position().y != 0.0)):
	   #                 reporter.report(node.__class__.__name__, node.index(),
	   #                                 "at", node.position(),
	   #                                 "has no periodic partner in y")
	   #                 reporter.report("   partners are at",
	   #                                 [(ptnr.position(), ptnr.index())
	   #                                  for ptnr in node.getPartners()])
	   #                 reporter.report([ptnr.position()-primitives.Point(x, ymax)
	   #                                  for ptnr in node.getPartners()])
	   #                 sane = False
	   #         # Check self consistency of partner lists
	   #         for partner in node.getPartners():
	   #             if node not in partner.getPartners():
	   #                 reporter.report("Inconsistent partner lists for",
	   #                                 node.__class__.__name__, node.index(),
	   #                                 "at", node.position(), "and",
	   #                                 partner.__class__.__name__, partner.index(),
	   #                                 "at", partner.position())

	*/
      
	i++;
	prog->setMessage("checking " + to_string(i) + "/" + to_string(nnodes())
			 + " nodes");
	prog->setFraction(i/(double) nnodes());
      } // end loop over nodes in the skeleton
    }
    
    // Loop over segments
    {
      int i = 0;
      for(CSkeletonSegmentIterator s=beginSegments(); s!=endSegments(); ++s) {
	// Check that segment's nodes are in the skeleton
	const CSkeletonNodeVector *nodes = (*s).second->getNodes();
	for(CSkeletonNodeIterator n=nodes->begin(); n!=nodes->end(); ++n) {
	  if(nodeset.find(*n) == nodeset.end())
	    diag << "Segment " << (*s).second->getUid() << " contains a node "
		 << (*n)->getUid() << " not in the skeleton" << std::endl;
	}
	++i;
	prog->setMessage("checking " + to_string(i) + "/" +
			 to_string(nsegments()) + " segments");
	prog->setFraction(i/(double) nsegments());
      } // end loop over segments in the skeleton
    }
    
    // Loop over faces
    {
      int i = 0;
      for(CSkeletonFaceIterator f=beginFaces(); f!=endFaces(); ++f) {
	const CSkeletonNodeVector *nodes = (*f).second->getNodes();
	for(CSkeletonNodeIterator n=nodes->begin(); n!=nodes->end(); ++n) {
	  if(nodeset.find(*n) == nodeset.end())
	    diag << "Face " << (*f).second->getUid() << " contains a node "
		 << (*n)->getUid() << " not in the skeleton" << std::endl;
	}
	ConstCSkeletonElementVector els;
	(*f).second->getElements(this, els);
	if(!(els.size()==2 || (els.size()==1 && onOuterFace(nodes)))) {
	  diag << "Face " << (*f).second->getUid()
	       << " has the wrong number of elements" << std::endl;
	}
      
	++i;
	prog->setMessage("checking " + to_string(i) + "/" + to_string(nfaces())
			 + " faces");
	prog->setFraction(i/(double) nfaces());
      }
  } // end loop over faces in the skeleton
  }
  catch(...) {
    diag << "An exception occured in CSkeletonBase::sanityCheck" << std::endl;
  }
  prog->finish();
  return new std::string(diag.str());
} // CSkeletonBase::sanityCheck

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

DeputyProvisionalChanges::DeputyProvisionalChanges(CDeputySkeleton *dep,
						   const std::string &n) 
  : ProvisionalChangesBase(n),
    deputy(dep),
    illegalCached(false)
{}

void DeputyProvisionalChanges::moveNode(CSkeletonNode *node, const Coord &x,
					bool *mob)
{
  MoveNode move;
  move.node = node;
  move.position = x;
  movednodes.push_back(move);
  CSkeletonElementVector *node_elements = node->getElements();
  elements.insert(elements.end(), node_elements->begin(),
		  node_elements->end());
}

// TODO: Combine illegal() and suspect(), if they're always used
// together.

bool DeputyProvisionalChanges::illegal() {
  // Will this change produce any illegal elements?
  if(!illegalCached) {
    makeNodeMove();
    for(CSkeletonElementIterator elit = elements.begin();
	elit != elements.end(); ++elit) {
      if((*elit)->illegal()) {
	moveNodeBack();
	cachedIllegal = true;
	illegalCached = true;
	break;
      }
    }
    if(!illegalCached) {
      moveNodeBack();
      cachedIllegal = false;
      illegalCached = true;
    }
  }
  return cachedIllegal;
}

bool DeputyProvisionalChanges::suspect() {
  // Will this change increase the number of suspect elements?
  // TODO: Cache the return value?
  int nBefore = 0;
  for(CSkeletonElement *el : elements) {
    if(el->suspect())
      ++nBefore;
  }
  makeNodeMove();
  int nAfter = 0;
  for(CSkeletonElement *el : elements) {
    if(el->suspect()) {
      ++nAfter;
    }
  }
  moveNodeBack();
  return nAfter > nBefore;
}

void DeputyProvisionalChanges::makeNodeMove() {
  for(unsigned int i=0; i<movednodes.size(); ++i) {
    deputy->moveNodeTo(movednodes[i].node, movednodes[i].position);
  }
}

void DeputyProvisionalChanges::moveNodeBack() {
  for(unsigned int i=0; i<movednodes.size(); ++i){
    deputy->moveNodeBack(movednodes[i].node);
  }
}

// deltaE() used to weight element energies by volume, and a TODO said
// "Make similar changes to ProvisionalChanges".  This seems to be the
// wrong thing to do, because it encourages anneal to flatten elements
// so that they have high shape energy but near zero volume.  The
// volume weighting has been commented out.

double DeputyProvisionalChanges::deltaE(double alpha) {
  // Return the change in energy per element if this move were to
  // be accepted.
  if(!deltaECached) {
    double oldE = 0.0;
    double oldV = 0.0;
    for(CSkeletonElementIterator elit=elements.begin(); elit!=elements.end();
	++elit) 
      {
	double vol = 1; // (*elit)->volume();
	oldE += vol*(*elit)->energyTotal(deputy, alpha);
	oldV += vol;
      }
    oldE /= oldV;
    // Move nodes accordingly to simulate the change
    makeNodeMove();
    // Energy after the change
    double newE = 0.0;
    double newV = 0.0;
    for(CSkeletonElementIterator elit=elements.begin(); elit!=elements.end();
	++elit) 
      {
	// we must call this explicitly so that the cached homogeneity
	// is correct
	(*elit)->findHomogeneityAndDominantPixel(deputy);
	const HomogeneityData &homogeneity = (*elit)->getHomogeneityData();
	double vol = 1; //(*elit)->volume();
	newE += vol*(*elit)->energyTotal(deputy, alpha);
	newV += vol;
	cachedNewHomogeneity[(*elit)] = homogeneity;
      }
    newE /= newV;
    moveNodeBack();
    //cachedDeltaE = (newE - oldE)/nelements;
    deltaECached = true;
    cachedDeltaE = (newE - oldE);
  }    
  return cachedDeltaE;
}

void DeputyProvisionalChanges::accept() {
  makeNodeMove();
  for(HomogeneityDataMap::iterator hdmit = cachedNewHomogeneity.begin();
      hdmit != cachedNewHomogeneity.end(); ++hdmit)
    {
      (*hdmit).first->setHomogeneityData((*hdmit).second);
    }
}

ProvisionalChanges::ProvisionalChanges(CSkeleton *skel, const std::string &n)
  : ProvisionalChangesBase(n),
    skeleton(skel)
{
  // oofcerr << "ProvisionalChanges::ctor: " << this << std::endl;
}

ProvisionalChanges::~ProvisionalChanges() {
  // oofcerr << "ProvisionalChanges::dtor: " << this << std::endl;
  // delete provisional elements that have not been promoted
  for(CSkeletonElementSet::iterator it=after.begin(); it!=after.end(); ++it)
    if((*it)->getIndex() == -1)
      delete *it;
}

bool ProvisionalChanges::illegal() {
  // Will this change produce any illegal elements?
  //* TODO OPT: should we cache the illegal status as we do for
  //* DeputyProvisionalChanges?
  bool verboten = false;
  makeNodeMove();
  for(CSkeletonElementSet::iterator elit = after.begin();
      elit != after.end(); ++elit) 
    {
      if((*elit)->illegal() || (*elit)->suspect()) {
	verboten = true;
	break;
      }
    }
  moveNodeBack();
  return verboten;
}

bool ProvisionalChanges::suspect() {
  // Will this change increase the number of suspect elements?
  int nBefore = 0;
  for(const CSkeletonElement *el : before) {
    if(el->suspect())
      ++nBefore;
  }
  makeNodeMove();
  int nAfter = 0;
  for(const CSkeletonElement *el : after) {
    if(el->suspect())
      ++nAfter;
  }
  moveNodeBack();
  return nAfter > nBefore;
}

void ProvisionalChanges::moveNode(CSkeletonNode *node, const Coord &x,
				  bool *mob) 
{
  MoveNode move;
  move.node = node;
  move.position = x;
  memcpy(move.mobility, mob, 3*sizeof(bool));
  movednodes.push_back(move);
  for(CSkeletonElementIterator el=node->getElements()->begin();
      el!=node->getElements()->end(); ++el)
    {
      before.insert(*el);
      if(removed.count(*el) == 0)
	after.insert(*el);
    }
}

void ProvisionalChanges::makeNodeMove() {
  for(unsigned int i=0; i<movednodes.size(); ++i)
    movednodes[i].node->moveTo(movednodes[i].position);
}

void ProvisionalChanges::moveNodeBack() {
  for(unsigned int i=0; i<movednodes.size(); ++i)
    movednodes[i].node->moveBack();
}

double ProvisionalChanges::deltaE(double alpha) {
  if(!deltaECached) {
    double oldE = 0.0;
    for(ConstCSkeletonElementSet::const_iterator elit = before.begin(); 
	elit != before.end(); ++elit) 
      {
	oldE += (*elit)->energyTotal(skeleton, alpha);
      }
    oldE /= before.size();
    makeNodeMove();
    double newE = 0.0;
    for(CSkeletonElementSet::const_iterator elit = after.begin(); 
	elit != after.end(); ++elit) 
      newE += (*elit)->energyTotal(skeleton, alpha);
    if(!after.empty())
      newE /= after.size();
    moveNodeBack();
    deltaECached = true;
    cachedDeltaE = newE - oldE;
  }
  return cachedDeltaE;
}

void ProvisionalChanges::removeElement(CSkeletonElement *el) {
  // oofcerr << "ProvisionalChanges::removeElement: " << this << " " << *el
  // 	  << std::endl;
  removed.insert(el);
  // oofcerr << "ProvisionalChanges::removeElement: added to removed" << std::endl;
  before.insert(el);
  // oofcerr << "ProvisionalChanges::removeElement: inserted in before" << std::endl;
  // oofcerr << "ProvisionalChanges::removeElement: after.count=" << after.count(el) << std::endl;
  if(after.count(el) != 0)
    after.erase(el);
  // oofcerr << "ProvisionalChanges::removeElement: done" << std::endl;
}

void ProvisionalChanges::removeElements(const CSkeletonElementVector &elements)
{
  removed.insert(elements.begin(), elements.end());
  before.insert(elements.begin(), elements.end());
  for(CSkeletonElementIterator el=elements.begin(); el!=elements.end(); ++el)
    if(after.count(*el) != 0)
      after.erase(*el);
}

void ProvisionalChanges::insertElement(CSkeletonElement *el) {
  inserted.insert(el);
  after.insert(el);
}

void ProvisionalChanges::substituteElement(CSkeletonElement *old,
					   CSkeletonElement *newEl) 
{
  // annotate << "substituting element: old= " << *old << std::endl;
  // annotate << "                      new= " << *newEl << std::endl;
  substitutions.insert(CSkeletonSelectablePair(old,newEl));
  before.insert(old);
  after.insert(newEl);
}

void ProvisionalChanges::substituteSegment(CSkeletonSegment *old,
					   CSkeletonSegment *newSeg)
{
  // annotate << "substituting segment: old= " << *old << std::endl;
  // annotate << "                      new= " << *newSeg << std::endl;
  substituteSegment(old, newSeg->getNode(0), newSeg->getNode(1));
}

void ProvisionalChanges::substituteSegment(CSkeletonSegment *old,
					   CSkeletonNode *node0,
					   CSkeletonNode *node1)
{
  // annotate << "substituting segment: old= " << *old << std::endl;
  // annotate << "                      new= " << node0->position()
  // 	   << " " << node1->position()  << std::endl;
  seg_substitutions.insert(SegmentSubstitution(old, node0, node1));
#if DIM==3  
  // Also find the face substitutions implied by this segment substitution.
  CSkeletonFaceVector faces;
  skeleton->getSegmentFaces(old, faces);
  for(CSkeletonFaceVector::iterator f=faces.begin(); f!=faces.end(); ++f) {
    CSkeletonNode *other_node = (*f)->get_other_node(old);
    if(*other_node != *node0 && *other_node != *node1) {
      face_substitutions.insert(FaceSubstitution(*f, node0, node1, other_node));
      // substituteFace(*f, node0, node1, other_node);
    }
  }
#endif // DIM==3
}

void ProvisionalChanges::substituteFace(CSkeletonFace *old,
					CSkeletonFace *newFace)
{
  substituteFace(old,
		 newFace->getNode(0), newFace->getNode(1), newFace->getNode(2));
}

void ProvisionalChanges::substituteFace(CSkeletonFace *old,
					CSkeletonNode *node0,
					CSkeletonNode *node1,
					CSkeletonNode *node2)
{
  // annotate << "substituting face: old= " << *old << std::endl;
  // annotate << "                 nodes= "
  // 	   << node0->getUid() << " " << node0->position() << " " 
  // 	   << node1->getUid() << " " << node1->position() << " " 
  // 	   << node2->getUid() << " " << node2->position() << std::endl;
  face_substitutions.insert(FaceSubstitution(old, node0, node1, node2));
}

CSkeletonMultiNodeSelectable *SegmentSubstitution::getSubstitute(
							 CSkeleton *skeleton)
  const
{
  if(*node0 == *node1)
    return NULL;
  // return skeleton->getOrCreateSegment(node0, node1);
  return skeleton->findExistingSegment(node0, node1);
}

CSkeletonMultiNodeSelectable *FaceSubstitution::getSubstitute(
						      CSkeleton *skeleton)
  const
{
  if(*node0 == *node1 || *node1 == *node2 || *node2 == *node0)
    return NULL;
  // return skeleton->getOrCreateFace(node0, node1, node2);
  return skeleton->findExistingFace(node0, node1, node2);
}

void SkeletonSubstitutionBase::substitute(CSkeleton *skeleton) const {
  CSkeletonSelectableList &rents = substitutee->getParents();
  CSkeletonMultiNodeSelectable *subs = getSubstitute(skeleton);
  if(!subs || subs->is_defunct() || subs->nElements() == 0) {
    // oofcerr << "SkeletonSubstitutionBase::substitute: skipping " << *subs
    // 	    << std::endl;
    return;
  }
  // oofcerr << "SkeletonSubstitutionBase::substitute: old= "
  // 	  << *substitutee << std::endl
  // 	  << "                                      new= "
  // 	  << *subs << std::endl;
  for(CSkeletonSelectableList::iterator p=rents.begin(); p!=rents.end(); ++p) {
    subs->add_parent(*p);
    (*p)->add_child(subs);
    (*p)->remove_child(substitutee);
  }
}

bool SegSubstitutionLT::operator()(const SegmentSubstitution &ss0, 
				   const SegmentSubstitution &ss1)
  const
{
  CSkeletonSelectableLTUid<CSkeletonMultiNodeSelectable> comparator;
  if(comparator(ss0.substitutee, ss1.substitutee)) return true;
  if(comparator(ss1.substitutee, ss0.substitutee)) return false;
  CSkeletonMultiNodeKey key0(ss0.node0, ss0.node1);
  CSkeletonMultiNodeKey key1(ss1.node0, ss1.node1);
  return key0 < key1;
}

bool FaceSubstitutionLT::operator()(const FaceSubstitution &fs0, 
				    const FaceSubstitution &fs1)
  const
{
  CSkeletonSelectableLTUid<CSkeletonMultiNodeSelectable> comparator;
  if(comparator(fs0.substitutee, fs1.substitutee)) return true;
  if(comparator(fs1.substitutee, fs0.substitutee)) return false;
  CSkeletonMultiNodeKey key0(fs0.node0, fs0.node1, fs0.node2);
  CSkeletonMultiNodeKey key1(fs1.node0, fs1.node1, fs1.node2);
  return key0 < key1;
}

void ProvisionalChanges::accept() {
#ifdef DEBUG
  int deltaSuspect = 0;
  int deltaIllegal = 0;
  // Count number of suspect and illegal elements being removed before
  // nodes are moved
  for(CSkeletonSelectablePairSet::iterator it=substitutions.begin();
      it!=substitutions.end(); ++it)
    {
      CSkeletonElement *oldel = dynamic_cast<CSkeletonElement*>((*it).first);
      if(oldel->suspect())
	--deltaSuspect;
      if(oldel->illegal())
	--deltaIllegal;
    }
  for(CSkeletonElement *el : removed) {
    if(el->illegal())
      --deltaIllegal;
    if(el->suspect())
      --deltaSuspect;
  }
#endif // DEBUG  


  // Must move nodes first because newly inserted elements legality
  // depends on the new positions
  // oofcerr << "ProvisionalChanges::accept: " << this << " " << name
  // 	  << std::endl;
  // oofcerr << "ProvisionalChanges::accept: narrative=" << std::endl
  //  	  << annotate.str() << std::endl;
  for(MoveNodeVector::iterator it=movednodes.begin(); it!=movednodes.end();
      ++it) 
    {
      // oofcerr << "    Moving node from " << (*it).node->position() 
      // 	      << " to " << (*it).position 
      // 	      << " with mobility "
      // 	      << (*it).mobility[0] << " " << (*it).mobility[1] << " "
      // 	      << (*it).mobility[2] << std::endl;
      (*it).node->moveTo((*it).position);
      (*it).node->setMobilityX((*it).mobility[0]);
      (*it).node->setMobilityY((*it).mobility[1]);
      (*it).node->setMobilityZ((*it).mobility[2]);
    }


  // Element insertions.
  for(CSkeletonElementSet::iterator it=inserted.begin(); it!=inserted.end(); 
      ++it)
    {
      // acceptProvisionalElement() calls addElement(), which creates
      // the face and segment objects if necessary.
      // oofcerr << "   Inserting element " << **it << std::endl;
      skeleton->acceptProvisionalElement((*it));
#ifdef DEBUG
      if((*it)->suspect()) {
	++deltaSuspect;
	// oofcerr << "ProvisionalChanges::accept: suspect element created by "
	// 	<< name << std::endl;
	// oofcerr << "ProvisionalChanges::accept:    " << *(*it) << std::endl;
      }
      if((*it)->illegal())
	++deltaIllegal;
#endif // DEBUG
    }

  // Element substitutions (insertion of one and removal of another
  // with no topological changes).
  for(CSkeletonSelectablePairSet::iterator it=substitutions.begin(); 
      it != substitutions.end(); ++it) 
    {
      // oofcerr << "    Substituting element: old= " << *(*it).first << std::endl
      // 	      << "                          new= " << *(*it).second <<std::endl;
      CSkeletonElement *oldel = dynamic_cast<CSkeletonElement*>((*it).first);
      CSkeletonElement *newel = dynamic_cast<CSkeletonElement*>((*it).second);
#ifdef DEBUG
      if(newel->suspect())
	++deltaSuspect;
      if(newel->illegal())
	++deltaIllegal;
#endif // DEBUG
      skeleton->acceptProvisionalElement(newel);
      // the old segments and faces must be in the same order
      for(unsigned int i = 0; i < oldel->getNumberOfSegments(); ++i) {
	CSkeletonSegment *oldseg = skeleton->getElementSegment(oldel,i);
	CSkeletonSegment *newseg = skeleton->getElementSegment(newel,i);
	// the elements may still share segments
	if(*newseg != *oldseg) { 
	  // oofcerr << "    Implicit segment substitution: old= "
	  // 	  << *oldseg << std::endl
	  // 	  << "                                   new= "
	  // 	  << *newseg << std::endl;
	  CSkeletonSelectableList &parents = oldseg->getParents();
	  for(CSkeletonSelectableList::iterator p=parents.begin(); 
	      p != parents.end(); ++p)
	    {
	      newseg->add_parent(*p);
	      (*p)->add_child(newseg);
	    }
	}
      }	// end loop over element segments
      for(unsigned int i=0; i<oldel->getNumberOfFaces(); ++i) {
	CSkeletonFace *oldface = skeleton->getElementFace(oldel,i);
	CSkeletonFace *newface = skeleton->getElementFace(newel,i);
	if(*newface != *oldface) {
	  // oofcerr << "     Implicit face substitution: old= "
	  // 	  << *oldface << std::endl
	  // 	  << "                                 new= "
	  // 	  << *newface << std::endl;
	  CSkeletonSelectableList &parents = oldface->getParents();
	  for(CSkeletonSelectableList::iterator p=parents.begin(); 
	      p!=parents.end(); ++p)
	    {
	      newface->add_parent(*p);
	      (*p)->add_child(newface);
	    }
	}
      }	// end loop over element faces
      // oofcerr << "ProvisionalChanges::accept: removing " << *oldel << std::endl;
      skeleton->removeElement(oldel);
      // oofcerr << "ProvisionalChanges::accept: removed element" << std::endl;
    } // end loop over element substitutions

  for(SegmentSubstitutionSet::const_iterator it=seg_substitutions.begin();
      it!=seg_substitutions.end(); ++it)
    {
      (*it).substitute(skeleton);
    }
  for(FaceSubstitutionSet::const_iterator it=face_substitutions.begin();
      it!=face_substitutions.end(); ++it)
    {
      (*it).substitute(skeleton);
    }

  // for(CSkeletonSelectablePairSet::iterator it = seg_substitutions.begin();
  //     it != seg_substitutions.end(); ++it) 
  //   {
  //     CSkeletonSelectableList &parents = (*it).first->getParents();
  //     for(CSkeletonSelectableList::iterator p=parents.begin(); 
  // 	  p!=parents.end(); ++p)
  //     {
  // 	(*it).second->add_parent(*p);
  // 	(*p)->add_child((*it).second);
  //     }
  //   }

  // for(CSkeletonSelectablePairSet::iterator it=face_substitutions.begin();
  //     it!=face_substitutions.end(); ++it) 
  //   {
  //     CSkeletonSelectableList &parents = (*it).first->getParents();
  //     for(CSkeletonSelectableList::iterator p = parents.begin(); 
  // 	  p != parents.end(); ++p)
  // 	{
  // 	  (*it).second->add_parent(*p);
  // 	  (*p)->add_child((*it).second);
  // 	}
  //   }

//             # Call Skeleton.removeElements only *after* the segment
//             # parents have been reestablished, because removing the
//             # elements may remove the segments from the skeleton.
//             # self.skeleton.removeElements(old)
//         for old in self.seg_subs.keys():
//             new_segs = self.seg_subs[old]
//             for new in new_segs:
//                 for parent in old.getParents():
//                     new.add_parent(parent)
//                     parent.add_child(new)
//
  // oofcerr << "ProvisionalChanges::accept: removing elements" << std::endl;
  skeleton->removeElements(removed);
  // oofcerr << "ProvisionalChanges::accept: done" << std::endl;

#ifdef DEBUG
  if(deltaIllegal > 0 || deltaSuspect > 0)
    oofcerr << "ProvisionalChanges::accept: " << name << " deltaIllegal="
	    << deltaIllegal << " deltaSuspect=" << deltaSuspect << std::endl;
#endif	// DEBUG
  
} // end ProvisionalChanges::accept

void ProvisionalMerge::accept() {  
  node0->makeSibling(node1);
  skeleton->removeNode(node0);
  ProvisionalChanges::accept();
}

void ProvisionalInsertion::removeAddedNodes() {
  for(CSkeletonNodeIterator n=added_nodes.begin(); n!=added_nodes.end(); ++n)
    skeleton->removeNode(*n);
}

void ProvisionalChanges::checkVolume() {
  double tol = 0.001;
  double old_vol = 0;
  double new_vol = 0;
  makeNodeMove();
  for(ConstCSkeletonElementSet::iterator i=before.begin(); i!=before.end(); ++i) {
    old_vol += (*i)->volume();
  }
  for(CSkeletonElementSet::iterator i=after.begin(); i!=after.end(); ++i) {
    new_vol += (*i)->volume();
  }
  moveNodeBack();
  if(fabs(new_vol - old_vol)/old_vol > tol) {
    oofcerr << "ProvisionalChanges::checkVolume: " <<  old_vol << " "
	      << new_vol << std::endl;  
    oofcerr << "old: " << std::endl;
    for(ConstCSkeletonElementSet::iterator i=before.begin(); i!=before.end();
	++i)
      {
	(*i)->printNodes(std::cerr);
	oofcerr << std::endl;
      }
    oofcerr << "new: " << std::endl;
    for(CSkeletonElementSet::iterator i=after.begin(); i!=after.end(); ++i) {
      (*i)->printNodes(std::cerr);
      oofcerr << std::endl;
    }
    throw ErrProgrammingError("ProvisionalChanges: total volume is incorrect",
			      __FILE__, __LINE__);
  }
}

void ProvisionalChanges::sanityCheck() {
  checkVolume();

  for(CSkeletonElementSet::const_iterator i=after.begin(); i!=after.end(); ++i)
    {
      if((*i)->illegal())
	oofcerr << "ILLEGAL ELEMENT" << std::endl;
      for(CSkeletonNodeIterator n=(*i)->getNodes()->begin();
	  n!=(*i)->getNodes()->end(); ++n)
	{
	  if(!(*n)->hasElement((*i)))
	    oofcerr << "ELEMENT NOT CONNECTED TO NODE " << (*i)->getUid()
		      << " " << (*n)->getUid() << std::endl;
	}
      for(int j = 0; j<4; ++j) {
	CSkeletonFace *f = skeleton->getElementFace((*i), j);
	if(f==NULL) {
	  oofcerr << "NULL FACE" << std::endl;
	  break;
	}
	if(!skeleton->onOuterFace(f->getNodes()) &&
	   skeleton->getSister((*i), f) == NULL) 
	  {
	    oofcerr << "\n\nELEMENT IS MISSING SISTER " << (*i)->getUid() 
		      << " " << f->getUid() << std::endl;
	    oofcerr << "function " << (*i)->get_function() << std::endl;
	    CSkeletonElementVector face_els;
	    skeleton->getFaceElements(f, face_els);
	    oofcerr << "face elements: ";
	    for(CSkeletonElementIterator k=face_els.begin(); k!=face_els.end();
		++k)
	      {
		oofcerr << (*k)->getUid() << " ";
	      }
	    oofcerr << std::endl;
	    oofcerr << "face nodes and node elements: " << std::endl;
	    for(int k=0; k<3; ++k) {
	      CSkeletonElementVector *els = f->getNode(k)->getElements();
	      Coord x;
	      x = f->getNode(k)->position();
	      oofcerr << "n " << f->getNode(k)->getUid() << " " << x[0]
			<< " " << x[1] << " " << x[2]; 
	      oofcerr << " els " << els->size() << " ";
	      for(CSkeletonElementIterator l=els->begin(); l!=els->end(); ++l)
		oofcerr << (*l)->getUid() << " ";
	      oofcerr << std::endl;
	    }
	    Coord x;
	    Coord n;
	    x = f->center();
	    n = f->normal();
	    double tiny = 1e-4;
	    Coord c1(x[0]+tiny*n[0],x[1]+tiny*n[1],x[2]+tiny*n[2]);
	    Coord c2(x[0]-tiny*n[0],x[1]-tiny*n[1],x[2]-tiny*n[2]);
	    const CSkeletonElement *e_el1 = skeleton->enclosingElement(&c1);
	    const CSkeletonElement *e_el2 = skeleton->enclosingElement(&c2);
	    oofcerr << "test points " << c1 << " " << c2 << std::endl;
	    oofcerr << "interior? " << (*i)->interior(&c1) << " "
		      << (*i)->interior(&c2) << std::endl;
	    oofcerr << "enclosing elements ";
	    if(e_el1 != NULL) {
	      oofcerr << e_el1->getUid() << " " << e_el1->get_function() << " ";
	      for(int k=0; k<4; ++k)
		oofcerr << e_el1->getNode(k)->getUid() << " ";
	      oofcerr << std::endl;
	    }
	    if(e_el2 != NULL) {
	      oofcerr << e_el2->getUid() << " " << e_el2->get_function() << " ";
	      for(int k=0; k<4; ++k)
		oofcerr << e_el2->getNode(k)->getUid() << " ";
	      oofcerr << std::endl;
	    }
	    // throw ErrProgrammingError("CSkeleton: Element missing sister.",
	    // 			    __FILE__, __LINE__);
	  }
      }
    }
} // ProvisionalChanges::sanityCheck

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO OPT: Why do these loop over all the whole skeleton?  Shouldn't
// they just loop over the objects in the group?

// These functions are called by NodeGroupSet.impliedAddDown, et al.

void CSkeleton::nodesAddGroupsDown(CGroupTrackerVector *vector) {
  for(CSkeletonNodeIterator nit=nodes.begin(); nit!=nodes.end(); ++nit) {
    (*nit)->addDown(vector->begin(), vector->end());
  }
}

void CSkeleton::segmentsAddGroupsDown(CGroupTrackerVector *vector) {
  for(CSkeletonSegmentMap::iterator sit=segments.begin(); 
      sit != segments.end(); ++sit)
    {
      (*sit).second->addDown(vector->begin(), vector->end());
    }
}

void CSkeleton::facesAddGroupsDown(CGroupTrackerVector *vector) {
  for(CSkeletonFaceMap::iterator fit=faces.begin(); fit!=faces.end(); ++fit) {
    (*fit).second->addDown(vector->begin(), vector->end());
  }
}

void CSkeleton::elementsAddGroupsDown(CGroupTrackerVector *vector) {
  for(CSkeletonElementIterator eit=elements.begin(); eit!=elements.end();
      ++eit)
    {
      (*eit)->addDown(vector->begin(), vector->end());
    }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonBase::clearVSBs() const {
  for(VoxelSetBoundary *vsb : voxelSetBdys)
    delete vsb;
  voxelSetBdys.clear();
}

void CSkeletonBase::buildVSBs() const {
  if(vsbTimeStamp > getTimeStamp())
    return;
  // Get the bin size from the average element volume.  Each bin is a
  // rectangular region of the microstructure.  A VSBGraph is computed
  // in each bin for each voxel category, instead of constructing one
  // graph that spans the whole microstructure.

  // This constructs bins that are the same size in each direction,
  // but it doesn't need to be that way.

  // The default size is used when there are no elements yet in the
  // Skeleton.  It's set by the constructor to DEFAULT_VSB_BIN, but
  // if this Skeleton is a copy of another Skeleton, it has been reset
  // by setDefaultVSBbinSize to the bin size of the copied Skeleton.
  ICoord3D newBinSize = defaultVSBbin;
  if(nelements() > 0) {
    newBinSize = getDefaultVSBbinSize();
  }
  // Don't recompute the VSBs if neither the bin size nor the voxel
  // categories have changed.
  const CMicrostructure *ms = getMicrostructure();
  if(newBinSize == vsbBinSize && vsbTimeStamp > ms->getTimeStamp()) {
    return;
  }

  vsbBinSize = newBinSize;
  ICoord3D msSize = ms->sizeInPixels();
  
  // Find out how many bins to use.  
  unsigned int nbins[3];
  for(unsigned int c=0; c<3; c++) {
    nbins[c] = msSize[c]/vsbBinSize[c]; // integer division
    if(nbins[c] == 0)
      nbins[c] = 1;
  }

  // Compute how large each bin should be in each direction.  They
  // won't all be the same and the actual sizes of some bins will be
  // larger than the nominal size if it does not divide the
  // microstructure size exactly.
  std::vector<std::vector<unsigned int>> sizes(3); // size of each bin
  std::vector<std::vector<unsigned int>> sumsizes(3); // cumulative sum of sizes
  for(unsigned int c=0; c<3; c++) {
    int subsize = msSize[c]/nbins[c]; // integer division.
    int extra = msSize[c] - subsize*nbins[c]; // remainder
    sizes[c].clear();
    sizes[c].resize(nbins[c], subsize);
    if(extra > 0) {
      for(int i=0; i<extra; i++)
	sizes[c][i] += 1;
    }
    // sumsizes gives the starting and ending voxels for each bin
    int sum = 0;
    sumsizes[c].resize(nbins[c]+1);
    for(unsigned int i=0; i<nbins[c]; i++) {
      sumsizes[c][i] = sum;
      sum += sizes[c][i];
    }
    assert(sum == msSize[c]);
    sumsizes[c][nbins[c]] = msSize[c];
  }
      
  // Make the bins.  They're stored here rather than in the
  // VoxelSetBoundary objects because all VoxelSetBoundaries use the
  // same bins.  The order in which the bins are created here
  // determines the order in which the VoxelSetBoundaries will create
  // and store their VSBGraphs.  The order doesn't matter as long as
  // the CSkeletonBase and VoxelSetBoundaries agree on it.
  vsbBins.clear();
  vsbBins.reserve(nbins[0]*nbins[1]*nbins[2]);
  for(unsigned int ix=0; ix<nbins[0]; ix++) {
    for(unsigned int iy=0; iy<nbins[1]; iy++) {
      for(unsigned int iz=0; iz<nbins[2]; iz++) {
	vsbBins.emplace_back(
	     ICoord3D(sumsizes[0][ix], sumsizes[1][iy], sumsizes[2][iz]),
	     ICoord3D(sumsizes[0][ix+1], sumsizes[1][iy+1], sumsizes[2][iz+1]));
      }
    }
  }

  ms->categorizeIfNecessary();
  clearVSBs();
  voxelSetBdys.reserve(ms->nCategories());

  for(int cat=0; cat<ms->nCategories(); cat++) {
    // All the work is done in the VoxelSetBoundary constructor, which
    // calls buildVSB, defined in VSB/vsb.h.
    voxelSetBdys[cat] = new VoxelSetBoundary(ms, vsbBins, cat);
  } // end loop over categories

  ++vsbTimeStamp;
} // end CSkeletonBase::buildVSBs


void CSkeletonBase::setDefaultVSBbinSize(const CSkeletonBase *other) {
  // Compute a new bin size from the other Skeleton.  The other
  // skeleton may have been modified after it last constructed its
  // bins, so don't simply copy its bin size.
  if(other->nelements() != 0) {
    defaultVSBbin = other->getDefaultVSBbinSize();
  }
  else if(other->vsbBinSize != ICoord3D(0,0,0)) {
    defaultVSBbin = other->vsbBinSize;
  }
  else {
    // The other skeleton hasn't even created elements somehow...
    defaultVSBbin = ICoord3D(DEFAULT_VSB_BIN, DEFAULT_VSB_BIN, DEFAULT_VSB_BIN);
  }
}

ICoord3D CSkeletonBase::getDefaultVSBbinSize() const {
  const CMicrostructure *ms = getMicrostructure();
  // Get the average bounding box for the elements.  If the average
  // element has an aspect ratio far from 1, assuming that it's near 1
  // will lead to a very non-optimum bin size.
  Coord3D avgsize;
  for(CSkeletonElementIterator el=beginElements(); el!=endElements(); ++el) {
    CRectangularPrism bbox = (*el)->boundingBox();
    avgsize += bbox.upperrightfront() - bbox.lowerleftback();
  }
  avgsize /= nelements();
  Coord3D voxelsize = ms->sizeOfPixels();
#define MAX(a,b) (a > b ? a : b)
  return ICoord3D(MAX(avgsize[0]/voxelsize[0], MIN_VSB_BINSIZE),
		  MAX(avgsize[1]/voxelsize[1], MIN_VSB_BINSIZE),
		  MAX(avgsize[2]/voxelsize[2], MIN_VSB_BINSIZE));
}


double CSkeletonBase::clippedCategoryVolume(
			    unsigned int cat,
			    const CRectangularPrism &ebbox,
			    const std::vector<VSBPlane<Coord3D>> &planes)
  const
{
  return voxelSetBdys[cat]->clippedVolume(ebbox, planes);
}


// Check that that total volume of each category, summed over
// elements, is the same as the volume of the voxels in the category.
// Return true if the test passes.

CategoryVolumesData *CSkeletonBase::checkCategoryVolumes() const {
  const CMicrostructure *ms = getMicrostructure();
  unsigned int ncat = ms->nCategories();
  buildVSBs();
  DoubleVec volumes(ncat, 0.0);
  double avgerr = 0;
  double avgerr2 = 0;
  double maxabserr = 0.0;

  CategoryVolumesData *data = new CategoryVolumesData;
  
  for(CSkeletonElementIterator elit = beginElements();
      elit!=endElements(); ++elit)
    {
      double evol = 0.0;	// element volume from sum of category volumes
      DoubleVec evols = (*elit)->categoryVolumes(this);
      for(unsigned int c=0; c<ncat; c++) {
	volumes[c] += evols[c];
	evol += evols[c];
      }
      // Accumulate statistics on error in element volume.
      double vol = (*elit)->volumeInVoxelUnits(ms);
      assert(vol > 0.0);
      double err = (evol - vol)/vol;
      avgerr += fabs(err);
      avgerr2 += err*err;
      if(fabs(err) > maxabserr)
	maxabserr = fabs(err);
    }
  avgerr /= nelements();
  data->avgerr = avgerr;
  data->rmserr = sqrt(avgerr2/nelements() - avgerr*avgerr);
  data->maxerr = maxabserr;
  data->catVolumes = volumes;

  // Count voxels in each category
  data->catCounts.resize(ncat, 0);
  data->catErrors.resize(ncat, 0);
  const Array<int> *catMap = ms->getCategoryMap();
  for(Array<int>::const_iterator i=catMap->begin(); i!=catMap->end(); ++i) {
    data->catCounts[*i]++;
  }
  // Since categoryVolumes returns volumes in voxel units, the total
  // volume of each category should be the number of voxels in the
  // category.
  for(unsigned int c=0; c<ncat; c++) {
    // oofcerr << "CSkeletonBase::checkCategoryVolumes: category="
    // 	    << c << " volume=" << volumes[c] << " #voxels=" << catCounts[c];
    if(data->catCounts[c] != 0) {
      data->catErrors[c] =
	fabs(data->catCounts[c] - volumes[c])/data->catCounts[c];
      //      oofcerr << " error=" << err;
    }
    //    oofcerr << std::endl;
  }
  return data;
} // end CSkeletonBase::checkCategoryVolumes

bool CSkeletonBase::checkVSB(int cat) const {
  getMicrostructure()->categorizeIfNecessary();
  buildVSBs();
  return voxelSetBdys[cat]->checkEdges();
}

void CSkeletonBase::dumpVSB(int cat, const std::string &file) const {
  getMicrostructure()->categorizeIfNecessary();
  buildVSBs();
  std::ofstream f(file);
  voxelSetBdys[cat]->dump(f);
}

void CSkeletonBase::dumpVSBLines(int cat, const std::string &file)
  const
{
  getMicrostructure()->categorizeIfNecessary();
  buildVSBs();
  voxelSetBdys[cat]->dumpLines(file);
}

void CSkeletonBase::drawVoxelSetBoundary(LineSegmentLayer *layer,
					 int category)
  const
{
  const CMicrostructure *ms = getMicrostructure();
  ms->categorizeIfNecessary();
  assert(category < ms->nCategories());
  buildVSBs();
  const VoxelSetBoundary *vsb = voxelSetBdys[category];
  auto iter = vsb->iterator();
  layer->set_nSegs(vsb->size()*3/2);
  while(!iter.done()) {
    Coord3D pt0 = ms->pixel2Physical(iter.node0()->position);
    Coord3D pt1 = ms->pixel2Physical(iter.node1()->position);
    if(pt1 > pt0) {
      layer->addSegment(&pt0, &pt1);
    }
    iter.next();
  }
  // vsb->dump(std::cerr);
  // double vol = vsb->volume();
  // oofcerr << "CSkeletonBase::drawVoxelSetBoundary: volume=" << vol
  // 	  << std::endl;
}

void CSkeletonBase::saveClippedVSB(int cat,
				   const std::vector<VSBPlane<Coord3D>> &planes,
				   const std::string &filename)
  const
{
  const CMicrostructure *ms = getMicrostructure();
  ms->categorizeIfNecessary();
  buildVSBs();
  assert(cat < ms->nCategories());
  voxelSetBdys[cat]->saveClippedVSB(planes, filename);
}

void CSkeletonBase::saveClippedVSB(int cat,
				   const VSBPlane<Coord3D> &plane,
				   const std::string &filename)
  const
{
  std::vector<VSBPlane<Coord3D>> planes(1, plane);
  saveClippedVSB(cat, planes, filename);
}

double CSkeletonBase::clipVSBVol(int cat,
				 const VSBPlane<Coord3D> &plane)
  const
{
  const CMicrostructure *ms = getMicrostructure();
  ms->categorizeIfNecessary();
  buildVSBs();
  std::vector<VSBPlane<Coord3D>> planes(1, plane);
  CRectPrism<Coord3D> bbox(Coord3D(0,0,0), ms->sizeInPixels().coord());
  return voxelSetBdys[cat]->clippedVolume(bbox, planes);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const CSkeletonBase &skel) {
  skel.printSelf(os);
  return os;
}

void CSkeleton::printSelf(std::ostream &os) const {
  os << "CSkeleton(uid=" << uid << ")";
}

void CDeputySkeleton::printSelf(std::ostream &os) const {
  os << "CDeputySkeleton(uid=" << uid << ")";
}
