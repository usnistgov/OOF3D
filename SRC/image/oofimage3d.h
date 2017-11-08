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

#ifndef OOFIMAGE3D_H
#define OOFIMAGE3D_H

#include "common/ccolor.h"
#include "common/colordifference.h"
#include "common/coord_i.h"
#include "common/imagebase.h"
#include "common/timestamp.h"

#include <vtkImageImport.h>
#include <vtkSmartPointer.h>

#include <string>
#include <vector>

class BoolArray;
class CMicrostructure;

/*----------*/

class OOFImage3D : public ImageBase {
protected:
  std::string name_;
  double scale;			// converts from int rgb to doubles in [0,1]
  void getPixelSizeFromImage();
  TimeStamp timestamp;
  CMicrostructure *microstructure;

public:
  OOFImage3D(const std::string &nm);
  OOFImage3D(const std::string &name, const std::vector<std::string> *files,
	     const Coord*);
  virtual ~OOFImage3D();

  const std::string &name() const { return name_; }
  void rename(const std::string &nm) { name_ = nm; }

  ICoord pixelFromPoint(const Coord*) const;
  bool pixelInBounds(const ICoord*) const;

  void setMicrostructure(CMicrostructure *ms) { microstructure = ms; }
  CMicrostructure *getMicrostructure() const { return microstructure; }
  void removeMicrostructure() { microstructure = 0; }

  OOFImage3D *clone(const std::string &name) const;

  void getColorPoints(const CColor &reference,
		      const ColorDifference &diff,
		      BoolArray &selected) const;

  TimeStamp *getTimeStamp() { return &timestamp; }

  void save(const std::string &filepattern, const std::string &format);


  const CColor operator[](const ICoord &c) const;
  // Version taking ICoord* arg is provided for use in SWIG typemaps.
  const CColor operator[](const ICoord *c) const { return operator[](*c); }

  bool compare(const OOFImage3D&, double) const;

  std::vector<unsigned char> *getPixels();
  
  void imageChanged();		// call this when done setting pixels.
  
  void gray();
  void threshold(double T);
  void blur(double radius, double sigma);
  void dim(double factor);
  void fade(double factor);
  void negate(double dummy);
  void medianFilter(int radius);
  void normalize();
  void contrast(double factor);
  void flip(const std::string &axis);
  void permuteAxes(const std::string&);

};

// OOFImage3DFromData needs to be a separate class so that it can hold
// on to a reference to the vtkImageImport object, which stores the
// only copy of the data.  It used to just be a separate constructor
// for OOFImage3D, but that stopped working with vtk 7 (or at least
// was noticed not to work when switching to vtk 7).

class OOFImage3DFromData : public OOFImage3D {
private:
  vtkSmartPointer<vtkImageImport> importer;
public:
  OOFImage3DFromData(const std::string &name, 
		     const Coord &size, const ICoord &isize,
		     const std::vector<unsigned char> *data);
  ~OOFImage3DFromData() {}
};

OOFImage3D *newImageFromData(const std::string &name,
			     const Coord *size,
			     const ICoord *isize,
			     const std::vector<unsigned char> *data);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


#endif // OOFIMAGE3D_H
