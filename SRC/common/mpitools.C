// -*- C++ -*-
// $RCSfile: mpitools.C,v $
// $Revision: 1.26.18.1 $
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
#include <string>
#include <Python.h>
#include <iostream>
#include "mpitools.h"
#include "ooferror.h"
#include "tostring.h"
#include "trace.h"


// core functions

void _Initialize(std::vector<char*> *argh)
{
  int argc = argh->size();
  char **argv;
  if (argc == 1)
    {
      argc = 1;
      argv = (char **)malloc(argc * sizeof(char *));
      argv[0] = "           ";
    }
  else
    {
      argv = (char **)malloc(argc * sizeof(char *));
    
      for(std::vector<char*>::size_type i=0; i<argh->size(); i++)
	{
	  argv[i] = (*argh)[i];
	}
    }
  MPI::Init(argc, argv); //initializes MPI
}

bool Initialized()
{
  return MPI::Is_initialized();
}

void Finalize()
{
  MPI::Finalize();
}

void Abort()
{
  int errorcode = 0;
  OOF_COMM().Abort(errorcode);
}

int Size()
{
  return OOF_COMM().Get_size();
}

int Rank()
{
  return OOF_COMM().Get_rank();
}

std::string Get_processor_name()
{
  char *processor_name = new char[MPI_MAX_PROCESSOR_NAME];
  int  namelen;
  MPI::Get_processor_name(processor_name, namelen);
  return processor_name;
}

void Barrier()
{
  OOF_COMM().Barrier();
}


// p2p communications
void _Send_Int(int message, int destination, int tag)
{
  OOF_COMM().Send(&message, 1, MPI::INT, destination, tag);
}

int _Recv_Int(int origin, int tag)
{
  int value;
  if (origin == -1)
    origin = MPI::ANY_SOURCE;
  OOF_COMM().Recv(&value, 1, MPI::INT, origin, tag);
  return value;
}

int _Sendrecv_Int(int message, int destination, int tag)
{
  int value;
  if (destination == -1)
    destination = MPI::ANY_SOURCE;
  OOF_COMM().Sendrecv(&message, 1, MPI::INT, destination, tag,
		      &value, 1, MPI::INT, destination, tag);
  return value;
}

void _Send_Double(double message, int destination, int tag)
{
  OOF_COMM().Send(&message, 1, MPI::DOUBLE, destination, tag);
}

double _Recv_Double(int origin, int tag)
{
  double value;
  if (origin == -1)
    origin = MPI::ANY_SOURCE;
  OOF_COMM().Recv(&value, 1, MPI::DOUBLE, origin, tag);
  return value;
}

void _Send_String(std::string message, int destination, int tag) {
  OOF_COMM().Send(message.c_str(),
		  message.size(), MPI::CHAR, destination, tag);
}

std::string _Recv_String(int origin, int size, int tag) {
  char *temp = new char[size];
  if (origin == -1)
    origin = MPI::ANY_SOURCE;
  OOF_COMM().Recv(temp, size, MPI::CHAR, origin, tag);
  std::string message = temp;
  delete temp;
  // MPI String issue: some times, it gets more than it was supposed to.
  if (message.size() > (unsigned int)size)
    message.erase(size);
  return message;
}

void _Send_IntVec(std::vector<int> *message, int destination, int tag)
{
  OOF_COMM().Send(&(*message)[0], message->size(),
		  MPI::INT, destination, tag);
}

std::vector<unsigned short> *_Recv_UnsignedShortVec(int origin, int size, int tag)
{
  std::vector<unsigned short> *values = new std::vector<unsigned short>(size);
  if (origin == -1)
    origin = MPI::ANY_SOURCE;
  OOF_COMM().Recv(&(*values)[0], size, MPI::UNSIGNED_SHORT, origin, tag);
  return values;  // caller is responsible for the deletion of "values".
}

std::vector<int> *_Recv_IntVec(int origin, int size, int tag)
{
  std::vector<int> *values = new std::vector<int>(size);
  if (origin == -1)
    origin = MPI::ANY_SOURCE;
  OOF_COMM().Recv(&(*values)[0], size, MPI::INT, origin, tag);
  return values;  // caller is responsible for the deletion of "values".
}

void _Send_DoubleVec(std::vector<double> *message,
		     int destination, int tag)
{
  OOF_COMM().Send(&(*message)[0], message->size(),
		  MPI::DOUBLE, destination, tag);
}

std::vector<double> *_Recv_DoubleVec(int origin, int size, int tag)
{
  std::vector<double> *values = new std::vector<double>(size);
  if (origin == -1)
    origin = MPI::ANY_SOURCE;
  OOF_COMM().Recv(&(*values)[0], size, MPI::DOUBLE, origin, tag);
  return values;  // caller is responsible for the deletion of "values".
}

void _Isend_Int(int message,
		std::vector<int> *destinations,
		int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&message, 1, MPI::INT,
				   (*destinations)[i], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
}

void _Isend_Double(double message,
		   std::vector<int> *destinations,
		   int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&message, 1, MPI::DOUBLE,
				   (*destinations)[i], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
}

void _Isend_Ints(std::vector<int> *message,
		 std::vector<int> *destinations,
		 int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&(*message)[i], 1, MPI::INT,
				   (*destinations)[i], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
}

std::vector<int> *_Irecv_Ints(std::vector<int> *origins, int tag)
{
  int ntraffic = origins->size();
  std::vector<int> *values = new std::vector<int>(ntraffic);
  MPI::Request requests[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    if ((*origins)[i] == -1)
      (*origins)[i] = MPI::ANY_SOURCE;
    requests[i] = OOF_COMM().Irecv(&(*values)[i], 1, MPI::INT,
				   (*origins)[i], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
  return values;  // the caller is responsible for ... you know.
}

void _Isend_String(std::string message,
		   std::vector<int> *destinations, int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&message.c_str()[0], message.size(),
				   MPI::CHAR, (*destinations)[i], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
}

void _Isend_Strings(std::string message, std::vector<int> *sizes,
		    std::vector<int> *destinations, int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  int offset = 0;
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&message.c_str()[offset],
				   (*sizes)[i], MPI::CHAR,
				   (*destinations)[i], tag);
    offset += (*sizes)[i];
  }
  MPI::Request::Waitall(ntraffic, requests);
}

void _Isend_UnsignedShortVec(std::vector<unsigned short> *message,
			     std::vector<int> *destinations,
			     int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&(*message)[0],
				   message->size(), MPI::UNSIGNED_SHORT,
				   (*destinations)[i], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
}

void _Isend_IntVecs(std::vector<int> *message,
		    std::vector<int> *sizes,
		    std::vector<int> *destinations,
		    int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  int offset = 0;
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&(*message)[offset],
				   (*sizes)[i], MPI::INT,
				   (*destinations)[i], tag);
    offset += (*sizes)[i];
  }
  MPI::Request::Waitall(ntraffic, requests);
}

void _Isend_DoubleVec(std::vector<double> *message,
		      std::vector<int> *destinations,
		      int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&(*message)[0],
				   message->size(), MPI::DOUBLE,
				   (*destinations)[i], tag);
  }
  MPI::Request::Waitall(ntraffic, requests);
}

void _Isend_DoubleVecs(std::vector<double> *message,
		       std::vector<int> *sizes,
		       std::vector<int> *destinations,
		       int tag)
{
  int ntraffic = destinations->size();
  MPI::Request requests[ntraffic];
  int offset = 0;
  for(int i=0; i<ntraffic; i++) {
    requests[i] = OOF_COMM().Isend(&(*message)[offset],
				   (*sizes)[i], MPI::DOUBLE,
				   (*destinations)[i], tag);
    offset += (*sizes)[i];
  }
  MPI::Request::Waitall(ntraffic, requests);
}

std::vector<double> *_Irecv_DoubleVecs(std::vector<int> *origins,
				       std::vector<int> *sizes, int tag)
{
  int ntraffic = origins->size();
  int total = 0;
  for(int i=0; i<ntraffic; i++)
    total += (*sizes)[i];
  std::vector<double> *values = new std::vector<double>(total);
  MPI::Request requests[ntraffic];
  int offset = 0;
  for(int j=0; j<ntraffic; j++) {
    if ((*origins)[j] == -1)
      (*origins)[j] = MPI::ANY_SOURCE;
    requests[j] = OOF_COMM().Irecv(&(*values)[offset],
				   (*sizes)[j], MPI::DOUBLE,
				   (*origins)[j], tag);
    offset += (*sizes)[j];
  }
  MPI::Request::Waitall(ntraffic, requests);
  return values;  // caller's responsible for the deletion of "values".
}

bool _Iprobe(int origin, int tag)
{
  if (origin == -1)
    return OOF_COMM().Iprobe(MPI::ANY_SOURCE, tag);
  else
    return OOF_COMM().Iprobe(origin, tag);
}

// Cellective communications
int _Allreduce_IntSum(int value)
{
  int result;
  OOF_COMM().Allreduce(&value, &result, 1, MPI::INT, MPI::SUM);
  return result;
}

double _Allreduce_DoubleSum(double value)
{
  double result;
  OOF_COMM().Allreduce(&value, &result, 1, MPI::DOUBLE, MPI::SUM);
  return result;
}

std::vector<int> *_Allgather_Int(int value)
{
  int _size = Size();
  std::vector<int> *values = new std::vector<int>(_size);
  OOF_COMM().Allgather(&value, 1, MPI::INT, &(*values)[0], 1, MPI::INT);
  return values;  // the caller is responsible for the deletion
}

std::vector<int> *_Allgather_IntVec(std::vector<int> *values, int size)
{
  int _size = Size();
  std::vector<int> *valuesVec = new std::vector<int>(size*_size);
  OOF_COMM().Allgather(&(*values)[0], size, MPI::INT,
		       &(*valuesVec)[0], size, MPI::INT);
  return valuesVec;  // the caller is responsible for the deletion
}

std::vector<double> *_Allgather_DoubleVec(std::vector<double> *values, int size)
{
  int _size = Size();
  std::vector<double> *valuesVec = new std::vector<double>(size*_size);
  OOF_COMM().Allgather(&(*values)[0], size, MPI::DOUBLE,
		    &(*valuesVec)[0], size, MPI::DOUBLE);
  return valuesVec;  // the caller is responsible for the deletion
}

void bcast_int(int message, int origin)
{
  int *msg = &message;
  OOF_COMM().Bcast(msg, 1, MPI::INT, origin);
}

int recv_bcast_int(int origin) {
  int msg = 0;
  OOF_COMM().Bcast(&msg, 1, MPI::INT, origin);
  return msg;
}

void bcast_double (double &message, int origin)
{
  return OOF_COMM().Bcast(&message, 1, MPI::DOUBLE, origin);
}

double recv_bcast_double(int origin)
{
  double  msg = 0.;
  OOF_COMM().Bcast(&msg, 1, MPI::DOUBLE, origin);
  return msg;
}

void bcast_string(const std::string &message, int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int length = std::strlen(message.c_str())+1;
  int *msg_length = &length;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  OOF_COMM().Bcast((char *) message.c_str(), length, MPI::CHAR, origin);
}

std::string recv_bcast_string(int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int * msg_length = new int;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  int length = *(msg_length);
  length += 1;
  char *temp = new char [length];
  OOF_COMM().Bcast(temp, length, MPI::CHAR, origin);
  delete msg_length;
  return temp;
}

void bcast_shorts(std::vector<unsigned short> *message,
		  int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int length = message->size();
  int *msg_length = &length;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  if (length > 0)
    OOF_COMM().Bcast(&(*message)[0], length, MPI::UNSIGNED_SHORT, origin);
}


std::vector<unsigned short> *recv_bcast_shorts(int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int *msg_length = new int;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  int length = *(msg_length);
  std::vector<unsigned short> *temp = new std::vector<unsigned short>(length);
  if (length > 0)
    OOF_COMM().Bcast(&(*temp)[0], length, MPI::UNSIGNED_SHORT, origin);
  delete msg_length;
  return temp;
}


void bcast_ints(std::vector<int> *message, int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int length = message->size();
  int *msg_length = &length;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  if (length > 0)
    OOF_COMM().Bcast(&(*message)[0], length, MPI::INT, origin);
}


std::vector<int> *recv_bcast_ints(int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int *msg_length = new int;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  int length = *(msg_length);
  std::vector<int> *temp = new std::vector<int>(length);
  if (length>0)
    OOF_COMM().Bcast(&(*temp)[0], length, MPI::INT, origin);
  delete msg_length;
  return temp;
}


void bcast_doubles(std::vector<double> *message, int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int length = message->size();
  int * msg_length = &length;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  if (length > 0)
    OOF_COMM().Bcast(&(*message)[0], length, MPI::DOUBLE, origin);
}


std::vector<double> *recv_bcast_doubles(int origin)
{
  // Message is broadcast in two steps.
  // First broadcast size of message and then broadcast actual message.
  int *msg_length = new int;
  OOF_COMM().Bcast(msg_length, 1, MPI::INT, origin);
  int length = *(msg_length);
  std::vector<double> *temp = new std::vector<double>(length);
  if (length > 0)
    OOF_COMM().Bcast(&(*temp)[0], length, MPI_DOUBLE, origin);
  delete msg_length;
  return temp;
}

// MPI communicator class

MPICommunicator::MPICommunicator()
{
  MPI::Group mpi_group;
  MPI::Group oof_group;
  //get the size of the virtual machine
  int world_size = MPI::COMM_WORLD.Get_size();
  int * world_ranks = new int [world_size];
  for (int i = 0; i<world_size; i++)
    world_ranks[i] = i; //get a copy of all the ranks
  //get a copy of the world of processes
  mpi_group = MPI::COMM_WORLD.Get_group();
  //pass a list of all the active processors
  oof_group = mpi_group.Incl(world_size, world_ranks);
  //create a new communicator
  communicator = MPI::COMM_WORLD.Create(oof_group);
}

MPI::Intracomm &OOF_COMM()
{
  static MPICommunicator OOF_COMM_WORLD;
  return OOF_COMM_WORLD.get();
}

// MPI Exception class

MPIException::MPIException(const std::string &m, const std::string &f,
			   int l, int proc_num)
  : file(f),
    line(l),
    msg(m),
    process(proc_num)
{}

std::string MPIException::pythonequiv() const
{
  return  "process number: " + to_string(process) + "\n" + " MPIException('" 
    + msg + "', '" + file + "', " + to_string(line) + ")";
}
