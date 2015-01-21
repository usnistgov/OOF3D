// -*- C++ -*-
// $RCSfile: oofcanvas3d.swg,v $
// $Revision: 1.1.2.7 $
// $Author: langer $
// $Date: 2011/09/14 18:49:44 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef OOFCANVAS3D_SWG
#define OOFCANVAS3D_SWG

%module oofcanvas3d
%include "common/typemaps.swg"
%extern "common/IO/ghostoofcanvas.swg"
%{
#include "common/IO/ghostoofcanvas.h"
#include "common/IO/GUI/oofcanvas3d.h"
#include "common/IO/GUI/rubberband3d.h"
  //#include "vtkPythonUtil.h"
#include "vtkUnstructuredGrid.h"
%}

%pragma(python) code="from ooflib.SWIG.common.IO.ghostoofcanvas import GhostOOFCanvasPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.GUI.rubberband3d import RubberBandPtr"

class OOFCanvas3D : public GhostOOFCanvas {
public:
  OOFCanvas3D();
  PyObject *widget();

  void set_mouse_callback(PyObject *pythonCallable);

  void show();

  void mouse_tumble(double x, double y);
  void mouse_track(double x, double y);
  void mouse_dolly(double x, double y);

  void set_rubberband(RubberBand*);

};




#endif


