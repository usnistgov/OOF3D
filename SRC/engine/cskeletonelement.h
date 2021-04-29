// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONELEMENT_H
#define CSKELETONELEMENT_H

#include <oofconfig.h>

#include "common/cachedvalue.h"
#include "common/coord.h"
#include "common/doublevec.h"
#include "common/IO/vtkutils.h"
#include "common/VSB/cplane.h"
#include "engine/cskeleton2_i.h"
#include "engine/cskeletonselectable.h"
#include "engine/homogeneity.h"

#include <vtkSmartPointer.h>
#include <vtkTetra.h>

#include <limits>

class CMicrostructure;
class CSkeleton;
class FEMesh;
class LineSegmentLayer;
class MasterElement;
class Material;
class Node;
class OrientedCSkeletonFace;
class VoxelBdyIntersection;

#define NUM_TET_FACES 4
#define NUM_TET_EDGES 6
#define NUM_TET_NODES 4
#define NUM_TET_FACE_EDGES 3

#define LEGAL_COS_TOLERANCE std::numeric_limits<double>::epsilon()
#define LEGAL_COS2_TOLERANCE 2*LEGAL_COS_TOLERANCE
#define SUSPECT_COS_TOLERANCE 1.0e-6
#define SUSPECT_COS2_TOLERANCE 2*SUSPECT_COS_TOLERANCE

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A map of VoxelBdyIntersections. The double key is the parametric
// coordinate of the Intersection along a tet edge.
typedef std::map<double, VoxelBdyIntersection> CellEdgeMap;

// A vector of CellEdgeMaps. The index of each vector entry is the tet
// edge id.
typedef std::vector<CellEdgeMap> CellEdge;
typedef std::pair<double, VoxelBdyIntersection> CellEdgeDatum;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A structure for storing where a line intersects an element, used by
// the LinearCrossSectionDomain.

class LineIntersectionPoint {
private:
  const CSkeletonElement *traversee;
  const CSkeletonSelectable *intersectee; // node, segment, or face
  Coord xstart;
  Coord xend;
  double alpha;			// parameter along the line
  ConstCSkeletonElementSet traversed;
public:
  LineIntersectionPoint(const CSkeletonElement *traversee,
			const CSkeletonSelectable *intersectee,
			const Coord &xstart, const Coord &xend,
			double alpha);
  virtual ~LineIntersectionPoint();
  double getAlpha() const { return alpha; }
  Coord position() const;
  LineIntersectionPoint *next(const CSkeletonBase*) const;
  virtual bool done() const { return false; }
  const CSkeletonElement *getElement() const { return traversee; }
  void addTraversedElement(const CSkeletonElement*);
  void addTraversedElements(const ConstCSkeletonElementSet&);
  friend std::ostream &operator<<(std::ostream&, const LineIntersectionPoint&);
};

class LineIntersectionEndPoint : public LineIntersectionPoint {
public:
  LineIntersectionEndPoint(const CSkeletonElement *traversee,
			   const Coord &xstart, const Coord &xend);
  virtual bool done() const { return true; }
};

std::ostream &operator<<(std::ostream&, const LineIntersectionPoint&);
			   
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: Do we still need to define NONE?  It was used heavily in the
// old failed (sad!) category volumes code.  It's still used in the
// tetrahedral topology tables, but most of those may not be needed
// any more either.

#define NONE 12345    // larger than any tet node, edge, or face index

class CSkeletonElement : public CSkeletonMultiNodeSelectable {
protected:
  // if the index is -1, the element is a provisional element.
  int index;
  int meshindex;
  const std::string &generating_function;
  mutable CachedValue<HomogeneityData> homogeneity_data;
  static const std::string modulename_;
  static const std::string classname_;
  static long globalElementCount;
  LineIntersectionPoint *getLineIntersectionPoint(
  			  const CSkeletonBase*, std::vector<int> &, double,
  			  const Coord&, const Coord&) const;
  std::vector<VSBPlane<Coord3D>> getPlanes(const std::vector<Coord3D>&) const;

public:
  // static topological info
  static const unsigned int faceEdges[4][3];
  static const unsigned int tetEdge2FaceEdge[4][6];
  static const int faceEdgeDirs[4][3];
  static const unsigned int edgeFaces[6][2];
  static const unsigned int edgeNodes[6][2];
  static const int edgeFaceDirs[6][4];
  static const unsigned int edgeEdgeFace[6][6];
  static const unsigned int nodeEdgeFace[4][6];
  static const unsigned int edgeEdgeNode[6][6];
  static const unsigned int faceFaceEdge[4][4];
  static const unsigned int oppFace[4];
  static const unsigned int oppNode[4];
  static const unsigned int oppEdge[6];
  static const unsigned int nodeFaces[4][3];
  static const unsigned int nodeEdges[4][3];
  static const unsigned int nodeNodeEdge[4][4];
  static const unsigned int ccwNeighborEdgeOrder[6][4];
  static const unsigned int cwNeighborEdgeOrder[6][4];
  static const unsigned int ccwNodeEdges[4][3];
  static const unsigned int cwNodeEdges[4][3];
  // static const double nodeEdgeParam[4][3];

  CSkeletonElement(int indx, CSkeletonNodeVector *ns); 
  CSkeletonElement(CSkeletonNodeVector *ns, CSkeletonElement *p=NULL,
		   const std::string &name=""); 
  CSkeletonElement(CSkeletonNodeVector *ns, CSkeletonSelectableList &parents,
		   const std::string &name=""); 
  CSkeletonElement(CSkeletonNode *n0, CSkeletonNode *n1, CSkeletonNode *n2,
		   CSkeletonNode *n3, CSkeletonElement *p=NULL,
		   const std::string &name="");
  virtual ~CSkeletonElement();

  virtual const std::string &modulename() const { return modulename_; }
  virtual const std::string &classname() const { return classname_; }
  const std::string &get_function() const {return generating_function;}

  virtual CSkeletonElement *copy_child(int, vtkSmartPointer<vtkPoints>);
  virtual CSkeletonElement *new_child(int, vtkSmartPointer<vtkPoints>);
  void promote(int idx);
  void connectToNodes();

  virtual VTKCellType getCellType() const { return VTK_TETRA; }
  virtual vtkSmartPointer<vtkCell> getEmptyVtkCell() const;

  int getIndex() const { return index; }
  void setIndex(int idx) { index = idx; }
  // TODO 3.1: Do we really need meshindex?  Is it ever different from
  // index?
  int getMeshIndex() const { return meshindex; }
  void setMeshIndex(int idx) { meshindex = idx; }
  void positionPointer(Coord *x) const;
  bool interior(const Coord *point) const;
  double volume() const;
  double volumeInVoxelUnits(const CMicrostructure *MS) const;
  double volumeInFractionalUnits(const CMicrostructure *MS) const;
  double cosCornerAngle(unsigned int fid, unsigned int cid) const;
  double cosCornerAngleSquared(unsigned int fid, unsigned int cid) const;
  double solidCornerAngle(unsigned int cid) const;
  double cosDihedralAngle(unsigned int fid1, unsigned int fid2) const;
  bool illegal() const;
  bool suspect() const;
  void edgeLengthAndDiameter2(unsigned int, unsigned int, double&, double&)
    const;
  void printAngles() const;

  std::vector<Coord3D> pixelCoords(const CMicrostructure*) const;
  
  // methods related to homogeneity, dominant pixel, and shape energy
  const DoubleVec categoryVolumes(const CSkeletonBase*) const;
  HomogeneityData c_homogeneity(const CSkeletonBase*) const;
  void findHomogeneityAndDominantPixel(const CSkeletonBase*) const;
  virtual double homogeneity(const CSkeletonBase*) const;
  void copyHomogeneity(const CSkeletonElement &el);
  void revertHomogeneity();
  double energyHomogeneity(const CSkeletonBase*) const;
  int dominantPixel(const CSkeletonBase*) const;
  const HomogeneityData &getHomogeneityData() const {
    return homogeneity_data.value();
  }
  void setHomogeneityData(const HomogeneityData &hd) {
    homogeneity_data.copy(hd);
  }
  double energyShape() const;
  static double energyShape(const Coord*);
  const Material *material(const CSkeletonBase*) const;
  double energyTotal(const CSkeletonBase*, double) const;
  //const std::vector<ICoord> *underlying_pixels(const CMicrostructure&)

  // TODO 3.1: make these return #defined numbers
  unsigned int getNumberOfSegments() const { return 6; }
  unsigned int nnodes() const { return 4; }
  unsigned int getNumberOfNodes() const { return 4; }
  unsigned int getNumberOfFaces() const { return 4; }
  static const IDTYPE *getEdgeArray(int);
  static const IDTYPE *getFaceArray(int);
  CSkeletonNode *getSegmentNode(int segidx, int nodeidx) const {
    return (*nodes)[vtkTetra::GetEdgeArray(segidx)[nodeidx]];
  }
  CSkeletonNode *getFaceNode(int faceidx, int nodeidx) const {
    return (*nodes)[vtkTetra::GetFaceArray(faceidx)[nodeidx]];
  }
  CSkeletonMultiNodeKey getSegmentKey(int segidx) const;
  CSkeletonMultiNodeKey getFaceKey(int faceidx) const;
  static unsigned int getFaceEdgeIndex(int i, int j) { return faceEdges[i][j]; }
  // getNodeEdgeIndex(i,j) returns the element-scope index of the jth
  // edge at node i.
  static unsigned int getNodeEdgeIndex(int i, int j) { return nodeEdges[i][j]; }
  static unsigned int getOppFaceIndex(int i) { return oppFace[i]; }
  static unsigned int getOppEdgeIndex(int i) { return oppEdge[i]; }
  static unsigned int getOtherFaceIndex(unsigned int f, unsigned int s);

  OrientedCSkeletonFace *getOrientedFace(const CSkeletonBase*, unsigned int)
    const;

  CSkeletonMultiNodeKey key() const;

  void lineIntersections(
  		 const CSkeletonBase*, const Coord&, const Coord&,
  		 LineIntersectionPoint**, LineIntersectionPoint**) const;
  const LineIntersectionPoint *startLinearXSection(const CSkeletonBase*,
  					 const Coord*, const Coord*) const;

  // The other subclasses of CSkeletonSelectable have getElements()
  // methods that return the CSkeletonElements that they are part of.
  // Defining getElements() for CSkeletonElement doesn't make much
  // sense.  TODO 3.1: Probably that means that we need a more complex
  // CSkeletonSelectable hierarchy.
  virtual void getElements(const CSkeletonBase*, ConstCSkeletonElementVector&)
    const;
  virtual void getElements(const CSkeletonBase*, CSkeletonElementVector&);
  virtual int nElements() const { return 1; }

  void realElement(FEMesh *femesh, int index,
		   const MasterElement *master,
		   const CSkeleton *skeleton,
		   SkelElNodeMap &edgeNodes,
		   SkelElNodeMap &faceNodes,
		   Material *mat=NULL);

  virtual void print(std::ostream &) const;

  friend class CSkeleton;
  friend long get_globalElementCount();

#ifdef DEBUG
  void dumpFaceInfo(const CSkeletonBase*) const; // debugging
  void drawVoxelCategoryIntersection(LineSegmentLayer*, const CSkeletonBase*,
  				     unsigned int) const;
#endif // DEBUG

};				// CSkeletonElement

long get_globalElementCount();

#endif	// CSKELETONELEMENT_H


