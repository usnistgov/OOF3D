// -*- C++ -*-
// $RCSfile: printvec.h,v $
// $Revision: 1.10.10.10 $
// $Author: langer $
// $Date: 2014/09/25 02:15:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PRINTVEC_H
#define PRINTVEC_H

// std::vector<> and friends need output operators.  Using a template
// argument for the stream allows these to be used by both
// std::ostream and oofcerr.

#include <iomanip>
#include <iostream>
#include <list>
#include <map>
#include <set>
#include <vector>

// TODO 3.1: PRECISION should also apply to vectors and maps printed
// using derefprint and derefkeyprint.

#define PRECISION 20

template <class VEC, class OSTREAM>
void print(const VEC &vec, OSTREAM &os) {
  if(vec.empty()) return;
  os << vec[0];
  for(unsigned int i=1; i<vec.size(); i++) {
    os << " " << vec[i];
  }
}

template <class OSTREAM, class TYPE>
OSTREAM &operator<<(OSTREAM &os, const std::vector<TYPE> &vec) {
  if(!vec.empty()) {
    int prec = os.precision();
    os << std::setprecision(PRECISION);
    os << vec[0];
    for(unsigned int i=1; i<vec.size(); i++)
      os << " " << vec[i];
    os << std::setprecision(prec);
  }
  return os;
}

template <class OSTREAM, class TYPE>
OSTREAM &operator<<(OSTREAM &os, const std::set<TYPE> &vec) {
  if(!vec.empty()) {
    bool first = true;
    int prec = os.precision();
    os << std::setprecision(PRECISION);
    for(typename std::set<TYPE>::const_iterator i=vec.begin(); i!=vec.end();
	++i) 
      {
	if(!first) {
	  os << " ";
	}
	os << *i;
	first = false;
      }
    os << std::setprecision(prec);
  }
  return os;
}

template <class OSTREAM, class TYPE>
OSTREAM &operator<<(OSTREAM &os, const std::list<TYPE> &list) {
  int prec = os.precision();
  os << std::setprecision(PRECISION);
  for(typename std::list<TYPE>::const_iterator i=list.begin(); i!=list.end();
      ++i)
    {
      os << " " << *i;
    }
  os << std::setprecision(prec);
  return os;
}

#include "common/tostring.h"

template <class TYPE>
std::vector<std::string> derefprint(const TYPE &ptrvec) {
  std::vector<std::string> strings;
  for(typename TYPE::const_iterator i=ptrvec.begin(); i!=ptrvec.end(); ++i)
    strings.push_back(to_string(*(*i)));
  return strings;
}

template <class KEYTYPE, class VALTYPE, class CMP, class ALLOC>
std::vector<std::string> derefkeyprint(
			       const std::map<KEYTYPE, VALTYPE, CMP, ALLOC> &m)
{
  std::vector<std::string> strings;
  for(typename std::map<KEYTYPE, VALTYPE, CMP, ALLOC>::const_iterator i=m.begin();
      i!=m.end(); ++i)
    {
      strings.push_back(to_string(*(*i).first) + ":" + to_string((*i).second));
    }
  return strings;
}

#endif	// PRINTVEC_H
