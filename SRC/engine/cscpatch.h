// -*- C++ -*-
// $RCSfile: cscpatch.h,v $
// $Revision: 1.9.10.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSCPATCH_H
#define CSCPATCH_H

#include <oofconfig.h>
#include "common/coord_i.h"
#include "common/smallmatrix.h"

#include <iostream>
#include <vector>

class Element;
//class FEMesh;
class CSubProblem;
class Flux;
class MasterCoord;
class Material;
class Node;


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSCPatch {
private:
  //FEMesh *mesh;
  CSubProblem* subproblem;
  const int femesh_order_;
  const Material* material_;
  const bool qualified_;

  std::vector<Element*> elements;  // elements in the patch
  std::vector<Node*> nodes;  // recovery nodes
  SmallMatrix Amtx;  // n x n matrix
  std::vector<SmallMatrix*> coefficients;
public:
  CSCPatch(CSubProblem*, const int, const Material*,
	   const std::vector<int>*, const std::vector<int>*, const int);
//   CSCPatch(const CSCPatch&);
  ~CSCPatch();

  const Material* material() { return material_; }
  std::vector<int> *get_elements() const;
  std::vector<int> *get_nodes() const;

  bool qualified() const { return qualified_; }
  double basis(int, const Coord&);  // 2D polynomial basis functions.
  int nsamples();  // total no. of sampling points in the patch.
  int get_size();  // re-size "size_"
  void recover_fluxes(const std::vector<Flux*>&);  // solve for coefficents.
  void eval_Amtx(const int&, const Coord&,
		 std::vector<SmallMatrix*>&);  // preliminary stuff.
  // solve for coefficients set. 
  void solve(const int&, const Flux*, std::vector<int>&,
	     std::vector<MasterCoord>&,
	     std::vector<SmallMatrix*>&);
  void recover_this_flux(const int&, const Node*, const int&, const Flux*);
};

#endif // CSCPATCH_H
