// -*- C++ -*-
// $RCSfile: fieldeqnlist.h,v $
// $Revision: 1.9.6.2 $
// $Author: langer $
// $Date: 2013/12/16 18:56:02 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef FIELDEQNLIST_H
#define FIELDEQNLIST_H

// Machinery for keeping track of which Fields are defined, or which
// Equations are activated, at a FuncNode.  This is complicated
// because the set of relevant Fields and Equations can differ from
// SubProblem to SubProblem, but if each Node has its own lists, there
// will be a lot of redundant data, since many Nodes will have the
// same lists.  The lists can't be stored in SubProblems, either,
// because Nodes can belong to more than one SubProblem.

// The solution used here is for each Node to store a pointer to a
// reference counted data structure.  The per-node memory overhead is
// a simple pointer, since many nodes share the same data structure.

// The classes defined here are (mostly) templates, since the code is
// otherwise identical for Fields and Equations.  In the discussion
// below, "TYPE" refers to either Field or Equation.

// The data that is needed for each Node is a list of FieldEqnData
// objects, one for each global TYPE.  That is, list[i] is the
// FieldEqnData for the TYPE whose index() is i.  FieldEqnData
// contains three ints:
//   * FieldEqnData.listed is a count of how many SubProblems are
//     using the TYPE object.  If a TYPE is listed, then space for it
//     has been allocated in the Node. When FieldEqnData.listed goes
//     to zero, the space is deallocated.  (Deallocation doesn't happen
//     here, but FieldEqnList.remove returns true to indicate that the
//     Node should deallocate the space.)
//   * FieldEqnData.offset indicates where the data for this TYPE
//     starts in the Node's list of DegreeOfFreedoms or 
//     NodalEquations.  It will depend on the *order* in which TYPEs
//     were added.
//   * FieldEqnData.order indicates the order in which the TYPEs were
//     added to the Node.

// Actually, the data stored for each TYPE is not a FieldEqnData
// object, but a TYPE::FEData object, where FEData is a typedef for
// either FieldEqnData or for a subclass of it.  If a subclass is
// used, operator< should be provided for the subclass.  This allows
// different additional data to be stored for each TYPE.

// The list of FieldEqnData objects is stored in an FEvector.  We
// don't want to create an FEvector for each Node, so FEvectors are
// wrapped by FEWrapper, which contains an FEvector and keeps a count
// of how many Nodes are using it.  All of the FEWrappers for a TYPE
// are stored in a std::map that's stored in the FEMesh and keyed by
// the FEvector. For convenience, the exact type of the std::map is
// typedef'd as FEWrapper::AllWrappers.  When a Node adds a TYPE to
// its FEvector, it first makes a copy of the old FEvector, modifies
// it, and looks it up in the map to see if a wrapper already exists
// for the new FEvector.  If a wrapper doesn't exist, a new one is
// made and added to the map.  The FEWrapper also keeps track of how
// many Field or Equation components are stored at the Node, so that
// the offsets can be computed in the FieldEqnData objects.

// The std::map mentioned above has to be retrieved from the FEMesh
// somehow. TYPE is expected to contain a typedef called "GetWrappers"
// which refers to a class that has (a) a constructor that takes an
// FEMesh* argument and (b) an operator() which takes no arguments and
// returns the map.

// Finally, the Nodes contain a FieldEqnList object, which contains
// the pointer to the FEWrapper and does all of the pointer and
// reference counting management.

template <class TYPE> class FieldEqnList;
template <class TYPE> class FEWrapper;

#include <vector>
#include <map>
#include <iostream>
#include <assert.h>

#include "engine/ooferror.h"

class FEMesh;

class FieldEqnData {
public:
  FieldEqnData() : order(-1), offset(-1), listed(0) {}
  virtual ~FieldEqnData() {}
  // "order" indicates the order in which TYPE objects were added to a
  // Node, and therefore the order in which their data appears in the
  // Nodes lists.
  int order;
  // "offset" is the position in a list of degrees of freedom or nodal
  // equations at which a given Field or Equations components appear.
  // It's different from "order" because Fields and Equations have
  // varying numbers of components.
  int offset;
  // Is this object defined (for fields) or activated (for equations)?
  // Stored as an int instead of a bool so that we know how many
  // SubProblems are using it.  When "listed" goes back to zero, the
  // Field or Equation can be removed from the node.
  int listed;	
};

std::ostream &operator<<(std::ostream&, const FieldEqnData&);

// The comparison operator for FieldEqnData objects is used to
// discover if two lists of FieldEqnData objects are the same, so that
// they can be reused.  It uses FieldEqnData.order and
// FieldEqnData.listed, but *not* FieldEqnData.offset, since the
// offsets might not have been computed yet, and they depend only on
// the orders.
bool operator<(const FieldEqnData &a, const FieldEqnData &b);

// Comparison operator used by the std::map of lists.  The map keys
// are pointers to FEvectors. 
template <class TYPE>
struct FEvectorCompare {
  bool operator()(const typename FEWrapper<TYPE>::FEvector *a,
		  const typename FEWrapper<TYPE>::FEvector *b)
    const
  {
    return *a < *b;		// lexicographically compare list contents
  }
};

// FEWrapper is the reference counted wrapper for the
// std::vector which is the actual list.  You might think that
// FEWrapper should be derived from std::vector, but that makes
// it harder to discover if an existing FEWrapper should be
// reused.  Because the FEWrapper constructor puts the newly
// created object in allWrappers, it's hard to create an
// FEWrapper object and see if it's a duplicate of one already
// in allWrappers.  It's cleaner to create a std::vector and see if
// it's the key for an FEWrapper object that's in allWrappers.

template <class TYPE>
class FEWrapper {
public:
  // AllWrappers is a typedef for a std::map that stores pointers to
  // FEWrapper objects.  The map is keyed by pointers to the wrapped
  // FEvectors.  This makes it easy to find an existing FEWrapper with
  // a given underlying FEvector.
  typedef std::vector<typename TYPE::FEData> FEvector;
  typedef std::map<const typename FEWrapper<TYPE>::FEvector*, FEWrapper<TYPE>*,
		   FEvectorCompare<TYPE> > AllWrappers;

  FEWrapper(const typename FEWrapper<TYPE>::FEvector *, FEMesh*);
  ~FEWrapper();
  typename FEWrapper<TYPE>::FEvector datalist; // the actual list
  int refcount;			// how many FieldEqnList objects are using this
  int dimsum;			// sum of the dimensions of objects in datalist.
  int size;			// number of objects listed
  int id_;
  static int counter;
  typename TYPE::GetWrappers allwrappers; // callable obj that returns AllWrappers map
  bool contains(const TYPE *const) const;
  int offset(const TYPE *const) const;
  int listed(const TYPE *const) const;
  void update();		// compute size, dimsum, and FieldEqnData.offset
  int id() const { return id_; }
private:
  FEWrapper(const FEWrapper&); // prohibited
};

// The FEWrapper constructor makes a *copy* of the given list.  This
// is important, because the initial list might be a temporary object.
// The initial reference count is set to zero. An FieldEqnList object
// will increment the reference count immediately.

template <class TYPE>
FEWrapper<TYPE>::FEWrapper(const typename FEWrapper<TYPE>::FEvector *list,
			   FEMesh *mesh)
  : datalist(*list),		// copy!
    refcount(0),
    dimsum(0),
    size(0),
    id_(counter++),
    allwrappers(mesh)
{
  update();
  allwrappers()[&datalist] = this; // insert self in std::map
}

template <class TYPE>
FEWrapper<TYPE>::~FEWrapper() {
  allwrappers().erase(&datalist); // remove self from std::map
}

// Recompute offsets for each stored object.

template <class TYPE>
void FEWrapper<TYPE>::update() {
  size = 0;
  // ordereddata[i] is the index in datalist of the FieldEqnData
  // object that has order==i.  For i >= the number of listed objects,
  // ordereddata[i] is -1.
  std::vector<int> ordereddata(datalist.size(), -1); // initialize to -1
  std::vector<const TYPE*> orderedobjs(datalist.size(), 0);
  for(typename FEWrapper<TYPE>::FEvector::size_type i=0; i<datalist.size(); ++i)
    {
      if(datalist[i].listed > 0) {
	int which = datalist[i].order;
	ordereddata[which] = i;
	orderedobjs[which] = TYPE::all()[i];
	++size;
      }
    }
  // Now loop over the data in installation order, updating the
  // offsets and the total dimension sum.
  dimsum = 0;
  if(size > 0) {
    for(typename FEWrapper<TYPE>::FEvector::size_type i=0;
	i<datalist.size() && ordereddata[i]>=0; ++i)
      {
	int which = ordereddata[i];
	datalist[which].offset = dimsum;
	dimsum += TYPE::all()[which]->ndof();
      }
  }
}

template <class TYPE>
bool FEWrapper<TYPE>::contains(const TYPE * const obj) const {
  return obj->index() < datalist.size() && datalist[obj->index()].listed > 0;
}

template <class TYPE>
int FEWrapper<TYPE>::offset(const TYPE *const obj) const {
  if(!contains(obj))
    throw ErrNoSuchField(obj->name());
  return datalist[obj->index()].offset;
}

template <class TYPE>
int FEWrapper<TYPE>::listed(const TYPE *const obj) const {
  if(!contains(obj))
    //throw ErrNoSuchField(obj->name());
    return 0;
  return datalist[obj->index()].listed;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// FieldEqnList is the only part of this mechanism that should be used
// directly by other classes.  It is very lightweight, containing only
// a single pointer datum.

template <class TYPE>
class FieldEqnList {
public:
  FieldEqnList(FEMesh*);
  FieldEqnList(const FieldEqnList<TYPE>&);
  ~FieldEqnList();
  // add() returns true if TYPE is not already in list
  bool add(const TYPE *const, FEMesh*);
  // remove() returns true if TYPE is completely gone
  bool remove(const TYPE *const, FEMesh*);
  bool contains(const TYPE *const) const;
  int offset(const TYPE *const) const;
  int listed(const TYPE *const) const;
  int size() const { return data->size; } // no. of listed objects
  int dimsum() const { return data->dimsum; }// sum of dimensions of listed objs
  bool operator<(const FieldEqnList<TYPE> &other) const {
    return data->datalist < other.data->datalist;
  }
  // id() is used to find all other objects that use the same
  // FEWrapper. See meshIO.py.
  int id() const { return data->id(); }
private:
  FEWrapper<TYPE> *data;
  void switchData(FEWrapper<TYPE>*);
};

template <class TYPE>
FEWrapper<TYPE> *
getFEWrapper(const typename FEWrapper<TYPE>::FEvector *flist, FEMesh *mesh) {
  // Return an existing FEWrapper object wrapping the given list of
  // const TYPE* pointers.  Return a new object if there is no
  // existing one.  Makes a copy of flist, so the original can be deleted.
  typename FEWrapper<TYPE>::AllWrappers
    allwrappers = typename TYPE::GetWrappers(mesh)();
  typename FEWrapper<TYPE>::AllWrappers::iterator
    i = allwrappers.find(flist);
  if(i == allwrappers.end()) {	// not found
    return new FEWrapper<TYPE>(flist, mesh);
  }
  return (*i).second;		// found existing object
}

template <class TYPE>
FieldEqnList<TYPE>::FieldEqnList(FEMesh *mesh) {
  const typename FEWrapper<TYPE>::FEvector flist;
  data = getFEWrapper<TYPE>(&flist, mesh); // copies flist
  ++data->refcount;
}

template <class TYPE>
FieldEqnList<TYPE>::FieldEqnList(const FieldEqnList<TYPE> &other)
  : data(other.data)
{
  ++data->refcount;
}

// switchData swaps the existing FEWrapper for a new one, and updates
// the reference counts.
template <class TYPE>
void FieldEqnList<TYPE>::switchData(FEWrapper<TYPE> *newdata)
{
  if(newdata != data) {
    if(newdata)
      ++newdata->refcount;
    if(data && --data->refcount==0) {
      delete data;
    }
    data = newdata;
  }
}

template <class TYPE>
FieldEqnList<TYPE>::~FieldEqnList() {
  switchData(0);		// decrements refcount
}

template <class TYPE>
bool FieldEqnList<TYPE>::add(const TYPE *const newobj, FEMesh *mesh) {
  // Make a copy of the old list
  typename FEWrapper<TYPE>::FEvector newlist(data->datalist);
  // Update the copy
  unsigned int newindex = newobj->index();
  if(newlist.size() <= newindex)
    newlist.resize(newindex+1);
  typename TYPE::FEData &fdata = newlist[newindex];
  ++fdata.listed;
  // If this is the first time that that TYPE object was listed, then
  // it'll be stored at the end of the list in the Nodes, and its offset
  // is just the number of components already stored.
  if(fdata.listed == 1) {
    fdata.offset = data->dimsum;
    fdata.order = data->size;
  }
  switchData(getFEWrapper<TYPE>(&newlist, mesh));
  return fdata.listed == 1;
}

template <class TYPE>
bool FieldEqnList<TYPE>::remove(const TYPE *const oldobj, FEMesh *mesh) {
  // Make a copy of the old list
  typename FEWrapper<TYPE>::FEvector newlist(data->datalist);
  // Update the copy
  int oldindex = oldobj->index();
  typename FEWrapper<TYPE>::FEvector::iterator i = newlist.begin() + oldindex;
  int oldorder = (*i).order;
  assert((*i).listed > 0);
  bool allgone = --(*i).listed == 0; // are we removing the last reference?
  if(allgone) {
    (*i).order = -1;
    // Update ordering in newlist.  This must be done before
    // getFEWrapper looks for an existing wrapper, because the
    // FieldEqnData comparator uses the order.
    for(typename FEWrapper<TYPE>::FEvector::iterator j=newlist.begin();
	j<newlist.end(); ++j)
      {
	if((*j).order > oldorder)
	  --(*j).order;
      }
  }
  switchData(getFEWrapper<TYPE>(&newlist, mesh));
  return allgone;
}

template <class TYPE>
bool FieldEqnList<TYPE>::contains(const TYPE *const obj) const {
  return data->contains(obj);
}

//In practice, this returns the number of subproblems on which
//obj (Field or Equation) is defined.
template<class TYPE>
int FieldEqnList<TYPE>::listed(const TYPE *const obj) const {
  return data->listed(obj);
}

template<class TYPE>
int FieldEqnList<TYPE>::offset(const TYPE *const obj) const {
  return data->offset(obj);
}

#endif // FIELDEQNLIST_H
