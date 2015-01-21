// -*- C++ -*-
// $RCSfile: cskeleton2.h,v $
// $Revision: 1.1.4.115 $
// $Author: langer $
// $Date: 2014/12/14 22:49:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CSKELETON2_H
#define CSKELETON2_H

#include "common/coord_i.h"
#include "common/pythonexportable.h"
#include "engine/cskeleton2_i.h"
#include "engine/cskeletonboundary.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonselectable_i.h"

#include <vtkSmartPointer.h>

class FEMesh;
class FaceSubstitution;
class GhostOOFCanvas;
class HomogeneityData;
class Material;
class ProvisionalMerge;
class SegmentSubstitution;
class SkeletonFilter;
class TimeStamp;

class vtkCellLocator;
class vtkDataArray;
class vtkMergePoints;
class vtkPoints;
class vtkUnstructuredGrid;

// TODO 3.1: make everything const that should be const.

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Tetrahedron arrangements for the initial Skeleton.  The members of
// this class must correspond to members of the Python Arrangement
// Enum class, which is defined in cskeleton2.spy.  The correspondence
// is defined in the TetArrangement* typemap in cskeleton2.swg.
//* TODO 3.1: This is ugly. Somehow make the Python and C++ enums agree
//* automatically.
enum TetArrangement {
  MODERATE_ARRANGEMENT,
  MIDDLING_ARRANGEMENT
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// OuterFaceID and OuterEdgeID objects are used to identify the face
// boudaries and edge boundaries when doing certain manipulations,
// such as detecting different situations in the rationalization
// process.

// TODO 3.1: These classes hold the same information as the predefined
// skeleton boundary definitions.  Probably they should be unified
// somehow.  Perhaps the skeleton boundaries can use these classes to
// determine the boundary geometry.  Eventually it might be a good
// idea to have an abstract way of determining which objects are on
// which boundaries.

class OuterFaceID {
private:
  const int dir;		// 0, 1, or 2, for x, y, z.
  const int id;
  const std::string name;
public:
  OuterFaceID(int d, int id, const std::string &n) : dir(d), id(id), name(n) {}
  int direction() const { return dir; }
  bool operator==(const OuterFaceID &other) const { return id == other.id; }
  bool operator!=(const OuterFaceID &other) const { return id != other.id; }
  operator bool() const { return id >= 0; } // OUTERFACE_NONE has id==-1
  bool contains(const Coord&, const CSkeletonBase*) const;
  friend std::ostream &operator<<(std::ostream&, const OuterFaceID&);
  friend class OuterEdgeID;
};

extern const OuterFaceID OUTERFACE_NONE,
  OUTERFACE_XMIN, OUTERFACE_XMAX,
  OUTERFACE_YMIN, OUTERFACE_YMAX,
  OUTERFACE_ZMIN, OUTERFACE_ZMAX;

typedef std::map<CSkeletonNode*, Coord> NodePositionsMap;
typedef std::list<CDeputySkeleton*> CDeputySkeletonList;

class OuterEdgeID {
private:
  const OuterFaceID face0, face1;
public:
  OuterEdgeID(const OuterFaceID&, const OuterFaceID&);
  bool operator==(const OuterEdgeID &other) const {
    return face0==other.face0 && face1==other.face1;
  }
  bool operator!=(const OuterEdgeID &other) const {
    return face0!=other.face0 || face1!=other.face1;
  }
  bool contains(const Coord &pt, const CSkeletonBase *skel) const {
    return face0.contains(pt, skel) && face1.contains(pt, skel); 
  }
  operator bool() const { return face0 != OUTERFACE_NONE; }
  friend std::ostream &operator<<(std::ostream&, const OuterEdgeID&);
};

extern const OuterEdgeID OUTEREDGE_NONE,
 OUTEREDGE_XMINYMIN, OUTEREDGE_XMINYMAX,
 OUTEREDGE_XMINZMIN, OUTEREDGE_XMINZMAX,
 OUTEREDGE_XMAXYMIN, OUTEREDGE_XMAXYMAX,
 OUTEREDGE_XMAXZMIN, OUTEREDGE_XMAXZMAX,
 OUTEREDGE_YMINZMIN, OUTEREDGE_YMINZMAX,
 OUTEREDGE_YMAXZMIN, OUTEREDGE_YMAXZMAX;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// CSkeletonBase is the base class for CSkeleton and CDeputySkeleton.

class CSkeletonBase : public PythonExportable<CSkeletonBase> {

protected:
  static uidtype uidbase;
  uidtype uid;
  bool illegal_;
  mutable int illegalCount;
  mutable int suspectCount;
  mutable double homogeneityIndex;
  mutable TimeStamp homogeneity_index_computation_time;
  // TimeStamp most_recent_geometry_change;
  mutable TimeStamp illegal_count_computation_time;
  mutable TimeStamp suspect_count_computation_time;
  TimeStamp timestamp;
  static const std::string modulename_;
  OuterFaceID onOuterFace_(const CSkeletonNodeVector*, bool boundary[6]) 
    const;

public:
  CSkeletonBase();
  virtual ~CSkeletonBase();
  virtual void destroy() = 0;
  uidtype getUid() const {
    return uid;
  }
  virtual const std::string &modulename() const {
    return modulename_; 
  }
  // void updateGeometry() { 
  //   ++timestamp;
  // }
  bool illegal() const {
    return illegal_;
  }
  void setIllegal() {
    illegal_=true; 
  }
  virtual void checkIllegality() = 0;
  void incrementTimestamp();
  const TimeStamp &getTimeStamp() const;

  // basic get methods
  virtual const CMicrostructure *getMicrostructure() const = 0;
  virtual vtkSmartPointer<vtkUnstructuredGrid> getGrid() const = 0;
  virtual void getVtkCells(SkeletonFilter*, 
			   vtkSmartPointer<vtkUnstructuredGrid>) = 0;
  const std::string &getElementType(int eidx);
  virtual vtkSmartPointer<vtkDataArray> getMaterialCellData(
					   const SkeletonFilter*) const = 0;
  virtual vtkSmartPointer<vtkDataArray> getEnergyCellData(
			    double alpha, const SkeletonFilter*) const = 0;
  virtual vtkSmartPointer<vtkPoints> getPoints() const = 0;

  virtual CSkeletonNode *getNode(unsigned int nidx) const = 0;
  virtual bool hasNode(CSkeletonNode *) const = 0;
  virtual CSkeletonElement *getElement(unsigned int eidx) const = 0;
  virtual bool hasElement(CSkeletonElement *) const = 0;
  virtual CSkeletonSegment *getSegment(const CSkeletonMultiNodeKey &h) const=0;
  virtual CSkeletonFace *getFace(const CSkeletonMultiNodeKey &h) const = 0;
  virtual CSkeletonSegment *getSegmentByUid(uidtype) const = 0;
  virtual CSkeletonFace *getFaceByUid(uidtype) const = 0;

  virtual CSkeletonNodeIterator beginNodes() const = 0;
  virtual CSkeletonNodeIterator endNodes() const = 0;
  virtual CSkeletonElementIterator beginElements() const = 0;
  virtual CSkeletonElementIterator endElements() const = 0;
  virtual CSkeletonSegmentIterator beginSegments() const = 0;
  virtual CSkeletonSegmentIterator endSegments() const = 0;
  virtual CSkeletonFaceIterator beginFaces() const = 0;
  virtual CSkeletonFaceIterator endFaces() const = 0;
  
  // basic info
  virtual int nnodes() const = 0;
  virtual int nelements() const = 0;
  virtual int nsegments() const = 0;
  virtual int nfaces() const = 0;
  virtual double volume() const = 0;
  virtual bool getPeriodicity(int dim) const = 0;
  virtual int getIllegalCount() = 0;
  virtual void getIllegalElements(CSkeletonElementVector &) const = 0;
  virtual int getSuspectCount() = 0;
  virtual void getSuspectElements(CSkeletonElementVector &) const = 0;

  virtual int nDeputies() const = 0;

  // TODO 3.1: Change these names.  These methods are called only by the
  // GenericGroupSet.impliedAddDown methods when building groups for
  // new CSkeletons and CDeputySkeletons.
  virtual void nodesAddGroupsDown(CGroupTrackerVector*) = 0;
  virtual void segmentsAddGroupsDown(CGroupTrackerVector*) = 0;
  virtual void facesAddGroupsDown(CGroupTrackerVector*) = 0;
  virtual void elementsAddGroupsDown(CGroupTrackerVector*) = 0;

  // connectivity
  void getSegmentElements(const CSkeletonSegment *segment,
			  CSkeletonElementVector &) const;
  void getConstSegmentElements(const CSkeletonSegment *segment,
			       ConstCSkeletonElementVector &) const;
  void getSegmentFaces(const CSkeletonSegment*, CSkeletonFaceVector&) const;
  void getFaceElements(const CSkeletonFace*, CSkeletonElementVector&) const;
  void getFaceElements(const CSkeletonFace*, ConstCSkeletonElementVector&)
    const;
  void getNeighborNodes(const CSkeletonNode *, CSkeletonNodeSet &) const;
  void getNodeSegments(const CSkeletonNode *, CSkeletonSegmentSet &) const;
  void getNodeFaces(const CSkeletonNode *, CSkeletonFaceSet &) const;
  CSkeletonSegment *getFaceSegment(const CSkeletonFace*, int idx) const;
  void getFaceSegments(const CSkeletonFace*, CSkeletonSegmentSet&) const;
  CSkeletonSegment *getElementSegment(const CSkeletonElement*, int idx) const;
  CSkeletonSegmentVector *getElementSegments(const CSkeletonElement*) const;
  CSkeletonFace *getElementFace(const CSkeletonElement*, int idx) const;
  CSkeletonFaceVector *getElementFaces(const CSkeletonElement*) const;
  CSkeletonElement *getSister(const CSkeletonElement*, const CSkeletonFace*)
    const;
  //CSkeletonElement *getSisterPeriodic(int face) const;
  void getInternalBoundaryNodes(CSkeletonNodeSet &nodes) const;

  ConstCSkeletonElementSet *getElementNeighbors(const CSkeletonElement*) const;

  Coord averageNeighborPosition(const CSkeletonNode*) const;
  Coord averageNeighborPosition(const CSkeletonNode*, const CSkeletonNodeSet&)
    const;

  // convenience functions for boundary building
  CSkeletonElement *getOrientedSegmentElement(OrientedCSkeletonSegment *seg);
  CSkeletonElement *getOrientedFaceElement(OrientedCSkeletonFace *face);

  // finding things
  virtual const Coord nodePositionForSkeleton(CSkeletonNode *n) = 0;
  const CSkeletonElement* enclosingElement(Coord *point);
  CSkeletonElement *findElement(vtkSmartPointer<vtkCell>) const;
  virtual vtkSmartPointer<vtkCellLocator> get_element_locator() = 0;
  const CSkeletonNode* nearestNode(Coord *point);
  virtual vtkSmartPointer<vtkMergePoints> get_point_locator() = 0;
  //virtual vtkPointLocator* get_point_locator() = 0;
  const CSkeletonSegment* nearestSegment(Coord *point);
  CSkeletonSegment* findExistingSegment(const CSkeletonNode *n1,
					const CSkeletonNode *n2) const;
  bool doesSegmentExist(const CSkeletonNode *n1, const CSkeletonNode *n2) const;
  virtual bool inSegmentMap(const CSkeletonMultiNodeKey &h) const = 0;
  const CSkeletonFace* nearestFace(Coord *point);
  CSkeletonFace* findExistingFace(CSkeletonNode *n1, CSkeletonNode *n2,
				  CSkeletonNode *n3) const;
  CSkeletonFace* findExistingFaceByIds(vtkSmartPointer<vtkIdList>) const;
  OrientedCSkeletonFace *createOrientedFace(CSkeletonNode *n1,
					    CSkeletonNode *n2,
					    CSkeletonNode *n3) const;
  
  OuterFaceID onOuterFace(const CSkeletonNodeVector*) const;
  OuterFaceID onSameOuterFace(const CSkeletonNodeVector*,
				const CSkeletonNodeVector*) const;
  bool onOuterFace(const OuterFaceID, const CSkeletonNodeVector*) const;
  OuterEdgeID onOuterEdge(const CSkeletonNodeVector*) const;
  // OuterEdgeID onOuterEdge(const CSkeletonNode*, const CSkeletonNode*,
  // 			  const CSkeletonNode*) const;
  bool checkExteriorSegments(const CSkeletonSegmentVector*) const;
  bool checkExteriorFaces(const CSkeletonFaceVector*) const;

  // homogeneity
  double getHomogeneityIndex() const;
  void calculateHomogeneityIndex() const;
  double energyTotal(double alpha) const;

  // methods related to deputies and copying
  virtual CSkeleton *sheriffSkeleton() = 0;
  virtual NodePositionsMap *getMovedNodes() const = 0;
  virtual void activate() = 0;
  CDeputySkeleton *deputyCopy();
  virtual CSkeleton *nodeOnlyCopy() = 0;
  virtual CSkeleton *completeCopy() = 0;

  virtual void needsHash() = 0;

  virtual CSkeletonPointBoundary *getPointBoundary(const std::string &name,
						   bool exterior) = 0; 
  virtual CSkeletonPointBoundary *makePointBoundary(const std::string &name,
						    CSkeletonNodeVector *nodes,
						    bool exterior=false) = 0;
  virtual CSkeletonEdgeBoundary *getEdgeBoundary(const std::string &name,
						 bool exterior) = 0;
  virtual CSkeletonEdgeBoundary *makeEdgeBoundary(
					  const std::string &name,
					  const CSkeletonSegmentVector *segs, 
					  const CSkeletonNode *start_node,
					  bool exterior=false) = 0;
  virtual CSkeletonEdgeBoundary *makeEdgeBoundary3D(
					    const std::string &name,
					    const SegmentSequence*,
					    bool exterior=false) = 0;
  virtual CSkeletonFaceBoundary *getFaceBoundary(const std::string &name,
						 OrientedSurface*,
						 bool exterior) = 0;
  virtual CSkeletonFaceBoundary *makeFaceBoundary(const std::string &name,
						  OrientedSurface*,
						  bool exterior=false) = 0;

  virtual CSkeletonPointBoundaryMap *getPointBoundaries() = 0;
  virtual CSkeletonEdgeBoundaryMap *getEdgeBoundaries() = 0;
  virtual CSkeletonFaceBoundaryMap *getFaceBoundaries() = 0;

  virtual std::string *compare(CSkeletonBase *other, double tolerance) const
    = 0;

  // real meshes
  //virtual FEMesh* femesh() = 0;
  virtual void populate_femesh(FEMesh *fem, Material *mat=NULL) = 0;

  virtual void cleanUp() = 0;

  virtual void printSelf(std::ostream&) const = 0;

  const std::string *sanityCheck() const;

  // TODO 3.1: 3D need to move more functions below to the base?
  
};				// CSkeletonBase

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeleton : public CSkeletonBase {

private:
  CMicrostructure *MS;
  Coord size;
  double volume_;
  bool *periodicity;
  vtkSmartPointer<vtkUnstructuredGrid> grid;
  vtkSmartPointer<vtkPoints> points;
  CSkeletonNodeVector nodes;
  CSkeletonElementVector elements;
  CSkeletonSegmentMap segments;
  CSkeletonFaceMap faces;
  vtkSmartPointer<vtkCellLocator> element_locator; // TODO 3.1: is this thread safe?
  vtkSmartPointer<vtkMergePoints> point_locator; // TODO 3.1: is this thread safe?
  CDeputySkeleton *deputy;	// The currently active deputy.
  CDeputySkeletonList deputy_list; // All deputies.
  bool washMe;
  int numDefunctNodes;
  static const std::string classname_;
  CSkeletonPointBoundaryMap pointBoundaries;
  CSkeletonEdgeBoundaryMap edgeBoundaries;
  CSkeletonFaceBoundaryMap faceBoundaries;
  // zombie is true if this CSkeleton has been pushed off the
  // SkeletonContext's undobuffer but still has deputies.
  bool zombie;
public:
  CSkeleton(CMicrostructure *ms, bool prdcty[DIM]);
  virtual ~CSkeleton();
  virtual void destroy();
  void destroyZombie();
  virtual const std::string &classname() const { return classname_; }

  // initialization members - TODO MER: add the 2D methods
  void createPointGrid(int m, int n, int l);
  void createTetra(const TetArrangement*, int m, int n, int l);
  CSkeletonNode *addNode(const Coord&);
  void addElement(CSkeletonElement *element, vtkIdType *ids);
  void createElement(vtkIdType type, vtkIdType numpts, vtkIdType *ids);
  void acceptProvisionalElement(CSkeletonElement *element);
  CSkeletonSegment *getOrCreateSegment(CSkeletonNode *n1, CSkeletonNode *n2);
  CSkeletonFace *getOrCreateFace(CSkeletonNode *n1, CSkeletonNode *n2,
				 CSkeletonNode *n3);
  void addGridSegmentsToBoundaries(const ICoord &, const ICoord &);
  void addGridFacesToBoundaries(const ICoord &idx, const ICoord &nml,
				bool flip);

  // basic get methods
  virtual const CMicrostructure *getMicrostructure() const {
    return MS;
  }
  virtual vtkSmartPointer<vtkUnstructuredGrid> getGrid() const {
    return grid;
  }
  virtual void getVtkCells(SkeletonFilter*,
			   vtkSmartPointer<vtkUnstructuredGrid>);
  virtual vtkSmartPointer<vtkDataArray> getMaterialCellData(
						   const SkeletonFilter*) const;
  virtual vtkSmartPointer<vtkDataArray> getEnergyCellData(
				    double alpha, const SkeletonFilter*) const;
  virtual vtkSmartPointer<vtkPoints> getPoints() const {
    return points;
  }
  virtual CSkeletonNode *getNode(unsigned int nidx) const;
  virtual bool hasNode(CSkeletonNode *) const;
  virtual CSkeletonElement *getElement(unsigned int eidx) const;
  virtual bool hasElement(CSkeletonElement *) const;
  virtual CSkeletonSegment *getSegment(const CSkeletonMultiNodeKey &h) const; 
  virtual CSkeletonFace *getFace(const CSkeletonMultiNodeKey &h) const; 
  virtual CSkeletonSegment *getSegmentByUid(uidtype) const;
  virtual CSkeletonFace *getFaceByUid(uidtype) const;

  virtual CSkeletonNodeIterator beginNodes() const {
    return nodes.begin();
  }
  virtual CSkeletonNodeIterator endNodes() const {
    return nodes.end();
  }
  virtual CSkeletonElementIterator beginElements() const {
    return elements.begin();
  }
  virtual CSkeletonElementIterator endElements() const {
    return elements.end();
  }
  virtual CSkeletonSegmentIterator beginSegments() const {
    return segments.begin();
  }
  virtual CSkeletonSegmentIterator endSegments() const {
    return segments.end();
  }
  virtual CSkeletonFaceIterator beginFaces() const {
    return faces.begin();
  }
  virtual CSkeletonFaceIterator endFaces() const {
    return faces.end();
  }

  // information and calculation methods

  // TODO 3.1: need to subtract defunct things?  Not subtracting
  // doesn't seem to be causing a problem...
  virtual int nnodes() const {
    return nodes.size();
  }
  virtual int nelements() const {
    return elements.size();
  }
  virtual int nsegments() const {
    return segments.size();
  }
  virtual int nfaces() const {
    return faces.size();
  }
  virtual double volume() const {
    return volume_;
  }
  virtual bool getPeriodicity(int dim) const {
    return periodicity[dim];
  }
  virtual void checkIllegality();
  virtual int getIllegalCount();
  //vtkPoints *getElementPoints(int eidx);
  virtual void getIllegalElements(CSkeletonElementVector &) const;
  virtual int getSuspectCount();
  virtual void getSuspectElements(CSkeletonElementVector &) const;
  uidtype getNodeUid(int nidx) const;
  uidtype getElementUid(int eidx) const;

  virtual const Coord nodePositionForSkeleton(CSkeletonNode *n);    
  virtual vtkSmartPointer<vtkCellLocator> get_element_locator();
  virtual vtkSmartPointer<vtkMergePoints> get_point_locator();
  virtual bool inSegmentMap(const CSkeletonMultiNodeKey &h) const;

  virtual std::string *compare(CSkeletonBase *other, double tolerance) const;

  // boundaries
  void checkBoundaryNames(const std::string &name);
  virtual CSkeletonPointBoundary *getPointBoundary(const std::string &name,
						   bool exterior);
  virtual CSkeletonPointBoundary *makePointBoundary(const std::string &name,
						    CSkeletonNodeVector *nodes,
						    bool exterior=false);
  virtual CSkeletonEdgeBoundary *getEdgeBoundary(const std::string &name,
						 bool exterior);
  virtual CSkeletonEdgeBoundary *makeEdgeBoundary(
					  const std::string &name,
					  const CSkeletonSegmentVector *segs, 
					  const CSkeletonNode *start_node,
					  bool exterior=false);
  virtual CSkeletonEdgeBoundary *makeEdgeBoundary3D(const std::string &name,
						    const SegmentSequence*,
						    bool exterior=false);
  virtual CSkeletonFaceBoundary *getFaceBoundary(const std::string &name,
						 OrientedSurface*,
						 bool exterior);
  virtual CSkeletonFaceBoundary *makeFaceBoundary(const std::string &name,
						  OrientedSurface*,
						  bool exterior=false);
  void removeBoundary(const std::string &name);
  void renameBoundary(const std::string &oldname, const std::string &newname);
  virtual CSkeletonPointBoundaryMap *getPointBoundaries() {
    return &pointBoundaries;
  }
  virtual CSkeletonEdgeBoundaryMap *getEdgeBoundaries() {
    return &edgeBoundaries;
  }
  virtual CSkeletonFaceBoundaryMap *getFaceBoundaries() {
    return &faceBoundaries;
  }

  // methods related to deputies and sheriffs
  virtual CSkeleton* sheriffSkeleton();
  void addDeputy(CDeputySkeleton* dep);
  virtual NodePositionsMap *getMovedNodes() const;
  virtual void activate();
  void deputize(CDeputySkeleton* deputy);
  virtual void needsHash();
  CDeputySkeleton* deputySkeleton() { return deputy; }
  const CDeputySkeletonList *getDeputyList() const { return &deputy_list; }
  void removeDeputy(CDeputySkeleton *dep);
  virtual int nDeputies() const { return deputy_list.size(); }

  void copyNodes(CSkeleton *) const;
  virtual CSkeleton *nodeOnlyCopy();
  virtual CSkeleton *completeCopy();

  ProvisionalMerge *mergeNode(CSkeletonNode *n0, CSkeletonNode *n1);
  ProvisionalMerge *addElementsToMerge(CSkeletonNode *n0, CSkeletonNode *n1,
				       ProvisionalMerge *merge);
  void removeElements(const CSkeletonElementSet&);
  void removeElement(CSkeletonElement*);
  void removeNode(CSkeletonNode*);
  void dirty() { washMe = true; }
  virtual void cleanUp();

  void moveNodeTo(CSkeletonNode *node, const Coord &position);
  void moveNodeBy(CSkeletonNode *node, const Coord &position);

  virtual void nodesAddGroupsDown(CGroupTrackerVector*);
  virtual void segmentsAddGroupsDown(CGroupTrackerVector*);
  virtual void facesAddGroupsDown(CGroupTrackerVector*);
  virtual void elementsAddGroupsDown(CGroupTrackerVector*);

  // real meshes
  //virtual FEMesh* femesh();
  virtual void populate_femesh(FEMesh *fem, Material *mat=NULL);

  virtual void printSelf(std::ostream&) const;

  friend class CDeputySkeleton;
};				// end CSkeleton

CSkeleton *newCSkeleton(CMicrostructure*, bool[DIM]);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A deputy Skeleton is a Skeleton that differs from another (its
// "sheriff") only in the positions of its nodes.  The deputy only
// stores the positions of the nodes.  It refers to the sheriff for
// all other Skeleton data.

class CDeputySkeleton : public CSkeletonBase {

private:
  CSkeleton *skeleton;
  NodePositionsMap *nodePositions;
  bool active;
  static const std::string classname_;
public:
  CDeputySkeleton(CSkeletonBase *skel);
  virtual ~CDeputySkeleton();
  virtual const std::string &classname() const { return classname_; }
  virtual void destroy();

  // basic get methods
  virtual const CMicrostructure *getMicrostructure() const {
    return skeleton->MS;
  }
  virtual vtkSmartPointer<vtkUnstructuredGrid> getGrid() const {
    return skeleton->grid;
  }
  virtual void getVtkCells(SkeletonFilter *f,
			   vtkSmartPointer<vtkUnstructuredGrid> g)
  {
    skeleton->getVtkCells(f, g);
  }
  virtual vtkSmartPointer<vtkDataArray> getMaterialCellData(
					   const SkeletonFilter *filter) const
  {
    return skeleton->getMaterialCellData(filter);
  }
  virtual vtkSmartPointer<vtkDataArray> getEnergyCellData(
			    double alpha, const SkeletonFilter *filter) const
  {
    return skeleton->getEnergyCellData(alpha, filter);
  }
  virtual vtkSmartPointer<vtkPoints> getPoints() const {
    return skeleton->points;
  }
  virtual CSkeletonNode *getNode(unsigned int nidx) const {
    return skeleton->getNode(nidx);
  }
  virtual bool hasNode(CSkeletonNode *n) const {
    return skeleton->hasNode(n);
  }
  virtual CSkeletonElement *getElement(unsigned int eidx) const {
    return skeleton->getElement(eidx);
  }
  virtual bool hasElement(CSkeletonElement *e) const {
    return skeleton->hasElement(e);
  }
  virtual CSkeletonSegment *getSegment(const CSkeletonMultiNodeKey &h) const {
    return skeleton->getSegment(h);
  }
  virtual CSkeletonFace *getFace(const CSkeletonMultiNodeKey &h) const {
    return skeleton->getFace(h);
  }
  virtual CSkeletonSegment *getSegmentByUid(uidtype i) const {
    return skeleton->getSegmentByUid(i);
  }
  virtual CSkeletonFace *getFaceByUid(uidtype i) const {
    return skeleton->getFaceByUid(i);
  }
  virtual CSkeletonNodeIterator beginNodes() const {
    return skeleton->nodes.begin();
  }
  virtual CSkeletonNodeIterator endNodes() const {
    return skeleton->nodes.end();
  }
  virtual CSkeletonElementIterator beginElements() const {
    return skeleton->elements.begin();
  }
  virtual CSkeletonElementIterator endElements() const {
    return skeleton->elements.end();
  }
  virtual CSkeletonSegmentIterator beginSegments() const {
    return skeleton->segments.begin();
  }
  virtual CSkeletonSegmentIterator endSegments() const {
    return skeleton->segments.end();
  }
  virtual CSkeletonFaceIterator beginFaces() const {
    return skeleton->faces.begin();
  }
  virtual CSkeletonFaceIterator endFaces() const {
    return skeleton->faces.end();
  }
  virtual int nDeputies() const { return 0; }

  // basic info
  virtual int nnodes() const {
    return skeleton->nnodes();
  }
  virtual int nelements() const {
    return skeleton->nelements();
  }
  virtual int nsegments() const {
    return skeleton->nsegments();
  }
  virtual int nfaces() const {
    return skeleton->nfaces();
  }
  virtual double volume() const {
    return skeleton->volume();
  }
  
  virtual void nodesAddGroupsDown(CGroupTrackerVector* v) {
    skeleton->nodesAddGroupsDown(v);
  }
  virtual void segmentsAddGroupsDown(CGroupTrackerVector* v) {
    skeleton->segmentsAddGroupsDown(v);
  }
  virtual void facesAddGroupsDown(CGroupTrackerVector* v) {
    skeleton->facesAddGroupsDown(v);
  }
  virtual void elementsAddGroupsDown(CGroupTrackerVector* v) {
    skeleton->elementsAddGroupsDown(v);
  }

  virtual bool getPeriodicity(int dim) const {
    return skeleton->getPeriodicity(dim);
  }
  virtual void checkIllegality() {
    skeleton->checkIllegality();
  }
  virtual int getIllegalCount() {
    return skeleton->getIllegalCount();
  }
  virtual void getIllegalElements(CSkeletonElementVector &ills) const {
    skeleton->getIllegalElements(ills);
  }
  virtual int getSuspectCount() {
    return skeleton->getSuspectCount();
  }
  virtual void getSuspectElements(CSkeletonElementVector &sus) const {
    skeleton->getSuspectElements(sus);
  }
  virtual const Coord nodePositionForSkeleton(CSkeletonNode *n);    
  const Coord originalPosition(CSkeletonNode *n);    

  // virtual methods needed for calculating stuff
  virtual vtkSmartPointer<vtkCellLocator> get_element_locator() {
    return skeleton->get_element_locator();
  }
  virtual vtkSmartPointer<vtkMergePoints> get_point_locator() {
    return skeleton->get_point_locator();
  }
  virtual bool inSegmentMap(const CSkeletonMultiNodeKey &h) const {
    return skeleton->inSegmentMap(h);
  }
  
  virtual CSkeletonPointBoundary *getPointBoundary(const std::string &name,
						   bool exterior)
  {
    return skeleton->getPointBoundary(name, exterior);
  }
  virtual CSkeletonPointBoundary *makePointBoundary(const std::string &name,
						    CSkeletonNodeVector *nodes,
						    bool exterior=false)
  {
    return skeleton->makePointBoundary(name, nodes, exterior);
  }
  virtual CSkeletonEdgeBoundary *getEdgeBoundary(const std::string &name,
						 bool exterior)
  {
    return skeleton->getEdgeBoundary(name, exterior);
  }
  virtual CSkeletonEdgeBoundary *makeEdgeBoundary(
					  const std::string &name,
					  const CSkeletonSegmentVector *segs, 
					  const CSkeletonNode *start_node,
					  bool exterior=false)
  {
    return skeleton->makeEdgeBoundary(name, segs, start_node, exterior);
  }
  virtual CSkeletonEdgeBoundary *makeEdgeBoundary3D(const std::string &name,
						    const SegmentSequence *seq,
						    bool exterior=false)
  {
    return skeleton->makeEdgeBoundary3D(name, seq, exterior);
  }
  virtual CSkeletonFaceBoundary *getFaceBoundary(const std::string &name,
						 OrientedSurface *surf,
						 bool exterior)
  {
    return skeleton->getFaceBoundary(name, surf, exterior);
  }
  virtual CSkeletonFaceBoundary *makeFaceBoundary(const std::string &name,
						  OrientedSurface *surf,
						  bool exterior=false)
  {
    return skeleton->makeFaceBoundary(name, surf, exterior);
  }


  virtual std::string *compare(CSkeletonBase *other, double tolerance) const
  {
    return skeleton->compare(other, tolerance);
  }

  // stuff related to deputies
  virtual CSkeleton* sheriffSkeleton();
  virtual NodePositionsMap *getMovedNodes() const;
  virtual void activate();
  virtual void deactivate();
  virtual CSkeleton *nodeOnlyCopy() {
    return skeleton->nodeOnlyCopy();
  }
  virtual CSkeleton *completeCopy() {
    return skeleton->completeCopy();
  }
  virtual void needsHash() {
    skeleton->needsHash();
  }

  // moving nodes
  void swapPositions();
  void moveNodeTo(CSkeletonNode *node, const Coord &position);
  void moveNodeBy(CSkeletonNode *node, const Coord &position);
  void moveNodeBack(CSkeletonNode *node);

  virtual CSkeletonPointBoundaryMap *getPointBoundaries() {
    return skeleton->getPointBoundaries();
  }
  virtual CSkeletonEdgeBoundaryMap *getEdgeBoundaries() {
    return skeleton->getEdgeBoundaries();
  }
  virtual CSkeletonFaceBoundaryMap *getFaceBoundaries() {
    return skeleton->getFaceBoundaries();
  }

  // real meshes
  //virtual FEMesh* femesh() {return skeleton->femesh();}
  virtual void populate_femesh(FEMesh *fem, Material *mat=NULL) {
    skeleton->populate_femesh(fem);
  }

  virtual void cleanUp() {
    skeleton->cleanUp();
  }
  virtual void printSelf(std::ostream&) const;
};				// end CDeputySkeleton

CDeputySkeleton *newCDeputySkeleton(CSkeletonBase *);

std::ostream &operator<<(std::ostream&, const CSkeletonBase&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO OPT: Move ProvisionalChanges classes to a separate file.  This one
// is too big.

struct MoveNode {
  CSkeletonNode *node;
  Coord position;
  bool mobility[3];
};

class SkeletonSubstitutionBase {
protected:
  CSkeletonMultiNodeSelectable *substitutee;
public:
  SkeletonSubstitutionBase(CSkeletonMultiNodeSelectable *s)
    : substitutee(s)
  {}
  virtual ~SkeletonSubstitutionBase() {}
  void substitute(CSkeleton*) const;
  virtual CSkeletonMultiNodeSelectable *getSubstitute(CSkeleton*) const = 0;
};

struct SegSubstitutionLT {
  bool operator()(const SegmentSubstitution&, const SegmentSubstitution&) const;
};

class SegmentSubstitution : public SkeletonSubstitutionBase {
private:
  CSkeletonNode *node0, *node1;
public:
  SegmentSubstitution(CSkeletonSegment *s, CSkeletonNode *n0, CSkeletonNode *n1)
    : SkeletonSubstitutionBase(s), node0(n0), node1(n1)
  {}
  virtual CSkeletonMultiNodeSelectable *getSubstitute(CSkeleton*) const;
  friend struct SegSubstitutionLT;
};

typedef std::set<SegmentSubstitution, SegSubstitutionLT> SegmentSubstitutionSet;

struct FaceSubstitutionLT {
  bool operator()(const FaceSubstitution&, const FaceSubstitution&) const;
};

class FaceSubstitution : public SkeletonSubstitutionBase {
private:
  CSkeletonNode *node0, *node1, *node2;
public:
  FaceSubstitution(CSkeletonFace *f, CSkeletonNode *n0, CSkeletonNode *n1,
		   CSkeletonNode *n2)
    : SkeletonSubstitutionBase(f), node0(n0), node1(n1), node2(n2)
  {}
  virtual CSkeletonMultiNodeSelectable *getSubstitute(CSkeleton*) const;
  friend struct FaceSubstitutionLT;
};

typedef std::set<FaceSubstitution, FaceSubstitutionLT> FaceSubstitutionSet;

typedef std::vector<MoveNode> MoveNodeVector;
typedef std::map<CSkeletonElement*, HomogeneityData> HomogeneityDataMap;

#ifndef HAVE_SSTREAM
#include <strstream.h>
#else
#include <sstream>
#endif

class ProvisionalChangesBase {
protected:
  MoveNodeVector movednodes;
  double cachedDeltaE; // the cached value
  bool deltaECached; // whether it was cached
public:
  ProvisionalChangesBase(const std::string &n)
    : deltaECached(false), name(n)
  {}
  const std::string name;	// useful for debugging
  virtual ~ProvisionalChangesBase() {};

  // Strings added by annotate can be printed by accept() to help
  // debug the skeleton modification process, without cluttering the
  // debugging output with details of rejected ProvisionalChanges.
// #ifndef HAVE_SSTREAM
//   std::ostrstream annotate;
// #else
//   std::ostringstream annotate;
// #endif

  virtual bool illegal() = 0;
  // deltaE() is not const because it may need to call moveNode.
  virtual double deltaE(double alpha) = 0;
  virtual void moveNode(CSkeletonNode *node, const Coord &x, bool *mob=NULL) = 0;
  virtual void accept() = 0;
  MoveNodeVector::const_iterator getMovedNodesBegin() {
    return movednodes.begin();
  }
  MoveNodeVector::const_iterator getMovedNodesEnd() {
    return movednodes.end();
  }
  virtual void removeAddedNodes() = 0;
};


class DeputyProvisionalChanges : public ProvisionalChangesBase {
protected:
  CDeputySkeleton *deputy;
  CSkeletonElementVector elements;
  bool cachedIllegal; // the cached value
  bool illegalCached; // whether it was cached
  HomogeneityDataMap cachedNewHomogeneity;

public:
  DeputyProvisionalChanges(CDeputySkeleton*, const std::string &);
  virtual ~DeputyProvisionalChanges() {};
  virtual void moveNode(CSkeletonNode *node, const Coord &x, bool *mob=NULL);
  virtual void accept();
  virtual bool illegal();
  void makeNodeMove();
  void moveNodeBack();
  virtual void removeAddedNodes() {};
  virtual double deltaE(double alpha);
};


class ProvisionalChanges : public ProvisionalChangesBase {
protected:
  CSkeleton *skeleton;
  CSkeletonElementSet removed;
  CSkeletonElementSet inserted;
  CSkeletonSelectablePairSet substitutions;
  SegmentSubstitutionSet seg_substitutions; 
  FaceSubstitutionSet face_substitutions;
  // CSkeletonSelectablePairSet seg_substitutions;
  // CSkeletonSelectablePairSet face_substitutions;
  //MoveNodeVector movednodes;
  ConstCSkeletonElementSet before;
  CSkeletonElementSet after;
public:
  ProvisionalChanges(CSkeleton *skel, const std::string &n);
  virtual ~ProvisionalChanges();
  virtual void removeAddedNodes() {}
  void removeElement(CSkeletonElement*);
  void removeElements(const CSkeletonElementVector &);
  void insertElement(CSkeletonElement *);
  void substituteElement(CSkeletonElement *, CSkeletonElement *);
  void substituteSegment(CSkeletonSegment*, CSkeletonNode*, CSkeletonNode*);
  void substituteSegment(CSkeletonSegment*, CSkeletonSegment*);
  void substituteFace(CSkeletonFace*, CSkeletonNode*, CSkeletonNode*,
		      CSkeletonNode*);
  void substituteFace(CSkeletonFace*, CSkeletonFace*);
  int nRemoved() { return removed.size(); }
  // nInserted
  // elBefore
  CSkeletonSelectablePairSet& getSubstitutions() { return substitutions; }
  CSkeletonElementSet& getRemoved() { return removed; }
  virtual bool illegal();
  virtual void moveNode(CSkeletonNode *node, const Coord &x, bool *mob=NULL);
  virtual void makeNodeMove();
  virtual void moveNodeBack();
  virtual double deltaE(double alpha);
  // deltaEBound
  virtual void accept();
  void checkVolume();
  void sanityCheck();
};

class ProvisionalMerge : public ProvisionalChanges {
protected:
  CSkeletonNode *node0;
  CSkeletonNode *node1;
public:
  ProvisionalMerge(CSkeleton *skel, CSkeletonNode *n0, CSkeletonNode *n1,
		   const std::string &n)
    : ProvisionalChanges(skel, n),
      node0(n0),
      node1(n1) 
  {}
  virtual ~ProvisionalMerge() {}
  virtual void accept();
};

// changes that can add nodes
class ProvisionalInsertion : public ProvisionalChanges {
protected:
  CSkeletonNodeVector added_nodes;
public:
  ProvisionalInsertion(CSkeleton *skel, const std::string &n)
    : ProvisionalChanges(skel, n)
  {}
  virtual ~ProvisionalInsertion() {}
  void addNode(CSkeletonNode *n) { added_nodes.push_back(n); }
  virtual void removeAddedNodes();
};

#endif //CSKELETON2_H
