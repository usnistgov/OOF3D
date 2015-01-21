// -*- C++ -*-
// $RCSfile: fieldindex.swg,v $
// $Revision: 1.23.4.3 $
// $Author: fyc $
// $Date: 2014/07/24 21:36:18 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef FIELDINDEX_SWG
#define FIELDINDEX_SWG

%module fieldindex

%include "engine/typemaps.swg"
%extern "engine/planarity.swg"
%{
#include "engine/fieldindex.h"
#include "common/tostring.h"
#ifndef HAVE_SSTREAM
#include <strstream.h>
#else 
#include <sstream>	
#endif // HAVE_SSTREAM
%}

%pragma(python) include="engine/fieldindex.spy"

class FieldIndex {
public:
  ~FieldIndex();
  int integer();
  bool in_plane();
  void set(IntVec*);
  %new IntVec *components();
  const string &shortstring();
  %addmethods {
    %new const string *__repr__() {
      return new std::string(to_string(*self)); 
    }
  }
};

class ScalarFieldIndex : public FieldIndex {
public:
  ScalarFieldIndex();
  %addmethods{
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

class VectorFieldIndex : public FieldIndex {
public:
  VectorFieldIndex(int);
  %addmethods{
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

class OutOfPlaneVectorFieldIndex : public VectorFieldIndex {
public:
  OutOfPlaneVectorFieldIndex(int);
  %addmethods{
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};


class SymTensorIndex : public FieldIndex {
public:
  SymTensorIndex(int, int);
  int row();
  int col();
  bool diagonal();
  %addmethods{
    %new const string *__repr__() { 
      return new std::string(to_string(*self));
    }
  }
};

class OutOfPlaneSymTensorIndex : public SymTensorIndex {
public:
  OutOfPlaneSymTensorIndex(int, int);
  %addmethods{
    %new const string *__repr__() { 
      return new std::string(to_string(*self));
    }
  }
};


class FieldIterator : public FieldIndex {
public:
  %addmethods{
    void next() {
      ++(*self);
    }
  }
  bool end();
  FieldIterator *cloneIterator();
};

class ScalarFieldIterator: public ScalarFieldIndex, public FieldIterator {
public:
  ScalarFieldIterator();
};

class VectorFieldIterator: public VectorFieldIndex, public FieldIterator {
public:
  VectorFieldIterator();
};

class OutOfPlaneVectorFieldIterator
  : public OutOfPlaneVectorFieldIndex, public FieldIterator
{
public:
  OutOfPlaneVectorFieldIterator();
};

class SymTensorIterator: public SymTensorIndex, public FieldIterator {
public:
  SymTensorIterator();
  %addmethods {
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

class SymTensorInPlaneIterator: public SymTensorIterator {
public:
  SymTensorInPlaneIterator();
};

class SymTensorOutOfPlaneIterator: public SymTensorIterator {
public:
  SymTensorOutOfPlaneIterator();
};

class OutOfPlaneSymTensorIterator:
  public OutOfPlaneSymTensorIndex, public FieldIterator
{
  OutOfPlaneSymTensorIterator();
}


// IndexP and IteratorP objects should NOT be created directly in
// Python, because it leads to arguments over whose job it is to
// delete the enclosed FieldIndex or FieldIterator object.

class IndexP {
public:
//   IndexP(FieldIndex*);   // DON'T SWIG THE CONSTRUCTOR
  ~IndexP();
  int integer();
  bool in_plane();
  IndexP cloneIndex();
  void set(IntVec*);
  %new IntVec *components();
  const string &shortstring();
  %addmethods{
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

class IteratorP: public IndexP {
public:
//   IteratorP(FieldIterator*);   // DON'T SWIG THE CONSTRUCTOR
  ~IteratorP();
  bool end();
  IteratorP cloneIterator();
  %addmethods{
    void next() { ++(*self); }
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
    

    // TODO OPT: INDEXING The swigged IteratorP should be a real Python
    // iterator, with next() and __iter__() methods.  next() should
    // raise a StopIteration exception when done.  Fixing this at this
    // late date will be a pain.

    // TODO OPT: INDEXING Don't swig IteratorP and IndexP.  Make the
    // underlying FieldIndex and FieldIterator classes
    // PythonExportable, and swig those.  Operations like
    // SymmMatrix.__getitem__ would expect a FieldIndex of the correct
    // type, not an IndexP, and the index object's special methods,
    // like SymTensorIndex.diagonal, would be available.

//     IteratorP __iter__() {
//       return self->cloneIterator();
//     }
  }
};

%new IteratorP *getSymTensorIterator(Planarity);

#endif // FIELDINDEX_SWG
