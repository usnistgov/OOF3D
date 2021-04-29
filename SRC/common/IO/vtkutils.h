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

#ifndef VTKUTILS_H
#define VTKUTILS_H

#include "common/coord_i.h"

class CDirection;

#include <vtkActor.h>
#include <vtkActorCollection.h>
#include <vtkCell.h>
#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkIdList.h>
#include <vtkIntArray.h>
#include <vtkLookupTable.h>
#include <vtkPlane.h>
#include <vtkPoints.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

#include <vector>

void initialize_vtk();
void initialize_X11();

vtkSmartPointer<vtkDoubleArray> fillDataArray(const std::vector<double>*);
void getDataArrayRange(vtkSmartPointer<vtkDataArray>, double*);
Coord cell2coord(vtkSmartPointer<vtkCell>);

// Typedefs used in swig files.  Each class defined here must also be
// added to vtkutils.swg, where its destructor must be swigged, in
// order for a Python reference to be counted correctly in the
// vtkSmartPointer's bookkeeping.

typedef vtkSmartPointer<vtkActor> vtkActorPtr;
typedef vtkSmartPointer<vtkActorCollection> vtkActorCollectionPtr;
typedef vtkSmartPointer<vtkCell> vtkCellPtr;
typedef vtkSmartPointer<vtkDataArray> vtkDataArrayPtr;
typedef vtkSmartPointer<vtkDoubleArray> vtkDoubleArrayPtr;
typedef vtkSmartPointer<vtkIdList> vtkIdListPtr;
typedef vtkSmartPointer<vtkIntArray> vtkIntArrayPtr;
typedef vtkSmartPointer<vtkPoints> vtkPointsPtr;
typedef vtkSmartPointer<vtkRenderer> vtkRendererPtr;
typedef vtkSmartPointer<vtkUnstructuredGrid> vtkUnstructuredGridPtr;
typedef vtkSmartPointer<vtkPlane> vtkPlanePtr;

// For some functions that returned int* in vtk8 and vtkIdType in vtk9.
#if VTK_MAJOR_VERSION < 9
#define IDTYPE int
#else
#define IDTYPE vtkIdType
#endif 

#endif // VTKUTILS_H
