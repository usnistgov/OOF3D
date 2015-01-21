// -*- C++ -*-
// $RCSfile: oofOverlayVoxels.h,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2012/07/25 21:19:46 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef __oofOverlayVoxels_h
#define __oofOverlayVoxels_h

#include <vtkRectilinearGridAlgorithm.h>

class ICoord;
class PixelSet;

#include <vector>

class oofOverlayVoxels : public vtkRectilinearGridAlgorithm
{
 public:
  vtkTypeRevisionMacro(oofOverlayVoxels, vtkRectilinearGridAlgorithm);
  void PrintSelf(std::ostream&, vtkIndent);
  static oofOverlayVoxels *New();

  vtkSetVector3Macro(Color, double);
  vtkGetVector3Macro(Color, double);

  vtkSetMacro(Opacity, double);
  vtkGetMacro(Opacity, double);

  void SetPixelSet(PixelSet*);
  PixelSet *GetPixelSet() const;
  
 protected:
  oofOverlayVoxels();
  virtual int RequestData(vtkInformation*, vtkInformationVector**,
			  vtkInformationVector*);
  double Color[3];
  double Opacity;
  PixelSet *pixelSet;

 private:
  oofOverlayVoxels(const oofOverlayVoxels&);
  void operator=(const oofOverlayVoxels&);

  template <class TYPE>
  void _doOverlayVoxels(vtkRectilinearGrid*,
			int, int, const TYPE*, TYPE*,
			const std::vector<ICoord>*,
			const double*, double);
};


//#include "common/pixelgroup.h"

// Dummy ICoord and PixelSet classes for testing.  The real OOF3D
// classes will be used later.

class ICoord {
private:
  int x[3];
public:
  ICoord() {
    x[0] = 0;
    x[1] = 0;
    x[2] = 0;
  }
  ICoord(int x0, int x1, int x2) {
    x[0] = x0;
    x[1] = x1;
    x[2] = x2;
  }
  int operator()(int i) const { return x[i]; }
  int &operator()(int i) { return x[i]; }
  int *xpointer() { return &x[0]; }
  const int *xpointer() const { return &x[0]; }
};
std::ostream &operator<<(std::ostream&, const ICoord&);

class PixelSet {
private:
  std::vector<ICoord> members_;
public:
  PixelSet() {}
  const std::vector<ICoord> *members() { return &members_; }
  void add(ICoord &vxl) { members_.push_back(vxl); }
  int len() const { return members_.size(); }
};

#endif // __oofOverlayVoxels_h
