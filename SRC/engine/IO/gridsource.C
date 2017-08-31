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

#include "common/IO/oofcerr.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/femesh.h"
#include "engine/skeletonfilter.h"
#include "engine/IO/gridsource.h"

#include <vtkCellData.h>
#include <vtkObjectFactory.h>
#include <vtkPointData.h>

// TODO: We need to have different kinds of GridSources for different
// kinds of cells: tets, faces, edges, & nodes.  Then each of those
// can have its own kind of SkeletonFilter.  Some DisplayMethods will
// use more than one GridSource and more than one vtk pipeline.  The
// SkeletonEdgeDisplay will use and EdgeSource and a TetSource, so
// that Tets can be selected, for example.  This should be done only
// after moving to vtk6 or vtk7.

vtkCxxRevisionMacro(SkeletonGridSource, "oofvtkmods 3.0.0");
vtkCxxRevisionMacro(MeshGridSource, "oofvtkmods 3.0.0");

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
    Filter(&defaultFilter),
    time(0.)
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef DEBUG

// SkeletonSegmentGridSource is just in DEBUG because doing it right
// involves some changes to our vtk scheme, which ought to be done
// only after migrating from vtk5 to vtk6 or vtk7 or vtk8.  For now,
// it's just being used to compare Skeleton reference files in the
// regression suite when testing the r3d categoryVolumes code.

vtkCxxRevisionMacro(SkeletonSegmentGridSource, "oofvtkmods 3.0.0");
vtkStandardNewMacro(SkeletonSegmentGridSource);

SkeletonSegmentGridSource::SkeletonSegmentGridSource()
  : skeleton(0),
    Filter(&defaultFilter)
{}

bool SkeletonSegmentGridSource::GetGrid(vtkUnstructuredGrid *grid) {
  if(!this->skeleton)
    return false;
  this->skeleton->getVtkSegments(this->Filter, grid);
  if(this->PointData)
    grid->GetPointData()->SetScalars(this->PointData);
  if(this->CellData)
    grid->GetCellData()->SetScalars(this->CellData);
  return true;
}

vtkSmartPointer<SkeletonSegmentGridSource> newSkeletonSegmentGridSource() {
  return vtkSmartPointer<SkeletonSegmentGridSource>::New();
}

void SkeletonSegmentGridSource::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
  os << indent << "SkeletonSegmentGridSource: skeleton = "
     << this->skeleton << "\n";
  os << indent << "SkeletonSegmentGridSource: filter = " << this->Filter
     << "\n";
}

vtkCxxRevisionMacro(SkeletonEdgeDiffGridSource, "oofvtkmods 3.0.0");
vtkStandardNewMacro(SkeletonEdgeDiffGridSource);

SkeletonEdgeDiffGridSource::SkeletonEdgeDiffGridSource()
  : skeleton(0),
    other(0)
{}

bool SkeletonEdgeDiffGridSource::GetGrid(vtkUnstructuredGrid *grid) {
  if(!this->skeleton || !this->other)
    return false;
  // Get segments that are in this but not in other.
  this->skeleton->getExtraVtkSegments(this->other, grid);
  return true;
}

vtkSmartPointer<SkeletonEdgeDiffGridSource> newSkeletonEdgeDiffGridSource() {
  return vtkSmartPointer<SkeletonEdgeDiffGridSource>::New();
}

void SkeletonEdgeDiffGridSource::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
  os << indent << "SkeletonEdgeDiffGridSource: skeleton = "
     << this->skeleton << "\n";
  os << indent << "SkeletonEdgeDiffGridSource: other = " << this->other
     << "\n";
}

#endif // DEBUG
