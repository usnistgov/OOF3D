// -*- C++ -*-
// $RCSfile: crationalizers.C,v $
// $Revision: 1.1.4.47 $
// $Author: langer $
// $Date: 2014/12/14 22:49:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/cdebug.h"
#include "common/coord.h"
#include "common/progress.h"
#include "common/random.h"
#include "common/tostring.h"
#include "common/IO/oofcerr.h"
#include "engine/crationalizers.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonsegment.h"

#include <vtkTetra.h>
#include <algorithm>
#include <math.h>

#define DEG2RAD M_PI/180
#define DEG2RAD2 DEG2RAD*DEG2RAD

#include <unistd.h>		// for getpid when debugging

bool verbose = false;		// for debugging

Rationalizer::Rationalizer() {
  // oofcerr << "Rationalizer::ctor: " << this << std::endl;
}

Rationalizer::~Rationalizer() {
  // oofcerr << "Rationalizer::dtor: " << this << std::endl;
}

void Rationalizer::rationalize(CSkeleton *skel, CSkelModTargets *targets,
			       CSkelModCriterion *criterion,
			       FixerFunction fixer)
{
  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("Fixing bad tetrahedra",
						DEFINITE));
  num_rationalized = 0;
  int count = 0;

  try {

    CSkeletonElementVector &elements = targets->getTargets(skel);
    std::set<int> processed;
    OOFRandomNumberGenerator r;
    oofshuffle(elements.begin(), elements.end(), r);

#ifdef DEBUG
    int nel = elements.size(); 
#endif

    for(CSkeletonElementIterator it=elements.begin(); it!=elements.end();
	++it, ++count) 
      {
	assert(elements.size() == nel);
	if(!processed.count((*it)->getUid()) && (*it)->active(skel)) {
	  assert(!(*it)->is_defunct());
	  // fixer is either Rationalizer::findAndFix or
	  // Rationalizer::fixAll.
	  ProvisionalChangesVector *changes = (this->*fixer)(skel,(*it));

	  // TODO OPT: find some way to eliminate the dynamic_cast here.
	  ProvisionalChanges *bestChange = 
	    dynamic_cast<ProvisionalChanges*>(
				      criterion->getBestChange(changes,skel));

	  // Rationalize is applied to a completeCopy of the original
	  // skeleton, so all operations performed here are done in
	  // place (unlike Refine, which builds a copy as it goes).
	  // Thus if bestChange is 0, there's nothing to do.
	  if(bestChange) {
	    bestChange->accept();
	    // #ifdef DEBUG
	    // 	bestChange->sanityCheck();
	    // #endif
	    num_rationalized += bestChange->nRemoved();
	    for(CSkeletonElementSet::iterator
		  rit=bestChange->getRemoved().begin();
		rit!=bestChange->getRemoved().end(); ++rit)
	      {
		processed.insert((*rit)->getUid()); 
	      }
	    for(CSkeletonSelectablePairSet::iterator 
		  pit=bestChange->getSubstitutions().begin(); 
		pit != bestChange->getSubstitutions().end(); ++pit)
	      {
		processed.insert((*pit).first->getUid());
	      }
	  } // end if bestChange != NULL
	  progress->setFraction(float(count)/elements.size());
	  progress->setMessage(to_string(count) + "/"
			       + to_string(elements.size()));
	  for(ProvisionalChangesVector::iterator pcvit = changes->begin();
	      pcvit != changes->end(); ++pcvit) 
	    {
	      delete *pcvit;
	    }
	  delete changes;
	} // end if not processed
      }	  // end loop over elements
    skel->cleanUp();    // closeDebugFile();
  }
  catch (...) {
    progress->finish();
    throw;
  }
  progress->finish();
} // end Rationalizer::rationalize

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RemoveBadTetrahedra::RemoveBadTetrahedra(double acute_angle,
					 double obtuse_angle) 
{
  acute = cos(acute_angle*DEG2RAD);
  obtuse = cos(obtuse_angle*DEG2RAD);
  // Convert angles into solid angles by assuming that the angle is
  // the opening angle of a cone.  A cone with opening angle 2*theta
  // subtends a solid angle 2*pi*(1-cos(theta)).
  small_solid = 2*M_PI*(1.0 - cos(0.5*acute_angle*DEG2RAD));
  large_solid = 2*M_PI*(1.0 - cos(0.5*obtuse_angle*DEG2RAD));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void RemoveBadTetrahedra::findAngles(const CSkeletonElement *element,
				     bool forced)
  const
{
  // TODO OPT: Use a class or struct instead of a std::pair for the
  // contents of the obtuse and acute angle lists.  It'll make the
  // meaning of the elements clearer.

  // TODO OPT: These vectors should not be class members.  That'll make it
  // hard to parallelize this operation.
  obtuse_angles.clear();
  acute_angles.clear();
  small_solid_angles.clear();
  large_solid_angles.clear();
  large_dihedral_angles.clear();
  small_dihedral_angles.clear();

  // If forced is true, don't use the given limits for acceptable
  // acute and obtuse angles.  Check all angles.
  double acute_ = acute, obtuse_, small_solid_, large_solid_;
  if(!forced) {
    acute_ = acute;
    obtuse_ = obtuse;
    small_solid_ = small_solid;
    large_solid_ = large_solid;
  }
  else {
    acute_ = 0;
    obtuse_ = 0;
    small_solid_ = 2*M_PI*(1.- cos(45*DEG2RAD));
    large_solid_ = small_solid_;
  }
  

  // First check the angle of each vertex
  for(int i=0; i<4; ++i) {	// loop over faces
    for(int j=0; j<3; ++j) {	// loop over corners of the face
      double cosAngle = element->cosCornerAngle(i,j);
      if(cosAngle <= obtuse_)
	obtuse_angles.push_back( std::pair<short,short>(i,j) );
      if(cosAngle >= acute_)
	acute_angles.push_back( std::pair<short,short>(i,j) );
    }
  }

  // now the solid angles
  for(int i=0; i<4; ++i) {	// loop over corners of the element
    double solidAngle = element->solidCornerAngle(i);
    if(solidAngle <= small_solid_)
      small_solid_angles.push_back(i);
    if(solidAngle >= large_solid_)
      large_solid_angles.push_back(i);
  }
  // if there are three small solid angles, we treat the fourth as a
  // large angle
  if(small_solid_angles.size() == 3 && large_solid_angles.empty()) {
    // TODO OPT: Why not just
    // large_solid_angles.push_back(6-sum of small_solid_angles)?
    for(int i=0; i<4; ++i) {
      if(small_solid_angles[0] != i && small_solid_angles[1] != i
	 && small_solid_angles[2] != i) 
	{
	  large_solid_angles.push_back(i);
	  break;
	}
    }
  }

  // finally the dihedral angles
  for(int i=0; i<6; ++i) {
    const int *faceIds = CSkeletonElement::edgeFaces[i];
    double cosAngle = element->cosDihedralAngle(faceIds[0], faceIds[1]);
    if(cosAngle <= obtuse_)
      large_dihedral_angles.push_back( i );
    if(cosAngle >= acute_)
      small_dihedral_angles.push_back( i );
  }

}

ProvisionalChangesVector *RemoveBadTetrahedra::findAndFix(
				  CSkeleton *skel, 
				  CSkeletonElement *element)
  const
{

  findAngles(element, false);
  int nbad = (obtuse_angles.size() + acute_angles.size() +
	      large_solid_angles.size() + small_solid_angles.size() + 
	      large_dihedral_angles.size() + small_dihedral_angles.size());
  if(nbad == 0)
    return new ProvisionalChangesVector; // return empty vector
  
  return fix(skel, element);
} // end RemoveBadTetrahedra::findAndFix


ProvisionalChangesVector* RemoveBadTetrahedra::fixAll(
			      CSkeleton *skel, CSkeletonElement *element)
  const
{
  findAngles(element, true);
  return fix(skel, element);
  // ProvisionalChangesVector *changes = new ProvisionalChangesVector;
  // return changes;
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Helper functions

 static void getCentroidAndMidpoints(const CSkeletonFace *face,
				     Coord midpoints[3], Coord& centroid)
 {

   for(int i=0; i<3; ++i) 
     midpoints[i] = 0.5*(face->getNode(i)->position() + 
			 face->getNode((i+1)%3)->position());
   centroid = face->center();
 }

 // gets what the mobility for node should be if it is moved to the
 // centroid of nodes.
 static void getMobility(const CSkeletonNodeVector *nodes, 
			 const CSkeletonNode *node, bool mobility[3]) 
 {
   // mobility[i] is true if any of "nodes" is mobile in the i
   // direction and "node" is also mobile in the i direction.
   mobility[0] = mobility[1] = mobility[2] = false;
   for(CSkeletonNodeIterator it=nodes->begin(); it!=nodes->end(); ++it) {
     mobility[0] = (mobility[0] || (*it)->movable_x());
     mobility[1] = (mobility[1] || (*it)->movable_y());
     mobility[2] = (mobility[2] || (*it)->movable_z());
   }
   mobility[0] &= node->movable_x();
   mobility[1] &= node->movable_y();
   mobility[2] &= node->movable_z();
 }

 static int getMobility(OuterFaceID fn, bool mobility[3]) {
   mobility[0] = true;
   mobility[1] = true;
   mobility[2] = true;
   mobility[fn.direction()] = false;
   return fn.direction();
 }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class SplitTetCallback {
protected:
  CSkeleton *skeleton;
public:
  SplitTetCallback(CSkeleton *skel) : skeleton(skel) {}
  virtual ~SplitTetCallback() {}
  virtual bool callback(ProvisionalChanges*, CSkeletonElement*,
			CSkeletonNode*)
    const
  {
    return true;
  }
};

static SplitTetCallback nullCallback(0);


// Utility function used by splitTetrahedronInHalf.  Given three
// nodes, knode, nodeA, and nodeB, where (nodeA, nodeB) is an existing
// segment in the Skeleton skel, make appropriate segment
// substitutions in the ProvisionalChanges object if the three nodes
// lie on an edge boundary of skel.

void edgeTest_(CSkeleton *skel,
	       CSkeletonNode *knode,
	       CSkeletonNode *nodeA,
	       CSkeletonNode *nodeB,
	       ProvisionalChanges *change)
{
  CSkeletonNodeVector nodes(3);
  nodes[0] = knode;
  nodes[1] = nodeA;
  nodes[2] = nodeB;
  if(skel->onOuterEdge(&nodes)) {
    CSkeletonSegment *oldseg = skel->findExistingSegment(nodeA, nodeB);
    assert(oldseg != NULL);
    // Find out if knode is between nodeA and nodeB.
    Coord dA = knode->position() - nodeA->position();
    Coord dB = knode->position() - nodeB->position();
    if(dot(dA, dB) > 0)
      {
	// knode is off to one side
	CSkeletonNode* fartherNode = (norm2(dA) > norm2(dB) ? nodeA : nodeB);
	// oofcerr << "edgeTest_: one sub: " << *oldseg << " --> " 
	// 	<< *knode << " " << *fartherNode << std::endl;
	change->substituteSegment(oldseg, knode, fartherNode);
      }
    else
      {
	// knode is in the middle
	// oofcerr << "edgeTest_: two subs A: " << *oldseg
	// 	<< " --> " << *knode << " " << *nodeA << std::endl;
	// oofcerr << "edgeTest_: two subs B: " << *oldseg
	// 	<< " --> " << *knode << " " << *nodeB << std::endl;
	change->substituteSegment(oldseg, knode, nodeA);
	change->substituteSegment(oldseg, knode, nodeB);
      }
  }
}
	       

// TODO 3.1: If removeFlat(), tetTetSplit, etc, belonged to separate
// subclasses of Rationalize, instead of being all called from a
// single subclass, then splitTetrahedronInHalf() would be a base
// class method and wouldn't need callback or callbackData args.

static bool splitTetrahedronInHalf(CSkeletonElement *element, 
				   CSkeletonSegment *seg,
				   CSkeletonNode *knode, 
				   ProvisionalChanges *change, 
				   CSkeleton *skel,
				   SplitTetCallback *callback,
				   const std::string &name) 
{
  // Split a tet in half by replacing edge "seg" with two new segments
  // joined at node "knode".  The new face joining the two halves
  // consists of node "knode" and the nodes on the original segment
  // opposite "seg".

  // Note that the new node knode need not be on the old segment, so
  // it's possible that one of the two new elements is squashed flat
  // on a boundary.  In that case, it shouldn't be created, and the
  // net effect is just that the old element has one node replaced by
  // the new node.
  
  // Actually, it's not quite that simple.  The squashed element is a
  // quadrilateral which can be divided into triangles in two ways.
  // One of those ways corresponds to boundary faces on the old
  // skeleton, and the other way corresponds to boundary faces on the
  // new skeleton.  We need to use the face substitution machinery to
  // establish the parent-child relationships for the triangles so
  // that the boundary will be propagated properly to the new
  // faces.  Ditto for the segments.

  // oofcerr << "splitTetrahedronInHalf: ----- " << std::endl;
  // oofcerr << "splitTetrahedronInHalf: element=" << *element << std::endl;
  // oofcerr << "splitTetrahedronInHalf: seg=" << *seg << std::endl;

  // change->annotate <<"splitTetrahedronInHalf: splitting " << *element
  // 		   << std::endl;
  // change->annotate << "splitTetrahedronInHalf:     seg= " << *seg
  // 		   << std::endl;
  // change->annotate << "splitTetrahedronInHalf:   knode= " << *knode
  // 		   << std::endl;

  change->removeElement(element);

  for(int i=0; i<2; i++) {	// loop over endpoints of seg & element halves
    CSkeletonNode *endpoint = seg->getNode(i);
    CSkeletonNodeVector *newNodes = 
      new CSkeletonNodeVector(*element->getNodes());
    for(unsigned int j=0; j<4; j++) { // loop over old nodes
      // Find the old node that is the i^th endpoint of seg.
      if(*(*newNodes)[j] == *endpoint) {
	// newNodes[j] is an endpoint of seg.  Replace it with the new
	// node to make a new element.  The new element uses the
	// *other* endpoint of seg.
	(*newNodes)[j] = knode;
	if(!skel->onOuterFace(newNodes)) {
	  // The new element isn't squashed.
	  CSkeletonElement *newElement = new CSkeletonElement(newNodes,
						element->getParents(), name);
	  // change->annotate << "splitTetrahedronInHalf: newElements["
	  // 		   << i << "] =" << *newElement << std::endl;
	  change->insertElement(newElement);
	  // oofcerr << "splitTetrahedronInHalf: substituting: "
	  // 	  << *seg << " --> " << *node << " " << *seg->getNode(1-i)
	  // 	  << std::endl;
	  change->substituteSegment(seg, knode, seg->getNode(1-i));
	  if(!callback->callback(change, newElement, knode))
	    return false;
	}
	else {
	  // The element half is squashed.  The face that *doesn't*
	  // contain knode has to be substituted by the faces that do
	  // contain knode.  Some of the new faces might not actually
	  // exist in the modified skeleton, but the substitution
	  // routine should check for that.
	  // change->annotate << "splitTetrahedronInHalf: squashed: "
	  // 		   << derefprint(*newNodes) << std::endl;
	  CSkeletonMultiNodeKey fk((*newNodes)[(j+1)%4],
				   (*newNodes)[(j+2)%4],
				   (*newNodes)[(j+3)%4]);
	  CSkeletonFace *f = skel->getFace(fk);
	  change->substituteFace(f, knode,
				 (*newNodes)[(j+1)%4], (*newNodes)[(j+2)%4]);
	  change->substituteFace(f, knode, 
				 (*newNodes)[(j+2)%4], (*newNodes)[(j+3)%4]);
	  change->substituteFace(f, knode, 
				 (*newNodes)[(j+3)%4], (*newNodes)[(j+1)%4]);
	  // If any three nodes (one of which must be knode) of the
	  // collapsed element are colinear on an edge boundary, the
	  // new edges (containing knode) subtitute for the old edge,
	  // which doesn't contain knode.
	  edgeTest_(skel, knode, (*newNodes)[(j+1)%4], (*newNodes)[(j+2)%4],
		   change);
	  edgeTest_(skel, knode, (*newNodes)[(j+2)%4], (*newNodes)[(j+3)%4],
		    change);
	  edgeTest_(skel, knode, (*newNodes)[(j+3)%4], (*newNodes)[(j+1)%4],
		    change);

	  delete newNodes;
	}
	break;		// go to next value of i
      }			// end if newNodes[j] == endpoint
    } // end loop over old nodes j
  } // end loop over endpoints i of seg

  // change->annotate << "splitTetrahedronInHalf: done" << std::endl;
  // oofcerr << "splitTetrahedronInHalf: done" << std::endl;
  return true;
} // end splitTetrahedronInHalf

static void tetNoneSplit(CSkeleton *skel,
			 CSkeletonNode *obtuseNode, 
			 CSkeletonFace *oppFace,
			 CSkeletonElement *el, 
			 ProvisionalChangesVector *changes)
{
  Coord midpoints[3];
  Coord centroid;
  bool mobility[3];
  getCentroidAndMidpoints(oppFace, midpoints, centroid);
  
  // move obtuseNode to centroid, removing this tet
  if(obtuseNode->canMoveTo(centroid)) {
    ProvisionalChanges *change = new ProvisionalChanges(skel, "tetNoneSplit");
    getMobility(oppFace->getNodes(), obtuseNode, mobility);
    change->moveNode(obtuseNode, centroid, mobility);
    change->removeElement(el);

    // The other three faces substitute for the oppFace
    for(unsigned int i = 0; i < el->getNumberOfFaces(); ++i) {
      CSkeletonMultiNodeKey h = el->getFaceKey(i);
      CSkeletonFace *f = skel->getFace(h);
      if(*f != *oppFace) 
	change->substituteFace(oppFace, f);
    }
    // change->checkVolume();
    changes->push_back(change);
  }

  for(int i=0; i<3; ++i) {
    // Move the obtuse node to the midpoint of oppFace's i^th segment.
    if(obtuseNode->canMoveTo(midpoints[i])) {
      ProvisionalChanges *change = new ProvisionalChanges(skel, 
							  "tetNoneSplit2");
      CSkeletonSegment *seg = skel->getFaceSegment(oppFace, i);
      getMobility(seg->getNodes(), obtuseNode, mobility);
      change->moveNode(obtuseNode, midpoints[i], mobility);
      CSkeletonFace *collapsedFace = skel->findExistingFace(
			    seg->getNode(0), seg->getNode(1), obtuseNode);
      // TODO OPT: There are checks below to see if collapsedFace is
      // 0.  Can it ever be 0?  That should be impossible, it seems.
      assert(collapsedFace != NULL);
      CSkeletonElement *collapsedElement = skel->getSister(el, collapsedFace);
      CSkeletonElementVector segElements, splitElements;
      skel->getSegmentElements(seg, segElements);
      for(CSkeletonElementIterator it=segElements.begin();
	  it!=segElements.end(); ++it) 
	{
	  if(**it != *el && 
	     (collapsedElement == NULL || **it != *collapsedElement))
	    splitElements.push_back(*it);
	}
      change->removeElement(el);

      // The two uncollapsed faces substitute for the oppFace
      for(unsigned int i = 0; i < el->getNumberOfFaces(); ++i) {
	CSkeletonMultiNodeKey h = el->getFaceKey(i);
	CSkeletonFace *f = skel->getFace(h);
	if(*f != *oppFace && *f != *collapsedFace) 
	  change->substituteFace(oppFace, f);
      }

      // If there are no split elements, substitute some segments.
      // The two segments leading from the obtuse node to the
      // endpoints of segment i substitute for segment i.
      if(splitElements.empty() && collapsedFace != NULL) {
	CSkeletonSegmentSet subsegs;
	for(int f=0; f<3; ++f) {
	  CSkeletonSegment *fseg = skel->getFaceSegment(collapsedFace, f);
	  if(fseg->getNode(0) == obtuseNode || fseg->getNode(1) == obtuseNode)
	    subsegs.insert(fseg);
	}
	for(CSkeletonSegmentSet::iterator s=subsegs.begin(); s!=subsegs.end();
	    ++s) 
	  {
	    change->substituteSegment(seg, *s);
	  }
      }
      
      if(collapsedElement != NULL) {
	// If the collapsed element is on the boundary, set the
	// parents for that as well.
	CSkeletonFace *faceOnBoundary = NULL;
	CSkeletonFaceSet substitutes;
	for(unsigned int i=0; i<collapsedElement->getNumberOfFaces(); ++i) {
	  CSkeletonMultiNodeKey h = collapsedElement->getFaceKey(i);
	  CSkeletonFace *f = skel->getFace(h);
	  if(*f != *collapsedFace) {
	    if(f->nElements() == 1)
	      faceOnBoundary = f;
	    else
	      substitutes.insert(f);
	  }
	}
	if(faceOnBoundary != NULL) {
	  for(CSkeletonFaceSet::iterator s = substitutes.begin(); 
	      s!=substitutes.end(); ++s)
	    {
	      change->substituteFace(faceOnBoundary, *s);
	    }
	}
  	change->removeElement(collapsedElement);
      }

      for(CSkeletonElementIterator it=splitElements.begin();
	  it!=splitElements.end(); ++it) 
	{
	  splitTetrahedronInHalf(*it, seg, obtuseNode, change, skel,
				 &nullCallback,
				 "tetNoneSplit2");
	}
      
      //change->checkVolume();
      changes->push_back(change);
    } // end if node can move to midpoint[i]
  } // end loop over midpoints i
} // end tetNoneSplit


static void tetTetSplit(CSkeleton *skel,
			int obtuseNodeIdx, // node with large angle
			CSkeletonFace *oppFace, // face opposite that node
			CSkeletonElement *el, // element containing that node
			CSkeletonElement *sister, // other element on oppFace
			ProvisionalChangesVector *changes) 
{
  // oppNode is the node of the sister element that's not in the
  // original element, el.
  CSkeletonNode *oppNode = NULL;
  CSkeletonNode *obtuseNode=el->getNode(obtuseNodeIdx);
  const CSkeletonNodeVector *oppfacenodes = oppFace->getNodes();
  for(CSkeletonNodeIterator it0=sister->getNodes()->begin();
      it0!=sister->getNodes()->end(); ++it0)
    {
      bool in = false;
      for(CSkeletonNodeIterator it1=oppfacenodes->begin();
	  it1!=oppfacenodes->end() && !in; ++it1) 
	{
	  in |= (**it0 == **it1);
	}
      if(!in) {
	oppNode = *it0;
	break;
      }
  }
  assert(oppNode != NULL);

  Coord midpoints[3];
  Coord centroid;
  getCentroidAndMidpoints(oppFace, midpoints, centroid);

  // allparents is only used by the CSkeletonElement constructor,
  // which can tolerate duplicate entries in it.  Using a std::list
  // instead of a std::set is ok.  TODO OPT: Why is it a std::list
  // instead of a pre-allocated std::vector?
  CSkeletonSelectableList allparents;
  // Rationalization happens on a copy of the skeleton made by
  // CSkeleton::completeCopy, which has already set parent/child
  // pointers.  Therefore the cells created here replace el and
  // sister, and their parents are the parents of el and sister, not
  // el and sister themselves.
  allparents.insert(allparents.begin(),
		    el->getParents().begin(), el->getParents().end());
  allparents.insert(allparents.begin(),
		    sister->getParents().begin(), sister->getParents().end());

  // This function produces a bunch of different ProvisionalChanges.
  // The blocks of code for each type of change have extra brackets
  // around them so that they can be omitted easily when testing.
  {
    // First split the two into three without moving any nodes.
    ProvisionalChanges *change = new ProvisionalChanges(skel, "tetTetSplit1");
    change->removeElement(el);
    change->removeElement(sister);
    // Loop over the faces of el that include obtuseNode.  For each
    // face, create a new element that includes that face and oppNode.
    for(int i=0; i<3; ++i) {
      int faceId = CSkeletonElement::nodeFaces[obtuseNodeIdx][i];
      CSkeletonNodeVector *newNodes = new CSkeletonNodeVector;
      for(int j=0; j<3; ++j)
	newNodes->push_back(el->getFaceNode(faceId,j));
      std::reverse(newNodes->begin(), newNodes->end());
      newNodes->push_back(oppNode);
      change->insertElement(new CSkeletonElement(newNodes, allparents,
						 "tetTetSplit1"));
    }
    // change->checkVolume();
    changes->push_back(change);
  }

  // Now, move the node to each of the midpoints of the edges of
  // oppFace and split the neighbors that share the same segment.
  // Doing this will collapse the element that shares the face formed
  // by the split segment and obtuseNode, if there is such an element.
  for(int i=0; i<3; ++i) {
    CSkeletonSegment *seg = skel->getFaceSegment(oppFace, i);
    CSkeletonFace *otherFace = skel->findExistingFace(
		      seg->getNode(0), seg->getNode(1), obtuseNode);
    CSkeletonElement *collapsedElement = skel->getSister(el, otherFace);

    // Find the neighboring elements that will have to be split.
    CSkeletonElementVector segElements, splitElements;
    skel->getSegmentElements(seg, segElements);

    for(CSkeletonElementIterator it = segElements.begin();
	it!=segElements.end(); ++it) 
      {
	if(**it != *el && (collapsedElement==NULL || **it != *collapsedElement))
	    splitElements.push_back(*it);
	  // if(collapsedElement == NULL)
	  //   splitElements.push_back(*it);
	  // else if(**it != *collapsedElement)
	  //   splitElements.push_back(*it);
      }

    {
      if(obtuseNode->canMoveTo(midpoints[i])) {
	ProvisionalChanges *change = new ProvisionalChanges(skel,
							    "tetTetSplit2");
	bool mobility[3];
	getMobility(seg->getNodes(), obtuseNode, mobility);
	change->moveNode(obtuseNode, midpoints[i], mobility);
	change->removeElement(el);
	if(collapsedElement != NULL) 
	  change->removeElement(collapsedElement);
	bool ok = true;
	for(CSkeletonElementIterator it = splitElements.begin();
	    it!=splitElements.end() && ok; ++it) 
	  {
	    ok = splitTetrahedronInHalf(*it, seg, obtuseNode, change, skel,
					&nullCallback, "tetTetSplit2");
	  }
	// change->checkVolume();
	if(ok)
	  changes->push_back(change);
	else
	  delete change;
      } // end if obtuseNode->canMoveTo(midpoints[i])
    }

    /*  The following tetTetSplit method is commented out because it's
	badly behaved when it creates collapsed elements on
	boundaries.  In particular, in autorationalizebug9.log, when
	working only on one of the elements in the (0, 0, 1) corner,
	it would do strange things to the elements on the XminZmax
	edge.

    {
      // Or we can perform the same topological change without moving
      // the node.  Don't do it if seg is external, because that would
      // create a dent.

      if(!skel->onOuterFace(seg->getNodes())) {
	ProvisionalChanges *change = new ProvisionalChanges(skel, 
							    "tetTetSplit3");
	// change->annotate << "tetTetSplit: el= " << *el << std::endl;
	// change->annotate << "tetTetSplit: sister= " << *sister << std::endl;
	// change->annotate << "     obtuseNode= " << *obtuseNode << std::endl;
	// change->annotate << "            seg= " << *seg << std::endl;
	change->removeElement(el);
	if(collapsedElement != NULL) {
	  // change->annotate << "   collapsedElement=" << *collapsedElement 
	  // 		 << std::endl;
	  change->removeElement(collapsedElement);
	}
	// else {
	// 	change->annotate << "   No collapsed element" << std::endl;
	// }
	bool ok = true;
	for(CSkeletonElementIterator it=splitElements.begin();
	    it!=splitElements.end() && ok; ++it)
	  {
	    // oofcerr << "tetTetSplit: calling splitTetrahedronInHalf, obtuseNode="
	    // 	  << obtuseNode << std::endl;
	    ok = splitTetrahedronInHalf(*it, seg, obtuseNode, change, skel,
					&nullCallback, "tetTetSplit3");
	  }
	// change->checkVolume();
	if(ok)
	  changes->push_back(change);
	else
	  delete change;
      }
    }
    */

  } // end loop over midpoints i


  {
    // Also try collapsing obtuse node to the centroid
    if(obtuseNode->canMoveTo(centroid)) {
      ProvisionalChanges *change = new ProvisionalChanges(skel,
							  "tetTetSplit2a");
      bool mobility[3];
      getMobility(oppFace->getNodes(), obtuseNode, mobility);
      change->moveNode(obtuseNode, centroid, mobility);
      change->removeElement(el);
      change->removeElement(sister);
      for(int i=0; i<3; ++i) {
	int faceId = CSkeletonElement::nodeFaces[obtuseNodeIdx][i];
	CSkeletonNodeVector *newNodes = new CSkeletonNodeVector;
	for(int j=0; j<3; ++j)
	  newNodes->push_back(el->getFaceNode(faceId,j));
	std::reverse(newNodes->begin(), newNodes->end());
	newNodes->push_back(oppNode);
	change->insertElement(new CSkeletonElement(newNodes, allparents, 
						   "tetTetSplit2a"));
      }
      // change->checkVolume();
      changes->push_back(change);
    } // end if obtuseNode->canMoveTo(centroid)
  }
} // end tetTetSplit

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// RemoveFlatCallback is the callback function object for the
// removeFlat rationalizer.

class RemoveFlatCallback : public SplitTetCallback {
private:
  CSkeletonElement *flatEl;
  CSkeletonSegment *splitSegment;
public:
  RemoveFlatCallback(CSkeleton *skel, CSkeletonElement *flatEl,
		     CSkeletonSegment *splitSeg)
    : SplitTetCallback(skel),
      flatEl(flatEl),
      splitSegment(splitSeg)
  {}
  virtual bool callback(ProvisionalChanges *change, CSkeletonElement *newEl,
			CSkeletonNode *splitNode)
    const
  {
    // A new element has been created.  Does one of its faces
    // correspond to half of a face of the original, flattened
    // element?  If it does, we need to use substituteFace to
    // establish parentage.
    const CSkeletonNodeVector *nodes = newEl->getNodes();
    // Which of the nodes is splitNode?
    int sn = -1;
    for(int i=0; i<4 && sn==-1; i++) {
      if(*(*nodes)[i] == *splitNode)
	sn = i;
    }
    assert(sn != -1);
    // Look at each of the three new element faces that include
    // splitNode.  (The new element hasn't actually been installed in
    // the Skeleton, so the faces might not exist there, and we can't use
    // el->getFaceKey() and skel->getFace() to get the faces.)
    checkFace(splitNode, (*nodes)[(sn+1)%4], (*nodes)[(sn+2)%4], change);
    checkFace(splitNode, (*nodes)[(sn+2)%4], (*nodes)[(sn+3)%4], change);
    checkFace(splitNode, (*nodes)[(sn+3)%4], (*nodes)[(sn+1)%4], change);

    // Is one of the edges of the new element aligned with splitSeg?
    // If so, it also needs to be substituted.  If the edge exists, it
    // has to start at splitNode.  Comparing positions to see if
    // splitNode and one of the endpoints of splitSeg are on an edge
    // of the new element would be subject to round off errors.
    // Instead, check to see if the nodes of splitSeg and the far node
    // of the new segment are on the same edge boundary in the old
    // skeleton.
    CSkeletonNodeVector threenodes(3);
    threenodes[0] = splitSegment->getNode(0);
    threenodes[1] = splitSegment->getNode(1);
    for(int i=0; i<4; i++) {
      if(i != sn) {
	threenodes[2] = (*nodes)[i];
	if(skeleton->onOuterEdge(&threenodes)) {
	  // oofcerr << "RemoveFlatCallback::callback: substituting "
	  // 	  << *splitNode << ", " << *(*nodes)[i]
	  // 	  << " for " << *splitSegment
	  // 	  << " on edge " << skeleton->onOuterEdge(&threenodes)
	  // 	  << std::endl;
	  change->substituteSegment(splitSegment, splitNode, (*nodes)[i]);
	}
      }
    }
    return true;
  } // end callback()

private:
  void checkFace(CSkeletonNode *splitNode,
		 CSkeletonNode *node0, CSkeletonNode *node1, 
		 ProvisionalChanges *change)
    const
  {
    // Look for a face of flatEl that contains node0 and node1 and
    // whichever end of splitSegment isn't node0 or node1.  If such a
    // face exists, it corresponds to the new face built from node0,
    // node1, and splitNode.
    for(int i=0; i<4; i++) {
      CSkeletonMultiNodeKey h = flatEl->getFaceKey(i);
      CSkeletonFace *oldFace = skeleton->getFace(h);
      int n0 = oldFace->getNodeIndexIntoList(node0);
      int n1 = oldFace->getNodeIndexIntoList(node1);
      if(n0 != -1 && n1 != -1) {
	// node0 and node1 are nodes of this old face of flatEl.  See
	// if the third node of this old face is at the far end of
	// splitSegment.
	CSkeletonNode *thirdNode = oldFace->getNode(3 - n0 - n1);
	if(splitSegment->getNodeIndexIntoList(thirdNode) != -1) {
	  change->substituteFace(oldFace, node0, node1, splitNode);
	}
      }
    }
  } // end checkface
};  // end class RemoveFlatCallback


static void removeFlat(CSkeleton *skel, short segidx1, short segidx2, 
		       CSkeletonElement *el,
		       ProvisionalChangesVector *changes) 
{
  // oofcerr << "removeFlat: el= " << *el << std::endl;
  // A flat tet is one with large dihedral angles on two opposing
  // edges.  Those edges will nearly intersect.  Try to remove the
  // flat tet by collapsing it and replacing the two edges with four,
  // joined at a point near where the old edges nearly
  // intersected. All of the neighbor elements that share one of the
  // old edges will have to be bisected through the junction point.
  CSkeletonSegment *seg1 = skel->getElementSegment(el, segidx1);
  CSkeletonSegment *seg2 = skel->getElementSegment(el, segidx2);
  // oofcerr << "removeFlat: seg1= " << *seg1 << std::endl;
  // oofcerr << "removeFlat: seg2= " << *seg2 << std::endl;
  Coord mp1 = seg1->center();
  Coord mp2 = seg2->center();

  // splitpoints contains candidates for the new junction point. Only
  // one will be used in each ProvisionalChange.
  std::vector<Coord> splitpoints;
  // Different splitpoints need different callbacks for splitTetrahedronInHalf.
  std::vector<SplitTetCallback*> callbacks;
  // If an edge is on the exterior of the Skeleton, the junction point
  // must also be on the exterior, so it must be on the exterior edge.
  OuterFaceID ob1 = skel->onOuterFace(seg1->getNodes()); // kenobi
  OuterFaceID ob2 = skel->onOuterFace(seg2->getNodes()); 
  if(ob1 && ob2)
    return; // If both edges are exterior, the element can't be removed.
  else if(ob1) {
    splitpoints.push_back(mp1);
    callbacks.push_back(new RemoveFlatCallback(skel, el, seg1));
  }
  else if(ob2) {
    splitpoints.push_back(mp2);
    callbacks.push_back(new RemoveFlatCallback(skel, el, seg2));
  }
  else {
    splitpoints.push_back(mp1);
    callbacks.push_back(new RemoveFlatCallback(skel, el, seg1));
    splitpoints.push_back(mp2);
    callbacks.push_back(new RemoveFlatCallback(skel, el, seg2));
    splitpoints.push_back(0.5*(mp1+mp2));
    callbacks.push_back(new SplitTetCallback(0));
  }

  // splitelements1 and splitelements2 are the neighbor elements that
  // need to be split.  el is included in these lists too, but we'll
  // check for it later.
  CSkeletonElementVector splitelements1, splitelements2;
  skel->getSegmentElements(seg1, splitelements1);
  skel->getSegmentElements(seg2, splitelements2);

  // Loop over splitpoints
  for(unsigned int i=0; i<splitpoints.size(); i++) {
      // oofcerr << "removeFlat: splitpoint = " << splitpoints[i] << std::endl;
      CSkeletonNode *newNode = skel->addNode(splitpoints[i]);
      ProvisionalInsertion *change = new ProvisionalInsertion(skel,
							      "removeFlat");
      change->addNode(newNode);
      change->removeElement(el);
      bool ok = true;
      for(CSkeletonElementIterator it=splitelements1.begin(); 
	  it!=splitelements1.end() && ok; ++it) 
	{
	  if(**it != *el) {
	    ok = splitTetrahedronInHalf(*it, seg1, newNode, change, skel,
					callbacks[i], "removeFlat1");
	  }
	}
      for(CSkeletonElementIterator it=splitelements2.begin();
	  it!=splitelements2.end() && ok; ++it) 
	{
	  if(**it != *el) {
	    ok = splitTetrahedronInHalf(*it, seg2, newNode, change, skel,
					callbacks[i], "removeFlat2");
	  }
	}

      // change->checkVolume();
      if(ok)
	changes->push_back(change);
      else
	delete change;
    }
  for(int i=0; i<callbacks.size(); i++)
    delete callbacks[i];
} // end removeFlat


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// TODO 3.1: This should be a CSkeletonElement method.
static OuterFaceID elementHasFaceOnBoundary(CSkeleton *skel,
					    CSkeletonElement *el,
					    int &faceId, CSkeletonFace **face)
{
  for(faceId=0; faceId<4; ++faceId) {
    *face = skel->getFace(el->getFaceKey(faceId));
    OuterFaceID fn = skel->onOuterFace((*face)->getNodes());
    if(fn != OUTERFACE_NONE)
      return fn;
  }
  return OUTERFACE_NONE;
}


static void flattenFlatOnBoundary(CSkeleton *skel, CSkeletonElement *el,
				  ProvisionalChangesVector *changes) 
{
  CSkeletonFace *face = NULL;
  int faceId;
  // We don't handle the case where the element has more than one
  // face on a boundary.  This can't happen unless the "large"
  // dihedral angle isn't very large, so it's probably not necessary.
  OuterFaceID outerface = elementHasFaceOnBoundary(skel, el, faceId, &face);
  if(outerface) {
    CSkeletonNode *collapsedNode = 
      el->getNode(CSkeletonElement::oppNode[faceId]);

    // The nodes on the face on the boundary are collectively immobile
    // in one direction, which depends on which face they're all on.
    // The collapsedNode has to move in that direction to go onto the
    // face.
    bool mobility[3];
    int dir = getMobility(outerface, mobility);
    Coord x = collapsedNode->position();
    // The coordinates of all of the face nodes have the same
    // dir-component, so we can use any of the nodes here.
    x[dir] = face->getNode(0)->position()[dir];

    // Don't do anything unless the node can move to the new position,
    // and the new position is inside the face.  If it's outside,
    // other rationalizers will apply.  Skipping that situation here
    // eliminates a whole bunch of special cases that are a pain to
    // deal with.
    if(collapsedNode->canMoveTo(x) && face->contains(x)) {
      
      ProvisionalChanges *change = new ProvisionalChanges(
					  skel, "flattenFlatOnBoundary");

      // oofcerr << "flattenFlatOnBoundary: -----------" << std::endl;
      // oofcerr << "flattenFlatOnBoundary: el= " << *el << std::endl;
      // oofcerr << "flattenFlatOnBoundary: bdy = " << outerface << std::endl;
      // oofcerr << "flattenFlatOnBoundary: node=" << *collapsedNode << std::endl;
      // oofcerr << "flattenFlatOnBoundary: face=" << *face << std::endl;

      change->moveNode(collapsedNode, x, mobility);
      // oofcerr << "flattenFlatOnBoundary: moving node from "
      // 	    << collapsedNode->position() << " to " << x << std::endl;
    
      // Remove the elements that will be collapsed.  There may be more
      // than one, even though only one was passed in to this routine.

      CSkeletonFaceSet face_subs_A, face_subs_B;
      CSkeletonElementVector *nodeElements = collapsedNode->getElements();

      // Look for other elements that collapse when the node is moved.
      // It's necessary to actually move the node to do this.
      change->makeNodeMove();
      CSkeletonElementVector collapsedElements;
      for(CSkeletonElementVector::iterator it=nodeElements->begin();
	  it!=nodeElements->end(); ++it)
	{
	  if(skel->onOuterFace(outerface, (*it)->getNodes()))
	    collapsedElements.push_back(*it);
	}
      if(collapsedElements.empty()) { // This probably can't happen.
	delete change;
	return;
      }

      // We need to move the node back before looking at the collapsed
      // faces, in order to tell which faces are moving onto the
      // boundary and which were there already.
      change->moveNodeBack();

      for(CSkeletonElementIterator it=collapsedElements.begin();
	  it!=collapsedElements.end(); ++it) 
	{
	  // All nodes of element *it are exterior after collapsedNode
	  // is moved.
	  change->removeElement((*it));
	  // Any segment that has only one element must be on an edge
	  // of the microstructure. If its element is being removed,
	  // it must be because the collapsed node is being moved onto
	  // that edge. In that case, the interiority check has failed
	  // (probably due to round off error).  We don't actually
	  // want to do this rationalization.
	
	  for(unsigned int i=0; i<(*it)->getNumberOfSegments(); ++i) {
	    CSkeletonMultiNodeKey h = (*it)->getSegmentKey(i);
	    CSkeletonSegment *s = skel->getSegment(h);
	    if(s->nElements() == 1) {
	      delete change;
	      return;
	    }
	  }

	  // Any face that has only one element is on the face
	  // boundary of the microstructure and must become a parent
	  // to the new faces that will be on the boundary.
	  for(unsigned int i=0; i<(*it)->getNumberOfFaces(); ++i) {
	    CSkeletonMultiNodeKey h = (*it)->getFaceKey(i);
	    CSkeletonFace *f = skel->getFace(h);
	  
	    if(f->nElements() == 1 && skel->onOuterFace(outerface,
							f->getNodes())) 
	      face_subs_A.insert(f);
	    else
	      face_subs_B.insert(f);
	  }
	} // end loop over collapsed elements

      change->makeNodeMove();

      for(CSkeletonFaceSet::iterator a=face_subs_A.begin(); 
	  a!=face_subs_A.end(); ++a) 
	{
	  for(CSkeletonFaceSet::iterator b=face_subs_B.begin(); 
	      b!=face_subs_B.end(); ++b) 
	    {
	      // only do the substitution if a and b are on the same
	      // outer face *after* the node move.
	      if(skel->onSameOuterFace((*a)->getNodes(), (*b)->getNodes()))
		change->substituteFace(*a, *b);
	    }
	}
      change->moveNodeBack();
      changes->push_back(change);
    } // end if node can move to x and x is inside the face
  } // end if element has face on boundary
} // end flattenFlatOnBoundary


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

typedef std::pair<CSkeletonNode*, CSkeletonNode*> CSkeletonNodePair;

struct ltCSkeletonNodePair{
  bool operator()(CSkeletonNodePair p1, CSkeletonNodePair p2) const {
    // This is a rewrite of a legacy bit of code that had the sense of
    // the 'second' comparison backwards.  Since the definition of
    // "less than" is arbitrary, I've preserved the backwardness,
    // because it could in principle affect the behavior of the test
    // suite.
    if(p1.first->getUid() == p2.first->getUid())
      return p1.second->getUid() > p2.second->getUid(); // should be '<'
    return p1.first->getUid() < p2.first->getUid();
  }
};

typedef std::set<CSkeletonNodePair, ltCSkeletonNodePair> CSkeletonNodePairSet;

ProvisionalChangesVector* RemoveBadTetrahedra::fix(CSkeleton *skel,
						   CSkeletonElement *element)
  const
{
  // oofcerr << "RemoveBadTetrahedra::fix: element=" << *element << std::endl;
  ProvisionalChangesVector *changes = new ProvisionalChangesVector;

  // Separate operations are in their own {} blocks so that they can
  // be easily removed for debugging.

  // Merge nodes opposite an acute face angle.
  // First, put the sorted pairs of nodes in a set so that we only
  // consider each pair once. It helps to sort the pairs carefully for
  // debugging and reproducibility purposes.

  if(true)
  {
    CSkeletonNodePairSet node_pairs;
    for(unsigned int i=0; i<acute_angles.size(); ++i) {
      CSkeletonNode *node0 = element->getFaceNode(acute_angles[i].first,
						  (acute_angles[i].second+1)%3);
      CSkeletonNode *node1 = element->getFaceNode(acute_angles[i].first,
						  (acute_angles[i].second+2)%3);
      if(node0->getUid() < node1->getUid())
	node_pairs.insert( CSkeletonNodePair(node0, node1) );
      else
	node_pairs.insert( CSkeletonNodePair(node1, node0) );
    }
    for(CSkeletonNodePairSet::iterator it=node_pairs.begin(); 
	it != node_pairs.end(); ++it) 
      {
	CSkeletonNode *node0 = (*it).first;
	CSkeletonNode *node1 = (*it).second;
	ProvisionalMerge *merge = skel->mergeNode(node0, node1);
	if(merge)
	  changes->push_back(merge);
	merge = skel->mergeNode(node1, node0);
	if(merge)
	  changes->push_back(merge);
      }
  }

  // Handle tets with a large solid angle - either flatten or do a 2
  // to 3 split with the neighbor on the opposing face, if any.
  if(true)			
  {
    // TODO OPT: Should we include the obtuse angles in this list?
    std::set<short> angles(large_solid_angles.begin(),
			   large_solid_angles.end());
    for(unsigned int i=0; i<obtuse_angles.size(); ++i)
      angles.insert(vtkTetra::GetFaceArray(
			   obtuse_angles[i].first)[obtuse_angles[i].second]);
    for(std::set<short>::iterator it = angles.begin(); it != angles.end(); ++it)
      {
	int nodeId = *it;
	int oppFaceId = CSkeletonElement::oppFace[nodeId];
	CSkeletonFace *oppFace = skel->getFace(element->getFaceKey(oppFaceId));
	CSkeletonElement *other_el = skel->getSister(element, oppFace);
	if(other_el != NULL) {
	  tetTetSplit(skel, nodeId, oppFace, element, other_el, changes);
	}
	else {
	  tetNoneSplit(skel, element->getNode(nodeId), oppFace, element,
	   	       changes);
	}
      }
  }

  // Flatten tets with two large dihedral angles on opposite segments
  // and split elements that share those segments.
  if(true)
  {
    if(large_dihedral_angles.size() == 2) {
      if(CSkeletonElement::oppEdge[large_dihedral_angles[0]] == 
	 large_dihedral_angles[1]) 
	{
	  removeFlat(skel, large_dihedral_angles[0], large_dihedral_angles[1],
		     element, changes);
	}
    }
  }

  // Finally, look for flat tets that have a face on the boundary.
  if(true) 
  {
    if(!large_dihedral_angles.empty()) {
      flattenFlatOnBoundary(skel, element, changes);
    }
  }
  // oofcerr << "RemoveBadTetrahedra::fix: done" << std::endl;
  return changes;
}


// autorationalizebug9 fails when using only tetTetSplit with only the
// tetTetSplit3 part preserved.
