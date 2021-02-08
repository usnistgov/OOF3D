// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/canvaslayers.h"
#include "common/IO/oofcerr.h"
#include "common/VSB/cplane.h"
#include "common/cdebug.h"
#include "common/cmicrostructure.h"
#include "common/lock.h"
#include "common/printvec.h"
#include "common/voxelsetboundary.h"
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
#include <set>
#include <math.h>

const std::string CSkeletonElement::modulename_(
					 "ooflib.SWIG.engine.cskeletonelement");
const std::string CSkeletonElement::classname_("CSkeletonElement");

// static CSkeletonElementSet allElements;
long CSkeletonElement::globalElementCount = 0;
static SLock globalElementCountLock;

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
   // for(unsigned int i=0; i<4; i++)
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
   // for(unsigned int i=0; i<4; i++)
   //   oofcerr << " " << (*nodes)[i]->getUid();
   // oofcerr << std::endl;
   connectToNodes();
 #ifdef DEBUG
   if(illegal()) {
     oofcerr << "ILLEGAL " << uid << " " << volume() << std::endl;
     for(unsigned int i=0; i<4; ++i) {
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

 void CSkeletonElement::positionPointer(Coord *x) const {
   for(unsigned int i=0; i<nodes->size(); ++i) {
     x[i] = (*nodes)[i]->position();
   }
 }

 bool CSkeletonElement::interior(const Coord *point) const {
   double bcoords[4];
   Coord x[4];
   positionPointer(x);
   vtkTetra::BarycentricCoords(
       // WTF doesn't vtk declare the const args as const?
       const_cast<Coord*>(point)->xpointer(),
       x[0].xpointer(), x[1].xpointer(),
       x[2].xpointer(), x[3].xpointer(),
       bcoords);
   for(unsigned int i=0; i<4; ++i)
     if(bcoords[i]<0)
       return false;
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
   for(unsigned int i=0; i<4; ++i) {
     epts[i] = (*nodes)[i]->position()/delta;
   }
   return vtkTetra::ComputeVolume(epts[0].xpointer(),epts[1].xpointer(),
				  epts[2].xpointer(),epts[3].xpointer());
 }

 double CSkeletonElement::volumeInFractionalUnits(const CMicrostructure *MS)
   const
 {
   // Get the points that define the element and convert them to pixel
   // units.
   Coord epts[4];
   Coord delta = MS->size();
   for(unsigned int i=0; i<4; ++i) {
     epts[i] = (*nodes)[i]->position()/delta;
   }
   return vtkTetra::ComputeVolume(epts[0].xpointer(),epts[1].xpointer(),
				  epts[2].xpointer(),epts[3].xpointer());
 }

 double CSkeletonElement::cosCornerAngle(unsigned int fid, unsigned int cid)
   const
 {
   Coord x[4];
   Coord s0;
   Coord s1;
   positionPointer(x);
   int *facePtIds = vtkTetra::GetFaceArray(fid);
   // TODO OPT: Some of this dereferencing can be moved out of the loop.
   for(unsigned int i=0; i<3; i++) {
     s0[i] = x[facePtIds[(cid+3-1)%3]][i] - x[facePtIds[cid]][i];
     s1[i] = x[facePtIds[(cid+1)%3]][i] - x[facePtIds[cid]][i];
   }
 #ifdef DEBUG
   if(vtkMath::Norm(s0.xpointer()) == 0 || vtkMath::Norm(s1.xpointer()) == 0)
     throw ErrProgrammingError(
		       "CSkeletonElement: Triangle with zero length edge",
		       __FILE__,__LINE__);
 #endif
   double cosAngle = vtkMath::Dot(s0.xpointer(),s1.xpointer()) /
     (vtkMath::Norm(s0.xpointer())*vtkMath::Norm(s1.xpointer()));
   if(cosAngle > 1.0 || (1-cosAngle) < LEGAL_COS_TOLERANCE)
     return 1.0;
   else if(cosAngle < -1.0 || (cosAngle+1) < LEGAL_COS_TOLERANCE)
     return -1.0;
   return cosAngle;
 }

 double CSkeletonElement::cosCornerAngleSquared(unsigned int fid,
						unsigned int cid)
   const
 {
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

 double CSkeletonElement::solidCornerAngle(unsigned int corner) const {
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
   for(unsigned int i = 0; i<3; i++) {
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

 double CSkeletonElement::cosDihedralAngle(unsigned int face1,
					   unsigned int face2)
   const
 {
   Coord n1;
   Coord n2;
   Coord x[4];
   for(unsigned int i=0; i<4; ++i)
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
   for(unsigned int i=0; i<4; ++i) {
     for(unsigned int j=0; j<3; ++j) {
       double cos = cosCornerAngleSquared(i,j);
       if(cos == 1 || cos == -1) {
	 return true;
       }
     }
   }
   for(unsigned int i=0; i<4; ++i) {
     for(unsigned int j=0; j<i; ++j) {
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
   for(unsigned int i=0; i<4; ++i) {   // loop over faces
     for(unsigned int j=0; j<3; ++j) { // loop over corners of face
       double cos = cosCornerAngleSquared(i,j);
       if( 1-cos < SUSPECT_COS2_TOLERANCE || 1+cos < SUSPECT_COS2_TOLERANCE ) {
   	 // printAngles();
   	 return true;
       }
     }
   }
   for(unsigned int i=0; i<3; ++i) {	 // loop over faces
     for(unsigned int j=i+1; j<4; ++j) { // loop over other faces
       double cos = cosDihedralAngle(i, j);
       if( 1-cos < SUSPECT_COS_TOLERANCE || 1+cos < SUSPECT_COS_TOLERANCE ) {
   	 // printAngles();
   	 return true;
       }
     } 
   }
   return false;
 }

 // Useful for debugging.
 void CSkeletonElement::printAngles() const {
   oofcerr << "CSkeletonElement::printAngles: this=" << *this << std::endl;
   OOFcerrIndent indent(2);
   oofcerr << "corner angles (face, corner, cos, 1-cos, 1+cos): " << std::endl;
   for(unsigned int i=0; i<4; ++i) {
     for(unsigned int j=0; j<3; ++j) {
       double cos = cosCornerAngleSquared(i,j);
       oofcerr << i << " " << j << " " << cos << " " << (1-cos) << " "
		 << (cos+1) << std::endl;
     }
   }
   oofcerr << "dihedral angles: (face, face, cos, 1-cos, 1+cos) " << std::endl;
   for(unsigned int i=0; i<4; ++i) {
     for(unsigned int j=0; j<i; ++j) {
       double cos = cosDihedralAngle(i, j);
       oofcerr << i << " " << j << " " << cos << " " << (1-cos) << " "
		 << (cos+1) << std::endl;
     } 
   }
   if(!parents.empty()) {
     oofcerr << "Parents:" << std::endl;
     OOFcerrIndent indent2(2);
     for(CSkeletonSelectable *p : parents) {
       CSkeletonElement *parent = dynamic_cast<CSkeletonElement*>(p);
       oofcerr << *parent << std::endl;
       OOFcerrIndent indent3(2);
       oofcerr << "edges (node, node, length, dist to opposite edge, ratio)"
	       << std::endl;
       for(unsigned int n0=0; n0<3; n0++) {
	 for(unsigned int n1=n0+1; n1<4; n1++) {
	   double len2, dist2;
	   parent->edgeLengthAndDiameter2(n0, n1, len2, dist2);
	   oofcerr << n0 << " " << n1 << " " << sqrt(len2)
		   << " " << sqrt(dist2) << " ratio=" << sqrt(len2/dist2)
		   << std::endl;
	 }
       }
     }
   }
 }

// Find the distance squared between nodes n0 and n1 divided by the
// distance squared from their midpoint to the midpoint of the
// opposite edge.

void CSkeletonElement::edgeLengthAndDiameter2(unsigned int n0, unsigned int n1,
					      double &len2, double &diam2) const
{
  unsigned int sharedEdge = CSkeletonElement::nodeNodeEdge[n0][n1];
  const CSkeletonNode *node0 = getNode(n0);
  const CSkeletonNode *node1 = getNode(n1);
  Coord3D pos0 = node0->position();
  Coord3D pos1 = node1->position();
  // Find the opposite edge of the tet.
  unsigned int oppEdge = CSkeletonElement::oppEdge[sharedEdge];
  const CSkeletonNode *oppNode0 = getSegmentNode(oppEdge, 0);
  const CSkeletonNode *oppNode1 = getSegmentNode(oppEdge, 1);
  Coord3D oPos0 = oppNode0->position();
  Coord3D oPos1 = oppNode1->position();
  // Find the distance between the midpoints
  diam2 = 0.25*norm2(pos0 + pos1 - oPos0 - oPos1);
  // and the length of the edge
  len2 = norm2(pos0 - pos1);
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonElement::findHomogeneityAndDominantPixel(
						const CSkeletonBase *skel)
   const 
{
  // writeDebugFile("computing el=" + to_string(getUid()) +
  // 		 " hd=" + to_string(homogeneity_data.timestamp()) + 
  // 		 " nodes=");
  // for(unsigned int i=0; i<nodes->size(); ++i)
  //   writeDebugFile(" " + to_string((*nodes)[i]->getUid()) +
  // 		   " " + to_string((*nodes)[i]->nodemoved));
  
  const CMicrostructure *MS = skel->getMicrostructure();
  if(homogeneity_data.timestamp() > MS->getTimeStamp() &&
     homogeneity_data.timestamp() > homogeneityAlgorithmChanged)
    {
      bool uptodate = true;
      // oofcerr << "CSkeletonElement::findHomogeneityAndDominantPixel: el="
      // 	      << getUid() << " nodes= ";
      for(unsigned int i=0; i<nodes->size() && uptodate; ++i) {
	// oofcerr << (*nodes)[i]->getUid() << " " << (*nodes)[i]->nodemoved
	// 		<< " ";
	if(homogeneity_data.timestamp() < (*nodes)[i]->nodemoved) {
	  uptodate = false;
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

// #ifdef DEBUG
//    if(debug()) {
//      oofcerr << "CSkeletonElement::findHomogeneityAndDominantPixel: el="
// 	     << getUid()
// 	     << " hd=" << homogeneity_data.timestamp()
// 	     << " ms=" << MS->getTimeStamp()
// 	     << " nodes=";
//      for(const CSkeletonNode *node : *nodes)
//        oofcerr << node->nodemoved << " ";
//      oofcerr << std::endl;
//    }
// #endif // DEBUG
  homogeneity_data.set_value(c_homogeneity(skel));
}

void CSkeletonElement::resetHomogeneity() {
  // Force homogeneity to be recomputed the next time
  // findHomogeneityAndDominantPixel is called.
  homogeneity_data.clear();
}

HomogeneityData CSkeletonElement::c_homogeneity(const CSkeletonBase *skel) const
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
  // if(suspect()) {
  //   // writeDebugFile("suspect element " + to_string(getUid()) + "\n");
  //   // oofcerr << "CSkeletonElement::c_homogeneity: suspect!" << std::endl;
  //   const CMicrostructure *ms = skel->getMicrostructure();
  //   return HomogeneityData(1.0/(ms->nCategories()+1), UNKNOWN_CATEGORY);
  // }
  switch(getHomogeneityAlgorithm()) {
  case HOMOGENEITY_ROBUST:
    return c_homogeneity_robust(skel);
  case HOMOGENEITY_FAST:
    return c_homogeneity_fast(skel);
  }
  throw ErrProgrammingError("Bad homogeneity algorithm type",
			    __FILE__, __LINE__);
}

HomogeneityData CSkeletonElement::c_homogeneity_robust(
					       const CSkeletonBase *skel) const
{
  // Compute homogeneity by finding the intersection of this element
  // with the polyhedra formed by the voxels in each voxel category.
  
  // writeDebugFile("computing homogeneity for element "+to_string(getUid())+"\n");

  skel->buildVSBs();
  
  double maxvolume = -std::numeric_limits<double>::max();
  double totalVolume = 0;
  int category = 0;
  
  const DoubleVec volumes = categoryVolumes(skel);
  
  for(DoubleVec::size_type i=0; i<volumes.size(); ++i) {
    double volume = volumes[i];
    totalVolume += volume;
    if(volume > maxvolume) {
      maxvolume = volume;
      category = i;
    }
  }

  // Use totalVolume instead of volumeInVoxelUnits() so that round
  // off error in categoryVolumes can't make the homogeneity of a
  // single-category element less than 1.0.
  double homogeneity = maxvolume/totalVolume;

#ifdef DEBUG
  double dV = totalVolume - volumeInVoxelUnits(skel->getMicrostructure());
  if(abs(dV) > 1.e-10)
    oofcerr << "CSkeletonElement::c_homogeneity: deltaV=" << dV << "!"
	    << std::endl;
#endif // DEBUG
  
  // oofcerr << "CSkeletonElement::c_homogeneity: element=" << getIndex()
  // 	   << " homogeneity=" << homogeneity
  // 	   << " (1-" << (1-homogeneity) <<")" << std::endl;
  
  if(homogeneity > 1.0)
    homogeneity = 1.0;
  return HomogeneityData(homogeneity, category);
}

HomogeneityData CSkeletonElement::c_homogeneity_fast(const CSkeletonBase *skel)
  const
{
  // Compute the homogeneity by counting the number of voxels in each
  // voxel category whose centers are within the element.  This is
  // faster than homogeneity_robust (maybe) but will be less accurate,
  // especially for small elements.
  
  const CMicrostructure *ms = skel->getMicrostructure();
  Coord3D voxsize= ms->sizeOfPixels();
  unsigned int ncat = ms->nCategories();
  std::vector<int> counts(ncat, 0); // # of voxels in each category in the elmt
  
  // Get the corners of the element in voxel coordinates.
  std::vector<Coord3D> epts = pixelCoords(ms);
  // Get the element's bounding box in voxel coordinates.
  ICRectangularPrism bbox(ms->pixelFromPoint((*nodes)[0]->position()),
			  ms->pixelFromPoint((*nodes)[1]->position()));
  bbox.swallow(ms->pixelFromPoint((*nodes)[2]->position()));
  bbox.swallow(ms->pixelFromPoint((*nodes)[3]->position()));

  // Loop over voxels
  bool foundone = false;
  for(unsigned int x=bbox.xmin(); x<=bbox.xmax(); x++)
    for(unsigned int y=bbox.ymin(); y<=bbox.ymax(); y++)
      for(unsigned int z=bbox.zmin(); z<=bbox.zmax(); z++)
	{
	  ICoord3D voxel(x, y, z);
	  Coord3D center = voxel + Coord3D(0.5, 0.5, 0.5);
	  Coord3D realcenter(center[0]*voxsize[0], center[1]*voxsize[1],
			     center[2]*voxsize[2]);
	  if(interior(&realcenter)) {
	    ++counts[ms->category(voxel)];
	    foundone = true;
	  }
	}

  if(foundone) {
    int total = 0;
    int topcount = -1;
    int category = -1;
    for(int i=0; i<counts.size(); i++) {
      int c = counts[i];
      total += c;
      if(c > topcount) {
	topcount = c;
	category = i;
      }
    }
    double homogeneity = topcount/((double) total);
    return HomogeneityData(homogeneity, category);
  }

  // No voxel centers were found inside the element.  The algorithm is
  // obviously failing.  Set the homogeneity to 1.0 and the category
  // to the category of the voxel at the center of the element.  
  Coord3D center = 0.25*(epts[0] + epts[1] + epts[2] + epts[3]);
  ICoord3D voxel = ms->pixelFromPoint(center);
  return HomogeneityData(1.0, ms->category(voxel));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

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

// Some of this topology info is no longer needed.  A lot of it was
// created for the homogeneity code, which has been completely
// rewritten.  It's left in here because it might be useful again and
// isn't impoosing any kind of performance penalty.

// Maps the edge ids at the face scope to edge ids at the tet scope.
const unsigned int CSkeletonElement::faceEdges[4][3] = {{0,4,3},
							{1,5,4},
							{2,3,5},
							{2,1,0}};
// Map edge ids at tet scope to edge ids at face scope.
const unsigned int CSkeletonElement::tetEdge2FaceEdge[4][6] =
  {{0, NONE, NONE, 2, 1, NONE},	 // face 0
   {NONE, 0, NONE, NONE, 2, 1},	 // face 1
   {NONE, NONE, 0, 1, NONE, 2},	 // face 2
   {2, 1, 0, NONE, NONE, NONE}}; // face 3
								

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
const unsigned int CSkeletonElement::edgeFaces[6][2] = {{0,3},
							{1,3},
							{2,3},
							{0,2},
							{0,1},
							{1,2}};

// Maps an edge index to the the two nodes at its ends.
const unsigned int CSkeletonElement::edgeNodes[6][2] = {{0,1},
							{1,2},
							{0,2},
							{0,3},
							{1,3},
							{2,3}};

// Gives the face between two edges.  NONE means the entry shouldn't
// be used.
const unsigned int CSkeletonElement::edgeEdgeFace[6][6] =
  {{NONE, 3, 3, 0, 0, NONE}, 
   {3, NONE, 3, NONE, 1, 1},
   {3, 3, NONE, 2, NONE, 2},
   {0, NONE, 2, NONE, 0, 2},
   {0, 1, NONE, 0, NONE, 1},
   {NONE, 1, 2, 2, 1, NONE}};

// Gives the face between an edge and a node.
const unsigned  int CSkeletonElement::nodeEdgeFace[4][6] =
  {{NONE, 3, NONE, NONE, 0, 2},
   {NONE, NONE, 3, 0, NONE, 1},
   {3, NONE, NONE, 2, 1, NONE},
   {0, 1, 2, NONE, NONE, NONE}};

// Gives the edge between two faces. 
const unsigned int CSkeletonElement::faceFaceEdge[4][4] =
  {{NONE, 4, 3, 0},
   {4, NONE, 5, 1},
   {3, 5, NONE, 2},
   {0, 1, 2, NONE}};

// Gives the node shared by two edges.
const unsigned int CSkeletonElement::edgeEdgeNode[6][6] =
  {{NONE, 1, 0, 0, 1, NONE},
   {1, NONE, 2, NONE, 1, 2},
   {0, 2, NONE, 0, NONE, 2},
   {0, NONE, 0, NONE, 3, 3},
   {1, 1, NONE, 3, NONE, 3},
   {NONE, 2, 2, 3, 3, NONE}};

// Gives the face opposite a node -- that is the only face that the
// given node is not a part of.
const unsigned int CSkeletonElement::oppFace[4] = {1,2,0,3};

// Gives the node opposite a face -- inverse of oppFace
const unsigned int CSkeletonElement::oppNode[4] = {2,0,1,3};

// Maps an edge id to the opposite edge id -- the only edge that the
// given edge is not connected to. This map is its own inverse.
const unsigned int CSkeletonElement::oppEdge[6] = {5,3,4,1,2,0};

// Maps a node to the three faces it is on.
const unsigned int CSkeletonElement::nodeFaces[4][3] = {{0,2,3},
							{0,1,3},
							{1,2,3},
							{0,1,2}};

// Maps a node to the three edges it is on.
const unsigned int CSkeletonElement::nodeEdges[4][3] = {{0,2,3},
							{0,1,4},
							{1,2,5},
							{3,4,5}};

// ccwNodeEdges is the same as nodeEdges except that the edges are
// ordered.  They go counterclockwise, as viewed at the node and
// facing the opposite face.  TODO: We could get rid of nodeEdges and
// just use ccwNodeEdges, but that might break the regression tests.
const unsigned int CSkeletonElement::ccwNodeEdges[4][3] = {{0,3,2},
							   {0,1,4},
							   {1,2,5},
							   {3,4,5}};
// cwNodeEdges is the same as ccwNodeEdges, but the ordering is
// reversed.
const unsigned int CSkeletonElement::cwNodeEdges[4][3] = {{0,2,3},
							  {0,4,1},
							  {1,5,2},
							  {3,5,4}};

// Gives the edge between two nodes.
const unsigned int CSkeletonElement::nodeNodeEdge[4][4] =
   {{NONE,0,2,3},
    {0,NONE,1,4},
    {2,1,NONE,5},
    {3,4,5,NONE}};

// Given an edge that's above an intersecting plane that intersects
// the edges four neighboring edges, this gives the indices of the
// neighboring edges such that the intersection points are ordered in
// a counterclockwise polygon on the plane.
const unsigned int CSkeletonElement::ccwNeighborEdgeOrder[6][4] =
  {{1,4,3,2},
   {0,2,5,4},
   {1,0,3,5},
   {0,4,5,2},
   {0,1,5,3},
   {1,2,3,4}};
// The other direction
const unsigned int CSkeletonElement::cwNeighborEdgeOrder[6][4] =
  {{2,3,4,1},
   {4,5,2,0},
   {5,3,0,1},
   {2,5,4,0},
   {3,5,1,0},
   {4,3,2,1}};

 // // Gives the parametric coordinate of the node for the edge given above.
 // const double CSkeletonElement::nodeEdgeParam[4][3] = {{0.0, 1.0, 0.0},
 // 						       {1.0, 0.0, 0.0}, 
 // 						       {1.0, 0.0, 0.0},
 // 						       {1.0, 1.0, 1.0}};

// Given a face f and a segment s, return the index of the other face
// shared by that segment.
unsigned int CSkeletonElement::getOtherFaceIndex(unsigned int f,
						 unsigned int s)
{
  unsigned int f0 = edgeFaces[s][0];
  unsigned int f1 = edgeFaces[s][1];
#ifdef DEBUG
  if(f != f0 && f != f1) {
    oofcerr << "CSkeletonElement::getOtherFaceIndex: f=" << f << " s=" << s
	    << " f0=" << f0 << " f1=" << f1 << std::endl;
    throw ErrProgrammingError("getOtherFaceIndex failed!", __FILE__, __LINE__);
  }
#endif // DEBUG
  return (f == f0? f1 : f0);
}

 /*
      END TETRAHEDRA TOPOLOGY INFO
 */

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given a vector of node positions, return the faces of the element
// as COrientedPlanes.  This doesn't get the node positions from the
// element itself, so that it can be used in different coordinate
// systems. It's a CSkeletonElement method only because if we ever
// have different element shapes, they'll have to have different
// getPlanes methods.

// Uses VSBPlane<Coord3D> instead of COrientedPlane because the planes
// are passed to the VSB code, which preserves modularity by not
// knowing the OOF3D plane class.

std::vector<VSBPlane<Coord3D>> CSkeletonElement::getPlanes(
					const std::vector<Coord3D> &epts)
  const
{
  std::vector<VSBPlane<Coord3D>> planes;
  planes.reserve(4);
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    Coord3D pt0 = epts[CSkeletonElement::getFaceArray(f)[0]];
    Coord3D pt1 = epts[CSkeletonElement::getFaceArray(f)[1]];
    Coord3D pt2 = epts[CSkeletonElement::getFaceArray(f)[2]];
    Coord3D center = (pt0 + pt1 + pt2)/3.0;
    // A more symmetric but more expensive expression for the area is
    // 0.5*(pt0%pt1 + pt1%pt2 + pt2%pt0).
    Coord3D areaVec = 0.5*((pt1 - pt0) % (pt2 - pt0));
    Coord3D normalVec = areaVec/sqrt(norm2(areaVec));
    double offset = dot(center, normalVec);
    planes.emplace_back(normalVec, offset);
  }
  return planes;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// categoryVolumes is the core of the homogeneity calculation. It
// calculates the volume intersection of a tetrahedral element with a
// voxelized region representing a material category in a
// microstructure.

// VOLTOL is the allowed fractional error in the sum of the volumes of
// the voxel categories relative to the total volume of the element.
//#define VOLTOL 5.e-4
#define VOLTOL 1.e-10

// categoryVolumes returns a vector containing the volume of the
// intersection of this element with each voxel category.  It's used
// by c_homogeneity to compute element homogeneities.

const DoubleVec CSkeletonElement::categoryVolumes(const CSkeletonBase *skel)
  const
{
  const CMicrostructure *ms = skel->getMicrostructure();
  // Get the corners and planes of the element in voxel coordinates.
  std::vector<Coord3D> epts = pixelCoords(ms);
  std::vector<VSBPlane<Coord3D>> planes = getPlanes(epts);
  // Get the element's bounding box in voxel coordinates.
  CRectangularPrism bbox(epts[0], epts[1]);
  bbox.swallow(epts[2]);
  bbox.swallow(epts[3]);

  // Get the number of voxel categories.  This recomputes categories
  // and boundaries if needed.
  unsigned int ncat = ms->nCategories();
  DoubleVec result(ncat, 0.0);
  double totalVol = 0.0;

  try {
    for(unsigned int cat=0; cat<ncat; cat++) {
// #ifdef DEBUG
// 	setVerboseVSB(index == 0 && cat == 1);
// #endif // DEBUG
      double vol = skel->clippedCategoryVolume(cat, bbox, planes);
      totalVol += vol;
      result[cat] = vol;
    } // end loop over categories

#ifdef DEBUG
    double actual = volumeInVoxelUnits(ms);
    double fracvol = (totalVol - actual)/actual;
    bool badvol = fabs(fracvol) >= VOLTOL;
    if(badvol) {
      oofcerr << "CSkeletonElement::categoryVolumes: element index=" << index
	      << " uid=" << uid
	      <<" measured volume=" << totalVol
	      << " [" << result << "]"
	      << " actual=" << actual
	      << " (error=" << fracvol*100 << "%)" << std::endl;
      // if(verboseVSB()) {
      // 	oofcerr << "CSkeletonElement::categoryVolumes: saving VSBs:" << std::endl;
      // 	for(unsigned int cat=0; cat < ncat; cat++) {
      // 	  if(result[cat] > 0) {
      // 	    std::string filename = "vsb_" + to_string(cat);
      // 	    oofcerr << "CSkeletonElement::categoryVolumes: " << filename
      // 		    << std::endl;
      // 	    skel->saveClippedVSB(cat, planes, filename);
      // 	  }
      // 	}
      // }
    }
    // TODONT: Throwing an exception here is incorrect.  If the Skeleton
    // contains illegal elements, it's possible that this element is
    // legal (shape-wise) but has nodes outside the Microstructure.
    // In that case some of its volume won't be in any pixel category.
#endif // DEBUG
  }
  catch (...) {
    oofcerr << "CSkeletonElement::categoryVolumes: failed for "
	    << *this << std::endl;
    throw;
  }

  return result;
} // end CSkeletonElement::categoryVolumes

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Compute the positions of the element's nodes in pixel coordinates.
// Used in homogeneity calculations.

std::vector<Coord3D> CSkeletonElement::pixelCoords(const CMicrostructure *ms)
  const
{
  std::vector<Coord3D> epts;
  epts.reserve(nnodes());
  Coord delta = ms->sizeOfPixels();
  for(unsigned int i=0; i<nnodes(); ++i) {
    Coord x = (*nodes)[i]->position();
    epts.push_back(x/delta);	// component-wise division
  }
  return epts;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


double CSkeletonElement::homogeneity(const CSkeletonBase *skel) const {
  findHomogeneityAndDominantPixel(skel);
  return homogeneity_data.value().get_homogeneity();
}

double CSkeletonElement::energyHomogeneity(const CSkeletonBase *skel) const {
  findHomogeneityAndDominantPixel(skel);
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

int CSkeletonElement::dominantPixel(const CSkeletonBase *skel) const {
  findHomogeneityAndDominantPixel(skel);
  return homogeneity_data.value().get_dominantpixel();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

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
  for(unsigned int i=0; i<4; ++i) {
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
  int dominantpixel = dominantPixel(skel);
  // getMaterialFromCategory is declared in material.h
  return getMaterialFromCategory(skel->getMicrostructure(), dominantpixel);
}

double CSkeletonElement::energyTotal(const CSkeletonBase *skel, double alpha)
  const 
{
  if(alpha == 1)
    return energyHomogeneity(skel);
  Coord x[4];
  positionPointer(x);
  if(alpha == 0)
    return energyShape(x);
  double eHomog = energyHomogeneity(skel);
  double eShape = energyShape(x);
  // writeDebugFile(to_string(getUid()) +
  // 		 " eHomog=" + to_string(eHomog) +
  // 		 " eShape=" + to_string(eShape) + "\n");
  return alpha*eHomog + (1-alpha)*eShape;
}

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

#ifdef DEBUG
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
#endif // DEBUG

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
				   const MasterElement *master,
				   const CSkeleton *skel,
				   SkelElNodeMap &edgeNodeMap,
				   SkelElNodeMap &faceNodeMap,
				   Material *mat) 
{
  const Material *m = (mat == nullptr? material(skel) : mat);
  Element *el = master->build(this, skel, femesh, m, edgeNodeMap, faceNodeMap);
  femesh->addElement(el);
  setMeshIndex(idx);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonElement::print(std::ostream &os) const {
  // os << "Element(" << uid << ", " << generating_function << ")";
  os << "Element(uid=" << uid
     << ", index=" << index
     << ", ";
  printNodes(os);
  os << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// These routines help to debug categoryVolumes. 

#ifdef DEBUG

void CSkeletonElement::drawVoxelCategoryIntersection(LineSegmentLayer *layer,
						     const CSkeletonBase *skel,
						     unsigned int category)
  const
{
  const CMicrostructure *ms = skel->getMicrostructure();
  ms->categorizeIfNecessary();
  std::vector<Coord3D> epts = pixelCoords(ms);
  std::vector<VSBPlane<Coord3D>> planes = getPlanes(epts);
  const VoxelSetBoundary *vsb = skel->getVoxelSetBoundary(category);
  auto *clipped = vsb->clipped(planes);
  int nEdges = clipped->nEdges();
  layer->set_nSegs(nEdges);
  auto iter = clipped->iterator();
  while(!iter.done()) {
    layer->addSegment(&iter.node0()->position, &iter.node1()->position);
    iter.next();
  }
  delete clipped;
}

#endif // DEBUG

