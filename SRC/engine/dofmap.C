// -*- C++ -*-
// $RCSfile: dofmap.C,v $
// $Revision: 1.11.2.2 $
// $Author: fyc $
// $Date: 2014/07/24 21:35:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/doublevec.h"
#include "common/printvec.h"
#include "common/vectormath.h"
#include "engine/dofmap.h"
#include "engine/ooferror.h"

#include <fstream>
#include <iostream>

// TODO OPT: Add a SparseDoFMap class that uses a std::map instead of
// a std::vector and use it when the map isn't expected to contain
// much data.

DoFMap::DoFMap()
  : range_(0)
{}

DoFMap::~DoFMap() {}

void DoFMap::reset(unsigned int len) {
  // len is the domain of the map.
  map_.clear();
  map_.resize(len, -1);
  range_ = 0;
}

void DoFMap::identity(unsigned int len) {
  map_.resize(len, 0.0);
  for(unsigned int i=0; i<len; i++)
    map_[i] = i;
  range_ = len;
}

int DoFMap::add(unsigned int n) { 
  // If n<0, an auxiliary equation is being added.
#ifdef DEBUG
  if(n >= domain()) {
    std::cerr << "DoFMap::add: n=" << n << " domain=" << domain() << std::endl;
  }
#endif // DEBUG
  assert(n < domain());
  assert(map_[n] == -1);
  map_[n] = range_;
  return range_++;
}

int DoFMap::operator[](unsigned int n) const {
  assert(0 <= n && n < domain());
  return map_[n];
}

void DoFMap::reassign(int src, int dest) {
  if(src != -1)
    map_[src] = dest;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Extract the mapped values from the given source vector and return
// them in a new'd vector.

DoubleVec *DoFMap::extract(const DoubleVec &source) const {
  // TODO OPT: MAp If making a copy is too expensive memory-wise, this
  // function could return a proxy object that acts like a vector but
  // actually uses the map to refer to the data in source.  Routines
  // that rely on having a copy would have to change, or the proxy
  // object would have to implement copy-on-write.

  assert(domain() == source.size());

  DoubleVec *target = new DoubleVec(range(), 0.0);
  for(unsigned int i=0; i<map_.size(); i++) {
    if(map_[i] != -1) {
      assert(map_[i] >= 0 && (unsigned int) map_[i] < range());
      (*target)[map_[i]] += source[i];
    }
  }
  return target;
}

// Version that extracts into a given DoubleVec, with an offset.  This
// one can check for array overflows in debug mode.

void DoFMap::extract(const DoubleVec &source, DoubleVec &dest, 
		     unsigned int oset) 
  const
{
  assert(map_.size() <= source.size());
  // The map may be many-to-one, so we can't just set
  // dest[map[i]]=source[i].  We have to use += instead.  But we also
  // can't assume that dest is initialized, nor can we assume that the
  // entries of dest that we're not using don't contain data.  So
  // first we have to explicitly zero just the entries that we are
  // using.
  //* TODO OPT: This shouldn't be necessary if the destination vector has
  //* been properly initialized by the calling routine, but removing
  //* this extra step makes solver_test.py fail.  If this were fixed
  //* and we could use += here, then we could avoid making a copy
  //* (fullresidual) in routines like
  //* LinearizedSystem::static_residual_MCKa.  We'd just have to call
  //* extract twice.
  for(unsigned int i=0; i<map_.size(); ++i) {
    int j = map_[i];
    if(j != -1)
      dest[j+oset] = 0.0;
  }
  for(unsigned int i=0;i<map_.size(); ++i) {
    int j = map_[i];
    if(j != -1) {
      assert(j >= 0 && (unsigned int) j < range());
      assert( j+oset < dest.size() );
      assert( i < source.size() );
      dest[j+oset] += source[i];
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// inject() copies values from the source and puts them into the
// destination in the locations from which extract() would have copied
// them.

void DoFMap::inject(const DoubleVec &source, DoubleVec &destination) const {
#ifdef DEBUG
  if(range() != source.size()) {
    std::cerr << "DoFMap::inject: range=" << range() << " source.size="
	      << source.size() << std::endl;
    throw ErrProgrammingError("Bad sizes in DoFMap::inject",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  assert(domain() == destination.size());
  assert(range() == source.size());
  inject(source, 0, destination);
}

// New bounds-checked three-argument form of the "inject" function. 
void DoFMap::inject(const DoubleVec &source, unsigned int oset,
		    DoubleVec &dest) 
  const
{
  for(unsigned int i=0; i<map_.size(); ++i) {
    int j = map_[i];
    if (j != -1) {
      assert( i < dest.size());
      assert( j+oset < source.size());
      dest[i] = source[j+oset];
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const DoFMap &dofmap) {
  os << " [";
  bool first = true;
  for(unsigned int i=0; i<dofmap.map_.size(); i++) {
    if(dofmap.map_[i] != -1) {
      if(!first)
  	os << " ";
      first = false;
      os << "(" << i << "," << dofmap.map_[i] << ")";
    }
  }
  os << "] (range=" << dofmap.range() << ", domain=" << dofmap.domain() << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Compute the inverse map, assuming that the original is 1:1.

// The return value isn't a well-formed map unless domain()==range()
// for the original map.  Using DoFMap::add() on the 'inverse' map
// will garble it, because the targets in the 'inverse' aren't
// necessarily contiguous integers starting at 0.  TODO 3.1: MAYBE Have a
// derived class for an inverse map that disallows adding new members.

DoFMap DoFMap::inverse() const {
  DoFMap result;
  result.reset(range());
  for(unsigned int i=0; i<map_.size(); i++) {
   if(map_[i] != -1) {
      assert(result[map_[i]] == -1);
      result.map_[map_[i]] = i;
    }
  }
  result.range_ = domain();
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// clean() compresses the target range of a map so that it becomes a
// set of consecutive integers beginning with zero.  It returns a
// vector containing the amount subtracted from each entry in the
// original map.

std::vector<int> *DoFMap::clean() {
  std::vector<bool> istarget(map_.size(), false);

  // Find which targets actually appear in the map.
  for(std::vector<int>::size_type i=0;i<map_.size();i++)
    if(map_[i] != -1)
      istarget[map_[i]] = true;

  // subtractors[i] is the number of unused target integers lower than
  // i.  This is the amount that will have to be subtracted from
  // map_[i].
  std::vector<int> *subtractors = new std::vector<int>(map_.size(), 0);
  int zcount = 0;		// number of unused targets
  for(std::vector<int>::size_type i=0 ; i<map_.size(); i++) {
    if(istarget[i]) {
      (*subtractors)[i] = zcount;
    }
    else {
      zcount++;
    }
  }

  // Now do the subtraction.
  do_clean(subtractors);
  return subtractors;
}

void DoFMap::do_clean(const std::vector<int> *subtractors) {
  int maxmap = -1;
  for(std::vector<int>::size_type i=0; i<map_.size(); i++) {
    int &idx = map_[i];
    if(idx != -1) {
      idx -= (*subtractors)[idx];
      if(idx > maxmap)
	maxmap = idx;
    }
  }
  range_ = maxmap+1;
}

void DoFMap::coerce_range(int n) {
  range_ = n;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// compose(mapA, mapB) returns a map that gives the same result as
// applying mapB to the output of mapA.

DoFMap compose(const DoFMap &mapA, const DoFMap &mapB) {
  DoFMap result;
  int max = -1;
  result.reset(mapA.domain());
  for(unsigned int i=0; i<mapA.domain(); i++) {
    int b = mapA[i];		// output of map A
    if(b != -1) {
      int res = mapB[b];
      if(res > max)
	max = res;
      result.map_[i] = mapB[b];
    }
  }
  result.range_ = mapB.range();
  return result;
}

// Create a map that concatenates the result of mapB to the result of
// mapA.  Both must have the same domain.  For example, if mapA takes
// a subset Da of domain D to [0,n] and mapB takes another subset Db
// to [0,n], where Da and Db are disjoint, then the concatenated map
// will take Da to [0, n] and Db to [n+1, 2n].

DoFMap concat(const DoFMap &mapA, const DoFMap &mapB) {
  assert(mapA.domain() == mapB.domain());
  int sizeA = mapA.range();
  DoFMap result;
  result.reset(mapA.domain());
  for(unsigned int i=0; i<mapA.domain(); i++)
    if(mapA[i] != -1)
      result.map_[i] = mapA[i];
  for(unsigned int i=0; i<mapB.domain(); i++)
    if(mapB[i] != -1)
      result.map_[i] = mapB[i] + sizeA;
  result.range_ = mapA.range() + mapB.range();
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

DoFMap DoFMap::translateDomain(unsigned int n,
			       const DoFMap::TranslationMap &trans)
  const
{
  DoFMap newmap;
  newmap.reset(n);
  newmap.coerce_range(range());
  for(unsigned int i=0; i<map_.size(); i++) {
    if(map_[i] != -1) {
      DoFMap::TranslationMap::const_iterator j=trans.find(i);
      if(j != trans.end())
	newmap.map_[(*j).second] = map_[i];
      else {
	throw ErrProgrammingError("Map translation failure",
				  __FILE__, __LINE__);
      }
    }
  }
  return newmap;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double DoFMap::maphash() const {
  double sum = 0;
  for(unsigned int i=0; i<map_.size(); i++) {
    if(map_[i] > -1) {
      sum += (map_[i]+1.0)/(i+1.0);
    }
  }
  return sum;
}
