// -*- C++ -*-
// $RCSfile: gridsourcebase.h,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2014/11/24 22:30:36 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GRIDSOURCEBASE_H
#define GRIDSOURCEBASE_H

#include <oofconfig.h>

#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkObjectFactory.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGridAlgorithm.h>

class GridSource : public vtkUnstructuredGridAlgorithm {
public:
  vtkTypeRevisionMacro(GridSource, vtkUnstructuredGridAlgorithm);
  void PrintSelf(std::ostream&, vtkIndent);
  vtkSetObjectMacro(PointData, vtkDoubleArray);
  vtkSetObjectMacro(CellData, vtkDataArray);
protected:
  GridSource();
  virtual ~GridSource();
  virtual int FillInputPortInformation(int, vtkInformation*) { return 1; }
  virtual int RequestData(vtkInformation*, vtkInformationVector**,
			  vtkInformationVector*);
  virtual bool GetGrid(vtkUnstructuredGrid*) = 0;
  vtkDoubleArray *PointData;
  vtkDataArray *CellData;
private:
  GridSource(const GridSource&);     // not implemented
  void operator=(const GridSource&); // not implemented
};

typedef vtkSmartPointer<GridSource> GridSourcePtr;

#endif // GRIDSOURCEBASE_H
