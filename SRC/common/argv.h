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

#ifndef ARGV_H
#define ARGV_H
#include <vector>


void init_argv(std::vector<char*>*);
const char ** get_argv();
int get_argc();
// void stringtest(std::vector<char*>*);

#endif // ARGV_H
