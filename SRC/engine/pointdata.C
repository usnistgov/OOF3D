// -*- C++ -*-
// $RCSfile: pointdata.C,v $
// $Revision: 1.5.6.3 $
// $Author: langer $
// $Date: 2014/11/05 16:54:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


// TODO: The PointData class was invented because we thought we would
// need to have fields and equations defined at gausspoints for some
// classes of problems.  We no longer think this, so it might be wise
// to re-incorporate the PointData functionality back into FuncNodes,
// which is where it was before.

// To dump index information about DoFs and eqns, uncomment this line
// and compile in debug mode.
//#define VERBOSE_POINTDATA

#include "engine/pointdata.h"
#include "engine/femesh.h"
#include "engine/freedom.h"
#include "engine/nodalequation.h"

PointData::PointData(FEMesh* mesh)
  : doflist(0),
    eqnlist(0),
    fieldset(mesh),
    equationset(mesh)
{
}


void PointData::addField(FEMesh* mesh, const Field &field) {  
  if(fieldset.add(&field, mesh)) {
    // This is the first time we've seen this field -- create and add
    // the DOFs.
    doflist.reserve(doflist.size() + field.ndof());
    for(int i=0;i<field.ndof(); i++) {
      DegreeOfFreedom *dof = mesh->createDoF();
#ifdef VERBOSE_POINTDATA 
#ifdef DEBUG
      std::cerr << "PointData::addField: " << field
      		<< " dof=" << dof->dofindex()
      		<< " comp=" << i << " pos=" << position() << std::endl;
#endif // DEBUG
#endif // VERBOSE_POINTDATA
      doflist.push_back(dof);
    }
  }
}

void PointData::removeField(FEMesh *mesh, const Field &field) {

  int offset = fieldset.offset(&field);
  
  if (fieldset.remove(&field, mesh)) {
    std::vector<DegreeOfFreedom*>::iterator start = doflist.begin() + offset;
    std::vector<DegreeOfFreedom*>::iterator end = start + field.ndof();
    for(std::vector<DegreeOfFreedom*>::iterator i=start; i< end; ++i) {
      mesh->removeDoF(*i);
    }
    doflist.erase(start,end);
  }
}
    
    
bool PointData::hasField(const Field &field) const {
  return fieldset.contains(&field);
}

int PointData::fieldDefCount(const Field & field) const {
  return fieldset.listed(&field);
}


void PointData::addEquation(FEMesh *mesh, const Equation &eqn) {
  if(equationset.add(&eqn, mesh)) {
    // Equation is new to this Node (ie, no other SubProblem has added it)
    eqnlist.reserve(eqnlist.size() + eqn.dim());
    for(int i=0; i<eqn.dim(); i++) {
      NodalEquation *ne = mesh->createNodalEqn();
#ifdef VERBOSE_POINTDATA
#ifdef DEBUG
      std::cerr << "PointData::addEquation: " << eqn
      		<< " nodaleqn=" << ne->ndq_index()
      		<< " comp=" << i << " pos=" << position() << std::endl;
#endif // DEBUG
#endif // VERBOSE_POINTDATA
      eqnlist.push_back(ne);
    }
  }
}


void PointData::removeEquation(FEMesh *mesh, const Equation &eqn) {
  int offset = equationset.offset(&eqn);
  if(equationset.remove(&eqn, mesh)) {
    std::vector<NodalEquation*>::iterator start = eqnlist.begin() + offset;
    std::vector<NodalEquation*>::iterator end = start + eqn.dim();
    for(std::vector<NodalEquation*>::iterator i=start; i<end; ++i) {
      mesh->removeNodalEqn(*i);
    }
    eqnlist.erase(start, end);
  }
}


bool PointData::hasEquation(const Equation &eqn) const {
  return equationset.contains(&eqn);
}
