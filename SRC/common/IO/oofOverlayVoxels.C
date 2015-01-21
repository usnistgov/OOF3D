// -*- C++ -*-
// $RCSfile: oofOverlayVoxels.C,v $
// $Revision: 1.1.2.7 $
// $Author: langer $
// $Date: 2014/08/23 15:53:27 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/oofcerr.h"
#include "common/IO/oofOverlayVoxels.h"
#include "common/coord.h"
#include "common/pixelgroup.h"

// vtkAlgorithm that changes the color of certain voxels in a
// vtkRectilinearGrid.  The set of voxels to change is given by an
// OOF3D PixelSet object, which contains the ICoords defining the
// voxels to be recolored.  (The OOF3D class names "PixelSet" and
// "ICoord" violate the VTK coding style standards, so the style in
// this class is rather avant garde.)


#include <vtkCellData.h>
#include <vtkInformation.h>
#include <vtkInformationVector.h>
#include <vtkObjectFactory.h>
#include <vtkStreamingDemandDrivenPipeline.h>
#include <vtkType.h>

#include <limits>

vtkCxxRevisionMacro(oofOverlayVoxels, "$Revision: 1.1.2.7 $")
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

// int oofOverlayVoxels::RequestInformation(vtkInformation *info,
// 					 vtkInformationVector **inputVector,
// 					 vtkInformationVector *outputVector)
// {
//   this->Superclass::RequestInformation(info, inputVector, outputVector);
//   vtkInformation *inInfo = inputVector[0]->GetInformationObject(0);
//   vtkInformation *outInfo = outputVector->GetInformationObject(0);
//   int extent[6];
//   inInfo->Get(vtkStreamingDemandDrivenPipeline::WHOLE_EXTENT(), extent);
//   outInfo->Set(vtkStreamingDemandDrivenPipeline::WHOLE_EXTENT(), extent, 6);

//   oofcerr << "oofOverlayVoxels::RequestInformation: " << this << " extent=";
//   for(int i=0; i<6; i++) oofcerr << " " << extent[i];
//   oofcerr << std::endl;

//   return 1;
// }

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
      
      // TODO OPT: This assumes that the image has three channels,
      // which is a good assumption only as long as we convert all
      // images to RGB.  See the TODO OPT in the OOFImage3D
      // constructor.
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
