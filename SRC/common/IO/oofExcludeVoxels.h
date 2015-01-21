// -*- C++ -*-
// $RCSfile: oofExcludeVoxels.h,v $
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

#ifndef __oofExcludeVoxels_h
#define __oofExcludeVoxels_h

#include <oofconfig.h>

#include <vtkExtractCells.h>

class VoxelFilter;

// vtkAlgorithm that removes cells from a vtkRectilinearGrid,
// converting it to a vtkUnstructuredGrid.  It's derived from and
// basically the same as vtkExtractCells, but uses a callback function
// instead of a vtkIdList to determine which cells to exclude from the
// vtkUnstructuredGrid.  This makes it easier to use in non-vtk code.

class oofExcludeVoxels : public vtkExtractCells {
public:
  vtkTypeRevisionMacro(oofExcludeVoxels, vtkExtractCells);
  void PrintSelf(std::ostream&, vtkIndent);
  static oofExcludeVoxels *New();

  vtkSetMacro(Filter, VoxelFilter*);
  vtkGetMacro(Filter, VoxelFilter*);

protected:
  oofExcludeVoxels();
  virtual int FillInputPortInformation(int, vtkInformation*);
  virtual int RequestData(vtkInformation*, vtkInformationVector**,
			  vtkInformationVector*);
  VoxelFilter *Filter;

private:
  oofExcludeVoxels(const oofExcludeVoxels&); // not implemented
  void operator=(const oofExcludeVoxels&);   // not implemented
};

#endif // __oofExcludeVoxels_h
