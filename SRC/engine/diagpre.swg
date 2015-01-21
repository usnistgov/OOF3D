// -*- C++ -*-
// $RCSfile: diagpre.swg,v $
// $Revision: 1.2.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:41 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DIAGPRE_SWG
#define DIAGPRE_SWG

%module diagpre

%include "engine/typemaps.swg"
%extern "engine/preconditioner.swg"
%extern "engine/sparsemat.swg"

%pragma(python) code="from ooflib.SWIG.engine.preconditioner import PreconditionerBasePtr"
%pragma(python) code="from ooflib.SWIG.engine.sparsemat import SparseMatPtr"

%{
#include "engine/diagpre.h"
%}

class DiagPreconditionerCore : public PreconditionerBase {
public:
  DiagPreconditionerCore(SparseMat&);
};

#endif // DIAGPRE_SWG
