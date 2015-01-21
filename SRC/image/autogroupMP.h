// -*- C++ -*-
// $RCSfile: autogroupMP.h,v $
// $Revision: 1.1.8.3 $
// $Author: langer $
// $Date: 2012/03/13 15:01:16 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef AUTOGROUPMP_H
#define AUTOGROUPMP_H

class CMicrostructure;
class OOFImage3D;

#include <string>

std::string *autogroup(CMicrostructure*, OOFImage3D*, const std::string&);


#endif // autogroupmp_h
