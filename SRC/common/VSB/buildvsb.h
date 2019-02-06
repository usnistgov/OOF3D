// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BUILDVSB_H
#define BUILDVSB_H

#include "vsb.h"

template <class IMAGE, class IMAGEVALUE, class ICOORD>
unsigned char voxelSignature(const IMAGE image, ICOORD &pos, IMAGEVALUE val,
			     ICOORD pt0, ICOORD pt1)
{
  // The voxelSignature indicates which of the eight voxels
  // surrounding a voxel corner in a given subregion of an image
  // have the given value.
  // The inputs are:
  //  image: The image containing the voxels.  
  //  pos: The position of the corner, in voxel units.
  //  val: The value of the voxels that we're interested in.
  //  pt0 and pt1: Two opposite corners of the subregion of the image.
  //  
  // pos is the lower-left-back corner of a voxel, so the components
  // of the coordinates of the other voxels at pos are one less.

  // A bit of the signature is 1 if the voxel corresponding to the bit
  // is in the category, cat.  The correspondence is
  // Bit          Position relative to pos
  // (0 is LSB)   
  // 0  0x1       (-1, -1, -1)
  // 1  0x2       (0, -1, -1)
  // 2  0x4       (-1, 0, -1)
  // 3  0x8       (0, 0, -1)
  // 4  0x10      (-1, -1, 0)
  // 5  0x20      (0, -1, 0)
  // 6  0x40      (-1, 0, 0)
  // 7  0x80      (0, 0, 0)
  ICRectPrism<ICOORD> region(pt0, pt1);
  unsigned char sig = 0;
  unsigned char b = 1;
  for(int k=0; k<2; k++) {
    for(int j=0; j<2; j++) {
      for(int i=0; i<2; i++) {
	ICoord3D offset = pos + ICoord3D(i-1, j-1, k-1);
	if(region.contains(offset) && categorymap[offset] == cat)
	  sig |= b;
	b <<= 1;
      }
    }
  }
  return sig;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class IMAGE, class IMAGEVAL, class COORD, class ICOORD>
VoxelSetBdy<COORD, ICOORD> *buildVSB(const IMAGE &image,
				     const IMAGEVAL &val,
				     std::vector<ICRectPrism<ICOORD>> &bins)
{
  VoxelSetBdy<COORD, ICOORD> *vsb = new VoxelSetBdy<COORD, ICOORD>(voxVol,
								   bins,
								   val);
}


#endif // BUILDVSB_H
