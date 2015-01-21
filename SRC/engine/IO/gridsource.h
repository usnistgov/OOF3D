// -*- C++ -*-
// $RCSfile: gridsource.h,v $
// $Revision: 1.1.2.7 $
// $Author: langer $
// $Date: 2014/03/14 21:14:43 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// vtkAlgorithms that create the vtkUnstructuredGrids for OOF
// Skeletons and Meshes.

#ifndef GRIDSOURCE_H

#include <oofconfig.h>
#include "common/IO/gridsourcebase.h" // defines GridSource

class CSkeletonBase; 
class FEMesh;
class SkeletonFilter;

#include <vtkSmartPointer.h>

class SkelMeshSource : public GridSource {
public:
virtual void Setskeleton(CSkeletonBase*) = 0;
};

class SkeletonGridSource : public SkelMeshSource {
public:
  vtkTypeRevisionMacro(SkeletonGridSource, SkelMeshSource);
  void PrintSelf(std::ostream&, vtkIndent);
  static SkeletonGridSource *New();
  
  vtkSetMacro(skeleton, CSkeletonBase*);
  vtkGetMacro(skeleton, CSkeletonBase*);
  vtkSetMacro(Filter, SkeletonFilter*);
  vtkGetMacro(Filter, SkeletonFilter*);
protected:
  SkeletonGridSource();
  virtual ~SkeletonGridSource() {}
  CSkeletonBase *skeleton;
  // Filter is defined in the derived classes instead of in GridSource
  // because Skeletons and Meshes will probably need different types
  // of Filter eventually.
  SkeletonFilter *Filter;
  virtual bool GetGrid(vtkUnstructuredGrid*);
private:
  SkeletonGridSource(const SkeletonGridSource&); // not implemented
  void operator=(const SkeletonGridSource&);	 // not implemented
};

class MeshGridSource : public SkelMeshSource {
public:
  vtkTypeRevisionMacro(MeshGridSource, SkelMeshSource);
  void PrintSelf(std::ostream&, vtkIndent);
  static MeshGridSource *New();
  
  vtkSetMacro(mesh, FEMesh*);
  vtkGetMacro(mesh, FEMesh*);
  vtkSetMacro(skeleton, CSkeletonBase*);
  vtkGetMacro(skeleton, CSkeletonBase*);
  vtkSetMacro(Enhancement, double);
  vtkGetMacro(Enhancement, double);
  vtkSetMacro(Filter, SkeletonFilter*);
  vtkGetMacro(Filter, SkeletonFilter*);
  vtkSetMacro(time, double);
protected:
  MeshGridSource();
  virtual ~MeshGridSource() {}
  CSkeletonBase *skeleton;
  FEMesh *mesh;
  double Enhancement;
  SkeletonFilter *Filter;
  double time;
  virtual bool GetGrid(vtkUnstructuredGrid*);
private:
  MeshGridSource(const MeshGridSource&); // not implemented
  void operator=(const MeshGridSource&); // not implemented
};

// These are used when creating the GridSources in python.
vtkSmartPointer<SkeletonGridSource> newSkeletonGridSource();
vtkSmartPointer<MeshGridSource> newMeshGridSource();

// Typedefs used in swig files.
typedef vtkSmartPointer<SkeletonGridSource> SkeletonGridSourcePtr;
typedef vtkSmartPointer<MeshGridSource> MeshGridSourcePtr;

#endif // GRIDSOURCE_H
