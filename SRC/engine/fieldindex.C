// -*- C++ -*-
// $RCSfile: fieldindex.C,v $
// $Revision: 1.12.4.3 $
// $Author: langer $
// $Date: 2013/11/08 20:44:23 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include "fieldindex.h"
#include "outputval.h"
#include "common/tostring.h"

bool operator==(const FieldIndex &a, const FieldIndex &b) {
  return a.integer() == b.integer();
}

std::vector<int> *ScalarFieldIndex::components() const {
  return new std::vector<int>;	// empty vector
}

const std::string &ScalarFieldIndex::shortstring() const {
  static std::string ss("");
  return ss;
}

void VectorFieldIndex::set(const std::vector<int> *component) {
  index_ = (*component)[0];
}

void VectorFieldIndex::set(int given_index) {
  index_ = given_index;
}

std::vector<int> *VectorFieldIndex::components() const {
  std::vector<int> *c = new std::vector<int>(1);
  (*c)[0] = index_;
  return c;
}

const std::string &VectorFieldIndex::shortstring() const {
  static const std::string names[] = {std::string("x"),
				      std::string("y"), 
				      std::string("z")};
  return names[index_];
}

static const int rowset[] = { 0, 1, 2, 1, 0, 0 };
static const int colset[] = { 0, 1, 2, 2, 2, 1 };

int SymTensorIndex::row() const {
  return rowset[v];
}

int SymTensorIndex::col() const {
  return colset[v];
}

void SymTensorIndex::set(const std::vector<int> *component) {
  v = ij2voigt((*component)[0], (*component)[1]);
}

std::vector<int> *SymTensorIndex::components() const {
  std::vector<int> *c = new std::vector<int>(2);
  (*c)[0] = rowset[v];
  (*c)[1] = colset[v];
  return c;
}

const std::string &SymTensorIndex::shortstring() const {
  // It looks like the conversion from char to string is handled
  // automatically here...
  static const std::string voigt[] = {"xx", "yy", "zz", "yz", "xz", "xy"};
  return voigt[v];
}

std::ostream &operator<<(std::ostream &os, const FieldIndex &fi) {
  fi.print(os);
  return os;
}

void ScalarFieldIndex::print(std::ostream &os) const {
  os << "ScalarFieldIndex()";
}

void VectorFieldIndex::print(std::ostream &os) const {
  os << "VectorFieldIndex(" << index_ << ")";
}

void SymTensorIndex::print(std::ostream &os) const {
  os << "SymTensorIndex(" << row() << "," << col() << ")";
}

std::ostream &operator<<(std::ostream &os, const IndexP &ip) {
  const FieldIndex &fi(ip);
  os << "IndexP(" << fi << ")";
  return os;
}

IteratorP *getSymTensorIterator(Planarity planarity) {
#if DIM==2
  if(planarity == IN_PLANE)
    return new IteratorP(new SymTensorInPlaneIterator());
  if(planarity == OUT_OF_PLANE)
    return new IteratorP(new SymTensorOutOfPlaneIterator());
#endif
  return new IteratorP(new SymTensorIterator());
}
