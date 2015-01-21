// -*- C++ -*-
// $RCSfile: despeckle.C,v $
// $Revision: 1.10.18.3 $
// $Author: langer $
// $Date: 2014/12/14 22:49:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Despeckle and Elkcepsed methods for the PixelSet class.

#include <oofconfig.h>
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/pixelgroup.h"
#include "common/boolarray.h"
#include "common/IO/oofcerr.h"

#include <set>

#if DIM==2
static ICoord north(0,1);
static ICoord east(1,0);
static ICoord northeast(1,1);
static ICoord northwest(-1, 1);
#endif // DIM==2

// Count number of selected neighbors.
static int Nnbrs(const ICoord &pxl, const BoolArray &sel) {
  int howmany = 0;	// number of neighbors selected
#if DIM==2
  int w = sel.width() - 1;
  int h = sel.height() - 1;
  int x = pxl(0);
  int y = pxl(1);
  if(x > 0) if(sel[pxl - east]) howmany++;
  if(x < w) if(sel[pxl + east]) howmany++;
  if(y > 0) if(sel[pxl - north]) howmany++;
  if(y < h) if(sel[pxl + north]) howmany++;
  if(x > 0 && y > 0) if(sel[pxl - northeast]) howmany++;
  if(x < w && y < h) if(sel[pxl + northeast]) howmany++;
  if(x < w && y > 0) if(sel[pxl - northwest]) howmany++;
  if(x > 0 && y < h) if(sel[pxl + northwest]) howmany++;
#else // DIM==3
  for(int k=-1; k<=1; k++) {
    for(int j=-1; j<=1; j++) {
      for(int i=-1; i<=1; i++) {
	if(i != 0 || j != 0 || k != 0) {
	  ICoord testpxl = pxl + ICoord(i, j, k);
	  if(sel.contains(testpxl) && sel[testpxl])
	    howmany++;
	}
      }
    }
  }
#endif // DIM==3
  return howmany;
}

// Is a pixel active and unselected? 
static inline bool actunsel(const CMicrostructure *ms, const ICoord &pxl,
			    const BoolArray &sel) 
{
  return !sel[pxl] && ms->isActive(pxl);
}

// Ditto, for selected pixels.
static inline bool actsel(const CMicrostructure *ms, const ICoord &pxl,
			  const BoolArray &sel) 
{
  return sel[pxl] && ms->isActive(pxl);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==2
static void addnbrs_unsel(const CMicrostructure *ms, const ICoord &pxl,
			  const BoolArray &sel, std::set<ICoord> &grp)
{
  int w = sel.width() - 1;
  int h = sel.height() - 1;
  int x = pxl(0);
  int y = pxl(1);
  if(x > 0)
    if(actunsel(ms, pxl-east, sel)) 
      grp.insert(pxl-east);
  if(x < w)
    if(actunsel(ms, pxl+east, sel))
      grp.insert(pxl+east);
  if(y > 0)
    if(actunsel(ms, pxl-north, sel))
      grp.insert(pxl-north);
  if(y < h) 
    if(actunsel(ms, pxl+north, sel)) 
      grp.insert(pxl+north);
  if(x > 0 && y > 0)
    if(actunsel(ms, pxl-northeast, sel))
      grp.insert(pxl-northeast);
  if(x < w && y < h)
    if(actunsel(ms, pxl+northeast, sel))
      grp.insert(pxl+northeast);
  if(x < w && y > 0)
    if(actunsel(ms, pxl-northwest, sel))
      grp.insert(pxl-northwest);
  if(x > 0 && y < h)
    if(actunsel(ms, pxl+northwest, sel))
      grp.insert(pxl+northwest);
}

static void addnbrs_sel(const CMicrostructure *ms, const ICoord &pxl,
			const BoolArray &sel, std::set<ICoord> &grp)
{
  int w = sel.width() - 1;
  int h = sel.height() - 1;
  int x = pxl(0);
  int y = pxl(1);
  if(x > 0)
    if(actsel(ms, pxl-east, sel))
      grp.insert(pxl-east);
  if(x < w) 
    if(actsel(ms, pxl+east, sel))
      grp.insert(pxl+east);
  if(y > 0) 
    if(actsel(ms, pxl-north, sel))
      grp.insert(pxl-north);
  if(y < h)
    if(actsel(ms, pxl+north, sel))
      grp.insert(pxl+north);
  if(x > 0 && y > 0)
    if(actsel(ms, pxl-northeast, sel))
      grp.insert(pxl-northeast);
  if(x < w && y < h)
    if(actsel(ms, pxl+northeast, sel))
      grp.insert(pxl+northeast);
  if(x < w && y > 0)
    if(actsel(ms, pxl-northwest, sel))
      grp.insert(pxl-northwest);
  if(x > 0 && y < h)
    if(actsel(ms, pxl+northwest, sel)) 
      grp.insert(pxl+northwest);
}

#else // DIM==3

static void addnbrs_unsel(const CMicrostructure *ms, const ICoord &pxl,
			  const BoolArray &sel, std::set<ICoord> &grp)
{
  // Add the unselected neighbors of pxl to grp.
  for(int k=-1; k<=1; k++) {
    for(int j=-1; j<=1; j++) {
      for(int i=-1; i<=1; i++) {
	ICoord testpxl = pxl + ICoord(i, j, k);
	if(sel.contains(testpxl) && actunsel(ms, testpxl, sel))
	  grp.insert(testpxl);
      }
    }
  }
}

static void addnbrs_sel(const CMicrostructure *ms, const ICoord &pxl,
			const BoolArray &sel, std::set<ICoord> &grp)
{
  // Add the selected neighbors of pxl to grp.
  for(int k=-1; k<=1; k++) {
    for(int j=-1; j<=1; j++) {
      for(int i=-1; i<=1; i++) {
	ICoord testpxl = pxl + ICoord(i, j, k);
	if(sel.contains(testpxl) && actsel(ms, testpxl, sel))
	  grp.insert(testpxl);
      }
    }
  }
}

#endif // DIM==3

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO 3.1: Add progress bars for despeckle and elkcepsed.  Is it
// possible to estimate how much time is remaining?  These operations
// are actually pretty fast, but they might need progress bars for
// very large (1000^3?) images.

void PixelSet::despeckle(int nbr_threshold, BoolArray &selected) const {
  // "selected" is an array of pixels that were selected by this
  // operation.  (TODO OPT: Might it be better to store it as a set of
  // coords?) "sel" is an array of the currently selected pixels,
  // including the ones that were selected before despeckling.
  BoolArray sel(geometry);
  for(std::vector<ICoord>::size_type i=0; i<members_.size(); i++)
    sel[members_[i]] = true;
  // The unselected neighbors are stored in a std::set. We used to use
  // a PixelSet here, but it was horribly slow because it was being
  // sorted each time its length was computed.
  std::set<ICoord> unselnbrs;

  // Find unselected neighbors by looping over sel
  for(BoolArray::iterator i=sel.begin(); i!=sel.end(); ++i)
    if(*i)			// pixel is selected
      addnbrs_unsel(microstructure, i.coord(), sel, unselnbrs);

  while(!unselnbrs.empty()) {
    // Remove last pixel from the unselected neighbor list.
    std::set<ICoord>::iterator first = unselnbrs.begin();
    ICoord candidate(*first);
    unselnbrs.erase(first);
    // If it has more than n selected neighbors...
    if(Nnbrs(candidate, sel) >= nbr_threshold) {
      // ... select it ...
      sel[candidate] = true;
      selected[candidate] = true;
      // ... and look at its nbrs
      addnbrs_unsel(microstructure, candidate, sel, unselnbrs);
    }
  }
}

void PixelSet::elkcepsed(int nbr_threshold, BoolArray &unselected) const {
  // array of selected pixels
  BoolArray sel(geometry);
  // Group of candidates for unselecting
  std::set<ICoord> candidates;
  for(std::vector<ICoord>::size_type i=0; i<members_.size(); i++) {
    sel[members_[i]] = true;
    candidates.insert(members_[i]);
  }

  // Examine pixels in group, 
  while(!candidates.empty()) {
    std::set<ICoord>::iterator first = candidates.begin();
    ICoord candidate(*first);
    candidates.erase(first);
    // A candidate may appear more than once in the list, so check to
    // see that it's still selected before doing anything.
    if(sel[candidate] && Nnbrs(candidate, sel) < nbr_threshold) {
      sel[candidate] = false;
      // add selected neighbors of this pixel to the list of pxls to
      // be examined
      addnbrs_sel(microstructure, candidate, sel, candidates);
      unselected[candidate] = true;
    }
  }
}
