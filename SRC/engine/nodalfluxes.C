// -*- C++ -*-
// $RCSfile: nodalfluxes.C,v $
// $Revision: 1.9.10.1 $
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

#include "engine/nodalfluxes.h"
#include "engine/outputval.h"
#include "engine/fieldindex.h"
#include "engine/planarity.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/recoveredflux.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

NodalFluxes::~NodalFluxes()
{
  // deleting new'd DoubleVecs.
  for(std::vector<RFVec*>::size_type i=0; i<flux_values.size(); i++) {
    for(RFVec::size_type j=0; j<flux_values[i]->size(); j++)
      delete (*(flux_values[i]))[j];
    delete flux_values[i];
  }
}


int NodalFluxes::mat_index(const Material *mat) const {
  for(std::vector<const Material*>::size_type i=0; i<materials.size(); i++)
    if(materials[i]==mat)
      return i;
  return -1;
}


int NodalFluxes::flux_index(const Flux *fluks) const {
  for(std::vector<const Flux*>::size_type i=0; i<fluxes.size(); i++)
    if(fluxes[i]==fluks)
      return i;
  return -1;
}


void NodalFluxes::add_flux_value(const Material *mat, const Flux *fluks,
				 DoubleVec *fv)
{
  int imat = mat_index(mat);
  if(imat==-1) { // brand new entry
    RFVec *vec = new RFVec;  // RFVec => std::vector<RecoveredFlux*>
    vec->push_back( new RecoveredFlux(fv) );
    flux_values.push_back(vec);
    materials.push_back(mat);
    fluxes.push_back(fluks);
  }
  else {
    int iflux = flux_index(fluks);
    if(iflux==-1) {  // new flux entry
      flux_values[imat]->push_back( new RecoveredFlux(fv) );
      fluxes.push_back(fluks);
    }
    else {  // existing entry -- fv needs to be averaged.
      (*(flux_values[imat]))[iflux]->average(fv);
    }
  }
} 

OutputValue NodalFluxes::get_flux_output(const Material *mat,
					 const Flux *fluks)
{
  int imat = mat_index(mat);
  int iflux = flux_index(fluks);
  DoubleVec *fv = (*(flux_values[imat]))[iflux]->get_flux_value();
  OutputValue output = fluks->newOutputValue();
  for(IteratorP it = fluks->iterator(ALL_INDICES); !it.end(); ++it) {
    output[it] = (*fv)[it.integer()];
  }
  return output;
}

double NodalFluxes::get_flux_component(const Material *mat,
				       const Flux *fluks, const int &i)
{
  int imat = mat_index(mat);
  int iflux = flux_index(fluks);
  DoubleVec *fv = (*(flux_values[imat]))[iflux]->get_flux_value();
  return (*fv)[i];
}
