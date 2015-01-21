// -*- C++ -*-
// $RCSfile: activearea.C,v $
// $Revision: 1.6.10.10 $
// $Author: langer $
// $Date: 2014/12/14 22:49:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/activearea.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/IO/oofcerr.h"


const std::string ActiveAreaList::displayname_("ActiveAreas");

// reg is set when the singleton ActiveAreasAttributeRegistration
// object is created, which is done when the activearea python module
// is imported.
static ActiveAreasAttributeRegistration *reg=0;

// Active areas don't affect microstructure pixel categorization,
// except when saving a Microstructure in a data file.  That means
// that for general purposes, when operator< is used, ActiveAreaLists
// should all be equal to each other.  strictLessThan is used instead
// of operator< when writing data files, so it has to actually compare
// the lists. 

bool ActiveAreaList::operator<(const PixelAttribute&) const {
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string ActiveAreasAttributeRegistration::classname_(
				     "ActiveAreasAttributeRegistration");

const std::string ActiveAreasAttributeRegistration::modulename_(
					"ooflib.SWIG.common.activearea");

ActiveAreasAttributeRegistration::ActiveAreasAttributeRegistration()
  : PxlAttributeRegistration("NamedActiveArea")
{
  reg = this;
}

PixelAttribute *ActiveAreasAttributeRegistration::createAttribute(
						   const CMicrostructure *ms)
  const 
{
  ActiveAreaList *aa =  new ActiveAreaList();
  addToGlobalData(ms, aa);
  return aa;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ActiveArea::ActiveArea(const ICoord *pxlsize, const Coord *size,
		       CMicrostructure *ms)
  : CPixelSelection(pxlsize, size, ms),
    SubAttribute(""),
    override_(false)
{}

ActiveArea::~ActiveArea() {}

// TODO OPT: Can named ActiveAreas be stored implicitly via the
// PixelAttributes in the Microstructure?  Unless they're actually
// being used, there's really no need to waste memory on the PixelSet
// and BitmapOverlay that are stored in the CPixelSelection part of
// the ActiveArea.

ActiveArea *ActiveArea::named_clone(const std::string &name) const { 
  ActiveArea *aa = new ActiveArea(*this); // copies pixset and bitmap
  aa->name_ = name;
  AttributeVectorMap avm;
  buildAttributeChangeMap(avm, &ActiveAreaList::add, aa, reg, 
			  pixset.getMicrostructure());
  for(ICoordVector::const_iterator i=pixset.members()->begin(); 
      i!=pixset.members()->end(); ++i)
    {
      pixset.getMicrostructure()->updateAttributeVector(*i, avm);
    }
  pixset.getMicrostructure()->recategorize();
  return aa;
}


void ActiveArea::clear() {
  AttributeVectorMap avm;
  buildAttributeChangeMap(avm, &ActiveAreaList::remove, this, reg,
			  pixset.getMicrostructure());
  for(ICoordVector::const_iterator i=pixset.members()->begin();
      i!=pixset.members()->end(); ++i) 
    {
      pixset.getMicrostructure()->updateAttributeVector(*i, avm);
    }
  pixset.getMicrostructure()->recategorize();
}



// Utility functions for IO operations.

ActiveAreaList *areaListFromPixel(const CMicrostructure *ms, 
				  const ICoord *pxl)
{
  ActiveAreaList *aalist = 
     dynamic_cast<ActiveAreaList*>(ms->getAttribute(*pxl, reg->index())); 
  // oofcerr << "areaListFromPixel: size=" << aalist->members().size()
  // 	  << std::endl;
  return aalist;
}


void ActiveArea::add_pixels(const ICoordVector *pxls) {
  bitmap.set(pxls);
  pixset.setFromBitmap(bitmap);
}
