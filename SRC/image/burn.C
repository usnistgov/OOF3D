// -*- C++ -*-
// $RCSfile: burn.C,v $
// $Revision: 1.6.18.7 $
// $Author: langer $
// $Date: 2014/11/05 16:54:59 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/activearea.h"
#include "common/boolarray.h"
#include "common/ccolor.h"
#include "common/cmicrostructure.h"
#include "common/IO/oofcerr.h"
#include "image/burn.h"
#if DIM==2
#include "image/oofimage.h"
#elif DIM==3
#include "image/oofimage3d.h"
#endif
#include <vector>

#if DIM==2

void Burner::burn(const OOFImage &image, const ICoord *spark, BoolArray &burned)
{
  // Initialize the data structures.
  int nburnt = 0;
  startcolor = image[spark];
  std::vector<ICoord> activesites; // sites whose neighbors have to be checked
  activesites.reserve(image.sizeInPixels()(0)*image.sizeInPixels()(1));

  // burn the first pixel
  burned[*spark] = true;
  nburnt++;
  activesites.push_back(*spark);

  while(!activesites.empty()) {
    // Remove the last site in the active list, burn its neighbors,
    // and add them to the list.
    int n = activesites.size() - 1;
    const ICoord here = activesites[n];
    activesites.pop_back();
    burn_nbrs(image, activesites, burned, nburnt, here);
  }
}

void Burner::burn_nbrs(const OOFImage &image,
		       std::vector<ICoord> &activesites,
		       BoolArray &burned, int &nburnt,
		       const ICoord &here) {
  // Burn neighboring pixels and put them in the active list.
  const ActiveArea *aa = image.getMicrostructure()->getActiveArea();
  int nbrmax = (next_nearest? 8 : 4);
  CColor thiscolor(image[here]);
  for(int i=0; i<nbrmax; i++) {
    ICoord target = here + neighbor[i];
    if(aa->isActive(&target) && burned.contains(target) && !burned[target]
       && spread(thiscolor, image[target])) {
      burned[target] = true;
      nburnt++;
      activesites.push_back(target);
    }
  }
};




#elif DIM==3

void Burner::burn(const OOFImage3D &image, const ICoord *spark,
		  BoolArray &burned)
{
  image.getVTKImageData()->Update();
  // Initialize the data structures.
  int nburnt = 0;
  startcolor = image[spark];
  std::vector<ICoord> activesites; // sites whose neighbors have to be checked
  const ICoord &isize = image.sizeInPixels();
  activesites.reserve(isize[0]*isize[1]*isize[2]);

  // burn the first pixel
  burned[*spark] = true;
  nburnt++;
  activesites.push_back(*spark);

  while(!activesites.empty()) {
    // Remove the last site in the active list, burn its neighbors,
    // and add them to the list.
    int n = activesites.size() - 1;
    const ICoord here = activesites[n];
    activesites.pop_back();
    burn_nbrs(image, activesites, burned, nburnt, here);
  }
}

void Burner::burn_nbrs(const OOFImage3D &image,
		       std::vector<ICoord> &activesites,
		       BoolArray &burned, int &nburnt,
		       const ICoord &here) {
  // Burn neighboring pixels and put them in the active list.
  const ActiveArea *aa = image.getMicrostructure()->getActiveArea();
  int nbrmax = (next_nearest? 18 : 6);
  CColor thiscolor(image[here]);
  for(int i=0; i<nbrmax; i++) {
    ICoord target = here + neighbor[i];
    if(aa->isActive(&target) && burned.contains(target) && !burned[target]
       && spread(thiscolor, image[target])) {
      burned[target] = true;
      nburnt++;
      activesites.push_back(target);
    }
  }
};

#endif

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Burner::Nbr Burner::neighbor;

#if DIM==2

Burner::Nbr::Nbr() {
  // don't change the order here without changing Burner::burn_nbrs(),
  // or the nearest neighbor/next nearest neighbor distinction will be
  // screwed up.
  nbr[0] = ICoord( 0, -1);
  nbr[1] = ICoord(-1,  0);
  nbr[2] = ICoord( 1,  0);
  nbr[3] = ICoord( 0,  1);
  nbr[4] = ICoord(-1, -1);
  nbr[5] = ICoord( 1, -1);
  nbr[6] = ICoord(-1,  1);
  nbr[7] = ICoord( 1,  1);
}

#elif DIM==3

Burner::Nbr::Nbr() {
  // don't change the order here without changing Burner::burn_nbrs(),
  // or the nearest neighbor/next nearest neighbor distinction will be
  // screwed up.
  nbr[0]  = ICoord( 0,  0, -1);
  nbr[1]  = ICoord( 0, -1,  0);
  nbr[2]  = ICoord(-1,  0,  0);
  nbr[3]  = ICoord( 1,  0,  0);
  nbr[4]  = ICoord( 0,  1,  0);
  nbr[5]  = ICoord( 0,  0,  1);

  nbr[6]  = ICoord(-1, -1,  0);
  nbr[7]  = ICoord( 1, -1,  0);
  nbr[8]  = ICoord(-1,  1,  0);
  nbr[9]  = ICoord( 1,  1,  0);
  nbr[10] = ICoord(-1,  0, -1);
  nbr[11] = ICoord( 1,  0, -1);
  nbr[12] = ICoord(-1,  0,  1);
  nbr[13] = ICoord( 1,  0,  1);
  nbr[14] = ICoord( 0, -1, -1);
  nbr[15] = ICoord( 0,  1, -1);
  nbr[16] = ICoord( 0, -1,  1);
  nbr[17] = ICoord( 0,  1,  1);
}

#endif

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool BasicBurner::spread(const CColor &from, const CColor &to) const {
  if(useL2norm) {
    double local_dist = L2dist2(from, to);
    double global_dist = L2dist2(startcolor, to);
    return local_dist < local_flammability*local_flammability &&
      global_dist < global_flammability*global_flammability;
  }
  else {
    double local_dist = L1dist(from, to);
    double global_dist = L1dist(startcolor, to);
    return local_dist < local_flammability && global_dist < global_flammability;
  }
}
