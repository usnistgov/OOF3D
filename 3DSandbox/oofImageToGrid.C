// -*- C++ -*-
// $RCSfile: oofImageToGrid.C,v $
// $Revision: 1.1.2.2 $
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

#include "oofImageToGrid.h"

#include <vtkCellData.h>
#include <vtkDoubleArray.h>
#include <vtkImageData.h>
#include <vtkInformation.h>
#include <vtkInformationVector.h>
#include <vtkObjectFactory.h>
#include <vtkPointData.h>
#include <vtkSmartPointer.h>
#include <vtkStreamingDemandDrivenPipeline.h>

vtkCxxRevisionMacro(oofImageToGrid, "$Revision: 1.1.2.2 $");
vtkStandardNewMacro(oofImageToGrid);

oofImageToGrid::oofImageToGrid() {}

void oofImageToGrid::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
  os << indent << "oofImageToGrid" << "\n";
}

int oofImageToGrid::FillInputPortInformation(int port, vtkInformation *info) {
  info->Set(vtkAlgorithm::INPUT_REQUIRED_DATA_TYPE(), "vtkImageData");
}

int oofImageToGrid::RequestInformation(vtkInformation *info,
				       vtkInformationVector **inputVector,
				       vtkInformationVector *outputVector)
{
  this->Superclass::RequestInformation(info, inputVector, outputVector);
  vtkInformation *inInfo = inputVector[0]->GetInformationObject(0);
  vtkInformation *outInfo = outputVector->GetInformationObject(0);

  int extent[6];
  inInfo->Get(vtkStreamingDemandDrivenPipeline::WHOLE_EXTENT(), extent);
  extent[1] += 1;
  extent[3] += 1;
  extent[5] += 1;
  vtkDebugMacro(<< "RequestInformation: extent= "
		<< extent[0] << " " << extent[1] << " "
		<< extent[2] << " " << extent[3] << " "
		<< extent[4] << " " << extent[5]);
  outInfo->Set(vtkStreamingDemandDrivenPipeline::WHOLE_EXTENT(), extent, 6);

  return 1;
}

int oofImageToGrid::RequestUpdateExtent(vtkInformation*,
					vtkInformationVector **inputVector,
					vtkInformationVector *outputVector)
{
  // Set the portion of the input data that will be queried.  This is
  // smaller than the size of the output data, because we've already
  // increased the output extent.  So here we have to decrease it again.
  // TODO: Is there a better way?  This seems to be perverse.
  vtkInformation *inInfo = inputVector[0]->GetInformationObject(0);
  vtkInformation *outInfo = outputVector->GetInformationObject(0);
  int extent[6];
  outInfo->Get(vtkStreamingDemandDrivenPipeline::UPDATE_EXTENT(), extent);
  vtkDebugMacro(<< "RequestUpdateExtent: output grid extent= "
  		<< extent[0] << " " << extent[1] << " "
  		<< extent[2] << " " << extent[3] << " "
  		<< extent[4] << " " << extent[5]);
  extent[1] -= 1;
  extent[3] -= 1;
  extent[5] -= 1;
  inInfo->Set(vtkStreamingDemandDrivenPipeline::UPDATE_EXTENT(), extent, 6);
  return 1;
}

int oofImageToGrid::RequestData(vtkInformation*,
				vtkInformationVector **inputVector,
				vtkInformationVector *outputVector)
{
  vtkImageData *image = vtkImageData::SafeDownCast(this->GetInput());
  vtkRectilinearGrid *output = this->GetOutput();

  vtkDebugMacro(<< "Converting to vtkRectilinearGrid");

  int extent[6];
  image->GetExtent(extent);
  vtkDebugMacro(<< "RequestData: input image extent= "
  		<< extent[0] << " " << extent[1] << " "
  		<< extent[2] << " " << extent[3] << " "
  		<< extent[4] << " " << extent[5]);
  extent[1] += 1;
  extent[3] += 1;
  extent[5] += 1;
  output->SetExtent(extent);
  
  double spacing[3];
  image->GetSpacing(spacing);

  vtkSmartPointer<vtkDoubleArray> xcoords =
    vtkSmartPointer<vtkDoubleArray>::New();
  int nx = extent[1] - extent[0] + 1;
  xcoords->SetNumberOfValues(nx);
  for(vtkIdType i=0; i<=nx; i++)
    xcoords->InsertValue(i, i*spacing[0]);
  output->SetXCoordinates(xcoords);

  vtkSmartPointer<vtkDoubleArray> ycoords =
    vtkSmartPointer<vtkDoubleArray>::New();
  int ny = extent[3] - extent[2] + 1;
  ycoords->SetNumberOfValues(ny);
  for(vtkIdType i=0; i<=ny; i++)
    ycoords->InsertValue(i, i*spacing[1]);
  output->SetYCoordinates(ycoords);

  vtkSmartPointer<vtkDoubleArray> zcoords =
    vtkSmartPointer<vtkDoubleArray>::New();
  int nz = extent[5] - extent[4] + 1;
  zcoords->SetNumberOfValues(nz);
  for(vtkIdType i=0; i<=nz; i++)
    zcoords->InsertValue(i, i*spacing[2]);
  output->SetZCoordinates(zcoords);

  vtkPointData *pointData = image->GetPointData();
  vtkCellData *cellData = output->GetCellData();
  cellData->ShallowCopy(pointData); // is this legal?

  return 1;
}
