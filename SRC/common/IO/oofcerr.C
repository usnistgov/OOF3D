// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/IO/oofcerr.h"
#include "common/threadstate.h"

#include <iomanip>

void OOFcerr::printHeader() const {
  std::cerr << "--*"
	    << std::setw(2) << std::setfill('0')
	    << findThreadNumber() 
	    << "*-- ";
  for(unsigned int i=0; i<indent; i++)
    std::cerr << " ";
};

// The one instance.
OOFcerr oofcerr;

