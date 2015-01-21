// -*- C++ -*-
// $RCSfile: dofmap.h,v $
// $Revision: 1.9.2.4 $
// $Author: langer $
// $Date: 2013/11/08 20:43:41 $

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

#ifndef DOFMAP_H
#define DOFMAP_H

// DoFMap keeps track of mapping between different sets of DoF
// indices.  It can be used for NodalEqns as well.

#include <map>
#include <vector>

class DoubleVec;

class DoFMap {
private:
  std::vector<int> map_;
  int range_;
public:
  DoFMap();
  virtual ~DoFMap();
  void reset(unsigned int len);		// len is the domain
  void identity(unsigned int len);	// make it the identity map
  int add(unsigned int n);

  // Sometime maps need to be manipulated manually.  Use these
  // functions carefully.
  void reassign(int src, int dest);
  void coerce_range(int); 

  int operator[](unsigned int n) const;

  int at(unsigned int n) const;

  DoFMap inverse() const;	// map must be 1 to 1!

  // clean() compresses the target range of a map so that it becomes a
  // set of consecutive integers beginning with zero.  It returns a
  // vector that do_clean can use to apply the same transformation to
  // another DoFMap.
  std::vector<int> *clean();	

  // do_clean() blindly applies the subtractors computed by clean()
  void do_clean(const std::vector<int> *subtractor);

  unsigned int range() const { return range_; }
  unsigned int domain() const { return map_.size(); }

  // extract() and inject() use the map to copy values from one vector
  // to another.  extract() uses the map to select values in the
  // source, and returns them in a new'd vector.  inject() copies
  // values from the source and puts them into the destination in the
  // locations from which extract() would have copied them.
  DoubleVec *extract(const DoubleVec&) const;
  void inject(const DoubleVec &src, DoubleVec &dest) const;
  void inject(const DoubleVec &src, unsigned int oset, DoubleVec &dest) const;
  void extract(const DoubleVec&, DoubleVec&, unsigned int) const;

  typedef std::map<unsigned int, unsigned int> TranslationMap;
  DoFMap translateDomain(unsigned int, const TranslationMap&) const;

  double maphash() const;	// for debugging

  friend std::ostream &operator<<(std::ostream&, const DoFMap&);
  friend DoFMap compose(const DoFMap&, const DoFMap&);
  friend DoFMap concat(const DoFMap&, const DoFMap&);
};

DoFMap compose(const DoFMap&, const DoFMap&);
DoFMap concat(const DoFMap&, const DoFMap&);

#endif // DOFMAP_H
