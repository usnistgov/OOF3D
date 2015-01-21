// -*- C++ -*-
// $RCSfile: argv.C,v $
// $Revision: 1.5.18.2 $
// $Author: langer $
// $Date: 2012/12/05 20:31:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// Routines to cache the command line arguments so that they can be
// passed to PETSc (and MPI?) when it starts up.

#include <string>
#include <signal.h>
#include <iostream>
#include <vector>
#include "common/argv.h"

static int argc;
static const char **argv;

void init_argv(std::vector<char*> *argh) {
  argc = argh->size();
  if (argc == 1)
    {
      argc = 1;
      argv = (const char **)malloc(argc * sizeof(char *));
      argv[0] = "           ";
      return;
    }
  argv = (const char **)malloc(argc * sizeof(char *));
  for(std::vector<char*>::size_type i=0; i<argh->size(); i++)
    {
      //std::cerr << (*argh)[i] << std::endl;
      argv[i] = (*argh)[i];
    }
}

const char ** get_argv() {
  return argv;
}

int get_argc() {
  return argc;
}

// void stringtest(std::vector<char*> *argv) {
//   for(int i=0; i<argv->size(); i++)
//     std::cerr << (*argv)[i] << std::endl;
// }
