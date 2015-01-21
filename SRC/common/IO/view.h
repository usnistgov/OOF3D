// -*- C++ -*-
// $RCSfile: view.h,v $
// $Revision: 1.1.2.14 $
// $Author: langer $
// $Date: 2014/07/31 18:32:48 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef VIEW_H
#define VIEW_H

#include "common/clip.h"
#include "common/coord.h"
#include "common/direction.h"

#include <vtkCamera.h>
#include <vtkPlanes.h>
#include <vtkSmartPointer.h>

class View {
public:
  int size_x, size_y;		// viewport size
  Coord pos;			// camera position
  Coord focal;			// camera focal point
  Coord up;			// camera view up vector
  double angle;			// camera view angle
  ClippingPlaneList clipPlanes;	// vector of ClippingPlanes
  vtkSmartPointer<vtkPlanes> vtkplanes;
  bool invClip;			// globally invert clipping
  bool suppressClip;		// globally suppress clipping
  
  View(const Coord *p, const Coord *f, const Coord *u, double a, int, int);
  View(const Coord &p, const Coord &f, const Coord &u, double a, int, int);
  View(const View&);
  ~View();
  void setCamera(vtkSmartPointer<vtkCamera>) const;
  void addClipPlane(const ClippingPlane&);
  void addClipPlaneWithoutRebuilding(const ClippingPlane&);
  void removeClipPlane(unsigned int);
  void replaceClipPlane(unsigned int, ClippingPlane&);
  void enableClipPlane(unsigned int);
  void disableClipPlane(unsigned int);
  bool enabledClipPlane(unsigned int) const;
  void flipClipPlane(unsigned int);
  void unflipClipPlane(unsigned int);
  void invertClipOn() { invClip = true; }
  void invertClipOff() { invClip = false; }
  bool invertedClip() const { return invClip; }
  void suppressClipOn() { suppressClip = true; }
  void suppressClipOff() { suppressClip = false; }
  bool suppressedClip() const { return suppressClip; }
  int nClipPlanes() const;
  const ClippingPlane &getClipPlane(unsigned int) const;
  bool operator==(const View &) const;
  bool equiv(const View &) const; // equal, except for clip planes

  void rebuildVtkPlanes();
};

std::ostream &operator<<(std::ostream&, const View&);

#endif // VIEW_H
