// -*- C++ -*-
// $RCSfile: mpitools.swg,v $
// $Revision: 1.19.10.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MPITOOLS_SWG
#define MPITOOLS_SWG

%module mpitools

%include "common/typemaps.swg"

%{
#include "common/mpitools.h"
using std::string;
%}
%pragma(python) include="mpitools.spy"
%pragma(python) code="from ooflib.SWIG.common.ooferror import ErrErrorPtr"
%extern "common/ooferror.swg"

void _Initialize(CharPtrVec *argv);
int Initialized();
void Finalize();
void Abort();
int Size();
int Rank();
string Get_processor_name();
void Barrier();

// p2p communications
void _Send_Int(int, int, int);
int _Recv_Int(int, int);

int _Sendrecv_Int(int, int, int);

void _Send_Double(double, int, int);
double _Recv_Double(int, int);

void _Send_String(char*, int, int);
string _Recv_String(int, int, int);

void _Send_IntVec(IntVec*, int, int);
%new IntVec* _Recv_IntVec(int, int, int);

void _Send_DoubleVec(DoubleList*, int, int);
%new DoubleList* _Recv_DoubleVec(int, int, int);

void _Isend_Int(int, IntVec*, int);
void _Isend_Ints(IntVec*, IntVec*, int);
%new IntVec* _Irecv_Ints(IntVec*, int);

void _Isend_Double(double, IntVec*, int);

void _Isend_String(char*, IntVec*, int);
void _Isend_Strings(char*, IntVec*, IntVec*, int);

void _Isend_IntVecs(IntVec*, IntVec*, IntVec*, int);

void _Isend_DoubleVec(DoubleList*, IntVec*, int);
void _Isend_DoubleVecs(DoubleList*, IntVec*, IntVec*, int);
%new DoubleList* _Irecv_DoubleVecs(IntVec*, IntVec*, int);

bool _Iprobe(int, int);

// collective communications
int _Allreduce_IntSum(int);
double _Allreduce_DoubleSum(double);

%new IntVec* _Allgather_Int(int);
%new IntVec* _Allgather_IntVec(IntVec*, int);
%new DoubleList* _Allgather_DoubleVec(DoubleList*, int);

void bcast_ints(IntVec*, int);
%new IntVec* recv_bcast_ints(int);

void bcast_doubles(DoubleList*, int);
%new DoubleList* recv_bcast_doubles(int);

void bcast_string(char*, int);
string recv_bcast_string(int);

// Args are: Message, filename, line-number, processor
class MPIException : public ErrError {
public:
  string message();
  string filename();
  int lineno();
  MPIException(char *, char *, int, int);
  ~MPIException();
  %addmethods {
    string __repr__() {
      return self->message();
    }
  }
};

#endif // MPITOOLS_SWG

