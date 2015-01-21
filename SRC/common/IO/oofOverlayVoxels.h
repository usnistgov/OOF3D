// -*- C++ -*-
// $RCSfile: oofOverlayVoxels.h,v $
// $Revision: 1.1.2.4 $
// $Author: langer $
// $Date: 2014/12/14 22:49:10 $

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

#include "common/coord_i.h"
#include <vtkRectilinearGridAlgorithm.h>

class PixelSet;

#include <vector>

// vtkAlgorithm that changes the color of certain voxels in a
// vtkRectilinearGrid.  The set of voxels to change is given by an
// OOF3D PixelSet object.  The OOF3D class name "PixelSet" violates
// the VTK coding style standards, so the style in this class is
// rather avant-garde.

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
  // virtual int RequestInformation(vtkInformation*, vtkInformationVector**,
  // 				 vtkInformationVector*);
  virtual int RequestData(vtkInformation*, vtkInformationVector**,
			  vtkInformationVector*);
  double Color[3];
  double Opacity;
  PixelSet *pixelSet;

 private:
  oofOverlayVoxels(const oofOverlayVoxels&); // not implemented
  void operator=(const oofOverlayVoxels&);   // not implemented

  template <class TYPE>
  void _doOverlayVoxels(vtkRectilinearGrid*,
			int, int, const TYPE*, TYPE*,
			const std::vector<ICoord>*,
			const double*, double);
};

#endif // __oofOverlayVoxels_h
