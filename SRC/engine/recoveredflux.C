// -*- C++ -*-
// $RCSfile: recoveredflux.C,v $
// $Revision: 1.6.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/vectormath.h"
#include "engine/recoveredflux.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RecoveredFlux::RecoveredFlux(DoubleVec *fv)
  : fvalue(fv),
    nfv(1)
{}


// Include *fv in the running average.

void RecoveredFlux::average(DoubleVec *fv) {
  *fvalue *= double(nfv);
  *fvalue += *fv;
  nfv += 1;
  *fvalue *= 1.0/double(nfv);
}
