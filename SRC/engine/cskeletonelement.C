 // -*- C++ -*-
 // $RCSfile: cskeletonelement.C,v $
 // $Revision: 1.1.2.101 $
 // $Author: langer $
 // $Date: 2014/12/14 01:07:48 $

 /* This software was produced by NIST, an agency of the U.S. government,
  * and by statute is not subject to copyright in the United States.
  * Recipients of this software assume all responsibilities associated
  * with its operation, modification and maintenance. However, to
  * facilitate maintenance we ask that before distributing modified
  * versions of this software, you first contact the authors at
  * oof_manager@nist.gov. 
  */

 #include "common/IO/oofcerr.h"
 #include "common/cdebug.h"
 #include "common/cmicrostructure.h"
 #include "common/lock.h"
 #include "common/pixelsetboundary.h"
 #include "common/printvec.h"
 #include "engine/cskeleton2.h"
 #include "engine/cskeletonelement.h"
 #include "engine/cskeletonnode2.h"
 #include "engine/element.h"
 #include "engine/elementnodeiterator.h"
 #include "engine/femesh.h"
 #include "engine/masterelement.h"
 #include "engine/material.h"
 #include "engine/ooferror.h"

 #include <vtkMath.h>
 #include <vtkTriangle.h>
 #include <vtkLine.h>
 #include <algorithm>
 #include <limits>
 #include <set>
 #include <math.h>

 #define LEGAL_COS_TOLERANCE std::numeric_limits<double>::epsilon()
 #define LEGAL_COS2_TOLERANCE 2*LEGAL_COS_TOLERANCE
 #define SUSPECT_COS_TOLERANCE 1.0e-6
 #define SUSPECT_COS2_TOLERANCE 2*SUSPECT_COS_TOLERANCE

 const std::string CSkeletonElement::modulename_(
					 "ooflib.SWIG.engine.cskeletonelement");
 const std::string CSkeletonElement::classname_("CSkeletonElement");


 #define NUM_TET_FACES 4
 #define NUM_TET_EDGES 6
 #define NUM_TET_NODES 4
 #define NUM_TET_FACE_EDGES 3
 // Maximum number of points where a tet can intersect a plane
 #define MAX_TET_PLANE_POINTS 4
 // Maximum number of points where a quad can intersect a tet (ie max
 // number of sides of the polygon formed in the plane of a quad by
 // intersecting the quad with the intersection of the tet and the
 // plane).
 #define MAX_TET_QUAD_IXS 8
 // The maximum number of voxel boundary quads that can be closest to a
 // tet point.
 #define MAX_CLOSEST_QUADS 6

 // static CSkeletonElementSet allElements;
 long CSkeletonElement::globalElementCount = 0;
 static SLock globalElementCountLock;

 //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

 // A structure for storing where a quad intersects a tet.  There are
 // members for storing topological information.

 // TODO 3.1: Use separate subclasses for intersections on faces and
 // edges.  This class used to be just a struct. See TODO in
 // createIPoint().

 class IntersectionPoint {
 public:
   // The actual point.
   double x[3];	 // TODO 3.1: Why not use a Coord?
   // Bools for whether the point is on each face / edge
   bool faces[4];
   bool edges[6];
   // The parametric position along each edge.
   double t[6];
   // A hash value corresponding to each of the three Cartesian axes.
   int hash[3];
   // Whether or not the point is a corner of a Voxel Boundary Quad
   bool corner;

   IntersectionPoint() {
     x[0] = x[1] = x[2] = 0;
     faces[0] = faces[1] = faces[2] = faces[3] = 0;
     edges[0] = edges[1] = edges[2] = edges[3] = edges[4] = edges[5] = 0;
     t[0] = t[1] = t[2] = t[3] = t[4] = t[5] = 0;
     hash[0] = hash[1] = hash[2] = 0;
     corner = 0;
   }
 };

 std::ostream &operator<<(std::ostream &os, const IntersectionPoint &ip) {
   return os << "IntersectionPoint(x=("
	     << ip.x[0] << "," << ip.x[1] << "," << ip.x[2]
	     << "), faces=" << ip.faces[0] << ip.faces[1] << ip.faces[2]
	     << ip.faces[3] 
	     << ", edges=" << ip.edges[0] << ip.edges[1] << ip.edges[2]
	     << ip.edges[3] << ip.edges[4] << ip.edges[5]
	     << ", corner=" << ip.corner << ")";
 }

 // A structure for storing IntersectionPoints on tet faces. Used with
 // to enforce topological consistency -- keeping track of "loose
 // ends". The name face intersection was chosen before realizing that
 // it was useful to store other intersection points in an "extra" bin.
 class FaceIntersection {
 public:
   // The actual point.
   IntersectionPoint *ip;
   // The other point in the segment that was being considered when an
   // instance of FaceIntersection was added to a
   // FaceIntersectionMap. This is used to detect spurious edges.
   IntersectionPoint *op; 
   // The type of edge intersection this would be. It's an entrance if
   // the segment went from op to ip, and an exit if it went from ip to
   // op.
   IntersectionCategory type; 
   // The contribution of the ip-op segment to a tet face.
   double contrib;
   // The quad that ip and op came from
   const Quad *quad;
   // The number of matches.
   int matches;
   // Whether the point came from a quad that is outside the tet.
   bool outside;
   // Whether this face intersection has been paired.
   bool paired;
 };

 std::ostream &operator<<(std::ostream &os, const FaceIntersection &fi) {
   return os << "FaceIntersection(quad=" << fi.quad << ")";
 }

 // A vector of IntersectionPoints gives the ordered set of points that
 // make up the intersection of a Voxel Boundary Quad and a tet.
 typedef std::vector<IntersectionPoint*> IntersectionPoints;
 typedef std::pair<int, FaceIntersection> FaceIntersectionDatum;
 // A map of Face Intersections is used to keep track of "loose
 // ends". The indices of the map are the hash values of the
 // points. These objects are used in a vector where the index of each
 // vector indicates the face id, with one extra bin for non-face
 // points. The extra bin is necessary to check for near misses.
 typedef std::multimap<int, FaceIntersection> FaceIntersectionMap;

 // A structure for storing the points where tet edges intersect a
 // plane.  There are members which are used for sorting these into a
 // convex hull as well as for storing topological information.
 class TetIntersectionPoint {
 public:
   // The actual point in 2D.
   double x[2];
   // The parametric coordinate of the intersection point along the tet
   // edge denoted by the edge member.
   double t;
   // dist2 and tan are used to find the convex hull.
   double dist2;
   double tan;
   // The edge id, if any.
   short int edge;
   // The node id, if any.
   short int node; 
 };

 std::ostream &operator<<(std::ostream &os, const TetIntersectionPoint &tip) {
   return os << "TetIntersectionPoint(x=(" << tip.x[0] << "," << tip.x[1]
	     << "), edge=" << tip.edge << ", node=" << tip.node << ")";
 }

 // A vector of TetIntersectionPoints gives the ordered set of points
 // where a tet intersects the axis aligned plane of Voxel Boundary Quads.
 typedef std::vector<TetIntersectionPoint> TetIntersectionPoints;

 //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

 // CSkeletonElements contain a 'generating_function' member, which is
 // a reference to a string that identifies how the element was
 // created.  (This is mostly for debugging.)  To reduce memory, the
 // elements store references, not the strings themselves.  The
 // unifyNames function wraps the strings that are passed into the
 // element constructor and ensures that there is only one copy of each
 // string, and that it's stored in a static variable so that the
 // reference stays valid.  This way the routines that call the
 // constructors don't have to worry about the data scope of the
 // string.

 typedef std::set<std::string> NameSet;

 const std::string &unifyNames(const std::string &name) {
   static NameSet names;
   // std::set::insert inserts an element into the set, if it doesn't
   // already exist.  It returns an iterator that points to the element
   // in the set in either case.
   std::pair<NameSet::iterator, bool> p = names.insert(name);
   return *p.first;
 }

 //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


 CSkeletonElement::CSkeletonElement(int indx, CSkeletonNodeVector *ns)
   : CSkeletonMultiNodeSelectable(ns),
     generating_function(unifyNames(""))
 {
   // oofcerr << "CSkeletonElement::ctor: indx=" << indx << " nodes=";
   // for(int i=0; i<4; i++)
   //   oofcerr << " " << (*nodes)[i]->getUid();
   // oofcerr << std::endl;
   index = indx;
   globalElementCountLock.acquire();
   ++globalElementCount;
   // allElements.insert(this);
   globalElementCountLock.release();
 }

 CSkeletonElement::CSkeletonElement(CSkeletonNodeVector *ns,
				    CSkeletonElement *p, 
				    const std::string &name)
   : CSkeletonMultiNodeSelectable(ns),
     generating_function(unifyNames(name))
 {
   // Provisional elements have an index of -1.
   index = -1;
   if(p!=NULL)
     add_parent(p);
   globalElementCountLock.acquire();
   ++globalElementCount;
   // allElements.insert(this);
   globalElementCountLock.release();
 }

 CSkeletonElement::CSkeletonElement(CSkeletonNodeVector *ns,
				    CSkeletonSelectableList &parents,
				    const std::string &name)
   : CSkeletonMultiNodeSelectable(ns),
     generating_function(unifyNames(name))
 {
   // Provisional elements have an index of -1.
   index = -1;
   add_parents(parents);
   globalElementCountLock.acquire();
   ++globalElementCount;
   // allElements.insert(this);
   globalElementCountLock.release();
 }

 CSkeletonElement::CSkeletonElement(
		    CSkeletonNode *n0, CSkeletonNode *n1, CSkeletonNode *n2, 
		    CSkeletonNode *n3, CSkeletonElement *p,
		    const std::string &name)
   : generating_function(unifyNames(name))
 {
   // provisional element
   index = -1;

   nodes->push_back(n0);
   nodes->push_back(n1);
   nodes->push_back(n2);
   nodes->push_back(n3);

   if(p!=NULL)
     add_parent(p);

   globalElementCountLock.acquire();
   ++globalElementCount;
   // allElements.insert(this);
   globalElementCountLock.release();
 }

 CSkeletonElement::~CSkeletonElement() {
   globalElementCountLock.acquire();
   --globalElementCount;
   // allElements.erase(this);
   globalElementCountLock.release();
 }

 // void dumpElements() {
 //   oofcerr << "dumpElements: " << allElements.size() << std::endl;
 //   for(CSkeletonElementSet::iterator i=allElements.begin();
 //       i!=allElements.end(); ++i)
 //     {
 //       oofcerr << **i << std::endl;
 //     }
 // }

 vtkSmartPointer<vtkCell> CSkeletonElement::getEmptyVtkCell() const {
   return vtkSmartPointer<vtkTetra>::New();
 }

 long get_globalElementCount() {
   return CSkeletonElement::globalElementCount;
 }

 CSkeletonMultiNodeKey CSkeletonElement::key() const {
   // TODO OPT: Cache this and return a reference?
   return CSkeletonMultiNodeKey((*nodes)[0], (*nodes)[1], (*nodes)[2],
				(*nodes)[3]);
 }

 void CSkeletonElement::connectToNodes() {
   for(CSkeletonNodeIterator it = nodes->begin(); it != nodes->end(); ++it)
     (*it)->addElement(this);
 }

 CSkeletonElement *CSkeletonElement::copy_child(int idx,
						vtkSmartPointer<vtkPoints> pts)
 {
   CSkeletonElement *child = dynamic_cast<CSkeletonElement*>(
				  CSkeletonSelectable::copy_child(idx, pts));
   child->copyHomogeneity(*this);
   return child;
 }

 CSkeletonElement *CSkeletonElement::new_child(int idx,
					       vtkSmartPointer<vtkPoints> pts) 
 {
   CSkeletonNodeVector *node_children = get_node_children();
   CSkeletonElement *child  = new CSkeletonElement(idx, node_children);
   child->copyHomogeneity(*this);
   child->connectToNodes();
   return child;
 }

 void CSkeletonElement::promote(int idx) {
   // oofcerr << "CSkeletonElement::promote: indx=" << idx << " nodes=";
   // for(int i=0; i<4; i++)
   //   oofcerr << " " << (*nodes)[i]->getUid();
   // oofcerr << std::endl;
   connectToNodes();
 #ifdef DEBUG
   if(illegal()) {
     oofcerr << "ILLEGAL " << uid << " " << volume() << std::endl;
     for(int i=0; i<4; ++i) {
       oofcerr << "CSkeletonElement::promote: " << (*nodes)[i]->getUid()
		 << " " << (*nodes)[i]->position() << std::endl;
     }
     oofcerr << "CSkeletonElement::promote: promoting illegal element!"
	       << std::endl;
     // throw ErrProgrammingError("CSkeletonElement: promoting illegal element",
     // 			      __FILE__, __LINE__);
   }
 #endif	// DEBUG
   if(index != -1)
     throw ErrProgrammingError(
	       "CSkeletonElement: attempt to promote a non-provisional element",
	       __FILE__, __LINE__);
   index = idx;
   for(CSkeletonSelectableList::iterator p=parents.begin(); p!=parents.end();
       ++p)
     {
       (*p)->add_child(this);
     }
 }

 /*void CSkeletonElement::positionPointer(double x[4][3]) const {
   for(unsigned int i=0; i<nodes->size(); ++i) {
     Coord x_ = (*nodes)[i]->position();
     x[i][0] = x_[0];
     x[i][1] = x_[1];
     x[i][2] = x_[2];
   }
 }*/

 void CSkeletonElement::positionPointer(Coord *x) const {
   for(unsigned int i=0; i<nodes->size(); ++i) {
     x[i] = (*nodes)[i]->position();
   }
 }

 bool CSkeletonElement::interior(const Coord *point) const {
   double bcoords[4]/*, y[3]*/;
   Coord x[4];
   positionPointer(x);
   //point->writePointer(y);
   vtkTetra::BarycentricCoords(
       // WTF doesn't vtk declare the const args as const?
       const_cast<Coord*>(point)->xpointer(),
       x[0].xpointer(), x[1].xpointer(),
       x[2].xpointer(),x[3].xpointer(),
       bcoords);
   for(int i=0; i<4; ++i)
     if(bcoords[i]<0) return false;
   return true;
 }

 double CSkeletonElement::volume() const {
   Coord x[4];
   positionPointer(x);
   return vtkTetra::ComputeVolume(x[0].xpointer(), x[1].xpointer(),
				  x[2].xpointer(), x[3].xpointer());
 }

 double CSkeletonElement::volumeInVoxelUnits(const CMicrostructure *MS) const {
   // Get the points that define the element and convert them to pixel
   // units.
   Coord epts[4];
   Coord delta = MS->sizeOfPixels();
   for(int i=0; i<4; ++i) {
     epts[i] = (*nodes)[i]->position()/delta;
   }
   return vtkTetra::ComputeVolume(epts[0].xpointer(),epts[1].xpointer(),epts[2].xpointer(),epts[3].xpointer());
 }

 double CSkeletonElement::volumeInFractionalUnits(const CMicrostructure *MS) const {
   // Get the points that define the element and convert them to pixel
   // units.
   Coord epts[4];
   Coord delta = MS->size();
   for(int i=0; i<4; ++i) {
     epts[i] = (*nodes)[i]->position()/delta;
   }
   return vtkTetra::ComputeVolume(epts[0].xpointer(),epts[1].xpointer(),epts[2].xpointer(),epts[3].xpointer());
 }

 double CSkeletonElement::cosCornerAngle(int fid, int cid) const {
   Coord x[4];
   Coord s0;
   Coord s1;
   positionPointer(x);
   int *facePtIds = vtkTetra::GetFaceArray(fid);
   // TODO OPT: Some of this dereferencing can be moved out of the loop.
   for(int i=0; i<3; i++) {
     s0[i] = x[facePtIds[(cid+3-1)%3]][i] - x[facePtIds[cid]][i];
     s1[i] = x[facePtIds[(cid+1)%3]][i] - x[facePtIds[cid]][i];
   }
 #ifdef DEBUG
   if(vtkMath::Norm(s0.xpointer()) == 0 || vtkMath::Norm(s1.xpointer()) == 0)
     throw ErrProgrammingError(
		       "CSkeletonElement: Triangle with zero length edge",
		       __FILE__,__LINE__);
 #endif
   double cosAngle = vtkMath::Dot(s0.xpointer(),s1.xpointer())/(vtkMath::Norm(s0.xpointer())*vtkMath::Norm(s1.xpointer()));
   if(cosAngle > 1.0 || (1-cosAngle) < LEGAL_COS_TOLERANCE)
     return 1.0;
   else if(cosAngle < -1.0 || (cosAngle+1) < LEGAL_COS_TOLERANCE)
     return -1.0;
   return cosAngle;
 }

 double CSkeletonElement::cosCornerAngleSquared(int fid, int cid) const {
   Coord x[4];
   positionPointer(x);
   int *facePtIds = vtkTetra::GetFaceArray(fid);
   Coord s0 = x[facePtIds[(cid+2)%3]] - x[facePtIds[cid]];
   Coord s1 = x[facePtIds[(cid+1)%3]] - x[facePtIds[cid]];
   double dist02 = norm2(s0);
   double dist12 = norm2(s1);
   double sdots = dot(s0, s1);
   double cos2 = sdots*sdots/(dist02*dist12);
   if(cos2 > 1.0 || (1-cos2) < LEGAL_COS2_TOLERANCE) {
     return 1.0;
   }
   if(cos2 < -1.0 || (cos2+1) < LEGAL_COS2_TOLERANCE)
     return -1.0;
   return cos2;
 }

 double CSkeletonElement::solidCornerAngle(int corner) const {
   // We want to be able to use the sign to determine whether the solid
   // angle is above or below pi, so we must order the three other
   // points such that the norm of the face they define points out.
   // The formula is from Oosterom and Strackee (IEEE
   // Trans. Biom. Eng., Vol BME-30, No 2, 1983) and gives the tangent
   // of half of the solid angle.
   Coord c = (*nodes)[corner]->position();
   int *ptIds = vtkTetra::GetFaceArray(oppFace[corner]);
   Coord x;
   Coord n;
   Coord s[3];
   for(int i = 0; i<3; i++) {
     x = (*nodes)[ptIds[i]]->position();
     s[i] = x-c;
     n[i] = sqrt(norm2((s[i])));
   }
   x = cross(s[1],s[2]);
   double triple = dot(s[0],x);
   double d0 = dot(s[1],s[2]);
   double d1 = dot(s[0],s[2]);
   double d2 = dot(s[0],s[1]);
   // we take the arctangent here because tangents of angles are no
   // good for comparison.
   double tanhalf = triple/(n[0]*n[1]*n[2]+d0*n[0]+d1*n[1]+d2*n[2]);
   if(tanhalf >= 0)
     return 2*atan(tanhalf);
   else
     return 2*(M_PI-atan(tanhalf));
 } 

 double CSkeletonElement::cosDihedralAngle(int face1, int face2) const {
   Coord n1;
   Coord n2;
   Coord x[4];
   for(int i=0; i<4; ++i)
     x[i] = (*nodes)[i]->position();
   int *ptIds = vtkTetra::GetFaceArray(face1);
   vtkTriangle::ComputeNormal(x[ptIds[0]].xpointer(),
			      x[ptIds[1]].xpointer(),
			      x[ptIds[2]].xpointer(),
			      n1.xpointer());
   ptIds = vtkTetra::GetFaceArray(face2);
   vtkTriangle::ComputeNormal(x[ptIds[0]].xpointer(),
			      x[ptIds[1]].xpointer(),
			      x[ptIds[2]].xpointer(),
			      n2.xpointer());
   double cosAngle = - dot(n1,n2);  
   if(cosAngle > 1.0 || (1-cosAngle) < LEGAL_COS_TOLERANCE)
     return 1.0;
   else if(cosAngle < -1.0 || (cosAngle+1) < LEGAL_COS_TOLERANCE)
     return -1.0;
   return cosAngle;
 }

 bool CSkeletonElement::illegal() const {
   if(volume() <= 0)
     return true;
   for(int i=0; i<4; ++i) {
     for(int j=0; j<3; ++j) {
       double cos = cosCornerAngleSquared(i,j);
       if(cos == 1 || cos == -1) {
	 return true;
       }
     }
   }
   for(int i=0; i<4; ++i) {
     for(int j=0; j<i; ++j) {
       double cos = cosDihedralAngle(i, j);
       if(cos == 1 || cos == -1) {
	 return true;
       }
     } 
   }
   return false;
 }

 // Suspect elements are almost illegal. They cannot be refined
 // reliably such that the resulting elements are legal and therefore
 // must be eliminated from skeleton modifications. Users should be
 // alerted to their presence so that they can correct them.
 bool CSkeletonElement::suspect() const {
   for(int i=0; i<4; ++i) {
     for(int j=0; j<3; ++j) {
       double cos = cosCornerAngleSquared(i,j);
       if( 1-cos < SUSPECT_COS2_TOLERANCE || 1+cos < SUSPECT_COS2_TOLERANCE )
	 return true;
     }
   }
   for(int i=0; i<4; ++i) {
     for(int j=0; j<i; ++j) {
       double cos = cosDihedralAngle(i, j);
       if( 1-cos < SUSPECT_COS_TOLERANCE || 1+cos < SUSPECT_COS_TOLERANCE )
	 return true;
     } 
   }
   return false;
 }

 // Useful for debugging.
 void CSkeletonElement::printAngles() const {
   oofcerr << "corner angles: " << std::endl;
   for(int i=0; i<4; ++i) {
     for(int j=0; j<3; ++j) {
       double cos = cosCornerAngleSquared(i,j);
       oofcerr << i << " " << j << " " << cos << " " << (1-cos) << " "
		 << (cos+1) << std::endl;
     }
   }
   oofcerr << "dihedral angles: " << std::endl;
   for(int i=0; i<4; ++i) {
     for(int j=0; j<i; ++j) {
       double cos = cosDihedralAngle(i, j);
       oofcerr << i << " " << j << " " << cos << " " << (1-cos) << " "
		 << (cos+1) << std::endl;
     } 
   }
 }


 CSkeletonMultiNodeKey CSkeletonElement::getSegmentKey(int segidx) const {
   return CSkeletonMultiNodeKey(getSegmentNode(segidx,0),
				getSegmentNode(segidx,1));
 }

 CSkeletonMultiNodeKey CSkeletonElement::getFaceKey(int faceidx) const {
   return CSkeletonMultiNodeKey(getFaceNode(faceidx,0),
				getFaceNode(faceidx,1),
				getFaceNode(faceidx,2));
 }


 void CSkeletonElement::findHomogeneityAndDominantPixel(
						const CMicrostructure *MS)
   const 
 {
   // oofcerr << "CSkeletonElement::findHomogeneityAndDominantPixel: el="
   // 	  << getUid() << " hd="
   // 	  << homogeneity_data.timestamp() << " ms=" 
   // 	  << MS->getTimeStamp()
   // 	  << std::endl;
   // writeDebugFile("computing el=" + to_string(getUid()) +
   // 		 " hd=" + to_string(homogeneity_data.timestamp()) + 
   // 		 " nodes=");
   // for(unsigned int i=0; i<nodes->size(); ++i)
   //   writeDebugFile(" " + to_string((*nodes)[i]->getUid()) +
   // 		   " " + to_string((*nodes)[i]->nodemoved));

   if(homogeneity_data.timestamp() > MS->getTimeStamp()) {
     bool uptodate = true;
     // oofcerr << "CSkeletonElement::findHomogeneityAndDominantPixel: el="
     // 	      << getUid() << " nodes= ";
     for(unsigned int i=0; i<nodes->size(); ++i) {
       // oofcerr << (*nodes)[i]->getUid() << " " << (*nodes)[i]->nodemoved
       // 		<< " ";
       if(homogeneity_data.timestamp() < (*nodes)[i]->nodemoved) {
	 uptodate=false;
	 break;
       }
     }
     // writeDebugFile(uptodate? " up-to-date\n" : " out-of-date\n");
     if(uptodate) {
       return;    
     }
   } // end homogeneity timestamp > microstructure timestamp
   // else
   //   writeDebugFile(" out-of-date\n");

   homogeneity_data.set_value(c_homogeneity(MS));
 }

 HomogeneityData CSkeletonElement::c_homogeneity(const CMicrostructure *MS)
   const 
 {
   if(illegal()) {
     // oofcerr << "CSkeletonElement::c_homogeneity: illegal!" << std::endl;
     // writeDebugFile("illegal element " + to_string(getUid()) + "\n");
     return HomogeneityData(0, UNKNOWN_CATEGORY);
   }

   // If the element is suspect, there's not much point in doing the
   // homogeneity calculation. We set the homogeneity to something a
   // little worse than the worst possible homogeneity that can occur
   // naturally, but not 0.
   if(suspect()) {
     // writeDebugFile("suspect element " + to_string(getUid()) + "\n");
     // oofcerr << "CSkeletonElement::c_homogeneity: suspect!" << std::endl;
     return HomogeneityData(1.0/(MS->nCategories()+1), UNKNOWN_CATEGORY);
   }

   // writeDebugFile("computing homogeneity for element "+to_string(getUid())+"\n");
   // oofcerr << "CSkeletonElement::c_homogeneity: computing element " << getUid()
   // 	  << ":";

   double maxvolume = 0;
   double totalVolume = 0;
   double elvol = volumeInVoxelUnits(MS);
   int category = 0;

   const DoubleVec *volumes = categoryVolumes(MS);

   for(DoubleVec::size_type i=0; i<volumes->size(); ++i) {
     double volume = (*volumes)[i];
     // oofcerr << " " << volume;
     totalVolume += volume;
     if(volume > maxvolume) {
       maxvolume = volume;
       category = i;
     }
   }
   // oofcerr << std::endl;

 // #ifdef DEBUG
 //    if( fabs(totalVolume-elvol)/elvol > 1e-2 && elvol > 1e-2 ) {  
 //      oofcerr << "invalid total volume" << std::endl;
 //      for(DoubleVec::size_type i=0;i<volumes->size();++i)
 //        oofcerr << i << " " << (*volumes)[i] << std::endl;
 //      oofcerr << totalVolume << " " << elvol << " " << fabs(totalVolume-elvol)/elvol << std::endl;
 //      oofcerr << energyShape() << " " << suspect() << std::endl;
 //      oofcerr << "POINTS:" << std::endl;
 //      double pt[3];
 //      for(int i=0; i<4; i++){
 //        (*nodes)[i]->position(pt);
 //        oofcerr << pt[0] << " " << pt[1] << " " << pt[2] << std::endl;
 //      }
 //      oofcerr << std::endl;
 //      throw ErrProgrammingError("Invalid total volume.", __FILE__, __LINE__);
 //    }
 // #endif

   double homogeneity = maxvolume/elvol;
   // oofcerr << "CSkeletonElement::c_homogeneity: uid=" << getUid()
   // 	    << " h=" << homogeneity << std::endl;
   delete volumes;

   if(homogeneity > 1.0)
     homogeneity = 1.0;
   return HomogeneityData(homogeneity, category);
 }


 // It is convenient to store some topological information which all
 // tets share in static variables.  This can save us some expensive
 // GetEdge or GetFace calls.  Other information is available in static
 // member functions of vtkTetra, specifically,
 // vtkTetra::GetEdgeArray(int) returns a pointer with two point ids
 // defining an edge.  vtkTetra::GetFaceArray(int) returns the point
 // ids defining a face.

 int *CSkeletonElement::getEdgeArray(int i) { // static method
   return vtkTetra::GetEdgeArray(i);
 }

 int *CSkeletonElement::getFaceArray(int i) { // static method
   return vtkTetra::GetFaceArray(i);
 }

 void CSkeletonElement::getElements(const CSkeletonBase*,
				    ConstCSkeletonElementVector &result)
   const
 {
   result.clear();
   result.push_back(this);
 }

 void CSkeletonElement::getElements(const CSkeletonBase*,
				    CSkeletonElementVector &result)
 {
   result.clear();
   result.push_back(this);
 }

 /*
    BEGIN TETRAHEDRON TOPOLOGY INFO
 */

 // TODO 3.1: These should be updated when we separate the CSkeletonElement
 // types.

 // Maps the edge ids at the face scope to edge ids at the tet scope.
 const int CSkeletonElement::faceEdges[4][3] = {{0,4,3},
						{1,5,4},
						{2,3,5},
						{2,1,0}};

 // The direction of an edge is defined at the tet scope and given by
 // the order of the node indices returned by
 // vtkTetra::GetEdgeArray. However the order of the nodes returned by
 // vtkTetra::GetFaceArray is such that the norm of the face points
 // outward and may differ from the ordering of nodes making up the
 // edges at the tet scope. This gives the relative sign of the edge
 // direction at the face scope compared to the direction at the tet
 // scope. That is, tet edge 2 is defined as node 2 to node 0 at the
 // tet scope however for face 3, in order for the edges to be defined
 // in a way such that the normal points out, this edge is directed
 // from node 0 to node 2.
 const int CSkeletonElement::faceEdgeDirs[4][3] = {{1,1,-1},
						   {1,1,-1},
						   {1,1,-1},
						   {-1,-1,-1}};

 // This is the inverse of faceEdgeDirs.
 const int CSkeletonElement::edgeFaceDirs[6][4] = {{ 1, 0, 0,-1}, // edge 0
						   { 0, 1, 0,-1}, // edge 1
						   { 0, 0, 1,-1}, // edge 2
						   {-1, 0, 1, 0}, // edge 3
						   { 1,-1, 0, 0}, // edge 4
						   { 0, 1,-1, 0}};// edge 5

 // Maps an edge index to the two faces it separates.
 const int CSkeletonElement::edgeFaces[6][2] = {{0,3},
						{1,3},
						{2,3},
						{0,2},
						{0,1},
						{1,2}};

 // Gives the face between two edges.
 const int CSkeletonElement::edgeEdgeFace[6][6] = {{-1, 3, 3, 0, 0, -1}, 
						   {3, -1, 3, -1, 1, 1},
						   {3, 3, -1, 2, -1, 2},
						   {0, -1, 2, -1, 0, 2},
						   {0, 1, -1, 0, -1, 1},
						   {-1, 1, 2, 2, 1, -1}};

 // Gives the face between an edge and a node.
 const int CSkeletonElement::nodeEdgeFace[4][6] = {{-1, 3, -1, -1, 0, 2},
						   {-1, -1, 3, 0, -1, 1},
						   {3, -1, -1, 2, 1, -1},
						   {0, 1, 2, -1, -1, -1}};

 // Gives the edge between two faces.
 const int CSkeletonElement::faceFaceEdge[4][4] = {{-1, 4, 3, 0},
						   {4, -1, 5, 1},
						   {3, 5, -1, 2},
						   {0, 1, 2, -1}};

 // Gives the face opposite a node -- that is the only face that the
 // given node is not a part of.
 const int CSkeletonElement::oppFace[4] = {1,2,0,3};

 // Gives the node opposite a face -- inverse of oppFace
 const int CSkeletonElement::oppNode[4] = {2,0,1,3};

 // Maps an edge id to the opposite edge id -- the only edge that the
 // given edge is not connected to. This map is its own inverse.
 const int CSkeletonElement::oppEdge[6] = {5,3,4,1,2,0};

 // Maps a node to the three faces it is on.
 const int CSkeletonElement::nodeFaces[4][3] = {{0,2,3},
						{0,1,3},
						{1,2,3},
						{0,1,2}};

 // Maps a node to the three edges it is on.
 const int CSkeletonElement::nodeEdges[4][3] = {{0,2,3},
						{0,1,4},
						{1,2,5},
						{3,4,5}};

 // Gives the edge between two nodes.
 const int CSkeletonElement::nodeNodeEdge[4][4] = {{-1,0,2,3},
						   {0,-1,1,4},
						   {2,1,-1,5},
						   {3,4,5,-1}};

 // Gives the parametric coordinate of the node for the edge given above.
 const double CSkeletonElement::nodeEdgeParam[4][3] = {{0.0, 1.0, 0.0},
						       {1.0, 0.0, 0.0}, 
						       {1.0, 0.0, 0.0},
						       {1.0, 1.0, 1.0}};

 /*
      END TETRAHEDRA TOPOLOGY INFO

      BEGIN HELPER FUNCTIONS FOR CATEGORY VOLUMES
 */

 // Sorting function for TetIntersectionPoints used for finding the convex hull.
 bool operator<(const TetIntersectionPoint &tp1, const TetIntersectionPoint &tp2)
 {
   if(tp1.tan<tp2.tan)
     return true;
   // if the angles are the same, the closer point is first
   if(tp1.tan==tp2.tan && tp1.dist2<tp2.dist2)
     return true;
   return false;
 }

 // Given two TetIntersectionPoint objects, determine which face the
 // line in between represents. The TetIntersectionPoints may or may
 // not coincide with tet nodes. This is used by convexPolyIntersection
 // to set the face id for the intersection point.
 int getFaceBetweenTetPoints(const TetIntersectionPoint &tp0,
			     const TetIntersectionPoint &tp1)
 {
   int faceId = -1;
   if(tp0.edge != -1 && tp1.edge != -1)
     faceId = CSkeletonElement::edgeEdgeFace[tp0.edge][tp1.edge];
   else if(tp0.node != -1 && tp1.node == -1) 
     faceId = CSkeletonElement::nodeEdgeFace[tp0.node][tp1.edge];
   else if(tp0.node == -1 && tp1.node != -1)
     faceId = CSkeletonElement::nodeEdgeFace[tp1.node][tp0.edge];
   else {
     // If both TetIntersectionPoints coincide with nodes, there are
     // two possibilities, but it's arbitrary which one we return
     // because in this case, the edge id (calculated elsewhere) will
     // be the pertinent topological information.
     int edge = CSkeletonElement::nodeNodeEdge[tp0.node][tp1.node];
     faceId = CSkeletonElement::edgeFaces[edge][0];
   }
   if(faceId == -1) {
 #ifdef DEBUG
     oofcerr << tp0.edge << " " << tp0.node << " " << tp0.t << std::endl;
     oofcerr << tp1.edge << " " << tp1.node << " " << tp1.t << std::endl;
 #endif // DEBUG
     throw ErrProgrammingError("CSkeletonElement: could not determine face id",
			       __FILE__, __LINE__);
   }
   return faceId;
 }


 #define TINY 10e-20

 // Convert a looseEnd to a tet edge intersection.
 static void looseEndToEdgeIntersection(const Coord &x, double t, 
					int edgeId, int faceId,
					CellEdge &elementEdgeData, 
					IntersectionCategory type)
 {
   // CellEdgeMap maps a parametric edge coord to a
   // VoxelBdyIntersection object.
   // CellEdge is a vector of CellEdgeMaps, one for each edge of a tet.
   // CellEdgeDatum is the value_type for CellEdgeMap.

   CellEdgeMap::iterator it = elementEdgeData[edgeId].find(t);
   if(it == elementEdgeData[edgeId].end()) {
     bool found = false;
     for(CellEdgeMap::iterator it1 = elementEdgeData[edgeId].begin();
	 it1 != elementEdgeData[edgeId].end(); ++it1) // and !found?
       {
	 // A tolerance is necessary here in order to to prevent
	 // intersections that are within roundoff but out of order when we
	 // add them because of the loose ends. Check if there is a point
	 // within tolerance of the new point. If so, this intersection's
	 // type will be altered accordingly.
	 double dist2 = norm2(x - (*it1).second.location);
	 if(dist2 < TINY) {
	   found = true;
	   it = it1;
	 }
       }
     // If there is no intersection within TINY, add one.
     if(!found) {
       int face0 = CSkeletonElement::edgeFaces[edgeId][0];
       int face1 = CSkeletonElement::edgeFaces[edgeId][1];
       VoxelBdyIntersection vxlbdyint(x[0], x[1], x[2], face0, face1);
       vxlbdyint.addType(faceId, type);
       // Use insert() instead of elementEdgeData[edgeId][t] = vxlbdyint
       // because VoxelBdyIntersection doesn't have a default constructor.
       elementEdgeData[edgeId].insert(CellEdgeDatum(t, vxlbdyint));
     }
   }
   else
     (*it).second.addType(faceId, type);

   // std::pair<CellEdgeMap::iterator, bool> it;
   // it.first = elementEdgeData[edgeId].find(t);
   // if(it.first == elementEdgeData[edgeId].end()) {
   //   // A tolerance is necessary here in order to to prevent
   //   // intersections that are within roundoff but out of order when we
   //   // add them because of the loose ends. Check if there is a point
   //   // within tolerance of the new point. If so, this intersection's
   //   // type will be altered accordingly.
   //   double dist2;
   //   bool found = false;
   //   for(CellEdgeMap::iterator it1 = elementEdgeData[edgeId].begin(); 
   // 	it1 != elementEdgeData[edgeId].end(); ++it1)
   //     {
   // 	//double y[3];
   // 	//(*it1).second.location.writePointer(y);
   // 	dist2 = norm2(x - (*it1).second.location);
   // 	if(dist2 <= TINY) {
   // 	  found = true;
   // 	  //oofcerr << "found close point" << std::endl;
     // 	  it.first = it1;
  // 	}
  //     }
  //   // If there is no intersection within TINY, add one.
  //   if(!found) {
  //     int face0 = CSkeletonElement::edgeFaces[edgeId][0];
  //     int face1 = CSkeletonElement::edgeFaces[edgeId][1];
  //     it = elementEdgeData[edgeId].insert(
  // 	  CellEdgeDatum(t, VoxelBdyIntersection(x[0],x[1],x[2],face0,face1)));
  //   }
  // }
  // (*it.first).second.addType(faceId,type);
}

// Add an edge intersection to the elementEdgeData and set its type.
static void addIntersectionToEdgeData(
		      Coord x, double t, int edgeId, int faceId, 
		      const std::vector<Coord> &epts,
		      CellEdge &elementEdgeData,
		      const Quad *q,
		      IntersectionCategory type=UNCATEGORIZED_INTERSECTION,
		      bool print = false)
{
// #ifdef DEBUG  
//   assert(Quad::validQuad(q));
//   if(print) {
//     oofcerr << "addIntersectionToEdgeData: q=" << q << std::endl;
//   }
// #endif  // DEBUG
  // Check whether the intersection point is already in elementEdgeData.
  CellEdgeMap::iterator it = elementEdgeData[edgeId].find(t);
  if(it == elementEdgeData[edgeId].end()) {
    // It's not there.  Add it.
    int face0 = CSkeletonElement::edgeFaces[edgeId][0];
    int face1 = CSkeletonElement::edgeFaces[edgeId][1];
    VoxelBdyIntersection vxlbdyint(x[0], x[1], x[2], face0, face1);
    std::pair<CellEdgeMap::iterator, bool> insertion =
      elementEdgeData[edgeId].insert(CellEdgeDatum(t, vxlbdyint));
    it = insertion.first;
  }

  // Determine the intersection type from the dot product of the quad
  // norm and the tet face norm. If the dot product is negative, it is
  // an exit. If it's positive, it's an entrance.
  int *ptIds = vtkTetra::GetEdgeArray(edgeId);
  double dot = q->norm*(epts[ptIds[1]][q->norm_dir] -
			epts[ptIds[0]][q->norm_dir]);

  // Set the intersection type.
  if((CSkeletonElement::edgeFaceDirs[edgeId][faceId]*dot<0 && type == 0) ||
     type == EXIT_INTERSECTION)
    {
      // (*it).second is a VoxelBdyIntersection
      (*it).second.addExit(faceId);
    }
  else if((CSkeletonElement::edgeFaceDirs[edgeId][faceId]*dot>0 && type == 0) ||
	  type == ENTRANCE_INTERSECTION)
    {
      (*it).second.addEntrance(faceId);
    }
// #ifdef DEBUG
//   if(print)
//     oofcerr << "addIntersectionToEdgeData: done" << std::endl;
// #endif // DEBUG

  // std::pair<CellEdgeMap::iterator, bool> it;
  // // Check whether the intersection point is already in elementEdgeData.
  // it.first = elementEdgeData[edgeId].find(t);
  // // If not, add it.
  // // oofcerr << "addIntersectionToEdgeData: got it.first" << std::endl;
  // if(it.first == elementEdgeData[edgeId].end()) {
  //   int face0 = CSkeletonElement::edgeFaces[edgeId][0];
  //   int face1 = CSkeletonElement::edgeFaces[edgeId][1];
  //   it = elementEdgeData[edgeId].insert(
  // 	CellEdgeDatum(t,VoxelBdyIntersection(x[0],x[1],x[2],face0,face1)));
  // }

  // // Determine the intersection type from the dot product of the quad
  // // norm and the tet face norm. If the dot product is negative, it is
  // // an exit. If it's positive, it's an entrance.
  // int *ptIds = vtkTetra::GetEdgeArray(edgeId);
  // double dot = q->norm*(epts[ptIds[1]][q->norm_dir] -
  // 			epts[ptIds[0]][q->norm_dir]);

  // // Set the intersection type.
  // if((CSkeletonElement::edgeFaceDirs[edgeId][faceId]*dot<0 && type == 0) ||
  //    type == EXIT_INTERSECTION)
  //   {
  //     // (*it.first).second is a VoxelBdyIntersection
  //     (*it.first).second.addExit(faceId);
  //   }
  // else if((CSkeletonElement::edgeFaceDirs[edgeId][faceId]*dot>0 && type == 0) ||
  // 	  type == ENTRANCE_INTERSECTION)
  //   {
  //     (*it.first).second.addEntrance(faceId);
  //   }
}

// Distance squared between two 2D points.
double dist2BetweenPoints2D(double x[2], double y[2]) {
  double a = y[0]-x[0];
  double b = y[1]-x[1];
  return a*a+b*b;
}

// Sort TetIntersectionPoints in place into CCW convex hull.
void convexHull(TetIntersectionPoints &tetPoints) {

  // Find the pivot -- the point with the lowest horizontal coordinate
  // (and lowest vertical coordinate in the case of a tie).
  TetIntersectionPoints::iterator pivot = tetPoints.begin();
  for(TetIntersectionPoints::iterator here=tetPoints.begin(); here!=tetPoints.end(); ++here) {
    if((*here).x[0] < (*pivot).x[0]) 
      pivot = here;
    if((*here).x[0] == (*pivot).x[0] 
       && (*here).x[1] < (*pivot).x[1])
      pivot = here;
  }

  // Set the value of the tangent of the angle from the
  // horizontal axis and distance to the pivot.
  for(TetIntersectionPoints::iterator here=tetPoints.begin(); here!=tetPoints.end(); ++here) {
    if(here==pivot) {
      // Set this so that the pivot is first when HullPoints is sorted.
      (*here).tan = -1*HUGE_VAL;
      (*here).dist2 = 0;
    }
    else {
      if(((*here).x[0]-(*pivot).x[0]) != 0)
	(*here).tan = ((*here).x[1]-(*pivot).x[1])/((*here).x[0]-(*pivot).x[0]);
      else
	(*here).tan = HUGE_VAL;
      (*here).dist2 = dist2BetweenPoints2D((*here).x,(*pivot).x); 
    }
  }

  // This uses the operator< defined above
  std::sort(tetPoints.begin(), tetPoints.end());

  // We know it's convex already because it is the intersection of a
  // tet with a plane, so we don't need this step.
//   HullPoints sortedHull;
//   sortedHull.push_back(hullPoints[0]);
//   sortedHull.push_back(hullPoints[1]);
//   for(int l=2; l<hullPoints.size(); ++l) {
//     while(sortedHull.size() >=2 && 
// 	  (sortedHull.back().x[0]-(*(sortedHull.end()-2)).x[0]) *
// 	  (hullPoints[l].x[1]-sortedHull.back().x[1]) -
// 	  (hullPoints[l].x[0]-sortedHull.back().x[0]) *
// 	  (sortedHull.back().x[1]-(*(sortedHull.end()-2)).x[1]) < 0) {
//       sortedHull.pop_back();
//     }
//     sortedHull.push_back(hullPoints[l]);
//   }
}

// Various 2D cross product helpers
static double cross2D(const double O[2], const double A[2], const double B[2]) {
  return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0]);
}

static double cross2D(const int O[2], const int A[2], const double B[2]) {
  return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0]);
}

static double cross2D(const double O[2], const double A[2], const int B[2]) {
  return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0]);
}

// double cross2D(const double O[3], const double A[3], const int B[2], int c) {
//   return (A[VoxelSetBoundary::proj_dirs[c][0]]-O[VoxelSetBoundary::proj_dirs[c][0]]) * 
//     (B[1]-O[VoxelSetBoundary::proj_dirs[c][1]]) - 
//     (A[VoxelSetBoundary::proj_dirs[c][1]]-O[VoxelSetBoundary::proj_dirs[c][1]]) * 
//     (B[0]-O[VoxelSetBoundary::proj_dirs[c][0]]);
// }

// double cross2D(const int O[2], const int A[2], const double B[3], int c) {
//   return (A[0]-O[0])*(B[VoxelSetBoundary::proj_dirs[c][1]]-O[1]) - 
//     (A[1]-O[1])*(B[VoxelSetBoundary::proj_dirs[c][0]]-O[0]);
// }

// These values are used in convexPolyIntersection to describe the
// state of the poly-poly traversal. PIN means the tet point was
// "inside" after the most recent intersection. QIN means the quad
// point was "inside" after the most recent intersection.
enum PolyTraversalState {UNKNOWN, PIN, QIN};

// These values classify seg-seg intersections and are used by
// convexPolyIntersection.
enum SegSegIntersectionType {NO_INTERSECTION, SIMPLE_INTERSECTION,
			     VERTEX_INTERSECTION, PARALLEL_INTERSECTION};

// This converts a TetIntersectionPoint to an IntersectionPoint,
// adding the necessary topological information.

IntersectionPoint *iPointFromTetPoint(const TetIntersectionPoint &tp, 
				      int c, int l) 
{
  IntersectionPoint *ip = new IntersectionPoint();
  ip->x[VoxelSetBoundary::proj_dirs[c][0]] = tp.x[0];
  ip->x[VoxelSetBoundary::proj_dirs[c][1]] = tp.x[1];
  ip->x[c] = (double)l;
  if(tp.node != -1) { 
    for(int i=0; i<3; ++i) {
      int edgeId = CSkeletonElement::nodeEdges[tp.node][i];
      int *ptIds = vtkTetra::GetEdgeArray(edgeId);
      ip->edges[edgeId] = true;
      ip->t[edgeId] = (tp.node == ptIds[0] ? 0.0 : 1.0);
      ip->faces[CSkeletonElement::nodeFaces[tp.node][i]] = true;
    }
  }
  else {
    ip->edges[tp.edge] = true;
    ip->faces[CSkeletonElement::edgeFaces[tp.edge][0]] = true;
    ip->faces[CSkeletonElement::edgeFaces[tp.edge][1]] = true;
    ip->t[tp.edge] = tp.t;
  }
  return ip;
}

// This creates a hash value of a quad edge represented by a 2D
// integer point and a Cartesian axis.
int hash(int x, int y, int dir) {
  int corned_beef = 0x345678;
  corned_beef ^= dir;
  corned_beef *= 1000003;
  corned_beef ^= x;
  corned_beef *= 1000003;
  corned_beef ^= y;
  return corned_beef;
}


// Is ip on an edge.
bool iPointOnEdge(IntersectionPoint *ip) {
  return (ip->edges[0] || ip->edges[1] || ip->edges[2] ||
	  ip->edges[3] || ip->edges[4] || ip->edges[5]);
}

// Is ip on a face, not on edge.
bool iPointOnFace(IntersectionPoint *ip) {
  return ((ip->faces[0] || ip->faces[1] || ip->faces[2] || ip->faces[3])
	  && !iPointOnEdge(ip));
}

int iPointNumFaces(IntersectionPoint *ip) {
  return (int(ip->faces[0]) + int(ip->faces[1]) + int(ip->faces[2]) +
	  int(ip->faces[3]));
}

// For two points that have been found to be identical, merge the
// topological information.
bool mergeTopologicalInfo(IntersectionPoint *ip1, IntersectionPoint *ip2,
			  bool sameFace, 
			  const std::vector<Coord> &epts)
{
  int i,k;
  bool changed = false; 
  for(i=0; i<NUM_TET_FACES; ++i) {
    if(ip1->faces[i] != ip2->faces[i]) changed = true;
    ip1->faces[i] |= ip2->faces[i];
    ip2->faces[i] |= ip1->faces[i];
  }

  for(i=0; i<NUM_TET_EDGES; ++i) {
    if(ip1->edges[i] != ip2->edges[i]) changed = true;
    if(ip1->edges[i] && !ip2->edges[i])
      ip2->t[i] = ip1->t[i];
    else if(ip2->edges[i] && !ip1->edges[i])
      ip1->t[i] = ip2->t[i];
    ip1->edges[i] |= ip2->edges[i];
    ip2->edges[i] |= ip1->edges[i];
  }

  int numFaces = iPointNumFaces(ip1);
  // If the points are now on two faces but does not have an
  // edge flag set, add the correct edge flag.
  if(changed && numFaces == 2 && !iPointOnEdge(ip1)) {
    int face1 = -1, face2 = -1;
    for(k = 0; k < NUM_TET_FACES; ++k) {
      if(ip1->faces[k]) {
	if(face1 == -1)
	  face1 = k;
	else 
	  face2 = k;
      }
    }
    int edge = CSkeletonElement::faceFaceEdge[face1][face2];
    ip1->edges[edge] = ip2->edges[edge] = true;
    // Set t
    int *ptIds = vtkTetra::GetEdgeArray(edge);
    double l[3];
    for(i=0; i<3; ++i)
      l[i] = fabs(epts[ptIds[1]][i]-epts[ptIds[0]][i]);
    if(l[0] >= l[1] && l[0] >= l[2])
      ip1->t[edge] = ip2->t[edge] = fabs(ip1->x[0] - epts[ptIds[0]][0]) / l[0];
    else if(l[1] >= l[0] && l[1] >= l[2])
      ip1->t[edge] = ip2->t[edge] = fabs(ip1->x[1] - epts[ptIds[0]][1]) / l[1];
    else
      ip1->t[edge] = ip2->t[edge] = fabs(ip1->x[2] - epts[ptIds[0]][2]) / l[2];
  }

  if(sameFace) {
    // in other cases, they will already have the same hash
    if(ip1->corner && !ip2->corner) {
      for(i=0; i<3; ++i)
	ip2->hash[i] = ip1->hash[i];
      ip2->corner = true;
    }
    if(ip2->corner && !ip1->corner) {
      for(i=0; i<3; ++i) 
	ip1->hash[i] = ip2->hash[i];
      ip1->corner = true;
    }
  }
  return changed;
} // end mergeTopologicalInfo
 
// Two Intersection Points are duplicates if they have exactly the
// same coordinates or if they constitute a hash collision.  For a
// hash collision to occur, both points must be on the same face, and
// neither must be on on edge since edge points don't have hashes.  If
// they are duplicates, their topological and hash information is
// merged.  A value of -1 is passed for c when comparing two points
// that are not necessarily part of the same axis aligned plane. In
// this case, don't check the coordinates.
static bool isDupe(IntersectionPoint *ip1, IntersectionPoint *ip2,
		   Coord fnormal[4], int c, bool print, 
		   const std::vector<Coord> &epts) 
{
  bool sameFace = false, sameEdge = false, diffEdges = false;
  int i, faceId = -1, edgeId = -1;
// #ifdef DEBUG
//   if(print) {
//     oofcerr << "isDupe: check if dupe " << *ip1 << " " << *ip2 << std::endl;
//   }
// #endif // DEBUG

  // Check faces.
  for(i=0; i<NUM_TET_FACES; ++i) {
    if(ip1->faces[i] && ip2->faces[i]) {
      sameFace = true;
      faceId = i;
      break;
    }
  }
// #ifdef DEBUG
//   if(print) oofcerr << "isDupe: sameface " << sameFace << " " << faceId 
// 		    << std::endl;
// #endif // DEBUG

  // Check edges.
  for(i=0; i<NUM_TET_EDGES; ++i) {
    if(ip1->edges[i] && ip2->edges[i]) {
      sameEdge = true;
      edgeId = i;
      break;
    }
  }

// #ifdef DEBUG
//   if(print) {
//     oofcerr << "isDupe: sameedge " << sameEdge << " " << edgeId << " " 
// 	    << ip1->t[edgeId] << " " << ip2->t[edgeId] << std::endl;
//     if(sameFace)
//       oofcerr << "isDupe: hashes= " << ip1->hash[0] << " " << ip2->hash[0]
// 	      << std::endl;
//   }
// #endif // DEBUG
  if(sameEdge)
    return (ip1->t[edgeId] == ip2->t[edgeId]);
  
  if(sameFace && !sameEdge) {
    if( (ip1->edges[CSkeletonElement::faceEdges[faceId][0]] || 
	 ip1->edges[CSkeletonElement::faceEdges[faceId][1]] || 
	 ip1->edges[CSkeletonElement::faceEdges[faceId][2]]) &&
	(ip2->edges[CSkeletonElement::faceEdges[faceId][0]] || 
	 ip2->edges[CSkeletonElement::faceEdges[faceId][1]] || 
	 ip2->edges[CSkeletonElement::faceEdges[faceId][2]]) )
      diffEdges = true;
  }

// #ifdef DEBUG
//   if(print) 
//     oofcerr << "isDupe: sameFace, sameEdge, diffEdges "
// 	    << sameFace << sameEdge << diffEdges
// 	    << (ip1->hash[0] == ip2->hash[0]) << (ip1->hash[0]==0) << std::endl;
// #endif	// DEBUG

  // check coordinates.
  if(c != -1) {
    if(ip1->x[VoxelSetBoundary::proj_dirs[c][0]] == 
       ip2->x[VoxelSetBoundary::proj_dirs[c][0]] &&
       ip1->x[VoxelSetBoundary::proj_dirs[c][1]] == 
       ip2->x[VoxelSetBoundary::proj_dirs[c][1]]) 
      {
	mergeTopologicalInfo(ip1, ip2, sameFace, epts);
	return true;
      }
// #ifdef DEBUG
//     if(print) {
//       oofcerr << "isDupe: not same coordinates "
// 	      << (ip1->x[VoxelSetBoundary::proj_dirs[c][0]] -
// 		  ip2->x[VoxelSetBoundary::proj_dirs[c][0]]) << " "
// 	      << (ip1->x[VoxelSetBoundary::proj_dirs[c][1]] -
// 		  ip2->x[VoxelSetBoundary::proj_dirs[c][1]]) << std::endl;
//     }
// #endif // DEBUG
  }

  if(!sameFace || diffEdges || ip1->hash[0] == 0 || ip2->hash[0] == 0)
    return false;
  
// #ifdef DEBUG
//   if(print)
//     oofcerr << "isDupe: face " << faceId << " normal " << fnormal[faceId][0]
// 	    << " " << fnormal[faceId][1] << " " << fnormal[faceId][2] 
// 	    << std::endl;
// #endif // DEBUG

  // Check for simple hash collision for non-corners.
  if(!ip1->corner && !ip2->corner) {
    if(ip1->hash[0] == ip2->hash[0]) {
      mergeTopologicalInfo(ip1, ip2, sameFace, epts);
      return true;
    }
    return false;
  }
  
  // Check for hash collisions in the case that it's a corner. It's
  // not a collision if the line that the hash is based on is parallel
  // to the plane of the face because in this case, both end points
  // could be on the face.
  bool collide;
  if(ip1->corner) {
    collide = ( (fnormal[faceId][0] != 0 && ip1->hash[0] == ip2->hash[0]) || 
		(fnormal[faceId][1] != 0 && ip1->hash[1] == ip2->hash[0]) || 
		(fnormal[faceId][2] != 0 && ip1->hash[2] == ip2->hash[0]) );
    if(collide)
      mergeTopologicalInfo(ip1, ip2, sameFace, epts);
    return collide;
  }
  
  
  // ip2->corner == true
  collide = ( (fnormal[faceId][0] != 0 && ip1->hash[0] == ip2->hash[0]) || 
	      (fnormal[faceId][1] != 0 && ip1->hash[0] == ip2->hash[1]) || 
	      (fnormal[faceId][2] != 0 && ip1->hash[0] == ip2->hash[2]) );
  if(collide)
    mergeTopologicalInfo(ip1, ip2, sameFace, epts);
  return collide;

} // end isDupe

// Add new IntersectionPoint to iPoints, checking for dupes.
static void addToIPoints(IntersectionPoint *ip, IntersectionPoints &iPoints,
			 IntersectionPoints &AllIPoints, Coord fnormal[4],
			 int c, bool print, 
			 const std::vector<Coord> &epts)
{
  // No need to check for dupes if iPoints is empty.
  if(iPoints.empty()) {
    iPoints.push_back(ip);
    AllIPoints.push_back(ip);
    return;
  }
  // If there's only one point in iPoints, just check that.
  if(iPoints.size() == 1 && !isDupe(ip, iPoints[0], fnormal, c, print, epts)) {
    iPoints.push_back(ip);
    AllIPoints.push_back(ip);
    return;
  }
  // Otherwise, check the first and last point.
  if(!isDupe(ip, iPoints.front(), fnormal, c, print, epts) &&
     !isDupe(ip, iPoints.back(), fnormal, c, print, epts)) 
    {
      iPoints.push_back(ip);
      AllIPoints.push_back(ip);
      return;
    }
// #ifdef DEBUG
//   if(print) 
//     oofcerr << "addToIPoints: Dupes!" << std::endl;
// #endif	// DEBUG
  delete ip;
} // end addToIPoints()

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// #ifdef DEBUG
// static void checkLooseEnds(const std::vector<FaceIntersectionMap> &looseEnds) {
//   for(std::vector<FaceIntersectionMap>::const_iterator i=looseEnds.begin();
//       i!=looseEnds.end(); ++i)
//     {
//       for(FaceIntersectionMap::const_iterator j=(*i).begin(); j!=(*i).end();
// 	  ++j)
// 	{
// 	  assert(Quad::validQuad((*j).second.quad));
// 	}
//     }
// }
// #endif // DEBUG

// Update the looseEnds object based on a new IntersectionPoint.
static void addToLooseEnds(IntersectionPoint *ip, IntersectionPoint *op,
			   IntersectionCategory type,
			   std::vector<FaceIntersectionMap> &looseEnds,
			   int faceId, 
			   const Coord &normal, // face normal
			   double contrib,
			   const Quad *current_quad, bool outside=false,
			   bool print=false) 
{
// #ifdef DEBUG
//   assert(Quad::validQuad(current_quad));
//   checkLooseEnds(looseEnds);
//   // if(print)
//   //   oofcerr << "addToLooseEnds: current_quad=" << current_quad << std::endl;
// #endif // DEBUG
  
  // Only add it if it's not on an edge
  if(ip->edges[CSkeletonElement::faceEdges[faceId][0]] ||
     ip->edges[CSkeletonElement::faceEdges[faceId][1]] || 
     ip->edges[CSkeletonElement::faceEdges[faceId][2]]) 
    return;
  
  bool corner = ip->corner;

// #ifdef DEBUG
//   if(print)
//     oofcerr << "addToLooseEnds: "
// 	    << ip->x[0] << "," << ip->x[1] << "," << ip->x[2]
// 	    << " corner " << ip->corner
// 	    << " type " << type << " face " << faceId << std::endl;
// #endif	// DEBUG


  FaceIntersectionMap::iterator singlematch;
  bool found = false;

  // Check for simple matches if ip is not a corner.
  if(!corner) {
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif
    // Find all matches and loop over them, checking type and corner status.
    std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator>
      matches = looseEnds[faceId].equal_range(ip->hash[0]);
    for(FaceIntersectionMap::iterator it=matches.first; it!=matches.second;
	++it)
      {
	// It's a simple match if it has the opposite type.
	if((*it).second.type != type) {
	  singlematch = it;
	  found = true;
	}
	// If a hash match is a corner, we have some updating to do
	// regardless of the type.
	if((*it).second.ip->corner) {
	  corner = true;
	  singlematch = it;
	  break;
	}
      }
  }

  // Only remove the match if it's not a corner and not
  // outside. Corners will be removed in a separate loop.
  if(found && !corner && !outside) {
// #ifdef DEBUG
//     if(print) {
//       oofcerr << "removing "
// 		<< ip->x[0] << "," << ip->x[1] << "," << ip->x[2]
// 		<< " " << ip->hash[0] << " from looseEnds " << type
// 		<< std::endl;
//     }
// #endif	// DEBUG
    looseEnds[faceId].erase(singlematch); 
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif
  }   

  else { // If either there was no match or the match was a corner.
      
    // Search for matches that aren't designated as corners and update
    // them to be corners so that everything is consistent.
    int n = (corner ? 3 : 1);
    int h[3];
    if(corner) {
      for(int i=0; i<n; ++i) {
	if(ip->corner)
	  h[i] = ip->hash[i];
	else
	  h[i] = (*singlematch).second.ip->hash[i];
      }
      if(!ip->corner) {
	ip->corner = true;
	for(int j=0; j<3; ++j)
	  ip->hash[j] = h[j];
      }
      // Loop over the possible hash values.
      for(int i=0; i<n; ++i) {
	// Find the matches for this hash value and loop over them.
	std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator>
	  matches = looseEnds[faceId].equal_range(h[i]);
	for(FaceIntersectionMap::iterator it=matches.first; it!=matches.second;
	    ++it)
	  {
	    if(!(*it).second.ip->corner) {
	      // Merge topo info and make sure each match has all
	      // three hash values.
	      (*it).second.ip->corner = true; 
	      //mergeTopologicalInfo(ip,(*it).second.ip,true);
	      for(int j=0; j<3; ++j)
		(*it).second.ip->hash[j] = h[j];
	      for(int j=0; j<3; ++j) {
// #ifdef DEBUG
// 		if(print && i!=j && normal[j] != 0)
// 		  oofcerr << "addToLooseEnds: updating non corner "
// 			  << h[j] << std::endl;
// #endif	// DEBUG
		if(i!=j && normal[j] != 0) {
		  // assert(Quad::validQuad((*it).second.quad));
		  looseEnds[faceId].insert(
				   FaceIntersectionDatum(h[j],(*it).second));
		}
	      }
	    }
	  }
      }
    } // end if(corner)
    else
      h[0] = ip->hash[0];

// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

    // Finally, add an entry for ip for each hash.
    FaceIntersection fi;
    fi.ip = ip;
    fi.op = op;
    fi.type = type;
    fi.contrib = contrib;
    fi.outside = outside;
    fi.quad = current_quad;
    fi.matches = 1;
    fi.paired = false;
    for(int i=0; i<n; ++i) {
      // Only add the value if the i-axis is not parallel to the face
      // because if the axis that the hash represents is parallel to
      // the face, multiple points on that axis could be on the face.
      if(n == 1 || normal[i] != 0) {
// #ifdef DEBUG
// 	// assert(Quad::validQuad(fi.quad));
// 	// if(print) {
// 	//   oofcerr << "addToLooseEnds: adding " << fi << std::endl;
// 	// }
// #endif // DEBUG
	looseEnds[faceId].insert(FaceIntersectionDatum(h[i],fi));
      }
    }
  }
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

} // end addToLooseEnds


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

 typedef std::vector<FaceIntersectionMap::iterator> FaceIntersectionMatches;
 typedef std::pair<int, FaceIntersectionMatches*> FaceIntersectionMatchesDatum;
 typedef std::map<int, FaceIntersectionMatches*> FaceIntersectionMatchMap;
 typedef std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator> FaceIntersectionPair;
 typedef std::vector<FaceIntersectionPair> FaceIntersectionPairVector;


// Remove matching pairs of loose ends, treating corners carefully.
// Sometimes this is called in situations in which it's not safe to
// erase a looseEnds iterator.  If active_it is not NULL, don't erase
// it, but return true if it should be erased.

static bool removeLooseEnds(std::vector<FaceIntersectionMap> &looseEnds,
			    int faceId,
			    FaceIntersectionMap::iterator *active_it,
			    bool print=false) 
{
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  //bool foundmatch = true;
  double dist2;
  FaceIntersectionMatchMap matches;
  
  // reset number of matches and pairs
  for(FaceIntersectionMap::iterator it1 = looseEnds[faceId].begin();
      it1 != looseEnds[faceId].end(); ++it1) 
    {
      (*it1).second.matches = 1;
      (*it1).second.paired = 0;
    }
  
  // store matches in a vector, increment each's match number instead of erasing
  
  // First do a double loop searching for simple matches.
  for(FaceIntersectionMap::iterator it1=looseEnds[faceId].begin(); 
      it1!=looseEnds[faceId].end(); ++it1)
    {
      // If this is part of a group that's already been matched, skip it.
      if((*it1).second.matches > 1) {
	continue;
      }
      
      //matches.clear();
      //matches.push_back(&(*it1).second);
      FaceIntersectionMatches *matchVector = new FaceIntersectionMatches;
      matchVector->push_back(it1);
      matches.insert(FaceIntersectionMatchesDatum((*it1).first, matchVector));
      FaceIntersectionMap::iterator it2 = it1;
      for(++it2; it2 != looseEnds[faceId].end(); ++it2) {
	// remove a simple match where the hash is equal
	// and the type is opposite
	if((*it1).first == (*it2).first) { 
 // #ifdef DEBUG
 // 	  if(print)
 // 	    oofcerr << "found match 1" << std::endl;
 // 	  // if(print)
 // 	  //   oofcerr << "removing looseEnds1 " << (*it2).first << " " 
 // 	  // 	      << (*it2).second.ip->x[0] << ", "
 // 	  // 	      << (*it2).second.ip->x[1] << ", "
 // 	  // 	      << (*it2).second.ip->x[2] << " " << (*it2).second.type
 // 	  // 	      << std::endl;
 // #endif
	  for(FaceIntersectionMatches::iterator it3=matchVector->begin();
	      it3!=matchVector->end(); ++it3) 
	    {
	      (**it3).second.matches++;
	    }
	  (*it2).second.matches = (*matchVector->front()).second.matches;
	  matchVector->push_back(it2);
	} // (*it1).first == (*it2).first

 //   // Now search for "matches" with very close coordinates and opposite
 //   // type. Using a tolerance is necessary here because if two points
 //   // are close enough, they will create intersections that should
 //   // cancel, but, the intersections could be out of order, or worse,
 //   // on different edges. This needs to be in a separate loop so that
 //   // all matches of the first type are found first. Make sure these
 //   // are not also matches of the first type.
	dist2 = vtkMath::Distance2BetweenPoints((*it1).second.ip->x, 
						(*it2).second.ip->x);
	if(dist2 < TINY && 
	   (*it1).first != (*it2).second.ip->hash[0] &&
	   (*it1).first != (*it2).second.ip->hash[1] &&
	   (*it1).first != (*it2).second.ip->hash[2])
	  {
 // #ifdef DEBUG
 // 	if(print) oofcerr << "found match 2" << std::endl;
 // // 	if(print) oofcerr << "removing looseEnds1b " << (*it2).first << " " << (*it2).second.ip->x[0] << ", " << (*it2).second.ip->x[1]  << ", " << (*it2).second.ip->x[2] << " " << (*it2).second.type << std::endl;
 // #endif
	    for(FaceIntersectionMatches::iterator it3=matchVector->begin();
		it3 != matchVector->end(); ++it3) 
	      {
		(**it3).second.matches++;
	      }
	    (*it2).second.matches = (*matchVector->front()).second.matches;
	    matchVector->push_back(it2);
	  }
      }	// end it2 loop
      
       // if(foundmatch) {
 // #ifdef DEBUG
 // 	if(print)
 // 	  oofcerr << "removing looseEnds2b " << (*temp).first << " "
 // 		    << (*temp).second.ip->x[0] << ", "
 // 		    << (*temp).second.ip->x[1] << ", "
 // 		    << (*temp).second.ip->x[2] << " "
 // 		    << (*temp).second.type << std::endl;
 // #endif	// DEBUG
       // 	looseEnds[faceId].erase(temp);
       // }
    } // end it1 loop

   // final loop, erase loose ends groups where all members can be
   // paired up with a match of the opposite type. If there are any
   // oddballs, keep the whole group.

// #ifdef DEBUG
//    if(print)
//      oofcerr << "removeLooseEnds: num loose ends before removing "
// 	     << looseEnds[faceId].size() << std::endl;
// #endif // DEBUG

  bool erase_active_it = false;

  for(FaceIntersectionMatchMap::iterator it=matches.begin(); it!=matches.end();
      ++it)
    {
      if((*it).second->size() % 2 == 0) {
	FaceIntersectionPairVector pairs;
	for(FaceIntersectionMatches::iterator it2=(*it).second->begin();
	    it2!=(*it).second->end(); ++it2) 
	  {
	    for(FaceIntersectionMatches::iterator it3=it2;
		it3!=(*it).second->end() && !(**it2).second.paired; ++it3)
	      {
		if((**it2).second.type != (**it3).second.type && 
		   !(**it3).second.paired)
		  {
		    (**it2).second.paired = true;
		    (**it3).second.paired = true;
		    pairs.push_back(FaceIntersectionPair(*it2, *it3));
		    break;
		  }
	      }
	  }
	
	if(pairs.size() == (*it).second->size() / 2) {
	  for(FaceIntersectionMatches::iterator it2=(*it).second->begin();
	      it2!=(*it).second->end(); ++it2)
	    {
	      if(active_it != NULL) {
		if(*it2 != *active_it)
		  looseEnds[faceId].erase(*it2);
		else
		  erase_active_it = true;
	      }
	      else
		looseEnds[faceId].erase(*it2);
	    }
	}
      }
    } // end loop over matches
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  for(FaceIntersectionMatchMap::iterator it=matches.begin(); it!=matches.end();
      ++it)
    {
      delete (*it).second;	// FaceIntersectionMatches*
    }
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif
  return erase_active_it;
} // end removeLooseEnds

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Use the looseEnds object to detect and remove spurious edgs.  If
// two connected points are in the looseEnds object, the whole edge
// was spurious.
static void removeSpuriousEdges(std::vector<FaceIntersectionMap> &looseEnds,
				CellEdge &elementEdgeData,
				std::vector<double> &facearea,
				Coord fnormal[NUM_TET_FACES], int faceId,
				bool print,
				const std::vector<Coord> &epts)
{
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  bool foundmatch = false;
  bool doublematch = false;
  // FaceIntersectionMap is a std::multimap, int to FaceIntersection,
  // where the int the hash value of the intersection point.
  // FaceIntersection is a struct defined in cskeletonelement.h.
  FaceIntersectionMap::iterator temp, it2;
  // Do a double loop through the loose ends looking for two loose
  // ends that constitute a segment.  temp and it2 are set by the
  // loops.  After foundmatch is set to true, both loops exit.
  for(FaceIntersectionMap::iterator it1=looseEnds[faceId].begin();
      it1!=looseEnds[faceId].end() && !foundmatch; ++it1 )
    {
// #ifdef DEBUG
//       if(print) 
// 	oofcerr << "removeSpuriousEdges: potential spurious edge: "
// 		  << (*it1).first << " " << (*it1).second.ip->x[0] << ", "
// 		  << (*it1).second.ip->x[1] << ", " << (*it1).second.ip->x[2]
// 		  << " " << (*it1).second.type << std::endl;
// #endif	// DEBUG

      temp = it1; 
      FaceIntersectionMap::iterator end;
      //foundmatch = false;
      // If the opposite point is on the same face, search the loose
      // ends on this face.
      if((*it1).second.op->faces[faceId] && !iPointOnEdge((*it1).second.op)) {
	it2 = it1;
	end = looseEnds[faceId].end();
	++it2;
      }
      // Otherwise, search the extra loose ends.

      // The following block was prefaced by 
      //      else if(iPointOnEdge((*it1).second.op))
      // in Valerie's code.  That leaves open the chance that it2 and
      // end could be left unset, if neither that condition or the one
      // above holds.  Since I don't know if that was intentional, and
      // I don't know what the conditions really mean, I've removed
      // the 'if' and added an assertion to test the proposition that
      // the 'if' was redundant.
      else {
	assert(iPointOnEdge((*it1).second.op)); // See comment above.
// #ifdef DEBUG
// 	if(print) oofcerr << "removeSpuriousEdges: on edge" << std::endl;
// #endif	// DEBUG
	it2 = looseEnds[4].begin();
	end = looseEnds[4].end();
      }
      for( ; it2!=end && !foundmatch; ++it2) {
	// Detect matches between ip and op.
	if(((*it1).second.op->hash[0] == (*it2).second.ip->hash[0] ||
	    ((*it1).second.op->corner &&
	     ((*it1).second.op->hash[0] == (*it2).second.ip->hash[0] ||
	      (*it1).second.op->hash[1] == (*it2).second.ip->hash[0] ||
	      (*it1).second.op->hash[2] == (*it2).second.ip->hash[0])) ||
	    ((*it2).second.ip->corner &&
	     ((*it1).second.op->hash[0] == (*it2).second.ip->hash[0] ||
	      (*it1).second.op->hash[0] == (*it2).second.ip->hash[1] ||
	      (*it1).second.op->hash[0] == (*it2).second.ip->hash[2])))
	   && (*it1).second.type != (*it2).second.type) 
	  {
// #ifdef DEBUG
// 	    if(print) 
// 	      oofcerr << "removeSpuriousEdges: potential spurious edge: "
// 		      << (*it1).first << " "
// 		      << (*it1).second.ip->x[0] << ", "
// 		      << (*it1).second.ip->x[1] << ", "
// 		      << (*it1).second.ip->x[2] << " " 
// 		      << (*it1).second.type << " " << (*it2).first << " "
// 		      << (*it2).second.ip->x[0] << ", "
// 		      << (*it2).second.ip->x[1] << ", "
// 		      << (*it2).second.ip->x[2] << " "
// 		      << (*it2).second.type << std::endl;
// #endif	// DEBUG
// 	    foundmatch = true;
	    break;
	  }
	// OR it1's op could match it2's op, which means both segments
	// are spurious. We need to detect this case since the op's
	// will not be loose ends. This is a quick and dirty fix for
	// the problem of two joining spurious segments. For multiple
	// joining spurious segments, a more general solution must be
	// found. This is a TODO 3.1 for when such a debugging case
	// arises.
	if(((*it1).second.op->hash[0] == (*it2).second.op->hash[0] ||
	    ((*it1).second.op->corner &&
	     ((*it1).second.op->hash[0] == (*it2).second.op->hash[0] ||
	      (*it1).second.op->hash[1] == (*it2).second.op->hash[0] ||
	      (*it1).second.op->hash[2] == (*it2).second.op->hash[0])))
	   && !isDupe((*it1).second.ip, (*it2).second.ip, fnormal, -1, print,
		      epts)
	   && (*it1).second.type != (*it2).second.type) 
	  {
// #ifdef DEBUG
// 	    if(print) {
// 	      oofcerr << "removeSpuriousEdges: potential spurious edge 2: "
// 		      << (*it1).first
// 		      << " " << (*it1).second.ip->x[0] << ", "
// 		      << (*it1).second.ip->x[1] << ", "
// 		      << (*it1).second.ip->x[2] << " " 
// 		      << (*it1).second.type << " "
// 		      << (*it2).first << " "
// 		      << (*it2).second.ip->x[0] << ", " 
// 		      << (*it2).second.ip->x[1] << ", " 
// 		      << (*it2).second.ip->x[2] << " "
// 		      << (*it2).second.type << std::endl;
// 	      oofcerr << (*it1).second.op->x[0] << ", " 
// 		      << (*it1).second.op->x[1] << ", "
// 		      << (*it1).second.op->x[2] << std::endl;
// 	      oofcerr << (*it2).second.op->x[0] << ", "
// 		      << (*it2).second.op->x[1] << ", "
// 		      << (*it2).second.op->x[2] << std::endl;
// 	      oofcerr << (*it2).second.ip->faces[0]
// 		      << (*it2).second.ip->faces[1]
// 		      << (*it2).second.ip->faces[2]
// 		      << (*it2).second.ip->faces[3] << std::endl;
// 	    }
// #endif	// DEBUG
	    foundmatch = true;
	    doublematch = true;
	    break;
	  }
      }	// end it2 loop
      if(foundmatch)
	break;
    } // end it1 loop over looseEnds

  if(foundmatch) {
// #ifdef DEBUG
//     if(print)
//       oofcerr << "removeSpuriousEdges: removing a spurious edge"
// 	      << std::endl;
// #endif	// DEBUG
    
    // First correct contribution to face area.
    facearea[faceId]-=(*temp).second.contrib;
    if(doublematch)
      facearea[faceId]-=(*it2).second.contrib;
    // Get the info that we will need after deleting temp
    IntersectionCategory type = (*temp).second.type;
    // Use the op to be consistent with above.
    bool onEdge = iPointOnEdge((*temp).second.op);
    int edgeId = -1;
    double t = 0;
    if(onEdge) {
      for(int i = 0; i < 6; ++i) 
	if((*temp).second.op->edges[i])
	  edgeId = i;
      t = (*temp).second.op->t[edgeId];
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "removeSpuriousEdges: on edge again " << edgeId 
// 		<< " " << t << std::endl;
// #endif	// DEBUG
    } // if onEdge

      for(int i = 0; i < 3; ++i) {
	std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator>
	  matches = looseEnds[faceId].equal_range((*temp).second.ip->hash[i]);
	for(FaceIntersectionMap::iterator temp2=matches.first;
	    temp2!=matches.second; ++temp2) 
	  {
	    if((*temp2).second.type == (*temp).second.type) {
	      looseEnds[faceId].erase(temp2);
	      break;
	    }		
	  }
      }

    // Now handle the second point.
    //if((*it2).second.ip->corner || onEdge) {
      if(onEdge) {
	CellEdgeMap::iterator it;
	it = elementEdgeData[edgeId].find(t);
// #ifdef DEBUG
// 	if(print) 
// 	  oofcerr << "removeSpuriousEdges: removing edge intersection "
// 		  << edgeId << " "
// 		  << (it == elementEdgeData[edgeId].end()) << std::endl;
// #endif // DEBUG
	(*it).second.addType(faceId, type);
      }
      for(int i = 0; i < 3; ++i) {
	std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator>
	  matches = looseEnds[faceId].equal_range((*it2).second.ip->hash[i]);
	for(FaceIntersectionMap::iterator temp2=matches.first;
	    temp2!=matches.second; ++temp2) 
	  {
	    if((*temp2).second.type == (*it2).second.type) {
	      looseEnds[faceId].erase(temp2);
	      break;
	    }		
	  }     
      }

      // removeSpuriousEdges is only called from processLooseEnds,
      // which isn't called from within a loop over looseEnds, so we
      // don't have to worry about deleting active iterators on this
      // call to removeLooseEnds.
      removeLooseEnds(looseEnds, faceId, NULL, print);

      // Now recurse to find more spurious edges
      removeSpuriousEdges(looseEnds, elementEdgeData, facearea, fnormal,
			  faceId, print, epts);
  } // end if(foundmatch)
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

} // end removeSpuriousEdges


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// Create an IntersectionPoint from a general 2D point and add
// topological information.
IntersectionPoint *createIPoint(double p[2], const Quad *q, bool onEdge,
				int edgeId, double t, bool onFace, int faceId,
				bool print=false)
{
  // Initialize the IntersectionPoint struct.
  //* t is unused if onEdge is false.  TODO 3.1: If IntersectionPoint were
  //* a class, there could be subclasses for points on and off edges,
  //* which might be less confusing.
  IntersectionPoint *ip = new IntersectionPoint();
  // Convert the 2D coordinate to a 3D coordinate using properties
  // from the quad.
  ip->x[VoxelSetBoundary::proj_dirs[q->norm_dir][0]] = p[0];
  ip->x[VoxelSetBoundary::proj_dirs[q->norm_dir][1]] = p[1];
  ip->x[q->norm_dir] = (double)q->height;
// #ifdef DEBUG
//   if(print) {
//     oofcerr << "createIPoint: new ipoint " << *ip << " faceId=" << faceId
// 	    << std::endl;
//   }
// #endif	// DEBUG
  // Set the edge flags and edge id.
  if(onEdge) {
    ip->edges[edgeId] = true;
    ip->faces[CSkeletonElement::edgeFaces[edgeId][0]] = true;
    ip->faces[CSkeletonElement::edgeFaces[edgeId][1]] = true;
    ip->t[edgeId] = t;
  }
  // Set the face flags and face id.
  else if(onFace) {
    ip->faces[faceId] = true;
  }
  return ip;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Set the hash value of an IntersectionPoint. b represents which
// segment (or point in the corner case) of the quad is used for the
// hash.

static void setHashValue(IntersectionPoint *ip, const Quad *q, int b,
			 bool corner=false)
{
  ip->corner = corner;
  if(!corner) {
    // This is the axis that the hashed segment is aligned with in the
    // 2D coordinate system.
    int i = VoxelSetBoundary::proj_dirs[q->norm_dir][(b+1)%2]; 
    if(q->norm_dir == VoxelSetBoundary::proj_dirs[i][0])
      ip->hash[0] = hash(q->height, q->coords[b][b%2], i);
    else
      ip->hash[0] = hash(q->coords[b][b%2], q->height, i);
  }
  else {
    // If it's on a corner, we need to hash all three axes because the
    // matching point could be from a segment that is aligned with any
    // Cartesian axis.
    int y[3];
    y[q->norm_dir] = q->height;
    y[VoxelSetBoundary::proj_dirs[q->norm_dir][0]] = q->coords[b][0];
    y[VoxelSetBoundary::proj_dirs[q->norm_dir][1]] = q->coords[b][1];
    for(int i=0; i<3; ++i) 
      ip->hash[i] = hash(y[VoxelSetBoundary::proj_dirs[i][0]],
			 y[VoxelSetBoundary::proj_dirs[i][1]],i);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Create an IntersectionPoint from a general 2D point (not a voxel
// boundary quad point) and set its hash value.
static IntersectionPoint *createIPointAndHash(
			      double p[2], const Quad *q, int b,
			      bool onEdge, int edgeId, double t,
			      bool onFace, int faceId, bool print=false) 
{
  IntersectionPoint *ip = createIPoint(p, q, onEdge, edgeId, t, onFace, faceId,
				       print);
  setHashValue(ip, q, b, false);
  return ip;
}

// Create an IntersectionPoint from a voxel boundary quad point and
// set its hash value.
IntersectionPoint *createIPointAndHash(
			       const Quad *q, int b,
			       bool onEdge, int edgeId, double t,
			       bool onFace, int faceId, bool print) 
{
  double x[2];
  x[0] = (double)q->coords[b][0];
  x[1] = (double)q->coords[b][1];
  IntersectionPoint *ip = createIPoint(x, q, onEdge, edgeId, t, onFace, faceId,
				       print);
  setHashValue(ip, q, b, true);
  return ip;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


/*
             \ a (the in-plane tet line)
   ^ j        \
   |           \
   -> i         \   \
                 \   V (s parameter)
                  \
                   \
c ----------------------------------------------- d (the quad edge)
          -> (t)     \
                      \
                       \
                        \
                         \ b

 */

// Finds the intersection of the segments a-b and c-d, if any and puts
// this 2D point in p. Returns a flag that describes the intersection
// type. s is the parametric coordinate of the intersection on the a-b
// segment and t is the parametric coordinate of the intersection on
// the c-d segment. k is the index of the quad point that corresponds
// to point d and indicates which axis in the 2D coordinate system the
// quad edge is aligned with (described below). aHB, aHB1, bHA, and
// bHA1 are described in convexPolyIntersection.
//* TODO 3.1: WTF are the return values, p, s and t, in the middle of the
//* argument list?
static SegSegIntersectionType segSegInt(
			const double a[2], const double b[2], 
			const int c[2], const int d[2],
			double p[2], double &s, double &t,
			int k, double aHB, double bHA, double aHB1, double bHA1,
			bool print)
{
  SegSegIntersectionType code = NO_INTERSECTION;
  
  // i is the coordinate that varies in the current segment of the
  // quad.  j is the coordinate that is constant.
  int i = (k+1)%2;
  int j = k%2;

// #ifdef DEBUG
//   if(print)
//     oofcerr << "segSegInt " << i << " " << j << " " <<  (c[j] == a[j])
// 	      << (c[j] == b[j]) << " " << (c[j]-a[j]) << " " << (c[j]-b[j])
// 	      << std::endl;
// #endif	// DEBUG

  if((b[j] == a[j] && c[j] == a[j]) ||
     (bHA == 0 && bHA1 == 0) || (aHB == 0 && aHB1 == 0))
    {
      // colinear and overlapping at least at a point since we've
      // eliminated quads for which the in-plane portion of the tet is
      // out of bounds
      t = (b[i] - c[i]) / (d[i] - c[i]);
      s = (d[i] - a[i]) / (b[i] - a[i]);
      return PARALLEL_INTERSECTION;
    }
  else if (b[j] == a[j]) // parallel but disjoint
    return NO_INTERSECTION;

  // p[j] has to be equal to c[j] because the quad segment does not
  // vary in the j coordinate.
  p[j] = c[j];

// #ifdef DEBUG
//   if(print) {
//     oofcerr << "segSegInt: conditions " << (c[j] == a[j]) << (a[i] == c[i])
// 	      << (a[i] == d[i]) << (c[j] == b[j]) << (b[i] == c[i])
// 	      << (b[i] == d[i]) << std::endl;
//     oofcerr << (c[j] - a[j]) << " " << (c[j] - b[j]) << std::endl;
//   }
// #endif	// DEBUG

  // Carefully detect vertex intersections and set s and t exactly to
  // avoid topological errors due to roundoff.
  if(c[j] == a[j] || aHB1 == 0) {
    // If the first vertex of the tet seg is exactly on the quad seg
    s = 0.0;
    code = VERTEX_INTERSECTION;
    if(a[i] == c[i] || bHA1 == 0) {
      // If the first vertex of the tet seg coincides with the first
      // vertex of the quad seg
      t = 0.0;
      p[i] = c[i];
      return code;
    }
    else if(a[i] == d[i] || bHA == 0) {
      // If the first vertex of the tet seg coincides with the second
      // vertex of the quad seg
      t = 1.0;
      p[i] = d[i];
      return code;
    }
  }
  else if(c[j] == b[j] || aHB == 0) {
    // If the second vertex of the tet seg is exactly on the quad seg
    // line
    s = 1.0;
    code = VERTEX_INTERSECTION;
    if(b[i] == c[i] || bHA1 == 0) {
      // If the second vertex of the tet seg coincides with the second
      // vertex of the quad seg
      t = 0.0;
      p[i] = c[i];
      return code;
    }
    else if(b[i] == d[i] || bHA == 0) {
      // If the second vertex of the tet seg coincides with the second
      // vertex of the quad seg
      t = 1.0;
      p[i] = d[i];
      return code;
    }
  }
  else
    // otherwise calculate s
    s = (c[j] - a[j]) / (b[j] - a[j]);

  // There will be no more adjustments to s
  if(s < 0 || s > 1)
    return NO_INTERSECTION;
    
  // Now calculate p[i] from s.
  p[i] = a[i] + s * (b[i] - a[i]);

// #ifdef DEBUG
//   if(print)
//     oofcerr << "segSegInt: prospective intersection: " << p[0] << " " << p[1]
// 	      << std::endl;
// #endif	// DEBUG

  // Check again for vertex intersections and set t exactly.
  if(c[i] == p[i] || bHA1 == 0) {
    // If the first vertex of the quad seg coincides with the
    // intersection.
    t = 0.0;
    p[i] = c[i];
    code = VERTEX_INTERSECTION;
  }
  else if(d[i] == p[i] || bHA == 0) {
    // If the second vertex of the quad seg coincides with the
    // intersection.
    t = 1.0;
    p[i] = d[i];
    code = VERTEX_INTERSECTION;
  }
  else
    t = (p[i] - c[i]) / (d[i] - c[i]); 

  // Check one last time to be sure to avoid topological errors due to
  // roundoff.
  if(t == 0.0) {
    p[i] = c[i];
    code = VERTEX_INTERSECTION;
  }
  else if(t == 1.0) {
    p[i] = d[i];
    code = VERTEX_INTERSECTION;
  }
  if(s==0 || s==1)
    code = VERTEX_INTERSECTION;
  
  if(s > 0.0 && s < 1.0 && t > 0.0 && t < 1.0)
    code = SIMPLE_INTERSECTION;
  else if(s < 0.0 || s > 1.0 || t < 0.0 || t > 1.0)
    code = NO_INTERSECTION;
  
  return code;
} // end segSegInt

// TODO 3.1: needs comment.
static bool isIntersection(const double a[2], const double b[2], int c,
			   bool print) 
{
  assert(c == 0 || c == 1);
  int j = 1 - c;
  double s = -1*a[j] / (b[j] - a[j]);
  double t = a[c] + s * (b[c] - a[c]);
  return (s > 0 && s < 1 && t > 0 && t < 1);
}

// These values classify the poly-poly intersection overall and are
// used by categoryVolumes to handle the output of
// convexPolyIntersection
enum PolyIntersectionType {POLY_INTERSECT,
			   POLY_DISJOINT,
			   QUAD_INSIDE,
			   TET_INSIDE,
			   POLY_UNKNOWN};

// This is the core of the categoryVolumes calculation and implements
// a modified version of the O'Rourke convex poly intersection
// algorithm. See section 7.6 of "Computational Geometry in C" by
// Joseph O'Rourke. Calculates the intersection of two convex polys -
// one being an axis aligned rectangle representing a voxel boundary
// face (stored in q) and the other being either a triangle or a quad
// representing the intersection of a tet with the voxel boundary quad
// plane (stored in tetPoints). The resulting polygon is stored as a
// series of counter-clockwise points with topological information in
// the iPoints object. epts represents all four points defining the
// tet. fnormal gives the normal vectors for each of the four tet
// faces. type is a flag that classifies the type of poly-poly intersection
// found here.

// TODO: It seems that using O'Rourke here is overkill, and that the
// calculation could be done faster without it, using the fact that
// the quad is aligned with the axes.  There are only a few cases to
// consider and they can be distinguished from one another using only
// numerical comparision and no arithmetic. It's easy to tell which
// tet points are inside the quad, and also which tet edges intersect
// which quad edges.  The only hard cases are the ones where a tet
// edge has both endpoints outside the quad but might or might not
// cross a corner.

static void convexPolyIntersection(const TetIntersectionPoints &tetPoints, 
				   IntersectionPoints &iPoints, 
				   IntersectionPoints &AllIPoints,
				   const Quad *q, 
				   const std::vector<Coord> &epts, 
				   Coord fnormal[4],
				   PolyIntersectionType &type, 
				   bool print=false) 
{
  // a, a1 and aa refer to the tetPoints index, b, b1 and ba refer to
  // the quad point index. The inflag describes which polygon is "in"
  // with repect to the most recent intersection.
  int a=0, b=0, aa=0, ba=0;
  // int loopcontrol=0;
  int n = tetPoints.size();	// must be 3 or 4
  PolyTraversalState inflag = UNKNOWN;
  int quadPointFaceId = -1;
  int quadPointEdgeId = -1; 
  bool firstPoint = true;
  bool quadPointOnFace = false;
  bool quadPointOnEdge = false;
  bool firstVertex = false;
  bool tetPointOnQuad = false;
  // A is the tet segment vector, B is the quad segment vector. aHB
  // (aHB1) is a cross product that determines whether the latest
  // (previous) tet point is in the half plane of the quad -- if aHB
  // is positive, the point is in the half plane. bHA (bHA1) is a
  // cross product that determines whether the latest (previous) quad
  // point is in the half plane of the tet segment. p stores the
  // coordinates of the intersection of A and B. s and t are the
  // parametric coordinates of the intersection of A and B.
  double O[2] = {0.0,0.0};
  double quadPointT = 0;
  // These flags are used to determine which is poly is inside the
  // other, if any, in cases where there are no intersections.
  bool tet_inside_quad = true;
  bool quad_inside_tet = true;
 

  // TODO OPT: figure out which of these conditions are necessary and sufficient
  while( ( (aa < n || ba < 4) && aa < 2*n && ba < 8 ) /*&& loopcontrol < 20*/) {

    // Update the indices and flags.
    // ++loopcontrol; // a safety measure
    int a1 = (a + n - 1) % n;	// previous tet intersection point
    int b1 = (b + 3) % 4;	// previous quad corner

    // Store the tet points for convenience.
    TetIntersectionPoint tp_a1 = tetPoints[a1];
    TetIntersectionPoint tp_a = tetPoints[a];

    // Calculate A and B.
    double A[2], B[2];
    A[0] = tp_a1.x[0] - tp_a.x[0];
    A[1] = tp_a1.x[1] - tp_a.x[1];
    B[0] = q->coords[b1][0] - q->coords[b][0];
    B[1] = q->coords[b1][1] - q->coords[b][1];
    // p[0] = p[1] = 0.0;
    
    // Calculate the relevant cross products.
    double cross = cross2D(O, A, B);
    // if aHB is positive, the tet point is in the half plane defined
    // by the quad segment
    double aHB = cross2D(q->coords[b1], q->coords[b], tp_a.x); 
    double aHB1 = cross2D(q->coords[b1], q->coords[b], tp_a1.x); 
    // if bHA is positive, the quad point is in the half plane defined
    // by the tet segment
    double bHA = cross2D(tp_a1.x, tp_a.x, q->coords[b]);
    double bHA1 = cross2D(tp_a1.x, tp_a.x, q->coords[b1]);

    // Update the flags used for non-intersecting cases. The tet is
    // inside the quad if every tet point is inside the half plane of
    // every quad segment considered and vice versa.
    tet_inside_quad &= (aHB >= 0);
    quad_inside_tet &= (bHA >= 0);
    
    // Calculate the intersection of A and B. p, s, and t are outputs.
    double p[2], s, t;
    SegSegIntersectionType code = segSegInt(
		    tp_a1.x, tp_a.x, q->coords[b1], q->coords[b], p, s, t,
		    b, aHB, bHA, aHB1, bHA1, print);

// #ifdef DEBUG
//     if(print) {
//       oofcerr << "\niteration " << loopcontrol << " " << aa << " " << ba 
// 		<< std::endl;
//       // oofcerr << a << " " << b << " " << firsta << " " << firstb << " "
//       // 		<< (a == firsta && b == firstb) << std::endl;
//       oofcerr << tp_a1.x[0] << "," << tp_a1.x[1] << " ";
//       oofcerr << tp_a.x[0] << "," << tp_a.x[1] << " ";
//       oofcerr << q->coords[b1][0] << "," << q->coords[b1][1] << " ";
//       oofcerr << q->coords[b][0] << "," << q->coords[b][1] << std::endl;
//       oofcerr << "cross=" << cross << " aHB=" << aHB << " " << (aHB==0)
// 		<< " bHA=" << bHA << " " << (bHA==0);
//       oofcerr << " " << aHB1 << " " << bHA1 << " inflag=" << inflag 
// 		<< std::endl;
//       oofcerr << "intersection code " << code << " s = " << s << " "
// 		<< (s==0.0) << (s==1.0) << " t = " << t << " " << (t==0.0)
// 		<< (t==1.0) << std::endl; 
//     }
// #endif	// DEBUG

    // If there was an intersection, add the appropriate points and
    // update the flags as needed.
    if(code == SIMPLE_INTERSECTION || code == VERTEX_INTERSECTION) {
      // A vertex intersection could still be disjoint.
      if(code == SIMPLE_INTERSECTION)
	type = POLY_INTERSECT;
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "convexPolyIntersection: found intersection "
// 		<< p[0] << ", " << p[1] << std::endl;
// #endif	// DEBUG
      // Reset aa and ba if this is the first intersection.
      if(inflag == UNKNOWN && firstPoint) {
	aa = ba = 0;
	firstPoint = false;
	firstVertex = (code == VERTEX_INTERSECTION);
      }
      // Set the inflag. If the tet point is in the half plane of the
      // quad segment, set PIN. If the quad point is in the half plane
      // of the tet segment, set QIN.
      if(aHB > 0)
	inflag = PIN;
      if(bHA > 0)
	inflag = QIN;
      // Add a point for the intersection found, taking care to set
      // the topological information. 
      IntersectionPoint *ip;
      // If s is 0 or 1, the intersection coincides with a tet point,
      // so convert the TetIntersectionPoint to an
      // IntersectionPoint. If t is also exactly 0 or exactly 1, set
      // the corner flag.
      if(s == 0.0) {
	ip = iPointFromTetPoint(tp_a1,q->norm_dir,q->height);
	setHashValue(ip, q, (t==0 ? b1 : b), (t==0 || t==1));
      }
      else if(s == 1.0) {
	ip = iPointFromTetPoint(tp_a,q->norm_dir,q->height);
	setHashValue(ip, q, (t==0 ? b1 : b), (t==0 || t==1));
      }
      // Otherwise, the intersection point is somewhere in the middle of A.
      else {
	int nodea1 = tp_a1.node, nodea = tp_a.node;
	// The point is on a tet edge (not in the middle of a face) if
	// both endpoints of A coincide with tet nodes. If it's on an
	// edge, we need to get the edge id and parametric coordinate.
	bool onEdge = (nodea1 != -1 && nodea != -1);
	int edgeId = -1;
	int faceId = -1;
	double u = 0.0;
	if(onEdge) {
	  edgeId = CSkeletonElement::nodeNodeEdge[nodea1][nodea];
	  int *ptIds = vtkTetra::GetEdgeArray(edgeId);
	  if(nodea1 == ptIds[0])
	    u = s;
	  else
	    u = 1-s;
	}
	// If it's not on an edge, it's on a face and we need the face id.
	else { 
	  faceId = getFaceBetweenTetPoints(tp_a1,tp_a);
	}
	// If t is 0 or t is 1, create the IntersectionPoint and hash
	// directly from the appropriate quad point.
	
	// u is not used by createIPoint if onEdge is false.
	if(t == 0.0)
	  ip = createIPointAndHash(q,b1,onEdge,edgeId,u,!onEdge,faceId,print);
	else if(t == 1.0)
	  ip = createIPointAndHash(q,b,onEdge,edgeId,u,!onEdge,faceId,print);
	// Otherwise, create the point from p.
	else
	  ip = createIPointAndHash(p,q,b,onEdge,edgeId,u,!onEdge,faceId,print);
      }
      // Finally, add the point to the iPoints object.
      addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print, epts);
    }
    
    // If A & B overlap, set the necessary flags so that we can add
    // the appropriate point later if necessary.
    if(code == PARALLEL_INTERSECTION) {
      // This quad point is on a tet face, set the flag and get the
      // face id.
      quadPointOnFace = true;
      quadPointFaceId = getFaceBetweenTetPoints(tp_a1,tp_a);
      tetPointOnQuad = true;
      // If both tet points are nodes, then the quad point is actually
      // on a tet edge. Set the flag, get the edge id, and calculate
      // the parametric coordinate.
      if(tp_a1.node != -1 && tp_a.node != -1) {
	quadPointOnEdge = true;
	quadPointEdgeId = CSkeletonElement::nodeNodeEdge[tp_a1.node][tp_a.node];
	int *ptIds = vtkTetra::GetEdgeArray(quadPointEdgeId);
	if(tp_a1.node == ptIds[0])
	  quadPointT = s;
	else
	  quadPointT = 1-s;
// #ifdef DEBUG
// 	if(print)
// 	  oofcerr << "convexPolyIntersection: next quad point on an edge "
// 		  << quadPointEdgeId << " " << quadPointT << std::endl;
// #endif	// DEBUG
      }
    }

    // If A & B overlap and are oppositely oriented, the polys are
    // disjoint.
    if(code == PARALLEL_INTERSECTION && A[0]*B[0]+A[1]*B[1] < 0) {
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "convexPolyIntersection: polys touch but do not intersect"
// 		<< std::endl;
// #endif // DEBUG
      type = POLY_DISJOINT;
      // Add points
      int c = (b+1)%2;
      double minA = std::min(tp_a1.x[c],tp_a.x[c]);
      double maxA = std::max(tp_a1.x[c],tp_a.x[c]);
      int minB = std::min(q->coords[b1][c],q->coords[b][c]);
      int maxB = std::max(q->coords[b1][c],q->coords[b][c]);
      if(minB > minA && minB < maxA) {
	IntersectionPoint *ip = 
	  createIPointAndHash(q, (minB == q->coords[b1][c] ? b1 : b),
			      quadPointOnEdge, quadPointEdgeId, quadPointT,
			      quadPointOnFace, quadPointFaceId, print);
	addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print,
		     epts);
      }
      if(maxB > minA && maxB < maxA) {
	IntersectionPoint *ip =
	  createIPointAndHash(q, (maxB == q->coords[b1][c] ? b1 : b), 
			      quadPointOnEdge, quadPointEdgeId, quadPointT,
			      quadPointOnFace, quadPointFaceId, print);
	addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print,
		     epts);
      }
      if(minA >= minB && minA <= maxB) {
	IntersectionPoint *ip =
	  iPointFromTetPoint((minA == tp_a1.x[c] ? tp_a1 : tp_a),
			     q->norm_dir,q->height);
	setHashValue(ip, q, (minA==q->coords[b1][c] ? b1 : b),
		     (minA==minB || minA==maxB));
	addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print,
		     epts);
      }
      if(maxA >= minB && maxA <= maxB) {
	IntersectionPoint *ip =
	  iPointFromTetPoint((maxA == tp_a1.x[c] ? tp_a1 : tp_a),
			     q->norm_dir,q->height);
	setHashValue(ip, q, (maxA==q->coords[b1][c] ? b1 : b),
		     (maxA==minB || maxA==maxB));
	addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print,
		     epts);
      }
 	
    }

    // If A & B parallel but separate, the polys are disjoint.
    if(cross == 0 && aHB < 0 && bHA < 0) {
      type = POLY_DISJOINT;
    }

    // Now handle the advancement rules.

    // If A & B are colinear, don't add a point but advance based on
    // the inflag.
    if(cross == 0 && aHB == 0 && bHA == 0) {
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "convexPolyIntersection: parallel case inflag: " << inflag 
// 		<< std::endl;
// #endif // DEBUG
      if(inflag == PIN) {
	++ba;
	b = (b+1)%4;
	quadPointOnFace = false;
	quadPointOnEdge = false;
      }
      else { 
	++aa;
	a = (a+1)%n;
	tetPointOnQuad = false;
      }
    }

    // Now for the general cases. See O'Rourke for an explanation.
    else if( (cross >= 0 && bHA > 0) || (cross < 0 && aHB <= 0) ) {
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "convexPolyIntersection: general case 1 "
// 		<< inflag << " " << (inflag==PIN) <<  std::endl;
// #endif // DEBUG
      if(inflag == PIN && aHB >= 0) { 
	IntersectionPoint *ip = iPointFromTetPoint(tp_a,q->norm_dir,q->height);
	if(tetPointOnQuad)
	  setHashValue(ip, q, b1);
	addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print,
		     epts);
      }
      ++aa;
      a = (a+1)%n;
      tetPointOnQuad = false;
    }
    else {
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "convexPolyIntersection: general case 2 "
// 		<< inflag << " " << (inflag==QIN) << std::endl;
// #endif // DEBUG
      if(inflag == QIN && bHA >= 0) { 
	IntersectionPoint *ip = createIPointAndHash(
		    q, b, 
		    quadPointOnEdge, quadPointEdgeId, quadPointT,
		    quadPointOnFace, quadPointFaceId, print);
	addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print,
		     epts);
      }
      ++ba;
      b = (b+1)%4;
      // reset these flags.
      quadPointOnFace = false;
      quadPointOnEdge = false;
    }

  } // end of while loop

  // Finally, handle cases where less than 3 intersection points were found.
  if(iPoints.size() <= 2 && type != POLY_DISJOINT) {
    if(quad_inside_tet && tet_inside_quad)
      throw ErrProgrammingError("they can't both be inside",
				__FILE__, __LINE__);
    if(quad_inside_tet && !tet_inside_quad && ba >= 3) {
      //if(ba < 4-1)
      //throw ErrProgrammingError("false positive quad in", __FILE__, __LINE__);
      iPoints.clear();
      for(int i = 0; i < 4; ++i) {
	IntersectionPoint *ip = createIPointAndHash(q, i, 
						    false, -1, 0,
						    false, -1, print);
	addToIPoints(ip, iPoints, AllIPoints, fnormal, q->norm_dir, print,
		     epts);
      }
      type = QUAD_INSIDE;
    }
    else if(tet_inside_quad && !quad_inside_tet && aa >= n-1) {
      //if(aa < n-1)
      //throw ErrProgrammingError("false positive tet in", __FILE__, __LINE__);
      type = TET_INSIDE;
    }
    else
      type = POLY_DISJOINT;
    // oofcerr << "num ipoints " << iPoints.size() << std::endl;
    // throw ErrProgrammingError("unhandled", __FILE__, __LINE__);
  }

} // end convexPolyIntersection


// Calculate the intersection of a segment and a plane, taking
// advantage of the fact that the plane is axis aligned. We already
// know that the segment defined by p1 and p2 is not parallel to the
// plane, nor does it begin or end on the plane. This is used to find
// where the tet intersects the plane of a voxel boundary quad.
static void segPlaneInt(const Coord p1, const Coord p2,
			const short proji[2], int c,
			double p3, double &t, double x[2]) 
{
  t = (p3-p1[c])/(p2[c]-p1[c]);
  x[0] = p1[proji[0]] + t*(p2[proji[0]]-p1[proji[0]]);
  x[1] = p1[proji[1]] + t*(p2[proji[1]]-p1[proji[1]]);
}

// TODO 3.1: comment the next several functions used for corner cases
// where there are no intersections between quads and the tet.
enum ElementNodeStatus {ELEMENT_NODE_OUT, ELEMENT_NODE_IN, ELEMENT_NODE_ON,
			ELEMENT_NODE_ON_EDGE, ELEMENT_NODE_UNKNOWN};

// Sets the inCategory variable, currentDistance to a quad, and the
// closestQuads vector with information from the current, passed in
// quad. These are all needed in cases where there is an element face
// that has no intersections with voxel group faces.
static void elementPointInCategory(
		   ElementNodeStatus &inCategory, 
		   double &currentDist,
		   std::vector<const Quad*> &closestQuads,
		   const Coord &pt,  // corner of a tet
		   const Quad *quad, // component of a pixel boundary
		   int c, int l,
		   bool print=false) 
{
  // We're looking at quads in a plane.  c is the normal direction,
  // and l is the coordinate of the plane in the normal direction.
  // It's in pixel units, so it's an integer.

  // First, calculate the distance from the point to the plane of the
  // quad.
  double dist = pt[c] - l;
  double dist2 = (pt[c] == l ? 0 : dist*dist); // TODO OPT: Why check pt[c]==l?

  // This function gets called a lot, so we want to return as early as
  // possible if we know we're not updating anything.
  if(dist2 > currentDist) return;

  for(int m=0; m<2; ++m) {	// loop over in-plane coordinates
    // Include the in-plane distance to the nearest side of the quad
    // if the projection of pt is outside the quad.
    if(pt[VoxelSetBoundary::proj_dirs[c][m]] < quad->coords[0][m]) {
      double temp = pt[VoxelSetBoundary::proj_dirs[c][m]] - quad->coords[0][m];
      dist2 += temp*temp;
    }
    else if(pt[VoxelSetBoundary::proj_dirs[c][m]] > quad->coords[2][m]) {
      double temp = pt[VoxelSetBoundary::proj_dirs[c][m]] - quad->coords[2][m];
      dist2 += temp*temp;
    }
  }
  // if(print) {
    // oofcerr << "face c = " << c << " l = " << l << " norm = " << quad->norm << " dist2 = " << dist2;
    // oofcerr << " " << (dist2 < currentDist) << (dist2 == currentDist) << std::endl;
  // }
  if(dist2 > currentDist) return;

  double dot = quad->norm * dist; // Quad::norm is +1 or -1
  const Quad *&firstQuad = closestQuads[0];
  if((dist2 < currentDist && pt[c] != l) || dist2 == 0) { 
    // pt is either on the plane of the quad, or is the closest so far
    currentDist = dist2;
    if(dot > 0) {
      inCategory = ELEMENT_NODE_OUT;
      firstQuad = quad;
      return;
    }
    else if(dot < 0) {
      inCategory = ELEMENT_NODE_IN;
      firstQuad = quad;
      return;
    }
    else if(dist2 == 0) {
      //oofcerr << "\nface c = " << c << " l = " << l << " norm = " << quad->norm << " currentDist = " << currentDist << std::endl;
      if( pt[VoxelSetBoundary::proj_dirs[c][0]] == quad->coords[0][0] ||
	  pt[VoxelSetBoundary::proj_dirs[c][1]] == quad->coords[0][1] ||
	  pt[VoxelSetBoundary::proj_dirs[c][0]] == quad->coords[2][0] ||
	  pt[VoxelSetBoundary::proj_dirs[c][1]] == quad->coords[2][1] )
	{
	  // pt is actually on the edge of the quad
	  if(inCategory == ELEMENT_NODE_ON_EDGE) {
	    // it's not the first point on the edge
	    closestQuads.push_back(quad);
	  }
	  else {
	    assert(closestQuads.size() == 1);
	    firstQuad = quad;
	  }
	  inCategory = ELEMENT_NODE_ON_EDGE;
	}
      else {
	inCategory = ELEMENT_NODE_ON;
	assert(closestQuads.size() == 1);
	firstQuad = quad;
      }
      return;
    }
  }
  else if(dist2 == currentDist) {
#ifdef DEBUG
    if(firstQuad == NULL)
      throw ErrProgrammingError("closest quad not initialized",
				__FILE__, __LINE__);
#endif
    // In this case, choose the quad with the longer perpendicular distance
    if(inCategory == ELEMENT_NODE_OUT && dot < 0) {
      if( fabs(dist) > fabs(pt[firstQuad->norm_dir]-firstQuad->height) ) {
	inCategory = ELEMENT_NODE_IN;
	assert(closestQuads.size() == 1);
	firstQuad = quad;
      }
    }      
    if(inCategory == ELEMENT_NODE_IN && dot > 0) {
      if( fabs(dist) > fabs(pt[firstQuad->norm_dir]-firstQuad->height) ) {
	inCategory = ELEMENT_NODE_OUT;
	assert(closestQuads.size() == 1);
	firstQuad = quad;
      }
    }
  }
}

enum ElPointLocation {ELPOINTINSIDE, ELPOINTOUTSIDE, ELPOINTUNKNOWN};

static ElPointLocation elementPointInCategoryForFace(
				     const Quad *quad,
				     const std::vector<Coord> &epts,
				     int *ptIds, int k, Coord fnormal)
{
  if(quad->norm == fnormal[quad->norm_dir])
    return ELPOINTINSIDE;
  else if(quad->norm == -1*fnormal[quad->norm_dir])
    return ELPOINTOUTSIDE;
  else {
    int c = quad->norm_dir;
    double dot;
    if(epts[ptIds[k]][c] != epts[ptIds[(k+1)%3]][c]) 
      dot = quad->norm * (epts[ptIds[(k+1)%3]][c]-epts[ptIds[k]][c]);
    else
      dot = quad->norm * (epts[ptIds[(k+2)%3]][c]-epts[ptIds[k]][c]);
    // If the two edges would give different answers, then we cannot
    // determine if the element node is in or out for this element
    // face based on this VGB face. This shouldn't happen.
    if(epts[ptIds[k]][c] != epts[ptIds[(k+1)%3]][c] &&
       epts[ptIds[k]][c] != epts[ptIds[(k+2)%3]][c] &&
       ((epts[ptIds[(k+1)%3]][c] - epts[ptIds[k]][c])*
	(epts[ptIds[(k+2)%3]][c] - epts[ptIds[k]][c])) < 0)
      {
	return ELPOINTUNKNOWN;
      }
    if(dot < 0)
      return ELPOINTINSIDE;
  }
  return ELPOINTOUTSIDE;
}

// angdist holds the "angular distance" for each edge: a measure that
// is positive if the element edge has a projection within the quad
// and negative if it does not. the return value is whether the
// element face overlaps the quad.
static bool elEdgeQuadAngularDistance(const Quad *closestQuad, 
				      double elEdge[2][3],
				      const Coord &node,
				      double angdist[2], bool perp[2],
				      bool print=false) 
{
  // the first index of dot refers to the element edge while the
  // second is for the quad edge. the first index of elEdgeN refers to
  // the element edge, while the second is for the two coordinates in
  // the plane. The indices of onQuadEdge refer to the quad edge
  // directions. The indices of perp refer to the element edges.
  double elEdgeN[2][2];
  int dir = closestQuad->norm_dir;

  double dot[2][2];
  for(int i=0; i<2; ++i)
    for(int j=0; j<2; ++j)
      dot[j][i] = 0;

  perp[0] = perp[1] = false;

  for(int j=0; j<2; ++j) {
    if(elEdge[j][VoxelSetBoundary::proj_dirs[dir][0]] == 0 &&
       elEdge[j][VoxelSetBoundary::proj_dirs[dir][1]] == 0) 
      {
	angdist[j] = 0;
	perp[j] = true;
	continue;
      }
    double norm2 = 0;
    for(int i=0; i<2; ++i)
      norm2 += (elEdge[j][VoxelSetBoundary::proj_dirs[dir][i]] *
		elEdge[j][VoxelSetBoundary::proj_dirs[dir][i]]);
    double norm = sqrt(norm2);
    for(int i=0; i<2; ++i)
      elEdgeN[j][i] = elEdge[j][VoxelSetBoundary::proj_dirs[dir][i]]/norm;
  }

  bool onQuadEdge[2] = {false, false};

  for(int i=0; i<2; ++i) {
    if(node[VoxelSetBoundary::proj_dirs[dir][i]] == closestQuad->coords[0][i]) {
      onQuadEdge[i] = true;
      if(!perp[0]) dot[0][i] = elEdgeN[0][i];
      if(!perp[1]) dot[1][i] = elEdgeN[1][i];
    }
    else if(node[VoxelSetBoundary::proj_dirs[dir][i]] ==
	    closestQuad->coords[2][i])
      {
	onQuadEdge[i] = true;
	if(!perp[0]) dot[0][i] = -1 * elEdgeN[0][i];
	if(!perp[1]) dot[1][i] = -1 * elEdgeN[1][i];
      }
  }

  bool overlap = false;

  if(onQuadEdge[0] && !onQuadEdge[1]) {
    if(!perp[0])
      angdist[0] = dot[0][0];
    if(!perp[1])
      angdist[1] = dot[1][0];
    overlap = !(dot[0][0] <= 0 && dot[1][0] <= 0);
  }
  else if(onQuadEdge[1] && !onQuadEdge[0]) {
    if(!perp[0])
      angdist[0] = dot[0][1];
    if(!perp[1])
      angdist[1] = dot[1][1];
    overlap = !(dot[0][1] <= 0 && dot[1][1] <= 0);
  }
  else {
    // this combination of dot products gives us the right sign.
    if(!perp[0])
      angdist[0] = dot[0][0] + dot[0][1] - 1;
    if(!perp[1])
      angdist[1] = dot[1][0] + dot[1][1] - 1;
    if(!perp[0] && !perp[1]) {
      // if either edge is within first quadrant or both edges are on
      // the border
      if( (dot[0][0] > 0 && dot[0][1] > 0) || 
	  (dot[1][0] > 0 && dot[1][1] > 0) ||
	  (angdist[0] == 0 && angdist[1] == 0))
	overlap = true;
      else
	overlap = (isIntersection(dot[0], dot[1], 0, print) ||
		   isIntersection(dot[0], dot[1], 1, print));
    }
  }
  return ( (!perp[0] && !perp[1]) && overlap );
} // end elEdgeQuadAngularDistance

// Calculate the contributions to the areas of each tet face and the
// intersections on each tet edge for cases where all the tet points
// are inside a quad. Return the area of the tet intersection which
// will be used to find the volume contribution of the quad for the
// category.
static double tetPointsInsideQuadContrib(
			 TetIntersectionPoints &tetPoints,
			 std::vector<double> &facearea, 
			 int c, int l, 
			 const std::vector<Coord> &epts, 
			 int fpi[4][3], CellEdge &elementEdgeData,
			 const Quad *quad, bool print) 
{
  double basearea = 0.0;
  TetIntersectionPoints::iterator here, next, prev;
  unsigned int num = tetPoints.size();

  // Loop over the tet points.
  for(unsigned int k = 0; k < num; ++k) {
    TetIntersectionPoint &here = tetPoints[k];
    TetIntersectionPoint &next = tetPoints[(k+1)%num];
    TetIntersectionPoint &prev = tetPoints[(k+num-1)%num];

    // Convert the coordinates back to 3D.
    double p1[3], p2[3];
    p1[c] = p2[c] = l;
    p1[VoxelSetBoundary::proj_dirs[c][0]] = here.x[0];
    p1[VoxelSetBoundary::proj_dirs[c][1]] = here.x[1];
    p2[VoxelSetBoundary::proj_dirs[c][0]] = next.x[0];
    p2[VoxelSetBoundary::proj_dirs[c][1]] = next.x[1];

    // Get the face ids, edge ids and parametric coordinates.
    int face0 = getFaceBetweenTetPoints(prev,here);
    int face1 = getFaceBetweenTetPoints(next,here);
    int edgeId = CSkeletonElement::faceFaceEdge[face0][face1];
    if(edgeId == -1)
      throw ErrProgrammingError("Could not determine element edge.",
				__FILE__, __LINE__);
    int *ptIds = vtkTetra::GetEdgeArray(edgeId);
    if(here.node == ptIds[0])
      here.t = 0.0;
    else if(here.node == ptIds[1])
      here.t = 1.0;

    // Add the points to the tet edge intersections if the points are
    // on a tet edge.
    if(here.node == -1 || prev.node == -1) {
      addIntersectionToEdgeData(p1, here.t, edgeId, face0, 
				epts, elementEdgeData, quad,
				UNCATEGORIZED_INTERSECTION, print);
    }
    if(here.node == -1 || next.node == -1) {
      addIntersectionToEdgeData(p1, here.t, edgeId, face1, 
				epts, elementEdgeData, quad, 
				UNCATEGORIZED_INTERSECTION, print);
    }

    // Add the contribution of this segment to the area of the tet-quad
    // intersection.
    basearea += (1.0/2.0)*(p1[VoxelSetBoundary::proj_dirs[c][0]]*
			   p2[VoxelSetBoundary::proj_dirs[c][1]] -
			   p1[VoxelSetBoundary::proj_dirs[c][1]]*
			   p2[VoxelSetBoundary::proj_dirs[c][0]]);

    // Finally add the contribution to the area on the tet faces. We
    // don't include contributions for points that are on the same
    // edge -- this can only happen if they are both nodes.
    if(here.node == -1 || next.node == -1) {
      int face = getFaceBetweenTetPoints(here, next);
      facearea[face] += (-quad->norm/2.0)*(p1[fpi[face][0]]*p2[fpi[face][1]] -
					   p1[fpi[face][1]]*p2[fpi[face][0]]);
    }
  }
  return basearea;
} // end tetPointsInsideQuadContrib

// Find the points where the tet defined by epts crosses axis-aligned
// plane where component c equals l and store them in tetPoints with
// their topological information.
static void findTetPlaneIntersectionPoints(const std::vector<Coord> &epts,
					   int c, int l,
					   TetIntersectionPoints &tetPoints) 
{
  // The element nodes above the plane and under the plane.
  std::vector<int> overnodes, undernodes;

  // Find which element points are on, above, or below the
  // plane, add them to tetPoints, and set their topological
  // information.
  for(unsigned int k=0; k<NUM_TET_NODES; ++k) {
    if(epts[k][c] == l) {
      // The node is on the plane.  Create an intersection point with
      // edge id set to -1 to indicate that it is coincident with
      // element nodes.
      // TODO: Rather than set edge=-1 for node intersections and
      // node=-1 for edge intersections, use subclasses of
      // TetIntersectionPoint.
      TetIntersectionPoint tp;
      tp.x[0] = epts[k][VoxelSetBoundary::proj_dirs[c][0]];
      tp.x[1] = epts[k][VoxelSetBoundary::proj_dirs[c][1]];
      tp.edge = -1;
      tp.node = k;
      tp.t = -1;
      tp.dist2 = tp.tan = 0.0;
      tetPoints.push_back(tp);
    }
    else { 
      if(epts[k][c] < l)
	undernodes.push_back(k);
      else if(epts[k][c] > l)
	overnodes.push_back(k);
    }
  }
	
  unsigned int novernodes = overnodes.size();
  unsigned int nundernodes = undernodes.size();
  // Calculate the seg plan intersections if we haven't
  // already found that a whole face is on the plane and there
  // are at least three tet intersection points on the plane.
  if((tetPoints.size() < NUM_TET_FACE_EDGES) &&
     (tetPoints.size()+novernodes*nundernodes) > 2) 
    {
      // Loop over the undernodes and overnodes to find segments that
      // actually intersect the plane.
      for(unsigned int k=0; k<novernodes; ++k) {
	for(unsigned int m=0; m<nundernodes; ++m) {
	  TetIntersectionPoint tp;
	  // Find the edge id of the intersection
	  tp.edge = CSkeletonElement::nodeNodeEdge[overnodes[k]][undernodes[m]];
	  // Get the ptIds of the edge in the right order
	  int *ptIds = vtkTetra::GetEdgeArray(tp.edge);
	  // The intersection coordinates are put directly into t and x.
	  segPlaneInt(epts[ptIds[0]], epts[ptIds[1]],
		      VoxelSetBoundary::proj_dirs[c], c, l, tp.t, tp.x);
	  // The node id is set to -1 because these are edge
	  // intersections.
	  tp.node = -1;
	  tp.dist2 = tp.tan = 0.0;
	  tetPoints.push_back(tp);
	}
      }
      // Sort the tet intersections into a convex hull
      convexHull(tetPoints);
    }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// This checks the looseEnds structure for identical corner points in
// iPoints and merges the topological information.

static void enforceTopo(IntersectionPoints &iPoints,
			std::vector<FaceIntersectionMap> &looseEnds, 
			const Quad *current_quad,
			Coord fnormal[NUM_TET_FACES], 
			int fpi[NUM_TET_FACES][3],
			bool outside, bool print,
			const std::vector<Coord> &epts)
{
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  unsigned int num = iPoints.size();
  if(num == 0)
    return;

  std::vector<bool> changed(num, false);
  std::vector<bool> fbefore(num, true);
  std::vector<bool> fafter(num, true); // initial value doesn't matter...

  // First loop over points and check topological information.
  for(unsigned int k=0; k<num; ++k) {
    IntersectionPoint *ip1 = iPoints[k];
    
// #ifdef DEBUG
//     if(print) {
//       oofcerr << "enforceTopo: enforcing topo for " << *ip1 << std::endl;
//     }
// #endif	// DEBUG
    // For corners, check if there is an exact coordinate match in
    // loose ends and make sure topological information is consistent
    unsigned int n = (ip1->corner? 3 : 1);
    // Loop over the possible hash values
    for(unsigned int m=0; m<n; ++m) {
      bool foundmatch = false;
      // Loop over looseEnds bins - one for each face plus one extra.
      for(unsigned int j=0; j<NUM_TET_FACES+1; ++j) {
	// Find loose ends in bin j that match hash m and loop over them.
	std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator> 
	  matches;
	matches = looseEnds[j].equal_range(ip1->hash[m]);
	// If any of the matches have changed, we'll recalculate the
	// contributions for all of them.
	if(matches.first != looseEnds[j].end()) {
	  // "fbefore[k] &= iPointEtc" doesn't work with std::vector<bool>
	  fbefore[k] = fbefore[k] && iPointOnFace((*matches.first).second.ip);
	}
	for(FaceIntersectionMap::iterator it = matches.first;
	    it != matches.second; ++it)
	  {
	    // compare the coord of ip1 to the coord in the hash match
	    // to detect match
	    //* TODO 3.1: Make IntersectionPoint a class (not a struct)
	    //* and give it an operator==.
	    if(ip1->x[0] == (*it).second.ip->x[0] &&
	       ip1->x[1] == (*it).second.ip->x[1] && 
	       ip1->x[2] == (*it).second.ip->x[2]) 
	      {

// #ifdef DEBUG
// 	    if(print) {
// 	      oofcerr << "enforceTopo: found match "
// 			<< ip1->x[0] << ", " << ip1->x[1] << ", " << ip1->x[2]
// 			<< " " 
// 			<< (*it).second.ip->x[0] << ", "
// 			<< (*it).second.ip->x[1] << ", "
// 			<< (*it).second.ip->x[2] << " ";
// 	      oofcerr << ip1->faces[0] << ip1->faces[1] << ip1->faces[2]
// 			<< ip1->faces[3] << " ";
// 	      oofcerr << ip1->edges[0] << ip1->edges[1] << ip1->edges[2]
// 			<< ip1->edges[3] << ip1->edges[4] 
// 			<< ip1->edges[5] << " " << ip1->corner << std::endl;
// 	      oofcerr << "face " << j << " hash " << ip1->hash[m]
// 			<< std::endl;
// 	      oofcerr << fbefore[k] << " " << fafter[k] << std::endl;
// 	    }
// #endif	// DEBUG

	    foundmatch = true;
	    // set the last argument (same face) to false so that
	    // addToLooseEnds will handle the corner status and hash.
	    changed[k] = (changed[k] ||
			  mergeTopologicalInfo(ip1,(*it).second.ip,false,epts));
	    fafter[k] = iPointOnFace((*it).second.ip);

// #ifdef DEBUG
// 	    if(print && changed[k]) {
// 	      oofcerr << "enforceTopo: new topo: ";
// 	      oofcerr << ip1->faces[0] << ip1->faces[1] << ip1->faces[2]
// 		   << ip1->faces[3] << " ";
// 	      oofcerr << ip1->edges[0] << ip1->edges[1] << ip1->edges[2]
// 		   << ip1->edges[3] << ip1->edges[4] << ip1->edges[5]
// 		   << " " << ip1->corner << std::endl;
// 	    }
// #endif	// DEBUG
	  } // end if coords agree
	} // end loop over hash matches
      }	// end loop over looseEnds bins j
    } // end loop over hashes
  } // end loop over points k

  // TODO OPT: calculate all new topos first, then do separate loop for
  // results. If two new face points are found, add their
  // contributions.

  for(unsigned int k=0; k<num; ++k) {
    IntersectionPoint *ip0 = iPoints[(k+num-1)%num];
    IntersectionPoint *ip1 = iPoints[k];
    IntersectionPoint *ip2 = iPoints[(k+1)%num];
    unsigned int n = (ip1->corner? 3 : 1);
    // if(ip1->corner) 
    //   n = 3;
    // else
    //   n = 1;

    // Loop over the possible hash values
    for(unsigned int m=0; m<n; ++m) {
      // Loop over looseEnds bins - one for each face plus one extra.
      for(unsigned int j=0; j<NUM_TET_FACES+1; ++j) {

	// Find loose ends in bin j that match hash m and loop over them.
	std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator> 
	  matches = looseEnds[j].equal_range(ip1->hash[m]);
// #ifdef DEBUG
// 	if(print) {
// 	  oofcerr << "enforceTopo: examining ip1 ("
// 		  << ip1->x[0] << ", " << ip1->x[1] << ", " << ip1->x[2]
// 		  << ") " << (matches.first == matches.second)
// 		  << " fafter=" << fafter[k] << fbefore[k]
// 		  << fafter[(k+1)%num] << fbefore[(k+1)%num]
// 		  << fafter[(k+num-1)%num] << fbefore[(k+num-1)%num]
// 		  << std::endl;
// 	}
// #endif // DEBUG

	for(FaceIntersectionMap::iterator it = matches.first;
	    it != matches.second; ++it)
	  {
	    // compare the coord of ip1 to the coord in the hash match
	    // to detect match
	    if(ip1->x[0] == (*it).second.ip->x[0] &&
	       ip1->x[1] == (*it).second.ip->x[1] &&
	       ip1->x[2] == (*it).second.ip->x[2])
	      {
		// If a point in the extra bin has been added to a
		// face, we must calculate its contribution to the
		// area of the face and store it.
		if(j == NUM_TET_FACES && fafter[k] &&
		   (!fbefore[k] || (fafter[(k+1)%num] && !fbefore[(k+1)%num])
		    || (fafter[(k+num-1)%num] && !fbefore[(k+num-1)%num]))) 
		  {
		    double *p1 = (*it).second.ip->x;
		    double *p2 = (*it).second.op->x;
		    int faceId = -1;
		    for(int l = 0; l < NUM_TET_FACES; ++l)
		      if((*it).second.ip->faces[l]) faceId = l;
		    if(faceId == -1)
		      throw ErrProgrammingError(
				"CSkeletonElement: could not identify face id",
				__FILE__, __LINE__);
		    //const Quad *quad = (*it).second.quad;
		    IntersectionCategory type = (*it).second.type;
		    // TODO OPT: Quad member still needed?
		    //double contrib = (-quad->norm/2.0)*(p1[fpi[faceId][0]]*p2[fpi[faceId][1]]-
		    //p1[fpi[faceId][1]]*p2[fpi[faceId][0]]);
		    double contrib = (0.5*(type == ENTRANCE_INTERSECTION ?
					   1 : -1))*
		      (p1[fpi[faceId][0]]*p2[fpi[faceId][1]] - 
		       p1[fpi[faceId][1]]*p2[fpi[faceId][0]]);
// #ifdef DEBUG
// 		    if(print)
// 		      oofcerr << "enforceTopo: old contrib "
// 			      << (*it).second.contrib << std::endl;
// #endif // DEBUG
		    (*it).second.contrib = contrib;
// #ifdef DEBUG
// 		    if(print) {
// 		      oofcerr << "enforceTopo: ip "
// 			      << p1[0] << ", " << p1[1] << ", "
// 			      << p1[2] << " op " << p2[0] << ", "
// 			      << p2[1] << ", " << p2[2] << std::endl;
// 		      oofcerr << "enforceTopo: new contrib " << contrib 
// 			      << std::endl;
// 		    }
// #endif	// DEBUG
		  }
		
	      }
	  }
      }
    }

    // If ip1 is a corner and still not a face point, add it to the
    // extra bin in looseEnds. If it is an edge point, add it to the
    // extra bin whether it's a corner or not. If it is outside, also
    // add it to the extra bin. If it grazes the face with neither
    // neighbor on the same face, then also add it to the extra bin.
    bool graze = false;
    if(iPointOnFace(ip1)) {
      int faceId = -1;
      for(int k = 0; k < NUM_TET_FACES; ++k)
	if(ip1->faces[k])
	  faceId = k;
      graze = !(ip0->faces[faceId] || ip2->faces[faceId]);
    }
    if((ip1->corner && 
	(!ip1->faces[0] && !ip1->faces[1] && !ip1->faces[2] && !ip1->faces[3]))
       ||
       (ip1->edges[0] || ip1->edges[1] || ip1->edges[2] || ip1->edges[3] ||
	ip1->edges[4] || ip1->edges[5]) 
       || outside || graze) 
      {
	FaceIntersection fi1, fi2;
	fi1.ip = ip1;
	fi1.op = ip2;
	fi1.type = (current_quad->norm == -1 ?
		    ENTRANCE_INTERSECTION : EXIT_INTERSECTION);
	fi1.contrib = 0;
	fi1.outside = outside;
	fi1.quad = current_quad;
	fi1.matches = 1;
	fi1.paired = false;
	fi2 = fi1;
	fi2.op = ip0;
	fi2.type = (current_quad->norm == -1 ?
		    EXIT_INTERSECTION : ENTRANCE_INTERSECTION);
// #ifdef DEBUG
// 	if(print) {
// 	  oofcerr << "adding loose end to extra bin "
// 		    << ip1->x[0] << ", " << ip1->x[1] << ", " << ip1->x[2]
// 		    <<  " op " 
// 		    << ip2->x[0] << ", " << ip2->x[1] << ", " << ip2->x[2]
// 		    << " " << graze << std::endl;
// 	  oofcerr << "adding loose end to extra bin "
// 		    << ip1->x[0] << ", " << ip1->x[1] << ", " << ip1->x[2]
// 		    <<  " op "
// 		    << ip0->x[0] << ", " << ip0->x[1] << ", " << ip0->x[2]
// 		    << std::endl;
// 	}
// #endif	// DEBUG
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

	for(unsigned int m=0; m<3; ++m) {
	  looseEnds[NUM_TET_FACES].insert(
					  FaceIntersectionDatum(ip1->hash[m], fi1));
	  looseEnds[NUM_TET_FACES].insert(
			FaceIntersectionDatum(ip1->hash[m], fi2));
	}
      }
  }
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  // Check for any newly detected dupes and remove them.
  if(num == 2) {
    if(isDupe(iPoints[0], iPoints[1], fnormal, -1, print, epts))
      iPoints.erase(iPoints.begin());
  }
  else {
    std::set<int> dupes;
    for(unsigned int k=0; k<num; ++k) {
      IntersectionPoint *ip1 = iPoints[k];
      IntersectionPoint *ip2 = iPoints[(k+1)%num];
      if(isDupe(ip1, ip2, fnormal, -1, print, epts)) {
	dupes.insert(k);
// #ifdef DEBUG
// 	if(print) 
// 	  oofcerr << "enforceTopo: removing dupe" << std::endl;
// #endif // DEBUG
      }
    }

    // If dupes were found, rebuild iPoints
    if(!dupes.empty()) {
      IntersectionPoints temp(iPoints);
      iPoints.clear();
      for(unsigned int k=0; k<num; ++k) {
	if(dupes.find(k) == dupes.end())
	  iPoints.push_back(temp[k]);
      }
    }
  }
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

} // end enforceTopo

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given intersection points that represent the intersection of a quad
// and a tet, calculate the contributions to the overall category
// volume, the faceareas, the element edge intersections, and the
// loose ends. Return the overall category volume contribution.
static double iPointsContribution(IntersectionPoints &iPoints, 
				  const Quad *current_quad,
				  const std::vector<Coord> &epts, 
				  std::vector<double> &facearea,
				  std::vector<FaceIntersectionMap> &looseEnds,
				  CellEdge &elementEdgeData, int c, int l, 
				  Coord fnormal[NUM_TET_FACES],
				  int fpi[NUM_TET_FACES][3], bool outside,
				  bool print) 
{
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  double basearea = 0;
  // assert(Quad::validQuad(current_quad));
  unsigned int num = iPoints.size();
  for(unsigned int k=0; k<num; ++k) {
    IntersectionPoint *ip1 = iPoints[k];
    IntersectionPoint *ip2 = iPoints[(k+1)%num];
    double *p1 = ip1->x;	// real space coord (double[3])
    double *p2 = ip2->x;
    if(!outside)
      basearea += 0.5*(p1[VoxelSetBoundary::proj_dirs[c][0]]*
		       p2[VoxelSetBoundary::proj_dirs[c][1]] -
		       p1[VoxelSetBoundary::proj_dirs[c][1]]*
		       p2[VoxelSetBoundary::proj_dirs[c][0]]);
// #ifdef DEBUG
//     oofcerr << "points (" << p1[0] << ", " << p1[1] << ", " << p1[2]
// 	      << ") (" << p2[0] << ", " << p2[1] << ", " << p2[2] << ")"
// 	      << " contrib "
// 	      << (1.0/2.0)*(p1[proji[0]]*p2[proji[1]]-p1[proji[1]]*p2[proji[0]])
// 	      << std::endl;
// #endif  // DEBUG
    for(unsigned int m=0; m<4; ++m) {
      if(ip1->faces[m] && ip2->faces[m] && 
	 // we don't want to consider points that are both on the same edge
	 !((ip1->edges[CSkeletonElement::faceEdges[m][0]] &&
	    ip2->edges[CSkeletonElement::faceEdges[m][0]]) ||
	   (ip1->edges[CSkeletonElement::faceEdges[m][1]] &&
	    ip2->edges[CSkeletonElement::faceEdges[m][1]]) ||
	   (ip1->edges[CSkeletonElement::faceEdges[m][2]] &&
	    ip2->edges[CSkeletonElement::faceEdges[m][2]])) ) 
	{
	  double contrib = (-current_quad->norm/2.0) *
	    (p1[fpi[m][0]]*p2[fpi[m][1]]-p1[fpi[m][1]]*p2[fpi[m][0]]);
// #ifdef DEBUG
// 	  if(print)
// 	    oofcerr << "iPointsContribution: contribution=" << contrib
// 		    << std::endl;
// #endif // DEBUG
	  facearea[m] += contrib;

// #ifdef DEBUG
// 	  if(print) {
// 	    oofcerr << "k = " << k << " quad->norm " << current_quad->norm
// 		      << std::endl;
// 	    oofcerr << "contribution to face " << m << " "
// 		      << -0.5*current_quad->norm*(p1[fpi[m][0]]*p2[fpi[m][1]]-
// 						  p1[fpi[m][1]]*p2[fpi[m][0]])
// 		      << std::endl;
// 	  }
// #endif
// 	  print = (m == 2);

	  // add points to the loose ends
// #ifdef DEBUG
// 	  if(print)
// 	    oofcerr << "iPointsContribution: calling addToLooseEnds"
// 		    << "current_quad=" << current_quad << std::endl;
// #endif // DEBUG
	  // assert(Quad::validQuad(current_quad));
	  if(current_quad->norm == -1) {
	    addToLooseEnds(ip1, ip2, ENTRANCE_INTERSECTION, looseEnds, m,
			   fnormal[m], contrib, current_quad, outside, print);
	    addToLooseEnds(ip2, ip1, EXIT_INTERSECTION, looseEnds, m,
			   fnormal[m], contrib, current_quad, outside, print);
	  }
	  else if(current_quad->norm == 1) {
	    addToLooseEnds(ip1, ip2, EXIT_INTERSECTION, looseEnds, m,
			   fnormal[m], contrib, current_quad, outside, print);
	    addToLooseEnds(ip2, ip1, ENTRANCE_INTERSECTION, looseEnds, m,
			   fnormal[m], contrib, current_quad, outside, print);
	  }

	  // add points to edge intersection data, only one of the
	  // edges is needed.
	  if(!outside) {
	    // assert(Quad::validQuad(current_quad));
	    for(unsigned int j=0; j<3; ++j) {
	      if(ip1->edges[CSkeletonElement::faceEdges[m][j]])  {
		addIntersectionToEdgeData(
			  ip1->x,
			  ip1->t[CSkeletonElement::faceEdges[m][j]], 
			  CSkeletonElement::faceEdges[m][j],
			  m, epts, elementEdgeData, current_quad,
			  UNCATEGORIZED_INTERSECTION, print);
		break;
	      }
	    }
	    for(unsigned int j=0; j<3; ++j) {
	      if(ip2->edges[CSkeletonElement::faceEdges[m][j]]) {
		addIntersectionToEdgeData(
			  ip2->x,
			  ip2->t[CSkeletonElement::faceEdges[m][j]], 
			  CSkeletonElement::faceEdges[m][j],
			  m, epts, elementEdgeData, current_quad, 
			  UNCATEGORIZED_INTERSECTION, print);
		break;
	      }
	    }
	  }
	  
	}
    } // end loop over m
  } // end loop over iPoints k
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

// #ifdef DEBUG
//   if(print)
//     oofcerr << "basearea " << basearea 
// 	      << " height " << (current_quad->norm * l)
// 	      << " volume contrib " << (1/3.*current_quad->norm*l*basearea)
// 	      << std::endl;
// #endif	// DEBUG

  // Finally return the contribution of the quad to the overall category volume.
  return 1.0/3.0 * current_quad->norm * l * basearea;
} // end iPointsContribution


typedef std::pair<FaceIntersectionMap::iterator, FaceIntersectionMap::iterator>
FaceIntMapPair;

static void addMissingEdgeIntersections(
			std::vector<FaceIntersectionMap> &looseEnds,
			CellEdge &elementEdgeData,
			const std::vector<Coord> &epts, 
			std::vector<double> &facearea,
			Coord fnormal[NUM_TET_FACES], int faceId,
			bool print, int uid)
{
// #ifdef DEBUG
//   checkLooseEnds(looseEnds);
// #endif

  if(!looseEnds[faceId].empty()) {

// #ifdef DEBUG
//     if(print)
//       oofcerr << "addMissingEdgeIntersections: faceId=" << faceId 
// 	      << " # of loose ends=" << looseEnds[faceId].size() << std::endl;
// #endif
    // FaceIntersectionMap is std::multimap<int, FaceIntersection>.
    // class FaceIntersection is defined in earlier in this file.

    // trash holds items being deleted from the map.  We can't delete
    // some of them right away because we're iterating over the map.
    std::vector<FaceIntersectionMap::iterator> trash;

    for(FaceIntersectionMap::iterator it = looseEnds[faceId].begin(); 
	it != looseEnds[faceId].end(); ++it)
      {
	FaceIntersection &faceInt = (*it).second;
	// assert(Quad::validQuad(faceInt.quad));
// #ifdef DEBUG
// 	if(print)
// 	  oofcerr << "addMissingEdgeIntersections: faceInt="
// 		  << faceInt << " " 
// 		  << iPointOnEdge(faceInt.ip)
// 		  <<  std::endl;      
// #endif // DEBUG
	if(iPointOnEdge(faceInt.ip)) {
// #ifdef DEBUG
// 	  if(print) 
// 	    oofcerr << "addMissingEdgeIntersections: adding " << faceInt.ip
// 		    << std::endl;
// #endif // DEBUG
	  int edgeId = -1;
	  for(int i = 0; i < 6; ++i) 
	    if(faceInt.ip->edges[i])
	      edgeId = i;
	  assert(edgeId != -1);
	  double t = faceInt.ip->t[edgeId]; // parametric pos. along edge
	  // assert(Quad::validQuad(faceInt.quad));
	  addIntersectionToEdgeData(faceInt.ip->x, t, edgeId, faceId,
				    epts, elementEdgeData, faceInt.quad,
				    faceInt.type, true);
	  // assert(Quad::validQuad(faceInt.quad));
	  for(int i=0; i<3; ++i) {
	    FaceIntMapPair matches = 
	      looseEnds[faceId].equal_range(faceInt.ip->hash[i]);
	    for(FaceIntersectionMap::iterator temp = matches.first;
		temp != matches.second; ++temp)
	      {
		if((*temp).second.type == faceInt.type) {
		  if(it == temp)
		    trash.push_back(temp);
		  else
		    looseEnds[faceId].erase(temp);
		  break;
		}		
	      }	
	  }
	  
	} // end if iPointOnEdge
// #ifdef DEBUG
// 	checkLooseEnds(looseEnds);
// #endif
      }	  // end loop over looseEnds
    // Delete FaceIntersections that couldn't be deleted earlier.
    for(std::vector<FaceIntersectionMap::iterator>::iterator i=trash.begin();
	i!=trash.end(); ++i)
      {
	looseEnds[faceId].erase(*i);
      }
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif
  } // end if looseEnds not empty
}

static void addMissingEdges(std::vector<FaceIntersectionMap> &looseEnds,
			    CellEdge &elementEdgeData,
			    const std::vector<Coord> &epts, 
			    std::vector<double> &facearea,
			    Coord fnormal[NUM_TET_FACES], int faceId,
			    bool print, int uid) 
{
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  if(looseEnds[NUM_TET_FACES].empty())
    return;
  std::vector<FaceIntersectionMap::iterator> trash;
  for(FaceIntersectionMap::iterator it = looseEnds[NUM_TET_FACES].begin(); 
      it != looseEnds[NUM_TET_FACES].end(); ++it) 
    {
      if((*it).second.ip->faces[faceId] && !(*it).second.outside &&
	 !iPointOnEdge((*it).second.ip))
	{
	  // We need to make sure we aren't applying a multiply
	  // hashed point more than once. So only use the point if
	  // the map index is the first hash value, or if the point
	  // is a corner, and the first (or first and second) hash
	  // values weren't used to begin with.
	  if((*it).first == (*it).second.ip->hash[0] ||
	     (((*it).second.ip->corner && fnormal[faceId][0] == 0 ) && 
	      (((*it).first == (*it).second.ip->hash[1]) || 
	       (fnormal[faceId][1] == 0 &&
		(*it).first == (*it).second.ip->hash[2]))))
	    {
	      // check that the point is a loose end and the opposite
	      // point is either a loose end or on the edge and not
	      // actually a dupe.
	      FaceIntersectionMap::iterator match1 = 
		looseEnds[faceId].find((*it).first);
	      FaceIntersectionMap::iterator match2 = 
		looseEnds[faceId].find((*it).second.op->hash[0]);
	      if(match1 != looseEnds[faceId].end() && 
		 (match2 != looseEnds[faceId].end() ||
		  iPointOnEdge((*it).second.op)) &&
		 (*it).second.op->faces[faceId] &&
		 !isDupe((*it).second.ip, (*it).second.op, fnormal, -1,
			 print, epts)) 
		{
		  // correct the facearea
		  facearea[faceId] += (*it).second.contrib;
		    
		  // Remove the matches from the loose ends.  Remove
		  // one match for each hash for the first point.
		  for(int i = 0; i < 3; ++i) {
		    FaceIntMapPair matches =
		      looseEnds[faceId].equal_range((*it).second.ip->hash[i]);
		    for(FaceIntersectionMap::iterator temp2 = matches.first;
			temp2 != matches.second; ++temp2) 
		      {
			if((*temp2).second.type != (*it).second.type) {
			  looseEnds[faceId].erase(temp2);
			  break;
			}		
		      }
		  }

		  // if the op is on an edge, add it
		  if(iPointOnEdge((*it).second.op)) {
		    int edgeId = -1;
		    for(int i = 0; i < 6; ++i) 
		      if((*it).second.op->edges[i])
			edgeId = i;
		    assert(edgeId != -1);
		    double t = (*it).second.op->t[edgeId];
		    // Since we are adding the op, use the opposite
		    // type given by the face intersection
		    IntersectionCategory type = 
		      ((*it).second.type == ENTRANCE_INTERSECTION ?
		       EXIT_INTERSECTION : ENTRANCE_INTERSECTION);
		    // assert(Quad::validQuad((*it).second.quad));
		    addIntersectionToEdgeData((*it).second.op->x, t, edgeId,
					      faceId, epts, 
					      elementEdgeData, 
					      (*it).second.quad, type, print);
		  }
		  // otherwise remove the matches
		  else {
		    // Remove one entry of opposite point for each
		    // hash value.
		    // TODO 3.1: MAYBE simplify code like this elsewhere
		    for(int i = 0; i < 3; ++i) {
		      FaceIntMapPair matches = 
			looseEnds[faceId].equal_range((*it).second.op->hash[i]);
		      for(FaceIntersectionMap::iterator temp2 = matches.first;
			  temp2 != matches.second; ++temp2) 
			{
			  if((*temp2).second.type == (*it).second.type) {
			    // It's safe to erase temp2 from
			    // looseEnds, because *it can't be *temp2.
			    assert(it != temp2);
			    looseEnds[faceId].erase(temp2);
			    break;
			  }		
			}
		    }
		  }
		  if(removeLooseEnds(looseEnds, faceId, &it, print))
		    trash.push_back(it);
		} // if !isDupe
	    }
	}
    } // end loop over looseEnds

  for(std::vector<FaceIntersectionMap::iterator>::iterator i=trash.begin(); 
      i!=trash.end(); ++i)
    {
      looseEnds[faceId].erase(*i);
    }
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

} // end addMissingEdges

// Remove looseEnds, then remove spurious edges, then convert any
// remaining looseEnds to edge intersections.
static void processLooseEnds(
	     std::vector<FaceIntersectionMap> looseEnds,
	     CellEdge &elementEdgeData,
	     const std::vector<Coord> &epts, 
	     std::vector<double> facearea,
	     Coord fnormal[NUM_TET_FACES], int faceId,
	     bool print, int uid)
{
  // epts[i] is the position of node i of a tet in pixel-space coordinates
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

  int *ptIds = vtkTetra::GetFaceArray(faceId);

  // Remove the loose ends that are corners of the quads. This
  // is done after the loop over quads is completed because all
  // the corner loose ends must be gathered before matching them
  // up in pairs.
  removeLooseEnds(looseEnds, faceId, NULL, print);

  // Detect and add any missing edge intersections
  addMissingEdgeIntersections(looseEnds, elementEdgeData, epts, facearea,
			      fnormal, faceId, print, uid);

  // Detect and add any missing edges
  addMissingEdges(looseEnds, elementEdgeData, epts, facearea, fnormal, faceId,
		  print, uid);

  // Detect and remove spurious edges using the looseEnds
  removeSpuriousEdges(looseEnds, elementEdgeData, facearea, fnormal, faceId,
		      print, epts);

  // If there are still any looseEnds left on the faces, convert
  // them into intersections.
  if(!looseEnds[faceId].empty()) {

    for(FaceIntersectionMap::iterator it = looseEnds[faceId].begin();
	it != looseEnds[faceId].end(); ++it) 
      {
	// (*it).first is a hash of a point.
	// (*it).second is a FaceIntersection, which is a struct
	// defined in cskeletonelement.h.

// #ifdef DEBUG
//       if(print) {
// 	oofcerr << "loose ends after removing edges: " << std::endl;
// 	oofcerr << "\n" << (*it).first << " " << (*it).second.ip->x[0] << ", "
// 		  << (*it).second.ip->x[1] << ", " << (*it).second.ip->x[2];
// 	oofcerr << " " << (*it).second.ip->corner << " hashes: "
// 		  << (*it).second.ip->hash[0] << ",";
// 	oofcerr << (*it).second.ip->hash[1] << ","
// 		  << (*it).second.ip->hash[2];
// 	oofcerr << " op " << (*it).second.op->x[0] << ", "
// 		  << (*it).second.op->x[1] << ", " << (*it).second.op->x[2];
// 	oofcerr  << std::endl;
//       }
// #endif // DEBUG

      // We need to make sure we aren't applying a multiply hashed
      // point more than once. So only use the point if the map index
      // is the first hash value, or if the point is a corner, and the
      // first (or first and second) hash values weren't used to begin
      // with.
      if((*it).first == (*it).second.ip->hash[0] ||
	 (((*it).second.ip->corner && fnormal[faceId][0] == 0 ) && 
	  (((*it).first == (*it).second.ip->hash[1]) || 
	   (fnormal[faceId][1] == 0 &&
	    (*it).first == (*it).second.ip->hash[2]))))
	{

// #ifdef DEBUG
// 	if(print)
// 	  oofcerr << "creating intersection from this loose end, type = "
// 		    << (*it).second.type << std::endl;
// #endif	// DEBUG
	      
	// Find the element edge with the minimum perpendicular distance.
	double t = 0;
	Coord y;
	double mindist2 = std::numeric_limits<double>::max();
	int minEdge = -1;
	for(unsigned int k=0; k<NUM_TET_FACE_EDGES; k++) {
	  double dist2;
	  double u;		// parametric coord along line
	  Coord x;		// nearest point on line
	  if(CSkeletonElement::faceEdgeDirs[faceId][k] == 1)
	    // stupid vtk doesn't have const args
	    dist2 = vtkLine::DistanceToLine(
		    (*it).second.ip->x,
		    const_cast<double*>(epts[ptIds[k]].xpointer()),
		    const_cast<double*>(epts[ptIds[(k+1)%NUM_TET_FACE_EDGES]].xpointer()),
		    u, x);
	  else
	    dist2 = vtkLine::DistanceToLine(
		    (*it).second.ip->x,
		    const_cast<double*>(epts[ptIds[(k+1)%NUM_TET_FACE_EDGES]].xpointer()), 
		    const_cast<double*>(epts[ptIds[k]].xpointer()),
		    u, x);
	  if(dist2 < mindist2) {
	    mindist2 = dist2;
	    minEdge = CSkeletonElement::faceEdges[faceId][k];
	    t = u;
	    y = x;
	  }
	} // end loop over edges k of face faceId
	assert(minEdge != -1);

// #ifdef DEBUG
// 	if(print)
// 	  oofcerr << "closest edge " << minEdge << " mindist " << mindist2
// 		    << " " << t << " " << y << " type " << (*it).second.type
// 		  << std::endl;
// 	if(mindist2 > 1e-5) {
// 	  oofcerr << "processLooseEnds: closest edge=" << minEdge
// 		  << " mindist=" << mindist2
// 		  << " t=" << t << " y=" << y
// 		  << " type=" << (*it).second.type << " uid=" << uid 
// 		  << std::endl;
// 	  throw ErrProgrammingError(
// 		    "CSkeletonElement: suspicious loose end intersection",
// 		    __FILE__, __LINE__);
// 	}
// #endif	// DEBUG

	// Convert the point to an intersection and add it to elementEdgeData
	looseEndToEdgeIntersection(y, t, minEdge, faceId, elementEdgeData,
				   (*it).second.type);
	      
      }	// end check for multiply hashed point
    } // end loop over FaceIntersectionMap iterator it

  } // end if(!looseEnds[faceId].empty()) 
// #ifdef DEBUG
//     checkLooseEnds(looseEnds);
// #endif

}   // end processLooseEnds

// Remove duplicate element edge intersections at corners.
static void removeDuplicateElementEdgeIntersections(CellEdge &elementEdgeData,
						    int faceId, bool print) 
{
   // loop through in order and check for duplicate entries at corners
  for(int k=0; k<NUM_TET_FACE_EDGES; k++) {
    int edgeId = CSkeletonElement::faceEdges[faceId][k];
    int edgeDir = CSkeletonElement::faceEdgeDirs[faceId][k];
    // oofcerr << "k = " << k << " edgeID " << edgeId << std::endl;
    // oofcerr << "size of vector " << elementEdgeData[edgeId].size()
    // 	      << std::endl;
    for(CellEdgeMap::iterator here = elementEdgeData[edgeId].begin();
	here!=elementEdgeData[edgeId].end(); ++here)
      {

// #ifdef DEBUG
// 	if(print)
// 	  oofcerr << "removeDuplicateElementEdgeIntersections: " 
// 		  << edgeId << " " << edgeDir << " " << (*here).first << " "
// 		  << (*here).second.location << " "
// 		  << (*here).second.getType(faceId) << std::endl;
// #endif	// DEBUG

      // first check if we are on a corner and the next edge
      // contains an identical intersection TODO OPT: this can
      // probably be avoided if we choose a convention for which
      // edge to put intersections that coincide with a node on
	int edgeId2 =
	  CSkeletonElement::faceEdges[faceId][(k+1)%NUM_TET_FACE_EDGES];
	int edgeDir2 =
	  CSkeletonElement::faceEdgeDirs[faceId][(k+1)%NUM_TET_FACE_EDGES];
	// only do this check if the next edge has any intersections
	if(!elementEdgeData[edgeId2].empty()) {
	  if((edgeDir==1 && (*here).first==1.0) ||
	     (edgeDir==-1 && (*here).first==0.0) ) 
	    {
	      CellEdgeMap::iterator here2;
	      if(edgeDir2==1)
		here2 = elementEdgeData[edgeId2].begin();
	      else {
		here2 = elementEdgeData[edgeId2].end();
		--here2;
	      }
	      if((edgeDir2==1 && (*here2).first==0.0) ||
		 (edgeDir2==-1 && (*here2).first==1.0))
		{
// #ifdef DEBUG
// 		  if(print)
// 		    oofcerr << "removeDuplicateElementEdgeIntersections: combining coincident intersections"
// 			      << std::endl;
// #endif // DEBUG
		  (*here).second.combine(faceId, (*here2).second);
		  
		}
	    }
	}
      }
  }
}

// Calculate the contribution to the element face area, modifying the
// facearea pointer. Pass back the height.  Called from
// categoryVolumes().

static double elementFaceContribution(CellEdge &elementEdgeData,
				      const std::vector<Coord> &epts,
				      std::vector<double> &facearea, 
				      Coord fnormal[NUM_TET_FACES], 
				      int faceId, int fpi[NUM_TET_FACES][3],
				      double fprojf[NUM_TET_FACES],
				      int &icount,
				      bool print, int uid, int idx) 
{
  // print = true;
  double x[3];
  int *ptIds = vtkTetra::GetFaceArray(faceId);
  double height = epts[ptIds[0]][0]*fnormal[faceId][0] + 
    epts[ptIds[0]][1]*fnormal[faceId][1] +  
    epts[ptIds[0]][2]*fnormal[faceId][2];

  // First count the exits and entrances. 
  icount = 0;
  int numexits = 0;
  int numentrances = 0;

  for(int k=0; k<NUM_TET_FACE_EDGES; k++) {
    int edgeId = CSkeletonElement::faceEdges[faceId][k];
    for(CellEdgeMap::iterator here = elementEdgeData[edgeId].begin();
	here!=elementEdgeData[edgeId].end(); ++here)
      {

	if((*here).second.getType(faceId)  == EXIT_INTERSECTION) {
	  numexits++;
	  icount++;
	}
	if((*here).second.getType(faceId)  == ENTRANCE_INTERSECTION) {
	  numentrances++;
	  icount++;
	}
      }
  }

  // Sanity check
#ifdef DEBUG	
  if(icount > 1 && numexits != numentrances) {
    oofcerr << "elementFaceContribution: inconsistent exits and entrances: "
	    << "numexits=" << numexits << " numentrances=" << numentrances
	    << " uid=" << uid << " index=" << idx <<  std::endl;
    for(int k=0; k<NUM_TET_FACE_EDGES; k++) {
      int edgeId = CSkeletonElement::faceEdges[faceId][k];
      for(CellEdgeMap::iterator here = elementEdgeData[edgeId].begin();
	  here!=elementEdgeData[edgeId].end(); ++here) 
	{
	  oofcerr << "elementFaceContribution:    " << edgeId << " " 
		  << (*here).first << " "
		  << (*here).second.location << " " 
		  << (*here).second.getType(faceId) << std::endl;
	}
    }
    throw ErrProgrammingError(
	      "CSkeletonElement: inconsistent number of exits and entrances",
	      __FILE__, __LINE__);
  }
#endif // DEBUG


  // Now traverse the element edges, adding up contributions to the
  // area based on the sections in between the exits and the
  // entrances.
  if(icount >= 2) {
    bool done = false;
    bool started = false;
    Coord starting_point;
    int k = 0;
    bool inside = false;
    double y[3], p2[3];

    while(!done) {
      // set first point of first edge as the starting point
      // regardless of category
      for(int l=0; l<3; ++l) {
	x[l] = epts[ptIds[k]][l];
	p2[l] = epts[ptIds[(k+1)%NUM_TET_FACE_EDGES]][l];
      }
	    				
      // get the element edgeId and dir
      int edgeId = CSkeletonElement::faceEdges[faceId][k];
      int edgeDir = CSkeletonElement::faceEdgeDirs[faceId][k];

      // Set the delimiters for the next while loop based on the
      // direction of the edge.
      CellEdgeMap::iterator here, end;
      if(edgeDir==1) {
	here = elementEdgeData[edgeId].begin();
	end = elementEdgeData[edgeId].end();
      }
      if(edgeDir==-1) {
	here = elementEdgeData[edgeId].end();
	end = elementEdgeData[edgeId].begin();
      }

      // Traverse the current edge.
      while(here!=end and !done) {

	// decrement at the beginning of the loop if we are going backwards
	if(edgeDir==-1) 
	  --here;

// #ifdef DEBUG
// 	oofcerr << "intersection info " << (*here).first << " " 
// 		  << (*here).second.location << " "
// 		  << (*here).second.getType(faceId) << std::endl;
// #endif	// DEBUG

	// We add up all the entrances and exits then mod by
	// grazes so we get the net effect at a given point.
	// (*here).second is a VoxelBdyIntersection.
	switch ((*here).second.getType(faceId)) {
	case EXIT_INTERSECTION:
	  //(*here).second.location.writePointer(x);
	  x[0] = (*here).second.location[0];
	  x[1] = (*here).second.location[1];
	  x[2] = (*here).second.location[2];
	  inside = true;
	  // Always start and finish on an exit.
	  if(!started) {
	    started = true;
	    starting_point = (*here).second.location;
	  }
	  else if(started && (*here).second.location == starting_point)
	    done = true;
	  break;
	case ENTRANCE_INTERSECTION:
	  if (started && inside) {
	    //(*here).second.location.writePointer(y);
	    y[0] = (*here).second.location[0];
	    y[1] = (*here).second.location[1];
	    y[2] = (*here).second.location[2];
// #ifdef DEBUG
// 	    if(print) {
// 	      oofcerr << "basearea contrib along el edge: "
// 			<< x[fpi[faceId][0]] << " " << x[fpi[faceId][1]]
// 			<< " to " << (*here).second.location(fpi[faceId][0])
// 			<< " " << (*here).second.location(fpi[faceId][1])
// 			<< " contrib: "
// 			<< 0.5*(x[fpi[faceId][0]]*(*here).second.location(fpi[faceId][1])-x[fpi[faceId][1]]*(*here).second.location(fpi[faceId][0]))
// 			<< std::endl;
// 	    }
// #endif

	    facearea[faceId] += 0.5*
	      (x[fpi[faceId][0]]*(*here).second.location[fpi[faceId][1]] -
	       x[fpi[faceId][1]]*(*here).second.location[fpi[faceId][0]]);
	  }		
	  inside = 0;
	  break;
	case UNCATEGORIZED_INTERSECTION:
	  break;
	default:
	  break;
	}

	// increment at the end of the loop if we are going forwards
	if(edgeDir==1) 
	  ++here; 
      }

      if(inside && started && !done) {
// #ifdef DEBUG
// 	if(print) {
// 	  oofcerr << "basearea contrib whole or rest of edge: "
// 		    << x[fpi[faceId][0]] << " " << x[fpi[faceId][1]]
// 		    << " to " << p2[fpi[faceId][0]] << " "
// 		    << p2[fpi[faceId][1]]
// 		    << " contrib: "
// 		    << (1.0/2.0)*(x[fpi[faceId][0]]*p2[fpi[faceId][1]]-x[fpi[faceId][1]]*p2[fpi[faceId][0]])
// 		    << std::endl;
// 	}
// #endif
	facearea[faceId] += 0.5*
	  (x[fpi[faceId][0]]*p2[fpi[faceId][1]] -
	   x[fpi[faceId][1]]*p2[fpi[faceId][0]]);
      }
      k = (k+1) % NUM_TET_FACE_EDGES;
    } // end while(!done)     loop over face edges
  }   // end if icount > 2
  facearea[faceId] /= fprojf[faceId];
  return height;
} // end elementFaceContribution


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// This is the core of the homogeneity calculation. It calculates the
// volume intersection of a tetrahedral element with a voxelized
// region representing a material category in a microstructure.

/*

NOTES FOR THE NEW CATEGORYVOLUMES ROUTINE

Get quadrilateral voxel category boundaries from CMicrostructure.

Loop over tet elements:

  Compute polygonal intersections of tet faces with each quad

    Use a canonical order for the endpoints of the tet edges (ie node
    positions) when computing intersections with a quad, so that
    round-off error is repeatable.

    Keep track of which segments of the polygon are on the tet faces
    and which are on the quad edges.

  Use the polygon edges that aren't shared with other polygons to
  create polygons on faces.

 */

const DoubleVec *CSkeletonElement::categoryVolumes(const CMicrostructure *MS)
  const
{
  // Get the points that define the element and convert them to pixel
  // units.
  std::vector<Coord> epts;
  epts.reserve(4);
  Coord delta = MS->sizeOfPixels();
  for(unsigned int i=0; i<NUM_TET_NODES; ++i) {
    Coord x  = (*nodes)[i]->position();
    epts.push_back(x/delta);		// component-wise division
  }
    
  // For debugging.
  bool print = false;
  // bool print = (index == 4);

// #ifdef DEBUG
//   if(print) {
//     cerr.precision(16);
//     oofcerr << "\ncategoryVolumes: ELEMENT " << index << " epts=" << epts
// 	    << std::endl;
//   }
// #endif	// DEBUG

  // Find a bounding box for the element, used to limit which voxel
  // boundary planes will be considered.

  // TODO 3.1: Use CRectangularPrism and CRectangularPrism::swallow
  // instead.
  std::vector<double> bounds(6);
  bounds[0] = bounds[2] = bounds[4] = std::numeric_limits<double>::max();
  bounds[1] = bounds[3] = bounds[5] = -std::numeric_limits<double>::max();
  for(unsigned int j=0; j<NUM_TET_NODES; ++j) {
    for(unsigned int k=0; k<3; ++k) {
      if(epts[j][k] < bounds[2*k])
	bounds[2*k] = epts[j][k];
      if(epts[j][k] > bounds[2*k+1])
	bounds[2*k+1] = epts[j][k];
    }
  }

// #ifdef DEBUG
//   if(print) {
//     oofcerr << "categoryVolumes: bounds=" << bounds << std::endl;
//   }
// #endif	// DEBUG

  // Find the axis direction that has the maximum contribution to the
  // normal. We save floating point operations later on by projecting
  // onto this direction, calculating the 2D cross products to find
  // projected area contributions, and then dividing by the cosine of
  // the normal (fprojf for face projection factor) to find the area
  // contribution for each segment.  The sign of the projfactor will
  // correct for whether the bounding segments are oriented CCW or CW
  // when projected onto the given axis oriented plane.

  // The normals for each tet face
  Coord fnormal[NUM_TET_FACES];
  // The first two indices of fpi (face projection indices) give the
  // 2D coordinates that the face is projected onto. The third is the
  // index of the maximum component of fnormal.
  int fpi[NUM_TET_FACES][3] = {{-1,-1,-1},{-1,-1,-1},{-1,-1,-1},{-1,-1,-1}};
  // The maximum component of the face normal. Projected areas are
  // divided by this to get the real area.
  double fprojf[NUM_TET_FACES] = {0,0,0,0};
  for(unsigned int j=0; j<NUM_TET_FACES; ++j) {
    int *ptIds = vtkTetra::GetFaceArray(j);
    vtkTriangle::ComputeNormal(const_cast<double*>(epts[ptIds[0]].xpointer()), 
			       const_cast<double*>(epts[ptIds[1]].xpointer()), 
			       const_cast<double*>(epts[ptIds[2]].xpointer()),
			       fnormal[j]);
    if(fabs(fnormal[j][0]) >= fabs(fnormal[j][1]) &&
       fabs(fnormal[j][0]) >= fabs(fnormal[j][2])) 
      {
	fprojf[j] = fnormal[j][0];
	fpi[j][0]=1;
	fpi[j][1]=2;
	fpi[j][2]=0;
      }
    else if(fabs(fnormal[j][1]) >= fabs(fnormal[j][0]) &&
	    fabs(fnormal[j][1]) >= fabs(fnormal[j][2])) 
      {
	fprojf[j] = fnormal[j][1];
	fpi[j][0]=2;
	fpi[j][1]=0;
	fpi[j][2]=1;
      }
    else if(fabs(fnormal[j][2]) >= fabs(fnormal[j][0]) &&
	    fabs(fnormal[j][2]) >= fabs(fnormal[j][1])) 
      {
	fprojf[j] = fnormal[j][2];
	fpi[j][0]=0;
	fpi[j][1]=1;
	fpi[j][2]=2;
      }
  } // end loop over tet faces j

  // Get the number of voxel categories. This recomputes categories &
  // boundaries if needed.
  unsigned int ncat = MS->nCategories();	
  // The category volumes are stored in result.
  DoubleVec *result = new DoubleVec(ncat);    
  for(unsigned int i=0; i<ncat; ++i)
    (*result)[i] = 0;
  // Get all the category boundaries.
  const std::vector<VoxelSetBoundary> &bdys = MS->getCategoryBdys();  

  // A map of points where quads intersect (or possibly intersect) an
  // element face, used to enforce topological sanity.
  std::vector<FaceIntersectionMap> looseEnds(NUM_TET_FACES+1);
  
  // Store the voxel boundary quads that are closest to each element
  // node, used to calculate whether the face is in or out in cases
  // where there are no intersections on the face.
  std::vector<const Quad*> closestQuads[NUM_TET_NODES];
  // Reserve the maximum number of closest quads
  for(unsigned int j=0; j<NUM_TET_NODES; ++j)
    closestQuads[j].reserve(MAX_CLOSEST_QUADS);

  // TODO OPT: Calculate numCategorys-1 category volumes using volume
  // intersection, and just subtract total intersections from total
  // volume for the last cateogory.  In debug mode, calculate all
  // volumes and check that they sum to the total volume correctly.

  // Loop over the voxel categories.
  for(unsigned int i=0; i<ncat; ++i) {

    // All iPoints stored so that FaceIntersections can point to them.
    IntersectionPoints AllIPoints;
    AllIPoints.reserve(10000); 
    // TODO OPT: calculate a better initial size for AllIPoints.  Maybe 0
    // is ok.  Is 10000 way too big?

    // The category area of each element face.
    //* TODO: facearea is never used.  We should use it to compute face
    //* homogeneities
    std::vector<double> facearea(NUM_TET_FACES, 0.0);
    // Whether each element node is in the category, out, or on the boundary
    std::vector<ElementNodeStatus> inCategory(NUM_TET_NODES,
					      ELEMENT_NODE_UNKNOWN);
    // The distance squared from a tet node to each nearest quad face
    std::vector<double> distToQuad(NUM_TET_NODES,
				   std::numeric_limits<double>::max());

    bool donewithplane = false;

    // Reset variables.
    const VoxelSetBoundary &current_bdy = bdys[i];
    for(unsigned int j=0; j<NUM_TET_FACES; ++j) {
      looseEnds[j].clear();
      closestQuads[j].clear();

      // There is always at least one quad, and we need to be able to
      // refer to it as closestQuads[0]. This pointer will be set in
      // elementPointInCategory.
      closestQuads[j].push_back((Quad*)NULL);
    } // loop over tet faces
    looseEnds[NUM_TET_FACES].clear();
    CellEdge elementEdgeData(NUM_TET_EDGES);

    // Keep track of number of quad faces that are in or on the element
    unsigned int numFacesNotOutside = 0;

// #ifdef DEBUG
//     if(print)
//       oofcerr << "\ncategoryVolumes: category " << i <<  std::endl;
// #endif
    
    // Loop over the x,y,z coords since the planes of quads are stored
    // this way. The iterator c tells us how the plane is oriented.
    for(unsigned int c=0; c<3; ++c) {

      // if(print) oofcerr << "c = " << c << " num planes = "
      // 		  << current_bdy.getQuads(c).size() << std::endl;

      // Loop over the planes with normals in the c direction.
      for(PlanesOfQuads::const_iterator plane = current_bdy.getQuads(c).begin();
	  plane != current_bdy.getQuads(c).end(); ++plane) 
	{
	  
	  // c-coordinate for every point in every quad in this plane
	  unsigned int l = (*plane).first; 
	  // Only consider planes within the element's bounding box.
	  // TODO OPT: This only checks the c direction.  If
	  // VoxelSetBoundary kept an in-plane 2D bounding box for
	  // each QuadVector, we could check the other directions too.
	  if(l>bounds[c*2] && l<bounds[c*2+1]) {

// #ifdef DEBUG
// 	    if(print)
// 	      oofcerr << "categoryVolumes: starting work on plane l=" << l
// 		      << " c=" << c 
// 		      << " nQuads=" << (*plane).second->size()
// 		      << std::endl;
// #endif
	    TetIntersectionPoints tetPoints;
	    tetPoints.reserve(MAX_TET_PLANE_POINTS);
	    findTetPlaneIntersectionPoints(epts, c, l, tetPoints);

// #ifdef DEBUG
// 	    if(print) {
// 	      oofcerr << "categoryVolumes: tet intersection points= ";
// 	      for(TetIntersectionPoints::iterator here=tetPoints.begin();
// 		  here!=tetPoints.end(); ++here) 
// 		oofcerr << "     " << *here << std::endl;
// 	    }
// #endif	// DEBUG
	  
	    // If the tet intersects the plane in at least three
	    // points, loop over quads in the plane to find where the
	    // quads intersect the tet.
	    if(tetPoints.size() > 2) {

	      donewithplane = false;
	      for(QuadVector::const_iterator quad=(*plane).second->begin();
		  quad!=(*plane).second->end(); ++quad)
		{
		  const Quad *current_quad = *quad;

// #ifdef DEBUG
// 		  if(print) {
// 		    oofcerr << "categoryVolumes: current_quad="
// 			    << current_quad << " c=" << c << " coords=";
// 		    for(unsigned int k=0; k<4; ++k) 
// 		      oofcerr << " (" << current_quad->coords[k][0] << ","
// 			      << current_quad->coords[k][1] << ")";
// 		    oofcerr << std::endl;
// 	      }
// #endif	// DEBUG

		  // Figure out whether the element nodes are in or
		  // out of the category according to this quad. This
		  // also sets the distToQuad and closestQuads
		  // variables.
		  // TODO 3.1: comment more.  How is this different from
		  // what's below?
		  for(unsigned int k=0; k<NUM_TET_NODES; ++k) {
		    elementPointInCategory(inCategory[k], distToQuad[k],
					   closestQuads[k], epts[k],
					   current_quad, c, l);
		  }
	      
		  // Quick check to see if tet-plane intersection
		  // points are all outside quad bounds. The quad
		  // coordinates are always ordered such that point 0
		  // is the lower left hand corner and point 2 is the
		  // upper right hand corner. outside4[0] is true if
		  // all points are left of the quad, outside4[1] is
		  // true if all points are right, outside4[2] is true
		  // if all points are below (in the 2D plane) and
		  // outside4[3] is true if all are above. We use
		  // strictly less (greater) than because points that
		  // are ON the quad will need to be added to the
		  // loose ends for their topological information.
		  bool outside4[4] = {true, true, true, true};
		  for(TetIntersectionPoints::iterator here = tetPoints.begin(); 
		      here!=tetPoints.end(); ++here)
		    {
		      double *pt = (*here).x;
		      outside4[0] &= pt[0] < current_quad->coords[0][0];
		      outside4[1] &= pt[0] > current_quad->coords[2][0];
		      outside4[2] &= pt[1] < current_quad->coords[0][1];
		      outside4[3] &= pt[1] > current_quad->coords[2][1];
		    }
		  // If the tet is outside this quad, we are done with the quad.
		  if(outside4[0] || outside4[1] || outside4[2] || outside4[3]) {
// #ifdef DEBUG		    
// 		    if(print)
// 		      oofcerr << "categoryVolumes: quad outside tet"
// 			      << std::endl;
// #endif // DEBUG
		    continue; 
		  }
	      

		  // Find the intersection of the quad and the in-plane
		  // tet polygon. convexPolyIntersection implements the
		  // O'Rourke convex poly intersection algorithm.
		  PolyIntersectionType poly_intersection_type = POLY_UNKNOWN;
		  IntersectionPoints iPoints; // pts where tet intersects quad
		  iPoints.reserve(MAX_TET_QUAD_IXS);
		  convexPolyIntersection(tetPoints, iPoints, AllIPoints,
					 current_quad, epts, fnormal,
					 poly_intersection_type, print);

// #ifdef DEBUG
// 		  if(print)
// 		    oofcerr << "num iPoints " << iPoints.size()
// 			    << " " << poly_intersection_type << std::endl;
// #endif	// DEBUG

		  // If the polygons are found to be disjoint, we are
		  // done with the quad. Add the points for their
		  // topological information.
		  if(poly_intersection_type == POLY_DISJOINT) {
		    //if(iPoints.size() >= 2) {
		    enforceTopo(iPoints, looseEnds, current_quad, fnormal, fpi,
				true, print, epts);
		//iPointsContribution(iPoints, current_quad, epts, facearea, looseEnds, 
		//		    elementEdgeData, c, l, fnormal, fpi, true, print);
		    continue;
		  } // end if poly_intersection_type == POLY_DISJOINT

		  // if we've reached this point, the quad is either
		  // in or intersects, so increment numFaceNotOutside.
		  ++numFacesNotOutside;

		  // If the quad is entirely inside the tet, add the
		  // contribution to the overall category volume, and
		  // then we are done with this quad.
		  if(poly_intersection_type == QUAD_INSIDE) {
		    enforceTopo(iPoints, looseEnds, current_quad, 
				fnormal, fpi, false, print, epts);
		    if(iPointOnFace(iPoints[0]) || iPointOnFace(iPoints[1]) || 
		       iPointOnFace(iPoints[2]) || iPointOnFace(iPoints[3]))
		      {
			(*result)[i] += iPointsContribution(
					    iPoints, current_quad, epts,
					    facearea, looseEnds,
					    elementEdgeData, c, l, 
					    fnormal, fpi, false, print);
		  }
		    else
		      (*result)[i] += (1.0/3.0 * current_quad->area * l *
				       current_quad->norm);
		    continue;
		  } // end if poly_intersection_type == QUAD_INSIDE

		  // If the tet is inside the quad, add the
		  // contribution to the overall category volume,
		  // faceareas, and element edge intersections. Then
		  // we're done with the quad and the whole plane.
		  if(poly_intersection_type == TET_INSIDE) {
		    double basearea = tetPointsInsideQuadContrib(
					 tetPoints, facearea, c, l, epts,
					 fpi, elementEdgeData, current_quad, 
					 print);
		    (*result)[i] += 1.0/3.0 * current_quad->norm * l * basearea;
		    donewithplane = true;
		    continue; 
		  }

// #ifdef DEBUG
// 		  if(print && !iPoints.empty()) {
// 		    oofcerr << "\nfound points: " << std::endl;
// 		    for(IntersectionPoints::iterator here=iPoints.begin();
// 			here!=iPoints.end(); ++here) 
// 		      {
// 			oofcerr << (*here).x[0] << "," << (*here).x[1] << ","
// 				  << (*here).x[2] << " "
// 				  << (*here).faces[0] << (*here).faces[1]
// 				  << (*here).faces[2] << (*here).faces[3] << " "
// 				  << (*here).edges[0] << (*here).edges[1]
// 				  << (*here).edges[2] << (*here).edges[3]
// 				  << (*here).edges[4] << (*here).edges[5]
// 				  << " " << (*here).corner
// 				  << std::endl;
// 		    }
// 		    oofcerr << std::endl;
// 		  }
// #endif // DEBUG

		  // If we found at least a triangle of intersection
		  // between the quad and the tet, calculate the
		  // contribution to the overall category volume, the
		  // faceareas, and the element edge
		  // intersections. Also, enforce topological sanity.
		  enforceTopo(iPoints, looseEnds, current_quad, fnormal,
			      fpi, false, print, epts);
		  if( iPoints.size() > 2 ) { 

// #ifdef DEBUG
// 		    if(print && !iPoints.empty()) {
// 		      oofcerr << "categoryVolumes: found points: " << std::endl;
// 		      for(IntersectionPoints::iterator here=iPoints.begin();
// 			  here!=iPoints.end(); ++here) 
// 			{
// 			  oofcerr << "categoryVolumes:      " << **here
// 				  << std::endl;
// 			}
// 		    }
// #endif // DEBUG


		    // Add the contribution of the quad to the overall
		    // category volume.
		    (*result)[i] += iPointsContribution(
					iPoints, current_quad, epts, facearea,
					looseEnds, elementEdgeData, c, l,
					fnormal, fpi, false, print);
		  }
// #ifdef DEBUG
// 		  if(print)
// 		    oofcerr << "categoryVolumes: done with quad" << std::endl;
// #endif // DEBUG
		} // end loop over quads to find where quads intersect tet
	    } // end if tet intersects plane in at least three places
	  } // end if level in bounds
	} // end loop over levels  (planes w/ normals in the c direction)
    } // end loop over orientations, c (ie, 3 dimensions)
    
    // #ifdef DEBUG
    //    if(print)
    // 	 oofcerr << "categoryVolumes: cat = " << i << " volume so far: "
    // 		   << (*result)[i] << std::endl;
    // #endif  // DEBUG

    // Now find the contribution of the faces of the element.  We have
    // already found the contributions to the face category areas from
    // the voxel group boundaries.  Now we need to traverse the edges
    // of each element face and add up the contributions from them
    // using the intersections found earlier.  If numFacesNotOutside
    // is 0, then either the whole element is in this category, or
    // it's out.
    if(numFacesNotOutside) {

      bool extraVGBfacesChecked = false;
      int originalicount = 0;

      // Loop over the tet faces.
      for(unsigned int j=0; j<NUM_TET_FACES; ++j) {
	int *ptIds = vtkTetra::GetFaceArray(j);

// #ifdef DEBUG
// 	if(print) {
// 	  oofcerr << "\ncategoryVolumes: face=" << j << " area so far "
// 		  << facearea[j] << std::endl;
// 	  oofcerr << "points: " << std::endl;
// 	  for(unsigned int k=0; k<NUM_TET_FACE_EDGES; ++k)
// 	    oofcerr << epts[ptIds[k]][0] << " " << epts[ptIds[k]][1]
// 	  	      << " " << epts[ptIds[k]][2] << std::endl;
// 	  oofcerr << "normal " << fnormal[j][0] << " " << fnormal[j][1]
// 	  	    << " " << fnormal[j][2] << std::endl;
// 	  oofcerr << "total face area "
// 	  	    << vtkTriangle::TriangleArea(epts[ptIds[0]],epts[ptIds[1]],
// 	  					 epts[ptIds[2]]) << std::endl;
// 	}
// #endif	// DEBUG
	// CellEdgeMap::iterator here2;
	for(unsigned int k=0; k<NUM_TET_FACE_EDGES; k++) {
	  int edgeId = faceEdges[j][k];
	  for(CellEdgeMap::iterator here = elementEdgeData[edgeId].begin();
	      here!=elementEdgeData[edgeId].end(); ++here)
	    {
	      if ( (*here).second.getType(j)  == EXIT_INTERSECTION ) {
		originalicount++;
	      }
	      if ( (*here).second.getType(j)  == ENTRANCE_INTERSECTION ) {
		originalicount++;
	      }
// #ifdef DEBUG
// 	      if(print) {
// 		int edgeDir = faceEdgeDirs[j][k];
// 		oofcerr << edgeId << " " << edgeDir << " "
// 			  << (*here).first << " " << (*here).second.location
// 			  << " " << (*here).second.getType(j) << std::endl;
// 	      }
// #endif	// DEBUG
	    }
	}
// #ifdef DEBUG	    
// 	if(print) {
// 	  oofcerr << "loose ends before removing corners:" << std::endl;
// 	  for(FaceIntersectionMap::iterator it=looseEnds[j].begin(); 
// 	      it!=looseEnds[j].end(); ++it)
// 	    {
// 	      oofcerr << (*it).first << " " << (*it).second.ip->x[0] << ", "
// 			<< (*it).second.ip->x[1] << ", "
// 			<< (*it).second.ip->x[2] << " "
// 			<< (*it).second.type  << " "
// 			<< (*it).second.ip->corner << " "
// 		      << (*it).second.quad << " "
// 			<< (*it).second.quad->norm_dir << " "
// 			<< (*it).second.quad->height << std::endl;
// 	    }
// 	}
// #endif	// DEBUG

        processLooseEnds(looseEnds, elementEdgeData, epts, facearea, fnormal,
			 j, print, uid);

	removeDuplicateElementEdgeIntersections(elementEdgeData, j, print);

	int icount = 0;
	double height = 0;
#ifdef DEBUG
	try {
#endif // DEBUG	  
	  height = elementFaceContribution(
				elementEdgeData, epts, facearea, fnormal,
				j, fpi, fprojf, icount, print, uid, getIndex());
#ifdef DEBUG
	}
	catch (...) {
	  oofcerr << "CSkeletonElement::categoryVolumes: element="
		  << *this << std::endl;
	  throw;
	}
#endif // DEBUG	
	if(icount < 2) { 
	  // we need to double check if any other faces not considered
	  // earlier are closer to the nodes
	  
	  // TODO OPT: we don't want to go through these loops for each
	  // face.  Using the flag is somewhat clumsy. It would be
	  // nice to find a more elegant way to do this.
	  if(!extraVGBfacesChecked) {
	    for(unsigned int k=0; k<4; ++k) { // loop over nodes
	      for(unsigned int c=0; c<3; ++c) {
		for(PlanesOfQuads::const_iterator plane=
		      current_bdy.getQuads(c).begin();
		    plane!=current_bdy.getQuads(c).end();
		    ++plane)
		  {
		    // c-coordinate for every point in every quad in this plane
		    int l = (*plane).first;
		    // only check this plane if it is out of bounds
		    // but closer than the previously found closest
		    // plane
		    double dist2 = (epts[k][c] - l)*(epts[k][c] - l);
		    if( (l<=bounds[c*2] || l>=bounds[c*2+1]) &&
			(dist2 < distToQuad[k] || epts[k][c] == l)) 
		      {
			// oofcerr << "categoryVolumes: checking plane c = "
			// 	<< c << " l = " << l << " " << dist2 << " "
			// 	<< distToQuad[k] << std::endl;
			for(QuadVector::const_iterator quad=
			      (*plane).second->begin();
			    quad != (*plane).second->end();
			    ++quad)
			  {
			    elementPointInCategory(inCategory[k], distToQuad[k],
						   closestQuads[k], epts[k],
						   *quad, c, l);
			  }
		      }
		  }
	      }	// end loop over axes c
	    }	// end loop over nodes k
	    extraVGBfacesChecked = true;
	  } // end if !extraVGBfacesChecked
// #ifdef DEBUG
// 	  if(print) {
// 	    oofcerr << "categoryVolumes: all edges are in or out " 
// 		    << facearea[j] << " : ";
// 	    for(unsigned int k=0; k<4; ++k)
// 	      oofcerr << " " << inCategory[k];
// 	    oofcerr << std::endl;
// 	  }
// #endif // DEBUG

	  bool inside = false;
	  bool outside = false;
	  bool localinside = false;
	  double elEdge[2][3], angdist[2], maxangdist = -10, maxangpair = -10;
	  bool perpcase;
	  for(unsigned int k=0; k<3; ++k) { //loop over face nodes
// #ifdef DEBUG
//  	    if(print) 
// 	      oofcerr << "\n\ncategoryVolumes: pt " << ptIds[k] << " in "
// 			<< inCategory[ptIds[k]] << " numquads "
// 			<< closestQuads[ptIds[k]].size() << std::endl;
// #endif // DEBUG
	    if(inCategory[ptIds[k]] == ELEMENT_NODE_ON_EDGE && 
	       closestQuads[ptIds[k]].size() == 1)
	      {
		inCategory[ptIds[k]] = ELEMENT_NODE_ON;
	      }

	    switch(inCategory[ptIds[k]]) {
	    case ELEMENT_NODE_IN:
	      inside = true;
	      break;

	    case ELEMENT_NODE_OUT:
	      outside = true;
	      break;

	    case ELEMENT_NODE_ON:
	      {
		ElPointLocation epicff = elementPointInCategoryForFace(
						 closestQuads[ptIds[k]][0],
						 epts, ptIds, k, fnormal[j]);
		if(epicff == ELPOINTINSIDE)
		  inside = true;
		else if(epicff == ELPOINTOUTSIDE)
		  outside = true;
		// In very special cases, there can be inconsistent
		// inside/outside information because there is an
		// intersection on the node, and a missing intersection
		// on the edge that is not handled properly by the loose
		// ends. The ideal solution would be to detect the loose
		// end on other faces. For now, just don't count nodes
		// that are inconclusive if there are also
		// intersections.
		else {
		  if(originalicount == 0) {
		    oofcerr << "categoryVolumes: icount " << originalicount
			    << std::endl;
		    oofcerr << "categoryVolumes: uid=" << uid << " " << index
			    << std::endl;
		    throw ErrProgrammingError(
			       "Inside/outside information inconsistent.",
			       __FILE__, __LINE__);
		  }
		}
	      }
	      break;

	    case ELEMENT_NODE_ON_EDGE:
	      for(unsigned int m = 0; m < 3; ++m) {
		elEdge[0][m] = epts[ptIds[(k+1)%3]][m] - epts[ptIds[k]][m];
		elEdge[1][m] = epts[ptIds[(k+2)%3]][m] - epts[ptIds[k]][m];
	      }
	      perpcase = false;
	      maxangdist = maxangpair = -10;
	      for(unsigned int n=0; n<closestQuads[ptIds[k]].size(); ++n) {
// #ifdef DEBUG
// 		if(print) 
// 		  oofcerr << "categoryVolumes: quad number " << n << std::endl;
// #endif // DEBUG
		bool perp[2];
		bool overlap = elEdgeQuadAngularDistance(
				 closestQuads[ptIds[k]][n], elEdge,
				 epts[ptIds[k]], angdist, perp, print);
// #ifdef DEBUG
// 		if(print)
// 		  oofcerr << "categoryVolumes: new function overlap, angdists " 
// 			  << overlap << " " << angdist[0] << " " << angdist[1]
// 			  << std::endl;
// #endif // DEBUG
		// if the element face and the vgb quad are in the
		// same plane and overlap, then this vgb quad gives
		// the right answer, otherwise, ignore it.
		if(closestQuads[ptIds[k]][n]->norm == 
		   fnormal[j][closestQuads[ptIds[k]][n]->norm_dir] || 
		   closestQuads[ptIds[k]][n]->norm == 
		   -1*fnormal[j][closestQuads[ptIds[k]][n]->norm_dir]) 
		  {
		    if(overlap) {
		      localinside = 
			closestQuads[ptIds[k]][n]->norm == 
			fnormal[j][closestQuads[ptIds[k]][n]->norm_dir];
		      break;
		    }
		    else 
		      continue;
		  }
		int dir = closestQuads[ptIds[k]][n]->norm_dir;
		double normEdgeDot[2];
		normEdgeDot[0] = closestQuads[ptIds[k]][n]->norm*elEdge[0][dir];
		normEdgeDot[1] = closestQuads[ptIds[k]][n]->norm*elEdge[1][dir];
// #ifdef DEBUG
// 		if(print)
// 		  oofcerr << "normEdgeDots " << normEdgeDot[0] << " "
// 			    << normEdgeDot[1] << std::endl;
// #endif	// DEBUG

		// The two normEdgeDots give consistent results for interiority.
		if(normEdgeDot[0]*normEdgeDot[1] >= 0) { 
		  if( (angdist[0] > 0 || angdist[1] > 0) &&
		      normEdgeDot[0]*normEdgeDot[1] >= 0)
		    {
		      localinside = (normEdgeDot[0] < 0 || normEdgeDot[1] < 0);
		      break;
		    }
		  if( (angdist[0] > maxangdist ||
		       (angdist[0] == maxangdist && angdist[1] > maxangpair))
		      && !perp[0] && !perpcase)
		    {
		      localinside = (normEdgeDot[0] < 0 || normEdgeDot[1] < 0);
		      maxangdist = angdist[0];
		      maxangpair = angdist[1];
		    }
		  if( (angdist[1] > maxangdist || 
		       (angdist[1] == maxangdist && angdist[0] > maxangpair)) 
		      && !perp[1] && !perpcase) 
		    {
		      localinside = (normEdgeDot[0] < 0 || normEdgeDot[1] < 0); 
		      maxangdist = angdist[1];
		      maxangpair = angdist[0];
		    }
		}
		else {
		  if(angdist[0] > 0) {
		    localinside = (normEdgeDot[0] < 0);
		    break;
		  }
		  if(angdist[1] > 0) {
		    localinside = (normEdgeDot[1] < 0);
		    break;
		  }
		  if( (angdist[0] > maxangdist || 
		       (angdist[0] == maxangdist && angdist[1] > maxangpair))
		      && !perp[0] ) 
		    {
		      localinside = (normEdgeDot[0] < 0);
		      maxangdist = angdist[0];
		      maxangpair = angdist[1];
		    }
		  if( (angdist[1] > maxangdist ||
		       (angdist[1] == maxangdist && angdist[0] > maxangpair))
		      && !perp[1]) 
		    {
		      localinside = (normEdgeDot[1] < 0);
		      maxangdist = angdist[1];
		      maxangpair = angdist[0];
		    }
		}
		// special case, the angdist can be 0 in two ways,
		// parallel to an edge or perpendicular to the whole
		// face. If two VGB faces meet this condition, they
		// must either agree, or there will be a third VGB
		// face in the plane of the element face.
		if(angdist[0] == 0 && angdist[1] == 0) {
		  if(angdist[0] >= maxangdist) {
		    localinside = (normEdgeDot[0] < 0 || normEdgeDot[1] < 0);
		    maxangdist = 0; //angdist[0];
		    perpcase = true;
		  }
		  if(angdist[1] >= maxangdist) {
		    localinside = (normEdgeDot[0] < 0 || normEdgeDot[1] < 0);
		    maxangdist = 0; //angdist[1];
		    perpcase = true;
		  }
		}
// #ifdef DEBUG
// 		if(print) {
// 		  oofcerr << "categoryVolumes: perpcase=" << perpcase 
// 			  << " maxangdist=" << maxangdist 
// 			  << " localinside=" << localinside << std::endl;
// 		}
// #endif // DEBUG
	      }	// end loop over closest quads n

	      if(localinside)
		inside = true;
	      else 
		outside = true;
	      break;

	    default:
	      break;
	    } // end switch(inCategory[ptIds[k]])

	    // if(print)
	    //   oofcerr << "inside/outside " << inside << outside 
	    // 		<< std::endl;
	  } // end loop over face nodes k

	  if(inside && !outside)
	    facearea[j] += vtkTriangle::TriangleArea(
			     const_cast<double*>(epts[ptIds[0]].xpointer()),
			     const_cast<double*>(epts[ptIds[1]].xpointer()), 
			     const_cast<double*>(epts[ptIds[2]].xpointer()));

	  if(inside && outside) {
// #ifdef DEBUG
// 	    if(print) {
// 	      oofcerr << "categoryVolumes: icount " << icount << std::endl;
// 	      for(unsigned int k=0; k<3; ++k) {
// 		oofcerr << "ptid = " << ptIds[k]
// 			  << " in " << inCategory[ptIds[k]]
// 			  << " numquads " << closestQuads[ptIds[k]].size()
// 			  << std::endl;
// 		oofcerr << "quad(s): " << std::endl;
// 		for(unsigned int n=0; n<closestQuads[ptIds[k]].size(); ++n) {
// 		  oofcerr << "norm " << closestQuads[ptIds[k]][n]->norm
// 			    << " dir " << closestQuads[ptIds[k]][n]->norm_dir
// 			    << " height " << closestQuads[ptIds[k]][n]->height
// 			    << " coords: " << std::endl;
// 		  for(unsigned int m=0; m<4; m++)
// 		    oofcerr << closestQuads[ptIds[k]][n]->coords[m][0] << " "
// 			      << closestQuads[ptIds[k]][n]->coords[m][1]
// 			      << std::endl;
// 		  oofcerr << std::endl;
// 		}
// 	      }
// 	      oofcerr << "ELEMENT " << index << " UID " << uid
// 			<< "\nPOINTS: " << std::endl;
// 	      for(unsigned int m=0; m<4; m++) {
// 		oofcerr << epts[m][0] << " " << epts[m][1] << " "
// 			  << epts[m][2] << std::endl;
// 	      }
// 	      oofcerr << "volume " << volumeInVoxelUnits(MS)
// 			<< " suspect " << suspect() << std::endl;
// 	    }
// #endif // DEBUG
	    throw ErrProgrammingError(
			      "Inside/outside information inconsistent.",
			      __FILE__, __LINE__);
	  } // inside && outside

// #ifdef DEBUG
// 	  if(!inside && !outside) { // all three points are ON the boundary
// 	    if(print) {
// 	      oofcerr << "categoryVolumes: all three points on boundary" 
// 		      << std::endl;
// 	      for(unsigned int k=0; k<3; ++k) {
// 		for(int m=0; m<4; ++m) 
// 		  oofcerr << closestQuads[ptIds[k]][0]->coords[m][0] << ","
// 			  << closestQuads[ptIds[k]][0]->coords[m][1]
// 			  << std::endl;
// 	      }
// 	    }
// 	  }
// #endif // DEBUG

	} // end if icount < 2


// #ifdef DEBUG
// 	if(print) {
// 	  oofcerr << "facearea: " << facearea[j]
// 		    << " fprojf[j]: " << fprojf[j] << " "
// 		    << facearea[j]*fprojf[j]
// 		    << " height: " << height << std::endl;
// 	  oofcerr << "volume contrib: " << 1.0/3.0 * height * facearea[j]
// 		    << std::endl;
// 	}
// #endif	// DEBUG

	//if(facearea[j] > 0) {
	(*result)[i] += 1.0/3.0 * height * facearea[j];

    // TODO 3.1: Cases where the removal (addition) of a spurious
    // (missing) edge is ambiguous can lead to invalid area
    // results. These should be relatively rare (one in millions) but
    // do happen and should be handled using topological information
    // somehow.

// #ifdef DEBUG
// 	if(facearea[j] > (1.03)*vtkTriangle::TriangleArea(epts[ptIds[0]],
// 							  epts[ptIds[1]],
// 							  epts[ptIds[2]]) ||
// 	   facearea[j] < (-0.03)*vtkTriangle::TriangleArea(epts[ptIds[0]],
// 							   epts[ptIds[1]],
// 							   epts[ptIds[2]]) )
// 	  {
// 	    oofcerr << "uid " << uid << std::endl;
// 	    oofcerr << "\n\n\nPOINTS: " << std::endl;
// 	    for(unsigned int m=0; m<4; m++) {
// 	      oofcerr << epts[m][0] << " " << epts[m][1] << " " << epts[m][2]
// 			<< std::endl;
// 	    }
// 	    oofcerr << "volume " << volumeInVoxelUnits(MS)
// 		      << " illegal " << illegal() << " suspect " << suspect()
// 		      << std::endl;
// 	    oofcerr << "strange area result " << facearea[j] << std::endl;
// 	    throw ErrProgrammingError("Invalid area.", __FILE__, __LINE__);
// 	  }
// #endif	// DEBUG

// #ifdef DEBUG
// 	oofcerr << "normal: " << fnormal[j][0] << " " << fnormal[j][1]
// 		  << " " << fnormal[j][2] << std::endl;
// 	oofcerr << "height = " << height << " vol: " <<  (*result)[i]
// 		  << std::endl;
// 	oofcerr << "element face contrib = " 
// 		  << 1.0/3.0 * height * facearea[j] << std::endl;
// #endif	// DEBUG

      } // end loop over element faces j
// #ifdef DEBUG
// 	if(print)
// 	  oofcerr << "end loop over faces" << std::endl;
// #endif // DEBUG
    } // end if numFacesNotOutside
    else {
      // the element is either entirely inside or entirely outside --
      // get the category at the center of the element.
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "CSkeletonElement::categoryVolumes: entirely in or out"
// 	      << std::endl;
// #endif // DEBUG
      double x[3] = {0.0, 0.0, 0.0};
      for(unsigned int j=0; j<4; ++j) {
	for(unsigned int k=0; k<3; ++k) 
	  x[k] += epts[j][k] / 4.0;
      }
      unsigned int cat = 
	MS->category(Coord(x[0]*delta[0],x[1]*delta[1],x[2]*delta[2]));
// #ifdef DEBUG
//       if(print)
// 	oofcerr << "CSkeletonElement::categoryVolumes: center cat=" << cat
// 		<< std::endl;
// #endif // DEBUG
      if(cat == i) {
	(*result)[i] = volumeInVoxelUnits(MS);
// #ifdef DEBUG
// 	if(print)
// 	  oofcerr << "CSkeletonElement::categoryVolumes: volume="
// 		  << (*result)[i] << std::endl;
// #endif // DEBUG
      }
      else
	(*result)[i] = 0;
    }

    // TODO 3.1: Cases where the removal (addition) of a spurious
    // (missing) edge is ambiguous can lead to invalid volume
    // results. These should be relatively rare (one in millions) but
    // do happen and should be handled using topological information
    // somehow.

// #ifdef DEBUG
//     if( ((*result)[i] > 1.03*volumeInVoxelUnits(MS) ||
// 	 (*result)[i] < -0.03*volumeInVoxelUnits(MS)) &&
// 	volumeInVoxelUnits(MS) > 1e-3) 
//       {
// 	oofcerr << "ELEMENT " << index << " " << uid
// 		  << " suspect " << suspect() << "\n\n\nPOINTS: " << std::endl;
// 	for(unsigned int m=0; m<4; m++) {
// 	  oofcerr << epts[m][0] << " " << epts[m][1] << " " << epts[m][2]
// 		    << std::endl;
// 	}
// 	oofcerr << "strange volume result " << (*result)[i] << " "
// 		  << volumeInVoxelUnits(MS) << std::endl;
// 	throw ErrProgrammingError("Invalid volume.", __FILE__, __LINE__);
//       }
// #endif	// DEBUG


    // Deallocate the pointers in AllIPoints and clear the vector.
    for(IntersectionPoints::iterator it = AllIPoints.begin();
	it != AllIPoints.end(); ++it) 
      {
	delete *it;
      }
    // AllIPoints.resize(0);

  } // end loop over voxel categories i

  return result;
} // end of categoryVolumes


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


double CSkeletonElement::homogeneity(const CMicrostructure *MS) const {
  findHomogeneityAndDominantPixel(MS);
  return homogeneity_data.value().get_homogeneity();
}

double CSkeletonElement::energyHomogeneity(const CMicrostructure *MS) const {
  findHomogeneityAndDominantPixel(MS);
  return homogeneity_data.value().get_energy();
}

void CSkeletonElement::copyHomogeneity(const CSkeletonElement &other) {
  homogeneity_data.copy(other.homogeneity_data);
}

void CSkeletonElement::revertHomogeneity() {
  // CachedValue::revert is a no-op if the object hasn't changed since
  // it was last reverted.
  homogeneity_data.revert();
}

int CSkeletonElement::dominantPixel(const CMicrostructure *MS) const {
  findHomogeneityAndDominantPixel(MS);
  return homogeneity_data.value().get_dominantpixel();
}


const double regularTetrahedraFactor = (1.5)*(pow(27,0.25)/sqrt(2));

static double triangleArea2(const Coord &p1, const Coord &p2, const Coord &p3) {
  // See http://en.wikipedia.org/wiki/Heron%27s_formula for the
  // formula we're using here.  That page says that this expression is
  // numerically unstable for triangles with a very small angle, but
  // we don't care too much about accuracy in that case.  The stable
  // version of the formula uses lengths, not lengths squared, and
  // requires sorting them, so it's going to be a lot slower to
  // compute.
  double a = norm2(p1 - p2);
  double b = norm2(p2 - p3);
  double c = norm2(p3 - p1);
  return (0.0625*fabs(4.0*a*c - (a-b+c)*(a-b+c)));
} 

double CSkeletonElement::energyShape() const {
  Coord x[4];
  positionPointer(x);
  return energyShape(x);
}

double CSkeletonElement::energyShape(const Coord *x) {
  double sum_area2 = 0;
  for(int i=0; i<4; ++i) {
    int *facePtIds = vtkTetra::GetFaceArray(i);
    sum_area2 += triangleArea2(x[facePtIds[0]],
			       x[facePtIds[1]],
			       x[facePtIds[2]]);
  }
  double e = 1 - (regularTetrahedraFactor * 
	      vtkTetra::ComputeVolume(const_cast<double*>(x[0].xpointer()),
				      const_cast<double*>(x[1].xpointer()),
				      const_cast<double*>(x[2].xpointer()),
				      const_cast<double*>(x[3].xpointer())) /
	      pow(0.25*sum_area2, 0.75));
  return e;
}
  
// TODO OPT: handle if there is no dominant pixel or no material
// TODO OPT: Handle materials assigned to element groups.  See comment in
// skeletongroupmenu.py.
const Material *CSkeletonElement::material(const CSkeletonBase* skel) const {
  // See if this element is in any groups to which Materials have been
  // assigned.
  const GroupNameSet *grps = groupNames();
  for(GroupNameSet::const_iterator g=grps->begin(); g!=grps->end(); ++g) {
    // TODO 3.1: Finish this.  The group itself isn't currently available
    // in C++.  This could use the Python API, but it would be better
    // to rewrite the groups in C++ and make the material directly
    // available.

    // The group is part of a python ElementGroupSet which is derived
    // from GenericMaterialGroupSet which is derived from
    // GenericGroupSet.  GenericMaterialGroupSet has a "materials"
    // dict, keyed by group name, which stores the material and a
    // timestamp for each assigned material.

    // Find which groups the element belongs to, and return the latest
    // material assigned to any of the groups.
  }
  
  // The element isn't in any groups that have assigned materials.
  // Return the material of the dominant pixel.
  int dominantpixel = dominantPixel(skel->getMicrostructure());
  // getMaterialFromCategory is declared in material.h
  return getMaterialFromCategory(skel->getMicrostructure(), dominantpixel);
}

double CSkeletonElement::energyTotal(const CMicrostructure *MS, double alpha)
  const 
{
  if(alpha == 1)
    return energyHomogeneity(MS);
  Coord x[4];
  positionPointer(x);
  if(alpha == 0)
    return energyShape(x);
  double eHomog = energyHomogeneity(MS);
  double eShape = energyShape(x);
  // writeDebugFile(to_string(getUid()) +
  // 		 " eHomog=" + to_string(eHomog) +
  // 		 " eShape=" + to_string(eShape) + "\n");
  return alpha*eHomog + (1-alpha)*eShape;
}

// const std::vector<ICoord> *
// CSkeletonQuad::underlying_pixels(const CMicrostructure &microstructure) const {
  // Divide the quad into two triangles with positive area, and mark
  // the pixels under them.  This avoids the possibly complicated
  // geometry of quadrilaterals.
//   const Coord c0 = nodes[0]->position();
//   const Coord c1 = nodes[1]->position();
//   const Coord c2 = nodes[2]->position();
//   const Coord c3 = nodes[3]->position();
//   CRectangle bbox(c0, c2);
//   bbox.swallow(c1);
//   bbox.swallow(c3);
//   MarkInfo *mm = microstructure.beginMarking(bbox);
//   if(triangleArea(c0, c1, c2) >= 0.0 &&
//      triangleArea(c0, c2, c3) >= 0.0) {
//     microstructure.markTriangle(mm, c0, c1, c2);
//     microstructure.markTriangle(mm, c0, c2, c3);
//   }
//   else if(triangleArea(c1, c2, c3) >= 0.0 &&
//           triangleArea(c2, c3, c0) >= 0.0) {
//     microstructure.markTriangle(mm, c1, c2, c3);
//     microstructure.markTriangle(mm, c1, c3, c0);
//   }
//   std::vector<ICoord> *pxls = microstructure.markedPixels(mm); // new'd vector
//   microstructure.endMarking(mm);
//   return pxls;

//}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Methods used when constructing one-dimensional cross sections
// through a Skeleton.

// Used by LinearCrossSectionDomain.get_elements() in
// analysisdomain.py.

OrientedCSkeletonFace *CSkeletonElement::getOrientedFace(
			 const CSkeletonBase *skel, unsigned int f)
  const
{
  CSkeletonMultiNodeKey facekey = getFaceKey(f);
  CSkeletonFace *face = skel->getFace(facekey);
  OrientedCSkeletonFace *oface = new OrientedCSkeletonFace(face);
  CSkeletonNode *n0 = getFaceNode(f, 0);
  CSkeletonNode *n1 = getFaceNode(f, 1);
  CSkeletonNode *n2 = getFaceNode(f, 2);
  oface->set_direction(n0, n1, n2);
  return oface;
}

void CSkeletonElement::dumpFaceInfo(const CSkeletonBase *skel) const {
  std::cout << "CSkeletonElement::dumpFaceInfo:" << std::endl
	    << *this << std::endl;
  for(unsigned int i=0; i<getNumberOfFaces(); i++) {
    OrientedCSkeletonFace *face = getOrientedFace(skel, i);
    Coord normal = face->get_direction_vector();
    face->print(std::cout);
    std::cout << std::endl << " normal: " << normal << std::endl;
    delete face;
  }
}

// Given a line segment (xstart, xend), parametrized by 
//        x = xstart + alpha*(xend-xstart)
// find the values of alpha (alphaEnter, alphaExit) and the face
// indices (alphaEnter, alphaExit) where the segment intersects the
// element.  If there are no intersections, return false.  If the
// intersection point is not on a face (ie, is on multiple faces) the
// face index is set to -1.

//#define EXACTDIFFER
#ifdef EXACTDIFFER
#define DIFFER(x, y) (x != y)
#else
#include "common/differ.h"
#define DIFFER(x, y) differ(x, y)
#endif

void CSkeletonElement::lineIntersections(
		 const CSkeletonBase *skel,
		 const Coord &xstart, const Coord &xend,
		 LineIntersectionPoint **entrancePoint,
		 LineIntersectionPoint **exitPoint)
  const
{
  // alphaExit is the smallest alpha at which a positively oriented
  // plane (a plane whose normal is in the xend-xstart direction)
  // intersects the line. 
  double alphaExit = std::numeric_limits<double>::max();
  double alphaEnter = -alphaExit;
  std::vector<int> entranceFaces;
  std::vector<int> exitFaces;
  Coord delta = xend - xstart;
  // There are two conditions that have to be tracked for parallel
  // lines.  If the line is parallel to a face and has a positive
  // offset from it (in the direction of the face's normal), then
  // there can be no intersection.
  bool posOffset = false;
  // If the line lies in the plane of a face, then that face will be
  // an intersection face for any alpha between 0 and 1, but only if
  // the line intersects other faces.
  std::vector<int> zeroOffsetFaces;

  for(unsigned int i=0; i<getNumberOfFaces() && !posOffset; i++) {
    OrientedCSkeletonFace *face = getOrientedFace(skel, i); // new
    Coord normal = face->get_direction_vector();
    double xnorm = dot(delta, normal);
    if(xnorm != 0) {
      double alpha = (face->get_offset() - dot(normal, xstart))/xnorm;
      if(xnorm < 0) {
	// This face sets a minimum value for alpha.  The line may
	// enter the element here.
	if(!DIFFER(alpha, alphaEnter)) {
	  // The line crosses this face at the same point that it
	  // crosses another face.
	  entranceFaces.push_back(i);
	}
	else if(alpha > alphaEnter) {
	  alphaEnter = alpha;
	  entranceFaces.clear();
	  entranceFaces.push_back(i);
	}
      }
      else {		 
	// xnorm > 0.  This face sets a maximum value for alpha.  The
	// line may exit the element here.
	if(!DIFFER(alpha, alphaExit)) {
	  // The line crosses this face at the same point that it
	  // crosses another face.
	  exitFaces.push_back(i);
	}
	else if(alpha < alphaExit) {
	  alphaExit = alpha;
	  exitFaces.clear();
	  exitFaces.push_back(i);
	}
      }	// end xnorm > 0
    }	// end xnorm != 0
    else {
      // xnorm == 0.  The face is parallel to the line.
      double offset = dot(xstart, normal) - face->get_offset();
      // If offset < 0, the line is inside the element and parallel to
      // the plane, so the plane is irrelevant to the intersections.
      if(!DIFFER(offset, 0.0)) {
	// The line is in the plane of this face.  If the line is in
	// the element, this face is both an exit face and an entrance
	// face.  We can't add it to exitFaces and entranceFaces yet,
	// because we don't know whether the line is in the element.
	zeroOffsetFaces.push_back(i);
      }
      else if(offset > 0) {
	// Line is outside the element.  No intersections are possible.
	posOffset = true;
      }
    } // end xnorm == 0
    delete face;
  } // end loop over faces i

  if(!exitFaces.empty()) {
    for(unsigned int i=0; i<zeroOffsetFaces.size(); i++) {
      exitFaces.push_back(zeroOffsetFaces[i]);
    }
  }

  if(!entranceFaces.empty()) {
    for(unsigned int i=0; i<zeroOffsetFaces.size(); i++) {
      entranceFaces.push_back(zeroOffsetFaces[i]);
    }
  }

  if(alphaExit < alphaEnter)
    return;

  if(alphaExit > 0.0 && alphaExit <= 1.0) {
    *exitPoint = getLineIntersectionPoint(skel, exitFaces, alphaExit,
					 xstart, xend);
  }

  if(alphaEnter >= 0.0 && alphaEnter < 1.0) {
    *entrancePoint = getLineIntersectionPoint(skel, entranceFaces, alphaEnter,
					     xstart, xend);
  }
} // end CSkeletonElement::lineIntersections

// Given a list of indices for the faces which a line intersects,
// return a LineIntersectionPoint object describing the intersection.

LineIntersectionPoint *CSkeletonElement::getLineIntersectionPoint(
					  const CSkeletonBase *skel,
					  std::vector<int> &faceIndices,
					  double alpha,
					  const Coord &xstart,
					  const Coord &xend)
  const
{
  unsigned int nfaces = faceIndices.size();
  CSkeletonFaceVector faces(nfaces);
  for(unsigned int i=0; i<nfaces; i++) {
    CSkeletonMultiNodeKey facekey = getFaceKey(faceIndices[i]);
    faces[i] = skel->getFace(facekey);
  }
  if(nfaces == 0) {		// No intersection.
    return 0;
  }
  if(nfaces == 1) {		// Simple face intersection.
    return new LineIntersectionPoint(this, faces[0], xstart, xend, alpha);
  }
  if(nfaces == 2) {    // Intersection on a segment between two faces.
    // Find the segment that is shared by the two faces.
    CSkeletonSegmentSet segs0;
    CSkeletonSegmentSet segs1;
    skel->getFaceSegments(faces[0], segs0);
    skel->getFaceSegments(faces[1], segs1);
    
    for(CSkeletonSegmentSet::iterator f=segs0.begin(); f!=segs0.end(); ++f) {
      CSkeletonSegmentSet::iterator g=segs1.find(*f);
      if(g != segs1.end()) {
	return new LineIntersectionPoint(this, *g, xstart, xend, alpha);
      }
    }
    throw ErrProgrammingError("Failed to find common segment!",
			      __FILE__, __LINE__);
  }
  // Intersection is a node between 3 (or more) faces. (Even if we ever
  // have non-tetrahedral elements, could there be more than 3 faces?)
  // First, count the number of times each node appears in the faces.
  std::multiset<CSkeletonNode*> nodecounts;
  for(unsigned int f=0; f<nfaces; f++) {
    for(unsigned int n=0; n<faces[f]->nnodes(); n++) {
      nodecounts.insert(faces[f]->getNode(n));
    }
  }
  // Find the node that appeared three (or more) times.  There can be
  // only one.
  for(unsigned int i=0; i<nnodes(); i++) { // loop over nodes of the element
    if(nodecounts.count(getNode(i)) >= 3) {
      return new LineIntersectionPoint(this, getNode(i), xstart, xend, alpha);
    }
  }
  throw ErrProgrammingError("Failed to find common node!", __FILE__, __LINE__);
} // end CSkeletonElement::getLineIntersectionPoint


// Find the first point where the line (xstart, xend) exits an
// element, to start off the computation of a linear cross section.
// The first exit point is special because although this method was
// called for the element that contains xstart, the point might be on
// the boundary of the element, and the line might not cross the
// element at all.

const LineIntersectionPoint *CSkeletonElement::startLinearXSection(
	const CSkeletonBase *skel, const Coord *xstart, const Coord *xend)
  const
{
  LineIntersectionPoint *entrancePt = 0;
  LineIntersectionPoint *exitPt = 0;
  if(interior(xend)) {
    return new LineIntersectionEndPoint(this, *xstart, *xend);
  }
  lineIntersections(skel, *xstart, *xend, &entrancePt, &exitPt);
  delete entrancePt;
  // If there was no exit point from the element supposedly containing
  // the starting point, then the starting point must be on the
  // boundary of the element and lead away from it. It must cross one
  // of the element's neighbors, going from alpha==0 to some positive
  // alpha.
  if(!exitPt) {
    // Look for a better starting point among the neighbors of this
    // element.
    ConstCSkeletonElementSet *nbrs = skel->getElementNeighbors(this);
    double maxAlpha = -std::numeric_limits<double>::max();
    for(ConstCSkeletonElementSet::const_iterator e=nbrs->begin();
	e!=nbrs->end(); ++e)
      {
	LineIntersectionPoint *tempexit = 0;
	entrancePt = 0;
	(*e)->lineIntersections(skel, *xstart, *xend, &entrancePt, &tempexit);
	if(tempexit) { 
	  // The exit point for the neighbor was found.
	  double exitAlpha = tempexit->getAlpha();
	  // If the entrance point for the neighbor isn't nearly at
	  // alpha==0 (within roundoff) this can't be the first
	  // element to be traversed by the line.  If the entrance point wasn't
	  // found, then roundoff error must have put it just inside
	  // the element (since we know that it's actually on the
	  // boundary).
	  if((!entrancePt || entrancePt->getAlpha() < 1.e-5*exitAlpha) &&
	     (exitAlpha > maxAlpha))
	    {
	      delete exitPt;
	      exitPt = tempexit;
	      maxAlpha = tempexit->getAlpha();
	    }
	  else {
	    delete tempexit;
	  }
	}
	delete entrancePt;
      }	// end loop over neighbors
    delete nbrs;
  }
  return exitPt;
}

// LineIntersectionPoint stores information about the intersection
// point of a line with the surface of an element.

LineIntersectionPoint::LineIntersectionPoint(
		     const CSkeletonElement *el, // the element that was crossed
		     const CSkeletonSelectable *obj, // face, segment
						     // or node at the
						     // intersection
		     const Coord &xs, const Coord &xe, // endpoints of the line
		     double alpha // line coordinate of the intersection
					     )
  : traversee(el), intersectee(obj), xstart(xs), xend(xe), alpha(alpha)
{}

LineIntersectionEndPoint::LineIntersectionEndPoint(
				   const CSkeletonElement *el,
				   const Coord &xs, const Coord &xe)
  : LineIntersectionPoint(el, 0, xs, xe, 1.0)
{}

LineIntersectionPoint::~LineIntersectionPoint() {}

Coord LineIntersectionPoint::position() const {
  return xstart + alpha*(xend-xstart);
}

std::ostream &operator<<(std::ostream &os, const LineIntersectionPoint &lip) {
  if(lip.intersectee)
    os << "[obj=" << *lip.intersectee << ", alpha" << lip.alpha << ", pos="
       << lip.position() << "]";
  else
    os << "[no intersection]";
  return os;
}

LineIntersectionPoint *LineIntersectionPoint::next(
					 const CSkeletonBase *skel)
  const 
{
  if(!intersectee)
    return 0;
  LineIntersectionPoint *intrsct = intersectee->nextIntersection(
						 skel, traversed, xstart, xend);
  intrsct->addTraversedElements(traversed);
  return intrsct;
}

void LineIntersectionPoint::addTraversedElement(const CSkeletonElement *el) {
  traversed.insert(el);
}

void LineIntersectionPoint::addTraversedElements(
					 const ConstCSkeletonElementSet &els)
{
  traversed.insert(els.begin(), els.end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonElement::realElement(FEMesh *femesh, int idx,
				   //std::vector<Node*> *fnodes,
				   const CSkeleton *skel, Material *mat) 
{
  // TODO 3.1: for now we're assuming linear tetrahedra only, matching
  // indices, and simplifying material thing

  std::vector<Node*> real_el_nodes;
  for(CSkeletonNodeIterator n = nodes->begin(); n != nodes->end(); ++n)
    real_el_nodes.push_back(femesh->getFuncNode((*n)->getIndex()));
    // real_el_nodes.push_back( (*fnodes)[(*n)->getIndex()] );

  Element *el;
  // TODO 3.1: tetname shouldn't be hard-coded here.  Different types of
  // CSkeletonElement (if we ever have them) will retrieve different
  // master elements.  Also, we will need to choose the element order.
  // ElementShape and order should be args?
  const std::string &tetname = "TET4_4";
  if(mat != NULL)
    el = getMasterElementByName(tetname)->build(this, mat, &real_el_nodes);
  else
    el = getMasterElementByName(tetname)->build(this, material(skel),
						&real_el_nodes);
  femesh->addElement(el);
  //
  setMeshIndex(idx);
}

void CSkeletonElement::print(std::ostream &os) const {
  // os << "Element(" << uid << ", " << generating_function << ")";
  os << "Element(uid=" << uid
     << ", index=" << index
     << ", ";
  printNodes(os);
  os << ")";
}
