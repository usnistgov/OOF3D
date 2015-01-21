// -*- C++ -*-
// $RCSfile: pixelattribute.h,v $
// $Revision: 1.11.18.19 $
// $Author: langer $
// $Date: 2014/12/12 19:38:51 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PIXELATTRIBUTE_H
#define PIXELATTRIBUTE_H

#include "common/coord.h"
#include "common/array.h"
#include "common/pythonexportable.h"
#include "common/pixelattribute_i.h"
#include <string>

class CMicrostructure;

// TODO 3.1: Rewrite this!

// Pixels in a Microstructure are assigned a pointer to a vector of
// attributes. The main storage for these attributes is the
// MicrostructureAttributes class.  Pixels with equivalent vectors of
// attributes (certain attributes do not affect this comparison) are
// put into the same category.  When a mesh is generated, it is
// adjusted to segregate pixels of different categories into different
// elements.

// In principle, the attributes of a pixel may not be definable within
// the "common" module, where the Microstructure lives.  For example,
// the Material assigned to a pixel is an attribute, but it's defined
// in "engine".  Therefore we need a generic way of managing unknown
// attributes.

// Each type of pixel attribute has two classes associated with it,
// derived from the base classes PixelAttribute and
// PxlAttributeRegistration.  The PxlAttributeRegistration contains
// information about how to create the attributes, retrieve values
// from a Microstructure, and save them to a file.  There is one
// PxlAttributeRegistration instance for each type of pixel attribute.
// On the other hand, there is one PixelAttribute instance for each
// unique (where all attributes contribute to the distinction) vector
// of attributes. This is what is stored in the
// MicrostructureAttributes class. Each pixel has a pointer to one of
// these vectors.

// Subclasses of PixelAttribute must provide an operator< const member
// function which takes a const PixelAttribute& argument.  The
// argument can be safely cast (with dynamic_cast) to the derived
// type.  This function is what's used to determine if two attributes
// are different when categorizing pixels. Certain pixel attributes
// are always equal in terms of meshing category.

// Subclasses of PixelAttribute must also provide a strictLessThan
// method, which is exactly like operator< except that it notices
// differences that are not relevant to meshing categories, such as
// the ActiveVolume (Area) attribute.  It's used when categorizing
// pixels in order to save them in a data file and to maintain a
// unique set of attributes in the PixelAttributeGlobalData.  For
// example, the pixel group attribute's operator< ignores groups that
// don't have the "meshable" flag set, but strictLessThan does not
// ignore the flag.

// Subclasses of PxlAttributeRegistration have the following requirements:

//* TODO 3.1: verify that these requirements are necessary and that
//* they are met in the new framework. (Changed to TODO 3.1 because it
//* seems to be working, except for possibly named active areas and
//* unmeshable voxel groups, which have problems that we're postponing
//* past 3.0.)

// 1. They must define a virtual function, createAttribute(), which
// returns a pointer to a new PixelAttribute of the appropriate
// derived type.

// 1a. They may contain an optional function
// createAttributeGlobalData(), which creates a subclass of
// PixelAttributeGlobalData, which holds data specific to a
// Microstructure but not to a pixel.

// 2. PxlAttributeRegistration is a PythonExportable class, so
// subclasses must define classname() and modulename() functions.

// 3. The subclass must be swigged.

// 4. The OOF.LoadData.Microstructure.DefineCategory menu (aka
// common.IO.microstructureIO.categorymenu) must be given a menu item
// whose name is the name of the PxlAttributeRegistration. This menu
// item reads attributes from a data file and stores them in a
// Microstructure.  It has at least two arguments: a microstructure
// name ("microstructure") and an integer ("category").  To be useful
// it should have *additional* arguments that define a pixel attribute.
// The callback should use microstructureIO.getCategoryPixels() to
// retrieve the list of pixels in the given category and then assign
// the pixel attribute to those pixels.

// 5. The Python shadow class for the PxlAttributeRegistration must
// have a writeData() function which writes the additional arguments
// mentioned above into a datafile.  The arguments to writeData are
// the DataFile object (see common/IO/datafile.py), the
// Microstructure, and a representative pixel from the Microstructure.
// The attributes of the given pixel should be used to construct the
// arguments, which should be written to the file with
// DataFile.argument().  If the given pixel does not have the
// attribute (eg, a pixel to which no Material has been assigned)
// writeData should return 0 and not call DataFile.argument().
// Otherwise it should return 1.

// 6. A single instance of the subclass must be created.


// The MicrostructureAttributes class keeps a set with one pointer to
// each unique attribute (using the PixelAttributeVector::ltAttributes
// function for distinguishing PAV's). TODO 3.1: more details here

// The CMicrostructure keeps a list of arrays of pointers to
// PixelAttributes.  The attribute code can get access to the array
// with PxlAttributeRegistration::map(CMicrostructure&).  It can then
// set the attributes for individual pixels in the array.

// -------------

// Base class for attributes.

class PixelAttribute {
public:
  PixelAttribute() {};
  virtual ~PixelAttribute() {}
  virtual bool operator<(const PixelAttribute&) const = 0;
  virtual bool strictLessThan(const PixelAttribute &other) const = 0;
  static bool strictLTAttributes(const PixelAttribute *p0,
				 const PixelAttribute *p1) 
  {
    return p0->strictLessThan(*p1);
  }
  virtual void print(std::ostream&) const = 0; // for debugging
  
};

std::ostream &operator<<(std::ostream&, const PixelAttribute&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PixelAttributeVector {
  // TODO MER: Should this be derived from std::vector<PixelAttribute*>
  // instead of containing one?
private:
  std::vector<PixelAttribute*> vec;
  int voxels;
public:
  PixelAttributeVector() 
    : vec(0), voxels(0) 
  {}
  PixelAttributeVector(const PixelAttributeVector &pav) 
  : vec(pav.vec),
    voxels(0)
  {}
  ~PixelAttributeVector() {}
  PixelAttribute*& operator[](const unsigned int &i) {
    assert(i>=0 && i<vec.size()); 
    return vec[i];
  }
  PixelAttribute* const & operator[](const unsigned int &i) const {
    assert(i>=0 && i<vec.size()); 
    return vec[i];
  }
  void push_back(PixelAttribute *pa) { vec.push_back(pa); }
  std::vector<PixelAttribute*>::size_type size() const { return vec.size(); }
  void incrementVoxelCount() { ++voxels; }
  void decrementVoxelCount() { --voxels; }
  int getNumberOfVoxels() { return voxels; }
  static bool ltAttributes(const PixelAttributeVector *pavec0,
			   const PixelAttributeVector *pavec1);
  static bool strictLTAttributes(const PixelAttributeVector *pavec0,
				 const PixelAttributeVector *pavec1);
  static bool pointerLTAttributes(const PixelAttributeVector *pavec0,
				  const PixelAttributeVector *pavec1);
  static bool isMapTrivial(const AttributeVectorMap &avm);
};


typedef std::set<PixelAttribute*, bool (*)(const PixelAttribute*,
					   const PixelAttribute*)> AttributeSet;

std::ostream &operator<<(std::ostream &, const PixelAttributeVector&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PixelAttributeGlobalData {
protected:
  AttributeSet attributeValues;
public:
  PixelAttributeGlobalData() 
    : attributeValues(PixelAttribute::strictLTAttributes)
  {}
  virtual ~PixelAttributeGlobalData();
  PixelAttribute *sync(PixelAttribute* pa);
  int nValues() { return attributeValues.size(); }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The PxlAttributeRegistration class stores information about a set
// of Attributes: name, initialization function, output functions, etc.

class PxlAttributeRegistration
  : public PythonExportable<PxlAttributeRegistration>
{
private:
  static std::vector<PxlAttributeRegistration*> &registrations();
  const std::string name_;
  int index_;
  friend class CMicrostructure;
public:
  PxlAttributeRegistration(const std::string &name);
  virtual ~PxlAttributeRegistration() {}
  static int nRegistrations() { return registrations().size(); }
  static const PxlAttributeRegistration *getRegistration(int i);
  const std::string &name() const { return name_; }
  int index() const { return index_; }
  PixelAttributeGlobalData *globalData(const CMicrostructure*) const;

  // Create a PixelAttribute object of the appropriate type.
  virtual PixelAttribute *createAttribute(const CMicrostructure*) const = 0;

  virtual PixelAttributeGlobalData *createAttributeGlobalData(
				      const CMicrostructure*) const;
 
  virtual void addToGlobalData(const CMicrostructure *MS, PixelAttribute *pa) 
    const;
};

int nAttributes();
const PxlAttributeRegistration *getRegistration(int);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// At least two types of pixel attributes are comprised of lists of
// other objects: GroupLists and ActiveAreaLists. These attributes are
// derived from the ListAttribute class. The other objects must be
// derived from the SubAttribute class.

class SubAttribute {
protected:
  std::string name_;
public:
  SubAttribute() {};
  SubAttribute(const std::string &name) : name_(name) {}
  virtual ~SubAttribute() {}
  virtual bool is_meshable() const { return false; }
  void rename(const std::string &nm) { name_ = nm; }
  const std::string &name() const { return name_; }
  virtual bool strictLessThan(const SubAttribute &o) const {
    return name_ < o.name_;
  }
  virtual void print(std::ostream&) const;
};

std::ostream &operator<<(std::ostream&, const SubAttribute&);

class ListAttribute;
typedef void (ListAttribute::*ManipulateListAttribute)(SubAttribute*);

class ListAttribute : public PixelAttribute {
protected:
  // The set is sorted by the default comparison function which
  // compares the pointer addresses of the SubAttribute pointers.
  mutable std::set<SubAttribute*> data;
public:
  ListAttribute() : PixelAttribute() {}
  ListAttribute(const ListAttribute &g) 
  : PixelAttribute(), data(g.data)
  {}
  virtual ListAttribute *clone() const = 0;
  virtual bool operator<(const PixelAttribute&) const = 0;
  bool strictLessThan(const PixelAttribute&) const;
  void add(SubAttribute *group);
  void remove(SubAttribute *group);
  void remove(const std::string &name);
  const std::set<SubAttribute*> &members() const;
  bool contains(const SubAttribute*) const;
  virtual const std::string &displayname() const = 0;
  void print(std::ostream&) const;
  std::vector<std::string> *names();
  static std::vector<std::string> *names(
	 const CMicrostructure *microstructure, int cat,
	 PxlAttributeRegistration *reg);
};

void buildAttributeChangeMap(AttributeVectorMap &avm,
			     ManipulateListAttribute manip, 
			     SubAttribute *sub, PxlAttributeRegistration *reg, 
			     CMicrostructure *microstructure);



#endif	// PIXELATTRIBUTE_H
