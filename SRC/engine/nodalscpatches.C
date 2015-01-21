// -*- C++ -*-
// $RCSfile: nodalscpatches.C,v $
// $Revision: 1.4.18.1 $
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
#include <iostream>
#include <map>

#include "common/ooferror.h"
#include "engine/cscpatch.h"
#include "engine/nodalscpatches.h"


NodalSCPatches::~NodalSCPatches()
{
  // deleting new'd CSCPatches
  for(std::vector<CSCPatch*>::iterator i=scpatches.begin(); i<scpatches.end();
      ++i)
    delete *i;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void NodalSCPatches::add_patch(CSCPatch *patch)
{
  scpatches.push_back(patch);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::vector<int> *NodalSCPatches::get_elements_from_patch(const Material *mat)
{
  for(std::vector<CSCPatch*>::iterator i=scpatches.begin(); i<scpatches.end();
      ++i)
    if((*i)->material() == mat)
      return (*i)->get_elements();
  throw ErrProgrammingError("Material not found", __FILE__, __LINE__);
//   for(int i=0; i<scpatches.size(); i++)
//     if(scpatches[i]->material() == mat)
//       return scpatches[i]->get_elements();
}

std::vector<int> *NodalSCPatches::get_nodes_from_patch(const Material *mat)
{
  for(std::vector<CSCPatch*>::iterator i=scpatches.begin(); i<scpatches.end();
      ++i)
    if((*i)->material() == mat)
      return (*i)->get_nodes();
  throw ErrProgrammingError("Material not found", __FILE__, __LINE__);
//   for(int i=0; i<scpatches.size(); i++)
//     if(scpatches[i]->material() == mat)
//       return scpatches[i]->get_nodes();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void NodalSCPatches::recover_fluxes(const std::vector<Flux*> &allfluxes)
{
  for(std::vector<CSCPatch*>::iterator i=scpatches.begin(); i<scpatches.end();
      ++i)
    (*i)->recover_fluxes(allfluxes);
//   for(int i=0; i<scpatches.size(); i++)
//     scpatches[i]->recover_fluxes(allfluxes);
}
