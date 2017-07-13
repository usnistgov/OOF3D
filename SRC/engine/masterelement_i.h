// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MASTERELEMENT_I_H
#define MASTERELEMENT_I_H

#include <oofconfig.h>
#include <map>
#include <vector>

class MasterElement;
class MasterEdge;
class MasterFace;

// The instances of each MasterElement type are stored in a
// MasterElementDict, from which they can be retrieved by name.

typedef std::map<std::string, MasterElement*> MasterElementDict;

// TODO: Find a better place to define NodeIndexVec.
typedef std::vector<unsigned int> NodeIndexVec;


#endif // MASTERELEMENT_I_H
