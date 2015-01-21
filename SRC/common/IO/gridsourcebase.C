// -*- C++ -*-
// $RCSfile: gridsourcebase.C,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2014/11/24 21:44:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/gridsourcebase.h"
#include "common/IO/oofcerr.h"

vtkCxxRevisionMacro(GridSource, "$Revision: 1.1.2.2 $");

GridSource::GridSource() 
  : PointData(0),
    CellData(0)
{
  this->SetNumberOfInputPorts(0);
  this->SetNumberOfOutputPorts(1);
}

GridSource::~GridSource() {
  if(this->PointData != NULL) {
    this->PointData->UnRegister(this);
  }
  if(this->CellData != NULL) {
    this->CellData->UnRegister(this);
  }
}

int GridSource::RequestData(vtkInformation*,
			    vtkInformationVector**, // input
			    vtkInformationVector *outputVector)
{
  vtkUnstructuredGrid *output = this->GetOutput();
  if(this->GetGrid(output))
    return 1;
  vtkErrorMacro("Error in GetGrid!");
  return 0;
}

void GridSource::PrintSelf(std::ostream &os, vtkIndent indent) {
  this->Superclass::PrintSelf(os, indent);
}

