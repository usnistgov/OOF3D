// -*- C++ -*-
// $RCSfile: orientmapproperty.C,v $
// $Revision: 1.3.12.1 $
// $Author: langer $
// $Date: 2013/11/08 20:46:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/cmicrostructure.h"
#include "common/corientation.h"
#include "engine/element.h"
#include "engine/femesh.h"
#include "engine/mastercoord.h"
#include "engine/ooferror.h"
#include "orientationmap/orientmapproperty.h"

OrientationMapProp::OrientationMapProp(PyObject *registry,
				       const std::string &name)
  : OrientationPropBase(registry, name)
{}

OrientationMapProp::~OrientationMapProp() {}

class OrientMapMeshData {
public:
  CMicrostructure *microstructure;
  OrientMap *odata;
  OrientMapMeshData(CMicrostructure *ms, OrientMap *orientmap)
    : microstructure(ms),
      odata(orientmap)
  {}
};

void OrientationMapProp::precompute(FEMesh *mesh) {
  if(mesh) {
    CMicrostructure *microstructure = mesh->get_microstructure();
    OrientMap *orientmap = getOrientMap(microstructure->name());
    if(orientmap == 0)
      throw ErrUserError("Microstructure does not have an Orientation Map!");
    set_mesh_data(mesh, new OrientMapMeshData(microstructure, orientmap)); 
  }
}

const COrientation *OrientationMapProp::orientation(const FEMesh *mesh,
						    const Element *element,
						    const MasterPosition &mpos
						    )
  const
{
  assert(mesh != 0);
  OrientMapMeshData *meshdata =
    static_cast<OrientMapMeshData*>(get_mesh_data(mesh));
  Coord where = element->from_master(mpos);
  ICoord pxl = meshdata->microstructure->pixelFromPoint(where);
  // const COrientation *ornt = &meshdata->odata->angle(pxl);
  // std::cerr << "OrientationMapProp::orientation:"
  // 	    << " where=" << where
  // 	    << " pixel=" << pxl
  // 	    << " ornt= " << ornt << " " << *ornt << std::endl;
  // return ornt;
  return &meshdata->odata->angle(pxl);
}

const COrientation *OrientationMapProp::orientation() const {
  throw ErrProgrammingError(
	    "OrientationMapProp::orientation() should never be called!",
	    __FILE__, __LINE__);
}

const COrientation *OrientationMapProp::orientation(
				    const CMicrostructure *microstructure,
				    const ICoord &where) const
{
  OrientMap *orientmap = getOrientMap(microstructure->name());
  return &orientmap->angle(where);
}

void OrientationMapProp::clear_mesh_data(FEMesh *mesh, void *data) const {
  delete static_cast<OrientMapMeshData*>(data);
}

