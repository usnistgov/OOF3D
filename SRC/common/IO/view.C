// -*- C++ -*-
// $RCSfile: view.C,v $
// $Revision: 1.1.2.19 $
// $Author: langer $
// $Date: 2014/07/31 18:32:47 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/differ.h"
#include "common/IO/oofcerr.h"
#include "common/IO/view.h"

#include <vtkDoubleArray.h>
#include <vtkPoints.h>

View::View(const Coord *p, const Coord *f, const Coord *u, double a,
	   int sx, int sy)
  : size_x(sx), size_y(sy), pos(*p), focal(*f), up(*u), angle(a),
    vtkplanes(vtkSmartPointer<vtkPlanes>::New()),
    invClip(false), suppressClip(false)
{}

View::View(const Coord &p, const Coord &f, const Coord &u, double a,
	   int sx, int sy)
  : size_x(sx), size_y(sy), pos(p), focal(f), up(u), angle(a),
    vtkplanes(vtkSmartPointer<vtkPlanes>::New()),
    invClip(false), suppressClip(false)
{}

View::View(const View &other)
  : size_x(other.size_x),
    size_y(other.size_y),
    pos(other.pos),
    focal(other.focal),
    up(other.up),
    angle(other.angle),
    vtkplanes(vtkSmartPointer<vtkPlanes>::New()),
    invClip(other.invClip), suppressClip(other.suppressClip)
{
  clipPlanes.reserve(other.clipPlanes.size());
  for(unsigned int i=0; i<other.clipPlanes.size(); i++) {
    clipPlanes.push_back(other.clipPlanes[i]); // makes a copy
  }
  rebuildVtkPlanes();
}

View::~View() {}

bool View::equiv(const View &other) const {
  return (pos == other.pos &&
	  focal == other.focal &&
	  norm2(up - other.up) <= 1.e-12 &&
	  angle == other.angle);
}

bool View::operator==(const View &other) const {
  if(!equiv(other) ||
     size_x != other.size_x ||
     size_y != other.size_y ||
     invClip != other.invClip ||
     suppressClip != other.suppressClip ||
     nClipPlanes() != other.nClipPlanes()) 
    {
// #ifdef DEBUG
//       if(pos != other.pos)
// 	oofcerr << "View::operator==: pos " << pos << " " << other.pos
// 		<< std::endl;
//       if(focal != other.focal)
// 	oofcerr << "View::operator==: focal " << focal << " " << other.focal
// 		<< std::endl;
//       if(norm2(up -other.up) > 1.e-22)
// 	oofcerr << "View::operator==: up " << up << " " << other.up
// 		<< std::endl;
//       if(angle != other.angle)
// 	oofcerr << "View::operator==: angle " << angle << " " << other.angle
// 		<< std::endl;
//       if(invClip != other.invClip)
// 	oofcerr << "View::operator==: invClip " << invClip << other.invClip
// 		<< std::endl;
//       if(nClipPlanes() != other.nClipPlanes())
// 	oofcerr << "View::operator==: nClipPlanes " << nClipPlanes() << " " 
// 		<< other.nClipPlanes() << std::endl;
// #endif // DEBUG
      return false;
    }
  ClippingPlaneList::const_iterator i = clipPlanes.begin();
  ClippingPlaneList::const_iterator j = other.clipPlanes.begin();
  // TODO OPT: When this comparison used to be done in
  // GhostOOFCanvas::set_view_nolock, it sorted the two lists of
  // planes before comparing them (by copying the std::vectors into
  // std::sets).  Is that really necessary?
  while(i != clipPlanes.end()) {
    if(*i != *j) {
      return false;
    }
    ++i;
    ++j;
  }
  return true;
}

void View::setCamera(vtkSmartPointer<vtkCamera> camera) const {
  assert(camera.GetPointer() != 0);
  camera->SetPosition(pos.xpointer());
  camera->SetFocalPoint(focal.xpointer());
  camera->SetViewUp(up.xpointer());
  camera->SetViewAngle(angle);
}

void View::addClipPlane(const ClippingPlane &plane) {
  addClipPlaneWithoutRebuilding(plane);
  rebuildVtkPlanes();
}

void View::addClipPlaneWithoutRebuilding(const ClippingPlane &plane) {
  clipPlanes.push_back(plane);
}

void View::removeClipPlane(unsigned int which) {
  assert(which >= 0 && which < clipPlanes.size());
  clipPlanes.erase(clipPlanes.begin() + which);
  rebuildVtkPlanes();
}

void View::replaceClipPlane(unsigned int which, 
			    ClippingPlane &newPlane)
{
  assert(which >= 0 && which < clipPlanes.size());
  const ClippingPlane &oldPlane = clipPlanes[which];
  if(oldPlane.enabled())
    newPlane.enable();
  else
    newPlane.disable();
  if(oldPlane.flipped())
    newPlane.flip();
  else
    newPlane.unflip();
  clipPlanes[which] = newPlane;
  rebuildVtkPlanes();
}

void View::enableClipPlane(unsigned int which) {
  assert(which >= 0 && which < clipPlanes.size());
  clipPlanes[which].enable();
  rebuildVtkPlanes();
}

void View::disableClipPlane(unsigned int which) {
  assert(which >= 0 && which < clipPlanes.size());
  (*(clipPlanes.begin() + which)).disable();
  rebuildVtkPlanes();
}

bool View::enabledClipPlane(unsigned int which) const {
  assert(which >=0 && which < clipPlanes.size());
  return clipPlanes[which].enabled();
}

void View::flipClipPlane(unsigned int which) {
  assert(which >= 0 && which < clipPlanes.size());
  (*(clipPlanes.begin() + which)).flip();
  rebuildVtkPlanes();
}

void View::unflipClipPlane(unsigned int which) {
  assert(which >= 0 && which < clipPlanes.size());
  (*(clipPlanes.begin() + which)).unflip();
  rebuildVtkPlanes();
}

int View::nClipPlanes() const { 
  return clipPlanes.size();
}

const ClippingPlane &View::getClipPlane(unsigned int i) const {
  return clipPlanes[i];
}

std::ostream &operator<<(std::ostream &os, const View &v) {
  return os << "View("
	    << std::setprecision(20)
	    << v.pos << ", " << v.focal << ", " << v.up << ", " << v.angle
	    << ")";
}

void View::rebuildVtkPlanes() {
  // Convert the OOF-friendly ClippingPlaneList into a vtk-friendly
  // vtkPlanes object.

  // rebuildVtkPlanes is called whenever the View's clipping planes
  // are changed in any way.  It's inefficient to rebuild the whole
  // structure every time, but it's easy and not all that expensive.
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  vtkSmartPointer<vtkDoubleArray> normals =
    vtkSmartPointer<vtkDoubleArray>::New();
  normals->SetNumberOfComponents(3);
  
  for(ClippingPlaneList::const_iterator i=clipPlanes.begin();
      i<clipPlanes.end(); ++i)
    {
      if((*i).enabled()) {
	CUnitVectorDirection nrml((*i).normal()->unitVector());
	const double *dir = nrml.pointer();
	double pt[3];
	for(int j=0; j<3; j++)
	  pt[j] = dir[j]*(*i).offset();
	points->InsertNextPoint(pt);

	if(!(*i).flipped())
	  normals->InsertNextTuple(dir);
	else {
	  double oppdir[3];
	  for(int j=0; j<3; j++)
	    oppdir[j] = -dir[j];
	  normals->InsertNextTuple(oppdir);
	}
      }
    }
  vtkplanes->SetPoints(points);
  vtkplanes->SetNormals(normals);
}

