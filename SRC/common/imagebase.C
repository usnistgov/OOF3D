// -*- C++ -*-
// $RCSfile: imagebase.C,v $
// $Revision: 1.1.2.25 $
// $Author: langer $
// $Date: 2014/12/14 22:49:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/oofcerr.h"
#include "common/imagebase.h"
#include "common/ooferror.h"

#include <vtkImageAppendComponents.h>
#include <vtkImageChangeInformation.h>
#include <vtkImageExtractComponents.h>


void ImageBase::setSize(const Coord *sighs) {
  size_ = *sighs;
  if(sizeInPixels_ != size_) {
    // We need to change the data spacing of the image object
    double x_spacing = size_[0]/(double)sizeInPixels_[0];
    double y_spacing = size_[1]/(double)sizeInPixels_[1];
    double z_spacing = size_[2]/(double)sizeInPixels_[2];

    if (!(x_spacing && y_spacing && z_spacing)) 
      throw ErrProgrammingError("Zero image spacing not allowed",
				__FILE__, __LINE__);

    vtkSmartPointer<vtkImageChangeInformation> changer
      = vtkSmartPointer<vtkImageChangeInformation>::New();
    changer->SetInputConnection(image->GetProducerPort());
    changer->SetOutputSpacing(x_spacing, y_spacing, z_spacing);
    image = changer->GetOutput();
  }	
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Filters.  These are static class methods.

// static
vtkSmartPointer<vtkImageData> ImageBase::getRGB(
					 vtkSmartPointer<vtkImageData> input) 
{
  // Get a 3 channel RGB image from image of 1, 2, 3, or 4 channels.

  int numcomponents = input->GetNumberOfScalarComponents();
  if(numcomponents == 3) 
    return input;

  vtkSmartPointer<vtkImageAppendComponents> appender = 
    vtkSmartPointer<vtkImageAppendComponents>::New();
  vtkSmartPointer<vtkImageExtractComponents> extractor = 
    vtkSmartPointer<vtkImageExtractComponents>::New();
  vtkSmartPointer<vtkImageData> result;

  switch(numcomponents) {
  case 1:
    for(int i=0; i<3; i++)
      appender->AddInputConnection(input->GetProducerPort());
    result = appender->GetOutput();
    break;
  case 2:
    extractor->SetInputConnection(input->GetProducerPort());
    extractor->SetComponents(0);
    for(int i=0; i<3; i++) 
      appender->AddInputConnection(extractor->GetOutputPort());
    result = appender->GetOutput();
    break;
  case 4:
    extractor->SetInputConnection(input->GetProducerPort());
    extractor->SetComponents(0,1,2);
    result = extractor->GetOutput();
    break;
  default:
    throw ErrProgrammingError("Bad number of image components",
			      __FILE__, __LINE__);
  }
  return result;
}

// // static
// vtkSmartPointer<vtkImageData> ImageBase::getRGBA(
// 					  vtkSmartPointer<vtkImageData> input)
// {
//   // get a 4 channel RGB image from image of 1,2,3,or 4 channels
//   // and set the fourth channel to 0 (representing total opacity)
//   int numcomponents = input->GetNumberOfScalarComponents();
//   vtkSmartPointer<vtkImageAppendComponents> appender = 
//     vtkSmartPointer<vtkImageAppendComponents>::New();
//   vtkSmartPointer<vtkImageData> result;
//   switch(numcomponents) {
//   case 1:
//     for(int i=0; i<4; i++) 
//       appender->AddInput(input);
//     result = appender->GetOutput();
//     break;
//   case 2:
//     {
//       vtkSmartPointer<vtkImageExtractComponents> extractor = 
// 	vtkSmartPointer<vtkImageExtractComponents>::New();
//       extractor->SetInputConnection(input->GetProducerPort());
//       extractor->SetComponents(0);
//       for(int i=0; i<4; i++)
// 	appender->AddInput(extractor->GetOutput());
//       result = appender->GetOutput();
//     }
//     break;
//   case 3:
//     {
//       vtkSmartPointer<vtkImageData> alpha =
//     	vtkSmartPointer<vtkImageData>::New();
//       alpha->SetExtent(input->GetExtent());
//       alpha->SetScalarTypeToUnsignedChar();
//       alpha->SetNumberOfScalarComponents(1);
//       alpha->AllocateScalars();
//       appender->AddInputConnection(input->GetProducerPort());
//       appender->AddInputConnection(alpha->GetProducerPort());
//       result = appender->GetOutput();
//     }
//     break;
//   case 4:
//     result = input;
//     break;
//   default:
//     throw ErrProgrammingError("Bad number of image components",
// 			      __FILE__, __LINE__);
//   }

//   result->Update();
//   result->GetPointData()->GetScalars()->FillComponent(3, 255);
//   return result;
// }
