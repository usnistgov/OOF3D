// -*- C++ -*-
// $RCSfile: crefinementcriterion.C,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2014/12/14 01:07:45 $

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

void RefinementTargets::mark(CSkeletonNode *n1, CSkeletonNode *n2, short d) {
  // Mark the segment from n1 to n2 for refinement d times.
  CSkeletonMultiNodeKey h(n1,n2);
  SegmentMarks::iterator it = segmentMarks.find(h);
  if(it == segmentMarks.end())
    segmentMarks.insert(SegmentMarkDatum(h,d));
}

void RefinementTargets::markSegment(CSkeletonSegment *segment, short d) {
  const CSkeletonNodeVector *ns = segment->getNodes();
  mark((*ns)[0],(*ns)[1],d);
  //TODO 3.1: take care of partners too
}

void RefinementTargets::markElement(CSkeletonElement *element, short d) {
  for(unsigned int i=0; i<element->getNumberOfSegments(); ++i) {
    mark(element->getSegmentNode(i,0), element->getSegmentNode(i,1), d);
  }
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

void CheckHomogeneity::createSegmentMarks(CSkeletonBase *skeleton,
					  RefinementCriterion *criterion,
					  short d) 
{
    for(CSkeletonElementIterator it = skeleton->beginElements();
	it != skeleton->endElements(); ++it) 
      {
	if(criterion->isGood(skeleton,*it) && (*it)->active(skeleton) && 
	   (*it)->homogeneity(skeleton->getMicrostructure()) < threshold)
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
      if(criterion->isGood(skeleton,(*it)) && (*it)->homogeneity(skeleton->getMicrostructure()) < threshold) 
	markSegment((*it),d);
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
