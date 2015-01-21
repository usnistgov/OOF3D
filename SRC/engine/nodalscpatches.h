// -*- C++ -*-
// $RCSfile: nodalscpatches.h,v $
// $Revision: 1.3.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:35 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef NODALSCPATCHES_H
#define NODALSCPATCHES_H

#include <map>
#include <vector>

class Flux;
class Material;
class CSCPatch;


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class NodalSCPatches {
private:
  std::vector<CSCPatch*> scpatches;
public:
  NodalSCPatches() {}
  ~NodalSCPatches();
  void add_patch(CSCPatch*);
  // debug-purpose functions
  std::vector<int> *get_elements_from_patch(const Material*);
  std::vector<int> *get_nodes_from_patch(const Material*);
  // recovering fluxes
  void recover_fluxes(const std::vector<Flux*>&);
};

#endif
