// -*- C++ -*-
// $RCSfile: oofExcludeVoxels.h,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2012/07/25 21:19:45 $

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

#include <vtkExtractCells.h>

class ICoord;

typedef bool (*ExclusionCondition)(const ICoord&);

class oofExcludeVoxels : public vtkExtractCells {
public:
  vtkTypeRevisionMacro(oofExcludeVoxels, vtkExtractCells);
  void PrintSelf(std::ostream&, vtkIndent);
  static oofExcludeVoxels *New();

  vtkSetMacro(Exclude, ExclusionCondition);
  vtkGetMacro(Exclude, ExclusionCondition);

protected:
  oofExcludeVoxels();
  virtual int FillInputPortInformation(int, vtkInformation*);
  virtual int RequestData(vtkInformation*, vtkInformationVector**,
			  vtkInformationVector*);
  ExclusionCondition Exclude;
private:
  oofExcludeVoxels(const oofExcludeVoxels&);
  void operator=(const oofExcludeVoxels&);
};

#endif // __oofExcludeVoxels_h
