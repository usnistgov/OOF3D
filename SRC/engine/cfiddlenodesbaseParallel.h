// -*- C++ -*-
// $RCSfile: cfiddlenodesbaseParallel.h,v $
// $Revision: 1.3.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:17 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CFIDDLENODESBASEPARALLEL_H
#define CFIDDLENODESBASEPARALLEL_H

#include "ooferror.h"
#include "common/mpitools.h"
#include <Python.h>
#include <vector>
#include <mpi++.h>

MPI::Datatype FIDDLEDATA_;  // Custom MPI datatype for fiddling

class CFiddleNodesMoveData;

class CFiddleNodesMoveData {
public:
  CFiddleNodesMoveData(int m, int i, double x, double y):
    master(m), index(i), x(x), y(y) {}
  CFiddleNodesMoveData():
    master(0), index(0), x(0.), y(0.) {}
  int master;
  int index;
  double x;
  double y;
};

struct CFNMoveData {
  int master;
  int index;
  double x;
  double y;
};


void tuneFiddle();
CFiddleNodesMoveData create_movedata(int, int, double, double);
void _Send_MoveData(std::vector<CFiddleNodesMoveData*>*,
		    std::vector<int>*, int);
void _Isend_MoveData(std::vector<CFiddleNodesMoveData*>*,
		     std::vector<int>*, int);
CFiddleNodesMoveData _Recv_MoveData(int, int);

#endif  // CFIDDLENODESBASEPARALLEL_H
