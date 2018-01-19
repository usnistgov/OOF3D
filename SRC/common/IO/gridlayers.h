// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GRIDLAYERS_H
#define GRIDLAYERS_H

#include <oofconfig.h>

#include "common/IO/canvaslayers.h"

#include "common/IO/oofCellLocator.h"

#include <vtkAbstractCellLocator.h>
#include <vtkBandedPolyDataContourFilter.h>
#include <vtkDataArray.h>
#include <vtkGeometryFilter.h>
#include <vtkPolyDataMapper.h>
#include <vtkRenderer.h>
#include <vtkScalarBarActor.h>
#include <vtkSmartPointer.h>

class GridSource;

// WireGridCanvasLayer draws the wire-frame representation of a grid
// of 3D cells.  To draw a grid of 1D cells, use
// SegmentGridCanvasLayer

class WireGridCanvasLayer : public OOFCanvasLayer {
protected:
  vtkSmartPointer<GridSource> gridsource;
  vtkSmartPointer<vtkActor> edgeActor;
  vtkSmartPointer<vtkActor> faceActor;
  vtkSmartPointer<vtkDataSetMapper> edgeMapper;
  vtkSmartPointer<vtkDataSetMapper> faceMapper;
  vtkSmartPointer<oofCellLocator> locator;
  vtkSmartPointer<vtkExtractEdges> edgeExtractor;
  vtkSmartPointer<vtkTableBasedClipDataSet> edgeClipper;
  vtkSmartPointer<vtkTableBasedClipDataSet> faceClipper;
  // For drawing the cut surface.  These aren't instantiated unless
  // the layer is clipped.
  vtkSmartPointer<vtkActor> cutActor;
  vtkSmartPointer<vtkDataSetMapper> cutMapper;
public:
  WireGridCanvasLayer(GhostOOFCanvas*, const std::string&,
		      vtkSmartPointer<GridSource>);
  ~WireGridCanvasLayer();
  virtual const std::string &classname() const;
  virtual void setModified();
  virtual int nVTKProps() const;
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
  void set_color(const CColor &lineColor);
  void set_lineWidth(int lineWidth);
  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
  virtual vtkSmartPointer<vtkPoints> get_pickable_points();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();

  vtkSmartPointer<GridSource> source() { return gridsource; }
  virtual bool visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
				  CRectangularPrism*) const;
};

// SegmentGridCanvasLayer displays a grid of line segments.  To
// display the edges of a grid of 3D cells, use WireGridCanvasLayer.

class SegmentGridCanvasLayer : public OOFCanvasLayer {
protected:
  vtkSmartPointer<GridSource> gridsource;
  vtkSmartPointer<vtkActor> edgeActor;
  vtkSmartPointer<vtkDataSetMapper> edgeMapper;
  // vtkSmartPointer<oofCellLocator> locator;
  vtkSmartPointer<vtkTableBasedClipDataSet> edgeClipper;
public:
  // TODO: Should the ctor arg be a SkeletonSegmentGridSource or
  // SegmentGridSource instead of a generic GridSource?
  SegmentGridCanvasLayer(GhostOOFCanvas*, const std::string&,
			 vtkSmartPointer<GridSource>);
  ~SegmentGridCanvasLayer();
  virtual const std::string &classname() const;
  virtual void setModified();
  virtual int nVTKProps() const { return 1; }
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
  void set_color(const CColor &lineColor);
  void set_lineWidth(int lineWidth);
  // virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  // virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
  // virtual vtkSmartPointer<vtkPoints> get_pickable_points();
  // virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();

  vtkSmartPointer<GridSource> source() { return gridsource; }
  virtual bool visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
				  CRectangularPrism*) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FilledGridCanvasLayer : public OOFCanvasLayer {
protected:
  vtkSmartPointer<GridSource> gridsource;
  vtkSmartPointer<vtkActor> actor;
  vtkSmartPointer<vtkDataSetMapper> mapper;
  vtkSmartPointer<vtkCellLocator> locator;
  vtkSmartPointer<vtkTableBasedClipDataSet> clipper;
  vtkSmartPointer<vtkLookupTable> lut;
  double vmin, vmax;		// min and max values to be plotted via lut
public:
  FilledGridCanvasLayer(GhostOOFCanvas*, const std::string&,
			vtkSmartPointer<GridSource>);
  ~FilledGridCanvasLayer();
  virtual const std::string &classname() const;
  virtual void setModified();
  virtual int nVTKProps() const { return 1; }

  // Colormap methods are defined to be virtual just in case a
  // subclass needs to override them.  They're not defined in general
  // OOFCanvasLayers, only in FilledGridCanvasLayer and its
  // subclasses.
  virtual void set_lookupTable(vtkSmartPointer<vtkLookupTable>, double, double);
  virtual vtkScalarsToColors *get_lookupTable();
  virtual double minval() const { return vmin; }
  virtual double maxval() const { return vmax; }

  virtual void start_clipping() = 0;
  virtual void stop_clipping() = 0;
  virtual void set_clip_parity(bool);
  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
  virtual vtkSmartPointer<vtkPoints> get_pickable_points();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();
  virtual bool visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
				  CRectangularPrism*) const;
};

class SolidFilledGridCanvasLayer : public FilledGridCanvasLayer {
public:
  SolidFilledGridCanvasLayer(GhostOOFCanvas*, const std::string&,
			     vtkSmartPointer<GridSource>);
  virtual const std::string &classname() const;
  virtual void start_clipping();
  virtual void stop_clipping();
  void set_CellData(vtkSmartPointer<vtkDataArray>);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ContourGridCanvasLayer : public OOFCanvasLayer {
protected:
  vtkSmartPointer<GridSource> gridsource;
  vtkSmartPointer<vtkActor> actor;
  vtkSmartPointer<vtkPolyDataMapper> mapper;
  vtkSmartPointer<vtkTableBasedClipDataSet> clipper;
  vtkSmartPointer<vtkGeometryFilter> geometryfilter;
  vtkSmartPointer<vtkBandedPolyDataContourFilter> contourfilter;
  vtkSmartPointer<vtkCellLocator> locator;
  vtkSmartPointer<vtkLookupTable> lut;
public:
  ContourGridCanvasLayer(GhostOOFCanvas*, const std::string&,
			 vtkSmartPointer<GridSource>);
  virtual const std::string &classname() const;
  virtual void setModified();
  virtual int nVTKProps() const { return 1; }
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
  void set_pointData(vtkSmartPointer<vtkDoubleArray>);
  void set_nContours(int, double vmin, double vmax);
  void set_lookupTable(vtkSmartPointer<vtkLookupTable>, double, double);
  virtual vtkScalarsToColors *get_lookupTable();
  virtual void writeVTK(const std::string&);
  virtual bool visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
				  CRectangularPrism*) const;
};

// TODO: SolidFilledGridCanvasLayer and ContourGridCanvasLayer should
// share a base class (FilledGridCanvasLayer?) other than
// OOFCanvasLayer.

#endif // GRIDLAYERS_H
