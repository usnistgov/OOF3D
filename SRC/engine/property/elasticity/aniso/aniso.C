// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/material.h"
#include "engine/ooferror.h"
#include "engine/property/elasticity/aniso/aniso.h"
#include "engine/property/orientation/orientation.h"

void CAnisoElasticity::cross_reference(Material *mat) {
//   Trace("CAnisoElasticity::cross_reference");
  try {
    orientation = 
      dynamic_cast<OrientationPropBase*>(mat->fetchProperty("Orientation"));
  }
  catch (ErrNoSuchProperty&) {
    // If fetchProperty failed, we have to ensure that an old pointer
    // value isn't still being stored.
    orientation = 0;
    throw;
  }
}

void CAnisoElasticity::precompute(FEMesh *mesh) {
  Elasticity::precompute(mesh);
  // This assumes/requires that the rotation matrix output by
  // orientation->eulerangle() multiplies a crystal-coordinate vector
  // to give the same vector in lab coordinates.
  if(orientation && orientation->constant_in_space())
    lab_cijkl = crystal_cijkl().transform(orientation->orientation());
}

const Cijkl CAnisoElasticity::cijkl(const FEMesh *mesh, const Element *el,
				   const MasterPosition &mpos)
  const
{
  assert(orientation != 0);
  if(orientation->constant_in_space())
    return lab_cijkl;
  return crystal_cijkl().transform(orientation->orientation(mesh, el, mpos));
}

const Cijkl &CAnisoElasticity::crystal_cijkl() const {
  return crystal_cijkl_;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CAnisoElasticity::output(FEMesh *mesh,
			      const Element *element,
			      const PropertyOutput *output,
			      const MasterPosition &pos,
			      OutputVal *data)
{
  const std::string &outputname = output->name();
  if(outputname == "Material Constants:Mechanical:Elastic Modulus C") {
    ListOutputVal *listdata = dynamic_cast<ListOutputVal*>(data);
    std::vector<std::string> *idxstrs =
      output->getListOfStringsParam("components");
    assert(idxstrs->size() <= listdata->size());
    const std::string *frame = output->getEnumParam("frame"); // Lab or Crystal
    
    if(*frame == "Lab") {
      // TODO: Use a timestamp and only precompute when necessary.
      precompute(mesh);
      copyOutputVals(cijkl(mesh, element, pos), listdata, *idxstrs);
    }
    else {
      assert(*frame == "Crystal");
      copyOutputVals(crystal_cijkl(), listdata, *idxstrs);
    }
    delete idxstrs;
    delete frame;
  }
  Elasticity::output(mesh, element, output, pos, data);
}
