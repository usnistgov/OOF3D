// -*- C++ -*-
// $RCSfile: field.C,v $
// $Revision: 1.64.2.4 $
// $Author: langer $
// $Date: 2014/09/17 17:47:57 $


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
#include "common/removeitem.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/csubproblem.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/fieldeqnlist.h"
#include "engine/fieldindex.h"
#include "engine/indextypes.h"
#include "engine/meshiterator.h"
#include "engine/node.h"
#include "engine/ooferror.h"
#include "engine/outputval.h"
#include "engine/pointdata.h"
#include "engine/property.h"
#include "engine/symmmatrix.h"
#include <iostream>
#include <vector>

std::vector<Field*> &Field::all() {
  static std::vector<Field*> all_fields;
  return all_fields;
}

std::vector<CompoundField*> &CompoundField::allcompoundfields() {
  static std::vector<CompoundField*> all_fields;
  return all_fields;
}

Field *getFieldByIndex(int index) {
  // getFieldByIndex is used by FEMesh::getFieldSetByID, which returns
  // a list of fields in the order in which they were defined.
  // Currently, this may be the only reason that Field::all() returns
  // a std::vector instead of a std::map.  A std::map would otherwise
  // be more natural, but the ordering is important, so a map can't be
  // used.
  return Field::all()[index];
}

CompoundField *getCompoundFieldByIndex(int index) {
  return CompoundField::allcompoundfields()[index];

}

FEWrapper<Field>::AllWrappers
&Field::FindAllFieldWrappers::operator()()
{
  return mesh->fieldwrappers;
}

bool operator<(const Field::FieldData &a, const Field::FieldData &b) {
  if(a.active == b.active)
    return dynamic_cast<const FieldEqnData&>(a) < 
      dynamic_cast<const FieldEqnData&>(b);
  return a.active < b.active;
}

int countFields() {
  return Field::all().size(); 
}

int countCompoundFields() {
  return CompoundField::allcompoundfields().size();
}

Field *Field::getField(const std::string &nm) {
  const std::vector<Field*> &list = all();
  for(std::vector<Field*>::size_type i=0; i<list.size(); i++) {
    if(list[i]->name() == nm) {
      return list[i];
    }
  }
  throw ErrProgrammingError("Unknown Field \"" + nm + "\"",
			    __FILE__, __LINE__);
}

Field::Field(const std::string &nm, int dofs)
  : name_(nm),
    index_(all().size()),
#if DIM==2
    in_plane_(true),
#endif	// DIM==2
    dim(dofs),
    time_derivative_(0)
{
  all().push_back(this);
}


Field::~Field() {
  // this should be called only if the program is exiting... Fields
  // are global static objects and aren't deleted
  remove_item(all(), this);
}

std::ostream &operator<<(std::ostream &os, const Field &field) {
  os << field.name();
  return os;
}

const std::string &Field::name() const {
  return name_;
}

//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//

void Field::define(CSubProblem *subproblem) const {
  subproblem->do_define_field(*this);
}

void Field::undefine(CSubProblem *subproblem) const {
  subproblem->do_undefine_field(*this);
}

bool Field::is_defined(const CSubProblem *subproblem) const {
  return subproblem->is_defined_field(*this);
}

//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//

void Field::activate(CSubProblem *subproblem) const {
  subproblem->do_activate_field(*this);
}

void Field::deactivate(CSubProblem *subproblem) const {
  subproblem->do_deactivate_field(*this);
}

bool Field::is_active(const CSubProblem *subproblem) const {
  return subproblem->is_active_field(*this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Field::registerProperty(Property *prop) const {
  prop->require_field(*this);
}

void CompoundField::registerProperty(Property *prop) const {
  prop->require_field(*this);
#if DIM==2
  prop->require_field(*zfield_);
#endif
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// position of a given component in the dof lists in the nodes

int Field::localindex(const PointData *node, const FieldIndex &component) const
{
  // offset() will raise ErrNoSuchField if this field isn't defined at the node.
  return node->fieldset.offset(this) + component.integer();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double Field::value(const FEMesh *mesh, const PointData *node, int component)
  const
{
  return operator()(node, component)->value(mesh);
}

double Field::value(const FEMesh *mesh, const ElementFuncNodeIterator &node,
		    int component) const 
{
  return operator()(node, component)->value(mesh);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==2
CompoundField::CompoundField(const std::string &name, int dim,
			     Field *outofplane,
			     Field *timederiv,
			     Field *outofplanetimederiv)
  : Field(name, dim),
    zfield_(outofplane),
    zfield_time_derivative_(outofplanetimederiv),
    cfield_indx(allcompoundfields().size())
{
  time_derivative_ = timederiv;
  zfield_->set_oop(); // Set z component to be out-of-plane.
  zfield_->set_time_derivative(outofplanetimederiv);
  allcompoundfields().push_back(this);
}

#elif DIM==3
CompoundField::CompoundField(const std::string &name, int dim,
			     Field *timederiv)
  : Field(name, dim),
    cfield_indx(allcompoundfields().size())
{
  time_derivative_ = timederiv;
  allcompoundfields().push_back(this);
}
#endif	// DIM==3

CompoundField::~CompoundField() {
  remove_item(allcompoundfields(), this);
}


#if DIM==2
bool CompoundField::in_plane(const FEMesh *mesh) const {
  return mesh->in_plane(*this);
}

bool CompoundField::in_plane(const CSubProblem *subproblem) const {
  return subproblem->mesh->in_plane(*this);
}
#endif // DIM==2

void CompoundField::define(CSubProblem *subproblem) const {
  subproblem->do_define_field(*this);
#if DIM==2
  subproblem->do_define_field(*zfield_);
#endif // DIM==2
}

void CompoundField::undefine(CSubProblem *subproblem) const {
  subproblem->do_undefine_field(*this);
#if DIM==2
  subproblem->do_undefine_field(*zfield_);
  subproblem->do_undefine_field(*zfield_time_derivative_);
#endif // DIM==2
  subproblem->do_undefine_field(*time_derivative_);
}

void CompoundField::activate(CSubProblem *subproblem) const {
  subproblem->do_activate_field(*this);
#if DIM==2
  if(!in_plane(subproblem->mesh))
    subproblem->do_activate_field(*zfield_);
#endif // DIM==2
}

void CompoundField::deactivate(CSubProblem *subproblem) const {
  subproblem->do_deactivate_field(*this);
#if DIM==2
  subproblem->do_deactivate_field(*zfield_);
#endif // DIM==2
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ScalarField::ScalarField(const std::string &nm)
  : Field(nm, 1),
    ScalarFieldBase(nm),
#if DIM==2
    CompoundField(nm, 1, new ScalarFieldBase(nm+std::string("_z")),
		  new ScalarFieldBase(nm+std::string("_t")),
		  new ScalarFieldBase(nm+std::string("_tz")))
#elif DIM==3
    CompoundField(nm, 1,
		  new ScalarFieldBase(nm+std::string("_t")))
#endif // DIM==3
{
}

const std::string ScalarField::classname_("ScalarField");

DegreeOfFreedom *ScalarFieldBase::operator()(const PointData *node) const {
  // offset() will raise ErrNoSuchField if this field isn't defined at the node.
  return node->doflist[node->fieldset.offset(this)];
}

DegreeOfFreedom *ScalarFieldBase::operator()(const ElementFuncNodeIterator &ei)
  const 
{
  return operator()(ei.funcnode());
}

// These two silly versions have to exist because these two functions
// have to be virtual in the Field base class. That's because
// CompoundField::out_of_plane returns a pointer to a Field base class
// object.
DegreeOfFreedom *ScalarFieldBase::operator()(const PointData *node,
					     int component) const
{
  assert(component == 0);
  // offset() will raise ErrNoSuchField if this field isn't defined at the node.
  return node->doflist[node->fieldset.offset(this)];
}

DegreeOfFreedom *ScalarFieldBase::operator()(const ElementFuncNodeIterator &ei,
					     int component) const 
{
  assert(component == 0);
  return operator()(ei.funcnode());
}

OutputValue ScalarFieldBase::newOutputValue() const {
  return OutputValue(new ScalarOutputVal(0.));
}

OutputValue ScalarFieldBase::output(const FEMesh *mesh, const PointData &node)
  const
{
  if(node.hasField(*this))
    return OutputValue(new ScalarOutputVal(operator()(node)->value(mesh)));
  else
    return OutputValue(new ScalarOutputVal(0.0));
}

OutputValue ScalarFieldBase::output(const FEMesh *mesh, 
				    const ElementFuncNodeIterator &node) const
{
  if(node.hasField(*this))
    return OutputValue(new ScalarOutputVal(operator()(node)->value(mesh)));
  else
    return OutputValue(new ScalarOutputVal(0.0));
}

void ScalarFieldBase::setValueFromOutputValue(FEMesh *mesh, 
					      const PointData &node,
					      const OutputValue *ov)
{
  assert(node.hasField(*this));
  const ScalarOutputVal &sov =
    dynamic_cast<const ScalarOutputVal&>(ov->valueRef());
  operator()(node)->value(mesh) = sov.value();
}


IteratorP ScalarFieldBase::iterator(Planarity) const {
  return IteratorP(new ScalarFieldIterator);
}

IndexP ScalarFieldBase::componenttype() const {
  return IndexP(new ScalarFieldIndex);
}

IndexP ScalarFieldBase::getIndex(const std::string &) const {
  return IndexP(new ScalarFieldIndex);
}

const std::string ScalarFieldBase::classname_("ScalarFieldBase");

//------------------------------

TwoVectorField::TwoVectorField(const std::string &nm)
  : Field(nm, 2),
    TwoVectorFieldBase(nm),
#if DIM==2
    CompoundField(nm, 2, new ThreeVectorField(nm+std::string("_z")),
		  new TwoVectorFieldBase(nm+std::string("_t")),
		  new ThreeVectorField(nm+std::string("_tz"))
		  )
#elif DIM==3
    CompoundField(nm, 2,
		  new TwoVectorFieldBase(nm+std::string("_t")))
#endif // DIM==3
{
}

const std::string TwoVectorField::classname_("TwoVectorField");

DegreeOfFreedom *TwoVectorFieldBase::operator()(const PointData *node, int comp)
  const
{
//   if(comp<0 || comp >= 2) {
//     std::cerr << "TwoVectorFieldBase::operator(): " << comp << " " << *this
// 	      << std::endl;
//   }
  assert(comp >= 0 && comp < 2);
  // offset() will raise ErrNoSuchField if this field isn't defined at the node.
  return node->doflist[node->fieldset.offset(this) + comp];
}

DegreeOfFreedom *
TwoVectorFieldBase::operator()(const ElementFuncNodeIterator &ei, int comp)
  const
{
  return operator()(ei.funcnode(), comp);
}

OutputValue TwoVectorFieldBase::newOutputValue() const {
  return OutputValue(new VectorOutputVal(2));
}

OutputValue TwoVectorFieldBase::output(const FEMesh *mesh, const PointData &node)
  const
{
  VectorOutputVal *vov = new VectorOutputVal(2);
  OutputValue ov(vov);
  if(node.hasField(*this)) {
    (*vov)[0] = operator()(node, 0)->value(mesh);
    (*vov)[1] = operator()(node, 1)->value(mesh);
  }
  return ov;
}

OutputValue TwoVectorFieldBase::output(const FEMesh *mesh, 
				       const ElementFuncNodeIterator &node)
  const 
{
  VectorOutputVal *vov = new VectorOutputVal(2);
  OutputValue ov(vov);
  if(node.hasField(*this)) {
    (*vov)[0] = operator()(node, 0)->value(mesh);
    (*vov)[1] = operator()(node, 1)->value(mesh);
  }
  return ov;
}

void TwoVectorFieldBase::setValueFromOutputValue(FEMesh *mesh,
						 const PointData &node,
						 const OutputValue *ov)
{
  assert(node.hasField(*this));
  const VectorOutputVal &vov = 
    dynamic_cast<const VectorOutputVal&>(ov->valueRef());
  (*this)(node, 0)->value(mesh) = vov[0];
  (*this)(node, 1)->value(mesh) = vov[1];
}

// // The TwoVectorHelper class allows TwoVectorField(FuncNode) to act like a
// Coord.
// TwoVectorHelper TwoVectorFieldBase::operator()(FEMesh *mesh, 
// 					       const FuncNode *node) const
// {
//   // offset() will raise ErrNoSuchField if this field isn't defined at the node.
//   int idx = node->fieldset.offset(this);
//   return TwoVectorHelper(mesh, node->doflist[idx], node->doflist[idx+1]);
// }

// TwoVectorHelper
// TwoVectorFieldBase::operator()(FEMesh *mesh, 
// 			       const ElementFuncNodeIterator &ei) const
// {
//   return operator()(mesh, ei.funcnode());
// }

// // field(node) = coord
// TwoVectorHelper &TwoVectorHelper::operator=(const Coord &v) {
//   x->value(mesh) = v(0);
//   y->value(mesh) = v(1);
//   return *this;
// }

// // coord = field(node)
// TwoVectorHelper::operator const Coord() const {
//   return Coord(x->value(mesh), y->value(mesh));
// }

IteratorP TwoVectorFieldBase::iterator(Planarity) const {
  return IteratorP(new VectorFieldIterator(0, 2));
}

IndexP TwoVectorFieldBase::componenttype() const {
  return IndexP(new VectorFieldIndex);
}

IndexP TwoVectorFieldBase::getIndex(const std::string &str) const {
  return IndexP(new VectorFieldIndex(str[0] - 'x'));
}

const std::string TwoVectorFieldBase::classname_("TwoVectorFieldBase");

//-------------------------------


const std::string VectorFieldBase::classname_("VectorFieldBase");

DegreeOfFreedom *VectorFieldBase::operator()(const PointData *node, int comp)
  const
{
  assert(comp >= 0 && comp < dim);
  // offset() will raise ErrNoSuchField if this field isn't defined at the node.
  return node->doflist[node->fieldset.offset(this) + comp];
}

DegreeOfFreedom *VectorFieldBase::operator()(const ElementFuncNodeIterator &ei,
					     int comp)
  const
{
  return operator()(ei.funcnode(), comp);
}

OutputValue VectorFieldBase::newOutputValue() const {
  return OutputValue(new VectorOutputVal(dim));
}

OutputValue VectorFieldBase::output(const FEMesh *mesh, const PointData &node)
  const 
{
  VectorOutputVal *vov = new VectorOutputVal(dim);
  OutputValue ov(vov);
  if(node.hasField(*this))
    for(int i=0; i<dim; i++)
      (*vov)[i] = operator()(node, i)->value(mesh);
  return ov;
}

OutputValue VectorFieldBase::output(const FEMesh *mesh, 
				    const ElementFuncNodeIterator &node) const
{
  VectorOutputVal *vov = new VectorOutputVal(dim);
  OutputValue ov(vov);
  if(node.hasField(*this))
    for(int i=0; i<dim; i++)
      (*vov)[i] = operator()(node, i)->value(mesh);
  return ov;
}

void VectorFieldBase::setValueFromOutputValue(FEMesh  *mesh,
					      const PointData &node,
					      const OutputValue *ov)
{
  assert(node.hasField(*this));
  const VectorOutputVal &vov = 
    dynamic_cast<const VectorOutputVal&>(ov->valueRef());
  for(int i=0; i<dim; i++)
    (*this)(node, i)->value(mesh) = vov[i];
}

// // The VectorHelper class allows VectorField(FuncNode) to act like a Vector.
// VectorHelper VectorFieldBase::operator()(FEMesh *mesh, const FuncNode *node)
//   const
// {
//   // offset() will raise ErrNoSuchField if this field isn't defined at the node.
//   return VectorHelper(mesh, &node->doflist[node->fieldset.offset(this)], dim);
// }

// VectorHelper VectorFieldBase::operator()(FEMesh *mesh,
// 					 const ElementFuncNodeIterator &ei)
//   const
// {
//   return operator()(mesh, ei.funcnode());
// }

// // field(node) = vector
// VectorHelper &VectorHelper::operator=(const VECTOR_D &v) {
// #ifdef DEBUG
//   assert(v.dim() == ndof);
// #endif
//   for(unsigned int i=0; i<ndof; i++)
//     x[i]->value(mesh) = v[i];
//   return *this;
// }

// // vector = field(node)
// VectorHelper::operator const VECTOR_D() const {
//   VECTOR_D v(ndof);
//   for(unsigned int i=0; i<ndof; i++)
//     v[i] = x[i]->value(mesh);
//   return v;
// }

IteratorP VectorFieldBase::iterator(Planarity planarity) const {
#if DIM==2
  int mindim = (planarity == OUT_OF_PLANE ? 2 : 0);
  int maxdim = (planarity == IN_PLANE ? 2 : ndof());
#elif DIM==3
  int mindim = 0;
  int maxdim = 3;
#endif // DIM==3
  return IteratorP(new VectorFieldIterator(mindim, maxdim));
}

IndexP VectorFieldBase::componenttype() const {
  return IndexP(new VectorFieldIndex);
}

IndexP VectorFieldBase::getIndex(const std::string &str) const {
  return IndexP(new VectorFieldIndex(str[0] - 'x'));
}

ThreeVectorField::ThreeVectorField(const std::string &nm)
  : Field(nm, 3),
    ThreeVectorFieldBase(nm)
#if DIM==3
  , CompoundField(nm, 3,
		  new ThreeVectorFieldBase(nm+std::string("_t")))
#endif // DIM==3
{
}

const std::string ThreeVectorField::classname_("ThreeVectorField");
const std::string ThreeVectorFieldBase::classname_("ThreeVectorFieldBase");

//////////////////////

const std::string SymmetricTensorField::classname_("SymmetricTensorField");

DegreeOfFreedom *SymmetricTensorField::operator()
  (const PointData* pd, int comp) const
{
  assert ((comp >= 0) && (comp <= 6));
  return pd->doflist[pd->fieldset.offset(this) + comp];
}

// TODO 3.1: Should have another one for (i,j) indices?


DegreeOfFreedom *SymmetricTensorField::operator()
  (const ElementFuncNodeIterator &ei, int comp) const 
{
  return this->operator()(ei.funcnode(),comp);
}

DegreeOfFreedom *SymmetricTensorField::operator()
  (const ElementFuncNodeIterator &ei, SymTensorIterator &sti) const 
{
  return this->operator()(ei.funcnode(),sti.integer());
}

DegreeOfFreedom *SymmetricTensorField::operator()
  (const PointData &pd, SymTensorIterator& sti) const 
{
  return this->operator()(&pd, sti.integer());
}

OutputValue SymmetricTensorField::newOutputValue() const {
  return OutputValue(new SymmMatrix3());
}

OutputValue SymmetricTensorField::output(const FEMesh *mesh,
					 const PointData &pd) const 
{
  SymmMatrix3 *oval = new SymmMatrix3();
  OutputValue ov(oval);
  if(pd.hasField(*this)) {
    for(SymTensorIterator i=SymTensorIterator(0); 
	!i.end(); ++i)
      (*oval)[i] = operator()(pd, i)->value(mesh);
  }
  return ov;
}


OutputValue 
SymmetricTensorField::output(const FEMesh *mesh,
			     const ElementFuncNodeIterator &pd) const 
{
  SymmMatrix3 *oval = new SymmMatrix3();
  OutputValue ov(oval);
  if(pd.hasField(*this)) {
    for(SymTensorIterator i=SymTensorIterator(0); 
	!i.end(); ++i)
      (*oval)[i] = operator()(pd, i)->value(mesh);
  }
  return ov;
}


void SymmetricTensorField::setValueFromOutputValue
(FEMesh* m, const PointData &pd, const OutputValue *v) 
{  
  assert(pd.hasField(*this));
  const SymmMatrix3 &sym_v = 
    dynamic_cast<const SymmMatrix3&>(v->valueRef());
  DoubleVec *vvec = sym_v.value_list();
  for(int i=0;i<6;++i) 
    (*this)(pd,i)->value(m) = (*vvec)[i];
  free(vvec);
}

IteratorP SymmetricTensorField::iterator(Planarity p) const {
  // Weird but right -- getSymTensorIterator returns an IteratorP*,
  // just dereference it to get what we want.
  return *getSymTensorIterator(p);
}

IndexP SymmetricTensorField::componenttype() const {
  return IndexP(new SymTensorIndex);
}

IndexP SymmetricTensorField::getIndex(const std::string& str) const {
  return IndexP(new SymTensorIndex(SymTensorIndex::str2voigt(str)));
}
