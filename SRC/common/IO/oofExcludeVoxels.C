// -*- C++ -*-
// $RCSfile: oofExcludeVoxels.C,v $
// $Revision: 1.1.2.7 $
// $Author: fyc $
// $Date: 2014/07/17 15:37:58 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/oofExcludeVoxels.h"
#include "common/IO/oofcerr.h"
#include "common/coord.h"
#include "common/voxelfilter.h"

#include <vtkIdList.h>
#include <vtkInformation.h>
#include <vtkObjectFactory.h>
#include <vtkRectilinearGrid.h>

vtkCxxRevisionMacro(oofExcludeVoxels, "$Revision: 1.1.2.7 $");
vtkStandardNewMacro(oofExcludeVoxels);

oofExcludeVoxels::oofExcludeVoxels() {
  this->Filter = 0;
}

void oofExcludeVoxels::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
  os << indent << "Filter: " << this->Filter << "\n";
}

int oofExcludeVoxels::FillInputPortInformation(int port, vtkInformation *info) {
  this->Superclass::FillInputPortInformation(port, info);
  info->Set(vtkAlgorithm::INPUT_REQUIRED_DATA_TYPE(), "vtkRectilinearGrid");
  return 1;
}

int oofExcludeVoxels::RequestData(vtkInformation *info,
				   vtkInformationVector **inputVector,
				   vtkInformationVector *outputVector)
{
  vtkDebugMacro(<< "Excluding");
  vtkRectilinearGrid *input =
    vtkRectilinearGrid::SafeDownCast(this->GetInput());

  // TODO OPT: It's inefficient to construct the list of cells.  Override
  // the routines that use the list so that they can use the Exclude
  // function directly.
  
  // Create list of cells to include.
  vtkIdList *inclusions = vtkIdList::New();
  // Loop over cells in the input
  int extent[6];
  input->GetExtent(extent);
  if(!this->Filter->precompute()) {
    oofcerr << "oofExcludeVoxels::RequestData: Filter=" << this->Filter
	    << " " << this->Filter->classname() << std::endl;
    vtkErrorMacro("Precompute failed for filter!");
  }
  for(int z=extent[4]; z<extent[5]; z++) {
    for(int y=extent[2]; y<extent[3]; y++) {
      for(int x=extent[0]; x<extent[1]; x++) {
	ICoord where(x, y, z);
	// Should this cell be included?
	if(this->Filter->includeVoxel(where)) {
	  const int *ijk = where.xpointer();
	  vtkIdType cellID = input->ComputeCellId(const_cast<int*>(ijk));
	  inclusions->InsertNextId(cellID);
	}
      }
    }
  }
  this->Filter->postcompute();
  vtkDebugMacro(<< "Including " << inclusions->GetNumberOfIds() << " cells");
  this->SetCellList(inclusions);
  inclusions->Delete();
  return this->Superclass::RequestData(info, inputVector, outputVector);
}
