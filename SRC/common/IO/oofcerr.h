// -*- C++ -*-
// $RCSfile: oofcerr.h,v $
// $Revision: 1.1.2.4 $
// $Author: langer $
// $Date: 2014/09/16 02:48:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef OOFCERR_H
#define OOFCERR_H

#include <oofconfig.h>
#include <iostream>

// Some of this is copied from http://stackoverflow.com/questions/1134388/stdendl-is-of-unknown-type-when-overloading-operator

// this is the type of std::cout
typedef std::basic_ostream<char, std::char_traits<char> > CoutType;

// this is the function signature of std::endl
typedef CoutType& (*StandardEndLine)(CoutType&);

// TODO 3.1: It would be convenient to derive the OOFcerr class from
// CoutType so that oofcerr could be passed as an argument to
// functions expecting a ostream, but for some reason the program
// segfaults on exit when that is done.  Why?

class OOFcerr { //: public CoutType {
private:
  bool newline;
  void printHeader() const;
public:
  OOFcerr() : newline(true) {}

  template <class TYPE> 
  OOFcerr &operator<<(const TYPE &x) { 
    if(newline) {
      printHeader();
      newline = false;
    }
    std::cerr <<  x;
    return *this;
  }

  OOFcerr &operator<<(StandardEndLine manip) {
    manip(std::cerr);
    newline = true;
    return *this;
  }

  // TODO 3.1: This needs to be done like std::setprecision or else
  // OOFcerr can't be used with the printvec.h templates.
  void precision(int p) { std::cerr.precision(p); }
};

extern OOFcerr oofcerr;

#endif // OOFCERR_H
