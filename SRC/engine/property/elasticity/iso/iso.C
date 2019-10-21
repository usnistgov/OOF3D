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
#include "engine/property/elasticity/iso/iso.h"

CIsoElasticityProp::CIsoElasticityProp(PyObject *registration,
				       PyObject *self,
				       const std::string &nm, 
				       const Cijkl &c)
  : PythonNative<Property>(self),
    Elasticity(nm,registration),
    c_ijkl(c)
{
}

void CIsoElasticityProp::output(FEMesh *mesh,
				const Element *element,
				const PropertyOutput *output,
				const MasterPosition &pos,
				OutputVal *data)
{
  const std::string &outputname = output->name();
  if(outputname == "Material Constants:Mechanical:Elastic Modulus C") {
    const Cijkl modulus = cijkl(mesh, element, pos);
    ListOutputVal *listdata = dynamic_cast<ListOutputVal*>(data);
    // The PropertyOutput's "components" parameter is a list of pairs
    // of Voigt indices in string form ("11", "62", etc).
    std::vector<std::string> *idxstrs =
      output->getListOfStringsParam("components");
    for(unsigned int i=0; i<idxstrs->size(); i++) { // loop over index pairs
      const std::string &voigtpair = (*idxstrs)[i];
      // Convert from string to int and 1-based indices to 0-based indices
      SymTensorIndex idx0(int(voigtpair[0]-'1'));
      SymTensorIndex idx1(int(voigtpair[1]-'1'));
      // Store the Cijkl component in the PropertyOutput.
      (*listdata)[i] = c_ijkl(idx0, idx1);
    }
    delete idxstrs;
  }
  Elasticity::output(mesh, element, output, pos, data);
}
