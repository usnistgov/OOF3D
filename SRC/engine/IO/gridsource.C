// -*- C++ -*-
// $RCSfile: gridsource.C,v $
// $Revision: 1.1.2.15 $
// $Author: langer $
// $Date: 2014/12/14 01:07:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/oofcerr.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/femesh.h"
#include "engine/skeletonfilter.h"
#include "engine/IO/gridsource.h"

#include <vtkCellData.h>
#include <vtkObjectFactory.h>
#include <vtkPointData.h>

vtkCxxRevisionMacro(SkeletonGridSource, "$Revision: 1.1.2.15 $");
vtkCxxRevisionMacro(MeshGridSource, "$Revision: 1.1.2.15 $");

vtkStandardNewMacro(SkeletonGridSource);
vtkStandardNewMacro(MeshGridSource);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

NullFilter defaultFilter;

SkeletonGridSource::SkeletonGridSource()
  : skeleton(0),
    Filter(&defaultFilter)
{}

MeshGridSource::MeshGridSource() 
  : skeleton(),
    mesh(0),
    Enhancement(0.),
    Filter(&defaultFilter)
{}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool SkeletonGridSource::GetGrid(vtkUnstructuredGrid *grid)
{
  if(!this->skeleton)
    return false;
  this->skeleton->getVtkCells(this->Filter, grid);
  if(this->PointData) {
    grid->GetPointData()->SetScalars(this->PointData);
  }
  if(this->CellData) {
    grid->GetCellData()->SetScalars(this->CellData);
  }
  return true;
}

bool MeshGridSource::GetGrid(vtkUnstructuredGrid *grid) {
  // TODO 3.1: How often is this called during plotting?  It looks
  // like we're spending 100% of the time in restoreCachedData when
  // drawing a large contour plot.
  if(!this->mesh)
    return false;
  this->mesh->restoreCachedData(this->time);
  try {
    this->mesh->getGrid(this->Enhancement, this->skeleton, this->Filter, grid);
    if(this->PointData) {
      grid->GetPointData()->SetScalars(this->PointData);
    }
    // TODO: Also handle cell data?  Do we ever have cell data for
    // Meshes?
  }
  catch (...) {
    this->mesh->releaseCachedData();
    return false;
  }
  this->mesh->releaseCachedData();
  return true;
}

vtkSmartPointer<SkeletonGridSource> newSkeletonGridSource() {
  return vtkSmartPointer<SkeletonGridSource>::New();
}

vtkSmartPointer<MeshGridSource> newMeshGridSource() {
  return vtkSmartPointer<MeshGridSource>::New();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void SkeletonGridSource::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
  os << indent << "SkeletonGridSource: skeleton = " << this->skeleton << "\n";
  os << indent << "SkeletonGridSource: filter = " << this->Filter << "\n";
}

void MeshGridSource::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
  os << indent << "MeshGridSource: mesh = " << this->mesh << "\n";
  os << indent << "MeshGridSource: skeleton = " << this->skeleton << "\n";
  os << indent << "MeshGridSource: enhancement = " << this->Enhancement << "\n";
  os << indent << "MeshGridSource: filter = " << this->Filter << "\n";
}

