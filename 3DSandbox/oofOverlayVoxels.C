// -*- C++ -*-
// $RCSfile: oofOverlayVoxels.C,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2013/11/08 19:36:51 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "oofOverlayVoxels.h"

#include <vtkCellData.h>
#include <vtkObjectFactory.h>
#include <vtkType.h>

#include <limits>

// TODO: Call oofOverlayVoxels::Modified() when the PixelSet is
// modified.  Call oofOverlayVoxels::SetPixelSet(0) when it's
// destroyed.

vtkCxxRevisionMacro(oofOverlayVoxels, "$Revision: 1.1.2.3 $")
vtkStandardNewMacro(oofOverlayVoxels);

oofOverlayVoxels::oofOverlayVoxels()
{
  this->Color[0] = 0.0;
  this->Color[1] = 0.0;
  this->Color[2] = 0.0;
  this->Opacity = 1.0;
  this->pixelSet = 0;
}

void oofOverlayVoxels::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
  os << indent << "Color:";
  for(int i=0; i<3; i++)
    os << " " << this->Color[i];
  os << "\n";
  os << indent << "Opacity: " << this->Opacity;
  os << indent << "PixelSet: " << this->pixelSet;
  if(this->pixelSet != 0)
    os << " (" << this->pixelSet->len() << " voxels)";
  os << "\n";
}

void oofOverlayVoxels::SetPixelSet(PixelSet *pset) {
  this->pixelSet = pset;
  this->Modified();
}

PixelSet *oofOverlayVoxels::GetPixelSet() const {
  return this->pixelSet;
}

template <class TYPE> 
void oofOverlayVoxels::_doOverlayVoxels(vtkRectilinearGrid *input,
					int tupleSize,
					int dataType,
					const TYPE *inData,
					TYPE *outData,
					const std::vector<ICoord> *voxels,
					const double *color,
					double opacity)
{
  const TYPE maxval = ((dataType == VTK_DOUBLE || dataType == VTK_FLOAT) ? 
		       1.0 : std::numeric_limits<TYPE>::max());

  TYPE tint[] = {maxval*color[0], maxval*color[1], maxval*color[2]};

  for(std::vector<ICoord>::const_iterator ijk=voxels->begin();
      ijk!=voxels->end(); ++ijk)
    {
      const int *ijkvals = (*ijk).xpointer();
      // Arggh. vtk doesn't use const args.
      vtkIdType cellID = input->ComputeCellId(const_cast<int*>(ijkvals));
      const TYPE *oldColor = inData + cellID*tupleSize;
      TYPE *newColor = outData + cellID*tupleSize;

      for(int i=0; i<3; i++) {
	newColor[i] = tint[i]*opacity + oldColor[i]*(1-opacity);
      }
    }
}

int oofOverlayVoxels::RequestData(vtkInformation *request,
				  vtkInformationVector **inputVector,
				  vtkInformationVector *outputVector)
{
  vtkRectilinearGrid *input = 
    vtkRectilinearGrid::SafeDownCast(this->GetInput());
  vtkRectilinearGrid *output = 
    vtkRectilinearGrid::SafeDownCast(this->GetOutput());
  output->SetDimensions(input->GetDimensions());
  output->SetXCoordinates(input->GetXCoordinates());
  output->SetYCoordinates(input->GetYCoordinates());
  output->SetZCoordinates(input->GetZCoordinates());
  
  if(this->pixelSet == 0 || this->pixelSet->len() == 0) {
    vtkDebugMacro(<< "Nothing to modify.  Copying cell data shallowly.");
    output->GetCellData()->ShallowCopy(input->GetCellData());
    return 1;
  }

  vtkDebugMacro(<< "Recoloring " << this->pixelSet->len() << " voxels");
  output->GetCellData()->DeepCopy(input->GetCellData());

  vtkDataArray *oScalars = output->GetCellData()->GetScalars();
  vtkDataArray *iScalars = input->GetCellData()->GetScalars();
  int dataType = iScalars->GetDataType();
  int tupleSize = iScalars->GetNumberOfComponents();
  //  vtkDebugMacro(<< "tupleSize=" << tupleSize);

  void *inData = iScalars->GetVoidPointer(0);
  void *outData = oScalars->GetVoidPointer(0);

  const std::vector<ICoord> *voxels = this->pixelSet->members();

  switch(dataType) {
    vtkTemplateMacro(
		     _doOverlayVoxels(input, tupleSize, dataType,
				      static_cast<const VTK_TT*>(inData),
				      static_cast<VTK_TT*>(outData),
				      voxels,
				      this->Color,
				      this->Opacity));
  default:
    vtkGenericWarningMacro("oofOverlayVoxels::RequestData: unknown input type");
  }
  return 1;
}
