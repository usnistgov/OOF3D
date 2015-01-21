// -*- C++ -*-
// $RCSfile: cfiddlenodesbaseParallel.C,v $
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
#include <iostream>
#include "engine/cfiddlenodesbaseParallel.h"


void tuneFiddle()
{
  CFNMoveData mydata;
  MPI::Datatype types[4] = {MPI::INT, MPI::INT,
			    MPI::DOUBLE, MPI::DOUBLE};
  int blens[4] = {1, 1, 1, 1};
  MPI::Aint disps[4];
  disps[0] = MPI::Get_address(&mydata.master);
  disps[1] = MPI::Get_address(&mydata.index);
  disps[2] = MPI::Get_address(&mydata.x);
  disps[3] = MPI::Get_address(&mydata.y);
  for(int i=3; i>=0; i--)
    disps[i] -= disps[0];
  FIDDLEDATA_ = FIDDLEDATA_.Create_struct(4, blens, disps, types);
  FIDDLEDATA_.Commit();
}

CFiddleNodesMoveData create_movedata(int m, int i,
				     double x, double y)
{
  return CFiddleNodesMoveData(m,i,x,y);
}

void _Send_MoveData(std::vector<CFiddleNodesMoveData*> *moves,
		    std::vector<int> *destinations, int tag)
{
  int ntraffic = destinations->size();
  CFNMoveData mydata[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    mydata[i].master = (*moves)[i]->master;
    mydata[i].index = (*moves)[i]->index;
    mydata[i].x = (*moves)[i]->x;
    mydata[i].y = (*moves)[i]->y;
  }
  for(int j=0; j<ntraffic; j++) {
    OOF_COMM().Send(mydata+j, 1, FIDDLEDATA_,
		    (*destinations)[j], tag);
  }
}

void _Isend_MoveData(std::vector<CFiddleNodesMoveData*> *moves,
		     std::vector<int> *destinations, int tag)
{
  int ntraffic = destinations->size();
  CFNMoveData mydata[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    mydata[i].master = (*moves)[i]->master;
    mydata[i].index = (*moves)[i]->index;
    mydata[i].x = (*moves)[i]->x;
    mydata[i].y = (*moves)[i]->y;
  }
  MPI::Request requests[ntraffic];
  for(int j=0; j<ntraffic; j++) {
    requests[j] = OOF_COMM().Isend(mydata+j, 1, FIDDLEDATA_,
				   (*destinations)[j], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
}

CFiddleNodesMoveData _Recv_MoveData(int origin, int tag)
{
  CFNMoveData mydata;
  if (origin == -1)
    origin = MPI::ANY_SOURCE;
  OOF_COMM().Recv(&mydata, 1, FIDDLEDATA_, origin, tag);
  return CFiddleNodesMoveData(mydata.master,
			      mydata.index,
			      mydata.x, mydata.y);
}
