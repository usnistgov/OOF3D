// -*- C++ -*-
// $RCSfile: entiremeshsubproblem.C,v $
// $Revision: 1.10.2.3 $
// $Author: fyc $
// $Date: 2014/04/18 20:00:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/IO/oofcerr.h"
#include "engine/femesh.h"
#include "engine/meshiterator.h"
#include "engine/entiremeshsubproblem.h"

CEntireMeshSubProblem::CEntireMeshSubProblem() {
  
  consistency = true;
}

CEntireMeshSubProblem::~CEntireMeshSubProblem() {
  
}

ElementIterator CEntireMeshSubProblem::element_iterator() const {
  return mesh->element_iterator();
}

NodeIterator CEntireMeshSubProblem::node_iterator() const {
  return mesh->node_iterator();
}

FuncNodeIterator CEntireMeshSubProblem::funcnode_iterator() const {
  return mesh->funcnode_iterator();
}

bool CEntireMeshSubProblem::contains(const Element*) const {
  return true;
}

bool CEntireMeshSubProblem::containsNode(const Node*) const {
  return true;
}

MaterialSet *CEntireMeshSubProblem::getMaterials() const {
  return mesh->getAllMaterials();
}
