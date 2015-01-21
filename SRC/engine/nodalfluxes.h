// -*- C++ -*-
// $RCSfile: nodalfluxes.h,v $
// $Revision: 1.6.10.1 $
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

#ifndef NODALFLUXES_H
#define NODALFLUXES_H

#include "engine/outputval.h"
#include <vector>

class Flux;
class Material;
class OutputValue;
class RecoveredFlux;

typedef std::vector<RecoveredFlux*> RFVec;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class NodalFluxes {
private:
  std::vector<const Material*> materials;
  std::vector<const Flux*> fluxes;
  std::vector<RFVec*> flux_values;
public:
  NodalFluxes() {}
  ~NodalFluxes();
  int mat_index(const Material*) const;
  int flux_index(const Flux*) const;
  void add_flux_value(const Material*, const Flux*, DoubleVec*);
  OutputValue get_flux_output(const Material*, const Flux*);
  double get_flux_component(const Material*, const Flux*, const int&);
};

#endif // NODALFLUXES
