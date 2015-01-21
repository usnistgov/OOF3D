// -*- C++ -*-
// $RCSfile: bdyanalysis.swg,v $
// $Revision: 1.5.4.3 $
// $Author: langer $
// $Date: 2014/03/24 21:09:23 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BDYANALYSIS_SWG
#define BDYANALYSIS_SWG

#include <oofconfig.h>

%module bdyanalysis

%include "engine/typemaps.swg"
%{
#include "engine/edgeset.h"
#include "engine/bdyanalysis.h"
%}

%extern "engine/outputval.swg"
%pragma(python) code="from ooflib.SWIG.engine.outputval import OutputValuePtr"

OutputValue integrateFlux(FEMesh*, Flux*, SubDimensionalSet*);
OutputValue averageField(FEMesh*, Field*, SubDimensionalSet*);

#endif // BDYANALYSIS_SWG
