// -*- C++ -*-
// $RCSfile: rubberband3d.C,v $
// $Revision: 1.1.2.4 $
// $Author: fyc $
// $Date: 2013/04/24 16:00:44 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "rubberband3d.h"
#include <vtkLine.h>
#include <vtkProperty.h>

RubberBand::RubberBand():
  active_(false),
  rubberband(vtkSmartPointer<vtkActor>::New()),
  mapper(vtkSmartPointer<vtkDataSetMapper>::New())
{}

void RubberBand::start(const Coord &pt) {
  startpt = pt;
  current = pt;
  active_ = true;
}

void RubberBand::stop(vtkRenderer *renderer) {
  clear(renderer);
  active_ = false;
}

void RubberBand::clear(vtkRenderer *renderer) {
  if(renderer->GetActors()->IsItemPresent(rubberband))
    renderer->RemoveActor(rubberband);
}

void RubberBand::redraw(vtkRenderer *renderer, const Coord &where) {
  clear(renderer);
  if(active_) {
    current = where;
    draw();	
    renderer->AddActor(rubberband);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SpiderRubberBand::SpiderRubberBand(const std::vector<Coord> *coords)
  : points(vtkSmartPointer<vtkPoints>::New()),
    poly(vtkSmartPointer<vtkPolyData>::New())
{
  int num = coords->size();
  points->Allocate(num+1, num+1);
  points->InsertNextPoint(0,0,0);
  for(std::vector<Coord>::const_iterator it = coords->begin(); it != coords->end(); ++it)
    points->InsertNextPoint((*it)[0], (*it)[1], (*it)[2]);
  poly->Allocate(num, num);
  poly->SetPoints(points);
  for(int i=1; i<num+1; ++i) {
    vtkLine *line = vtkLine::New();
    line->GetPointIds()->SetId(0,i);
    poly->InsertNextCell(line->GetCellType(), line->GetPointIds());
  }
  mapper->SetInput(poly);
}

SpiderRubberBand::~SpiderRubberBand() {}

void SpiderRubberBand::draw() {
  points->SetPoint(0,current[0],current[1],current[2]);
  rubberband = vtkActor::New();
  rubberband->SetMapper(mapper);
  rubberband->GetProperty()->SetRepresentationToWireframe();
  rubberband->GetProperty()->SetColor(0,0,0);
  rubberband->GetProperty()->SetLineWidth(2);
  rubberband->GetProperty()->SetLineStipplePattern(31);
}

