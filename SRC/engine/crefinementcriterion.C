// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/printvec.h"
#include "common/progress.h"
#include "common/tostring.h"
#include "engine/crefinementcriterion.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonsegment.h"
#include "engine/ooferror.h"
#include "common/IO/oofcerr.h"

#include <algorithm>


std::ostream& operator<<(std::ostream &o, const RefinementSignature &s) {
  o << "[";
  for(unsigned int i=0; i<s.size(); ++i) { 
    o << "(" << s[i].first << "," << s[i].second << ")";
    if(i!=s.size()-1) o << " ";
  }
  o << "]";
  return o;
}

// Some oddity about exception specifications causes compilation
// errors on clang++ --std=c++11 when this constructor is defined
// in-line in crefinementcriterion.h.
RefinementTargets::RefinementTargets() {}

void RefinementTargets::mark_(CSkeletonMultiNodeKey &h, short d) {
  if(unmarkable.count(h) == 0) {
    // TODO: do we need to search here?  Can't we just insert into the
    // map and let the map figure it out?
    SegmentMarks::iterator it = segmentMarks.find(h);
    if(it == segmentMarks.end())
      segmentMarks.insert(SegmentMarkDatum(h,d));
  }
  //TODO 3.1: take care of partners too
}

void RefinementTargets::mark(CSkeletonNode *n1, CSkeletonNode *n2, short d) {
  // Mark the segment from n1 to n2 for refinement d times.
  CSkeletonMultiNodeKey h(n1, n2);
  mark_(h, d);
}

void RefinementTargets::markSegment(CSkeletonSegment *segment, short d) {
  CSkeletonMultiNodeKey h(segment);
  mark_(h, d);
}

void RefinementTargets::markElement(CSkeletonElement *element, short d) {
  for(unsigned int i=0; i<element->getNumberOfSegments(); ++i) {
    mark(element->getSegmentNode(i,0), element->getSegmentNode(i,1), d);
  }
}

#define UNMARKABLE_TOLERANCE SUSPECT_COS_TOLERANCE*SUSPECT_COS_TOLERANCE
void RefinementTargets::findUnmarkableSegments(CSkeletonBase *skeleton) {
  // If refining a segment would create a suspect element, put the
  // segment in the "unmarkable" set, so that it won't be refined.
  // Since we don't know the possible results of the refinement here,
  // this procedure is inexact.
  for(CSkeletonElementIterator elit=skeleton->beginElements();
      elit!=skeleton->endElements(); ++elit)
    {
      CSkeletonElement *el = *elit;
      // Loop over edges of the element by looping over pairs of nodes
      for(unsigned int n0=0; n0<NUM_TET_NODES-1; n0++) {
	for(unsigned int n1=n0+1; n1<NUM_TET_NODES; n1++) {
	  double len2, diam2;
	  el->edgeLengthAndDiameter2(n0, n1, len2, diam2);
	  
	  // If the edge length is small compared to the diameter
	  // (distance from the midpoint of the edge to the midpoint
	  // of the opposite edge) mark the edge as unrefinable.
	  // Ditto if the diameter is small compared to the edge
	  // length. Use the same tolerance that's used in
	  // CSkeletonElement::suspect().
	  if(len2 < UNMARKABLE_TOLERANCE*diam2 ||
	     diam2 < UNMARKABLE_TOLERANCE*len2)
	    {
	      CSkeletonNode *node0 = el->getNode(n0);
	      CSkeletonNode *node1 = el->getNode(n1);
	      unmarkable.insert(CSkeletonMultiNodeKey(node0, node1));
#ifdef DEBUG
	      oofcerr << "RefinementTargets:findUnmarkableSegments: "
		      << " n0=" << n0 << " n1=" << n1
		      << " " << *el << std::endl;
#endif // DEBUG
	    }
	} // end loop over nodes n1
      }	// end loop over nodes n0
    } // end loop over elements
}

void RefinementTargets::signature(const CSkeletonElement *element, 
				  RefinementSignature *sig)
  const
{
  sig->clear();
  for(unsigned int i = 0; i<element->getNumberOfSegments(); ++i) {
    CSkeletonMultiNodeKey h(element->getSegmentNode(i,0),
			    element->getSegmentNode(i,1));
    SegmentMarks::const_iterator it = segmentMarks.find(h);
    if(it!=segmentMarks.end())
      sig->push_back(RefinementSignaturePair(i, (*it).second));
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool MinimumVolume::isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable)
  const
{
   if(units == "Voxel")
     return ((dynamic_cast<CSkeletonElement*> (selectable))->volumeInVoxelUnits(skeleton->getMicrostructure()) > threshold);
   else if(units == "Physical")
     return ((dynamic_cast<CSkeletonElement*> (selectable))->volume() > threshold);
   else if(units == "Fractional")
     return ((dynamic_cast<CSkeletonElement*> (selectable))->volumeInFractionalUnits(skeleton->getMicrostructure()) > threshold);
   else return false;
}

bool MinimumArea::isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable)
  const
{  
   if(units == "Voxel")
     return ((dynamic_cast<CSkeletonFace*> (selectable))->areaInVoxelUnits(skeleton->getMicrostructure()) > threshold);
   else if(units == "Physical")
     return ((dynamic_cast<CSkeletonFace*> (selectable))->area() > threshold);
   else if(units == "Fractional")
     return ((dynamic_cast<CSkeletonFace*> (selectable))->areaInFractionalUnits(skeleton->getMicrostructure()) > threshold);
   else return false;
}

bool MinimumLength::isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable)
  const
{  
   if(units == "Voxel")
     return ((dynamic_cast<CSkeletonSegment*> (selectable))->lengthInVoxelUnits(skeleton->getMicrostructure()) > threshold);
   else if(units == "Physical")
     return ((dynamic_cast<CSkeletonSegment*> (selectable))->length() > threshold);
   else if(units == "Fractional")
     return ((dynamic_cast<CSkeletonSegment*> (selectable))->lengthInFractionalUnits(skeleton->getMicrostructure()) > threshold);
   else return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CheckAllElements::createSegmentMarks(CSkeletonBase *skeleton,
					  RefinementCriterion *criterion,
					  short d) 
{
  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("Marking all elements",
						DEFINITE));

  int i=0, n = skeleton->nelements();
  for(CSkeletonElementIterator it = skeleton->beginElements();
      it != skeleton->endElements(); ++it)
    {
      if(criterion->isGood(skeleton,*it) && (*it)->active(skeleton))
	markElement(*it, d);
      ++i;
      progress->setFraction(float(i)/n);
      progress->setMessage("Marking all elements: " + to_string(i) + "/"
			   + to_string(n));
    }
  progress->finish();
};

void CheckSelectedElements::createSegmentMarks(CSkeletonBase *skeleton,
					       RefinementCriterion *criterion,
					       short d)
{
  for(CSkeletonElementIterator it = skeleton->beginElements();
      it != skeleton->endElements(); ++it)
    {
      if(criterion->isGood(skeleton,*it) && (*it)->active(skeleton) &&
	 (*it)->isSelected()) 
	{
	  markElement(*it, d);
	}
    }
}

void CheckElementsInGroup::createSegmentMarks(CSkeletonBase *skeleton, 
					      RefinementCriterion *criterion,
					      short d) 
{
  // TODO 3.1: It may be more efficient to access the groups set,
  // but it's tricky to access that
  for(CSkeletonElementIterator it = skeleton->beginElements();
      it != skeleton->endElements(); ++it)
    {
      if(criterion->isGood(skeleton,*it) && (*it)->active(skeleton) && 
	 (*it)->is_in_group(group))
	{
	  markElement(*it, d);
	}
    }
}

void CheckSingleElement::createSegmentMarks(CSkeletonBase *skeleton,
					    RefinementCriterion *criterion,
					    short d)
{
  CSkeletonElement *el = skeleton->getElement(index);
  markElement(el, d);
}

void CheckHomogeneity::createSegmentMarks(CSkeletonBase *skeleton,
					  RefinementCriterion *criterion,
					  short d) 
{
    for(CSkeletonElementIterator it = skeleton->beginElements();
	it != skeleton->endElements(); ++it) 
      {
	if(criterion->isGood(skeleton,*it) && (*it)->active(skeleton) && 
	   (*it)->homogeneity(skeleton) < threshold)
	  {
	    markElement(*it, d);
	  }
      }
}

CSkeletonSegmentVector *FromAllSegments::getSegments(CSkeletonBase *skeleton) {
  for(CSkeletonSegmentIterator it = skeleton->beginSegments(); 
      it != skeleton->endSegments(); ++it) 
    {
      if((*it).second->active(skeleton))
	segs->push_back((*it).second);
    }
  return segs;
}
  
CSkeletonSegmentVector *FromSelectedSegments::getSegments(
						  CSkeletonBase *skeleton) 
{
  for(CSkeletonSegmentIterator it = skeleton->beginSegments(); 
      it != skeleton->endSegments(); ++it) 
    {
      if((*it).second->active(skeleton) && (*it).second->isSelected())
	segs->push_back((*it).second);
    }
  return segs;
}
  
CSkeletonSegmentVector *FromSelectedElements::getSegments(
						  CSkeletonBase *skeleton) 
{
  for(CSkeletonElementIterator it = skeleton->beginElements();
      it != skeleton->endElements(); ++it)
    {
      if((*it)->isSelected()) {
	for(unsigned int i=0; i<(*it)->getNumberOfSegments(); ++i) {
	  CSkeletonSegment *s = skeleton->findExistingSegment(
					      (*it)->getSegmentNode(i,0),
					      (*it)->getSegmentNode(i,1));
	  if(s!=NULL) {
	    if(s->active(skeleton))
	      segs->push_back(s);
	  }
	}
      }
    }
  return segs;
}

void CheckHeterogeneousEdges::createSegmentMarks(CSkeletonBase *skeleton,
						 RefinementCriterion *criterion,
						 short d)
{
  CSkeletonSegmentVector *segs = chooser->getSegments(skeleton);
  for(CSkeletonSegmentVector::iterator it=segs->begin(); it!=segs->end(); ++it) 
    {
      if(criterion->isGood(skeleton,(*it)) &&
	 (*it)->homogeneity(skeleton) < threshold)
	{
	  markSegment((*it),d);
	}
    }
}

void CheckSelectedEdges::createSegmentMarks(CSkeletonBase *skeleton,
					    RefinementCriterion *criterion,
					    short d) 
{
  for(CSkeletonSegmentIterator it = skeleton->beginSegments(); 
      it != skeleton->endSegments(); ++it) 
    {
      if(criterion->isGood(skeleton,(*it).second) && (*it).second->active(skeleton) && (*it).second->isSelected())
	markSegment((*it).second,d);
    }
}

void CheckSegmentsInGroup::createSegmentMarks(CSkeletonBase *skeleton,
					      RefinementCriterion *criterion, 
					      short d)
{
  // TODO 3.1: It may be more efficient to access the groups set,
  // but it's tricky to access that
  for(CSkeletonSegmentIterator it = skeleton->beginSegments(); 
      it != skeleton->endSegments(); ++it) 
    {
      if(criterion->isGood(skeleton,(*it).second) && (*it).second->active(skeleton) && (*it).second->is_in_group(group))
	markSegment((*it).second,d);
    }
}

void CheckLongSegments::createSegmentMarks(CSkeletonBase *skeleton,
					   RefinementCriterion *criterion,
					   short d)
{
  for(CSkeletonElementIterator it = skeleton->beginElements();
      it!=skeleton->endElements(); ++it)
    {
      if(criterion->isGood(skeleton, *it) && (*it)->active(skeleton)) {
	CSkeletonElement *el = *it;
	std::vector<double> lengths(el->getNumberOfSegments());
	double shortest = std::numeric_limits<double>::max();
	for(unsigned int i=0; i<el->getNumberOfSegments(); i++) {
	  Coord3D disp = (el->getSegmentNode(i, 0)->position() -
			  el->getSegmentNode(i, 1)->position());
	  lengths[i] = sqrt(norm2(disp));
	  if(lengths[i] < shortest)
	    shortest = lengths[i];
	}
	for(unsigned int i=0; i<el->getNumberOfSegments(); i++) {
	  if(lengths[i] > factor*shortest)
	    mark(el->getSegmentNode(i,0), el->getSegmentNode(i,1), d);
	}
      }
    }
}

void CheckSelectedFaces::createSegmentMarks(CSkeletonBase *skeleton,
					    RefinementCriterion *criterion,
					    short d)
{
  for(CSkeletonFaceIterator it=skeleton->beginFaces();
      it!=skeleton->endFaces(); ++it)
    {
      const CSkeletonFace *face = (*it).second;
      if(criterion->isGood(skeleton,(*it).second) && face->active(skeleton) && face->isSelected()) {
	for(unsigned int i=0; i<face->nnodes(); i++) {
	  CSkeletonSegment *seg = skeleton->getFaceSegment(face, i);
	  markSegment(seg, d);
	}
      }
    }
}

void CheckFacesInGroup::createSegmentMarks(CSkeletonBase *skeleton,
					   RefinementCriterion *criterion,
					   short d)
{
  for(CSkeletonFaceIterator it=skeleton->beginFaces(); 
      it!=skeleton->endFaces(); ++it)
    {
      const CSkeletonFace *face = (*it).second;
      if(criterion->isGood(skeleton,(*it).second) && face->active(skeleton) && face->is_in_group(group)) {
	for(unsigned int i=0; i<face->nnodes(); i++) {
	  CSkeletonSegment *seg = skeleton->getFaceSegment(face, i);
	  markSegment(seg, d);
	}
      }
    }
}
