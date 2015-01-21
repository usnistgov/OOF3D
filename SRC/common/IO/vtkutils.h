// -*- C++ -*-
// $RCSfile: vtkutils.h,v $
// $Revision: 1.1.2.14 $
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

#include <oofconfig.h>

#ifndef VTKUTILS_H
#define VTKUTILS_H

#include "common/coord_i.h"

class CDirection;

#include <vtkCell.h>
#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkIdList.h>
#include <vtkIntArray.h>
#include <vtkLookupTable.h>
#include <vtkPlane.h>
#include <vtkPoints.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

#include <vector>

vtkSmartPointer<vtkDoubleArray> fillDataArray(const std::vector<double>*);
void getDataArrayRange(vtkSmartPointer<vtkDataArray>, double*);
Coord cell2coord(vtkSmartPointer<vtkCell>);

// Typedefs used in swig files.  Each class defined here must also be
// added to vtkutils.swg, where its destructor must be swigged, in
// order for a Python reference to be counted correctly in the
// vtkSmartPointer's bookkeeping.

typedef vtkSmartPointer<vtkCell> vtkCellPtr;
typedef vtkSmartPointer<vtkDataArray> vtkDataArrayPtr;
typedef vtkSmartPointer<vtkDoubleArray> vtkDoubleArrayPtr;
typedef vtkSmartPointer<vtkIdList> vtkIdListPtr;
typedef vtkSmartPointer<vtkIntArray> vtkIntArrayPtr;
typedef vtkSmartPointer<vtkPoints> vtkPointsPtr;
typedef vtkSmartPointer<vtkUnstructuredGrid> vtkUnstructuredGridPtr;
typedef vtkSmartPointer<vtkPlane> vtkPlanePtr;

#endif // VTKUTILS_H
