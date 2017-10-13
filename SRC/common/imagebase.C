// -*- C++ -*-

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
    changer->SetInputData(image);
    changer->SetOutputSpacing(x_spacing, y_spacing, z_spacing);
    image = changer->GetOutput();
  }	
}
