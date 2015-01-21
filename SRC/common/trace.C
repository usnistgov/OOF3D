// -*- C++ -*-
// $RCSfile: trace.C,v $
// $Revision: 1.8.10.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/trace.h"
#include "common/threadstate.h"

#include <iostream>

// This is just a debugging tool for tracking entering and exiting C++
// scopes.  It's not thread safe.

// The static data has to live outside the #ifdef DEBUG, because to
// keep swig and python happy, the Trace_t class is defined even if
// it's not used.  The Trace_t class is never instantiated if DEBUG is
// not defined.

int Trace_t::depth = 0;
bool Trace_t::enabled = true;

#ifdef DEBUG

// Called by the macro Trace(str).

Trace_t::Trace_t(const std::string &str) {
  if(enabled) {
    std::cerr << "==" << findThreadNumber() << " ";
    for(int i=0; i<depth; i++)
      std::cerr << "==";
    std::cerr << " " << str << " {" << std::endl;
    std::cerr.flush();
  }
  ++depth;
}

void Trace_t::msg(const std::string &message) const {
  if(enabled) {
    std::cerr << "==" << findThreadNumber() << " ";
    for(int i=0; i<depth; i++)
      std::cerr << "==";
    std::cerr << " " << message << std::endl;
    std::cerr.flush();
  }
}

Trace_t::~Trace_t() {
  --depth;
  if(enabled) {
    std::cerr << "==" << findThreadNumber() << " ";
    for(int i=0; i<depth; i++)
      std::cerr << "==";
    std::cerr << " }" << std::endl;
    std::cerr.flush();
  }
}

#endif














