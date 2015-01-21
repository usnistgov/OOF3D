// -*- C++ -*-
// $RCSfile: burn.h,v $
// $Revision: 1.5.18.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef BURN_H
#define BURN_H

#include "common/ccolor.h"
#include "common/coord.h"
#include "common/boolarray.h"
#include <vector>
#if DIM==2
class OOFImage;
#elif DIM==3
class OOFImage3D;
#endif

class Burner {
public:
  bool next_nearest;		// parameter
  Burner(bool nn) : next_nearest(nn) {};
  virtual ~Burner() {};

#if DIM==2
  void burn(const OOFImage&, const ICoord*, BoolArray&);
#elif DIM==3
  void burn(const OOFImage3D&, const ICoord*, BoolArray&);
#endif

  virtual bool spread(const CColor &from, const CColor &to) const = 0;
protected:
  CColor startcolor;
private:

#if DIM==2
  void burn_nbrs(const OOFImage&, std::vector<ICoord>&,
		 BoolArray&, int&, const ICoord&);

#elif DIM==3
  void burn_nbrs(const OOFImage3D&, std::vector<ICoord>&,
		 BoolArray&, int&, const ICoord&);
#endif

  // List of directions to neighbors. There is one static instance of
  // this class.
  class Nbr {
  private:
#if DIM==2
    ICoord nbr[8];
#elif DIM==3
    ICoord nbr[18];
#endif
    Nbr();			// loads the directions into the array.
    const ICoord &operator[](int x) const { return nbr[x]; }
    friend class Burner;
  };
  static Nbr neighbor;
};

class BasicBurner : public Burner {
public:
  double local_flammability;
  double global_flammability;
  bool useL2norm;
  BasicBurner(double lcl, double glbl, bool L2norm, bool nn)
    : Burner(nn),
      local_flammability(lcl),
      global_flammability(glbl),
      useL2norm(L2norm)
  {}
  virtual bool spread(const CColor &from, const CColor &to) const;
};

#endif // BURN_H
