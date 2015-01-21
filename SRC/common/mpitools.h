// -*- C++ -*-
// $RCSfile: mpitools.h,v $
// $Revision: 1.18.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:52 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef MPITOOLS_H
#define MPITOOLS_H

#include <Python.h>
#include <vector>
#include "ooferror.h"
#include <string>
#include <mpi++.h>

// core routines
void _Initialize(std::vector<char*>*);
bool Initialized();
void Finalize();
void Abort();
int Size();
int Rank();
std::string Get_processor_name();
void Barrier();


// p2p communications
void _Send_Int(int, int, int);
int _Recv_Int(int, int);

int _Sendrecv_Int(int, int, int);

void _Send_Double(double, int, int);
double _Recv_Double(int, int);

void _Send_String(std::string, int, int);
std::string _Recv_String(int, int, int);

std::vector<unsigned short> *_Recv_UnsignedShortVec(int, int, int);

void _Send_IntVec(std::vector<int>*, int, int);
std::vector<int> *_Recv_IntVec(int, int, int);

void _Send_DoubleVec(std::vector<double> *, int, int);
std::vector<double> *_Recv_DoubleVec(int, int, int);

void _Isend_Int(int, std::vector<int>*, int);
void _Isend_Ints(std::vector<int>*, std::vector<int>*, int);
std::vector<int> *_Irecv_Ints(std::vector<int>*, int);

void _Isend_Double(double, std::vector<int>*, int);

void _Isend_String(std::string, std::vector<int>*, int);
void _Isend_Strings(std::string, std::vector<int>*,
		    std::vector<int>*, int);

void _Isend_UnsignedShortVec(std::vector<unsigned short>*,
			     std::vector<int>*,
			     int);

void _Isend_IntVecs(std::vector<int>*,
		    std::vector<int>*,
		    std::vector<int>*,
		    int);

void _Isend_DoubleVec(std::vector<double>*,
		      std::vector<int>*,
		      int);
void _Isend_DoubleVecs(std::vector<double>*,
		       std::vector<int>*,
		       std::vector<int>*,
		       int);
std::vector<double> *_Irecv_DoubleVecs(std::vector<int>*,
				       std::vector<int>*,
				       int);

bool _Iprobe(int, int);

// collective communications
int _Allreduce_IntSum(int);
double _Allreduce_DoubleSum(double);

std::vector<int> *_Allgather_Int(int);
std::vector<int> *_Allgather_IntVec(std::vector<int>*, int);
std::vector<double> *_Allgather_DoubleVec(std::vector<double>*, int);

void bcast_int(int, int);
int recv_bcast_int(int);

void bcast_double(double&, int);
double recv_bcast_double(int);

void bcast_shorts(std::vector<unsigned short>*, int);
std::vector<unsigned short> *recv_bcast_shorts(int);

void bcast_ints(std::vector<int> *, int);
std::vector<int> * recv_bcast_ints(int);

void bcast_doubles(std::vector<double>*, int);
std::vector<double> *recv_bcast_doubles(int);

void bcast_string(const std::string&, int);
std::string recv_bcast_string(int);

 
// communicator
class MPICommunicator {
private:
  MPI::Intracomm communicator;
public:
  MPICommunicator();
  ~MPICommunicator(){};
  MPI::Intracomm &get() { return communicator; }
};

MPI::Intracomm &OOF_COMM();

// class to throw/catch MPI Exceptions
class MPIException : public ErrError {
private:
  const std::string file;
  const int line;
  const std::string msg;
  const int process;
public:
  MPIException(const std::string &m, const std::string &f,
	       int l, int proc_num);
  virtual ~MPIException() {}
  virtual std::string message() const { return msg; };
  std::string filename() const { return file; } 
  int lineno() const { return line; }           
  virtual std::string pythonequiv() const;
  virtual void throw_self() const {}
};

#endif // MPITOOLS_H
