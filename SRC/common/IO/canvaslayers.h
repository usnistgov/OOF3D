// -*- C++ -*-
// $RCSfile: canvaslayers.h,v $
// $Revision: 1.1.2.59 $
// $Author: langer $
// $Date: 2014/12/14 22:49:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CANVASLAYERS_H
#define CANVASLAYERS_H

// Classes defined in this file:
class FilledGridCanvasLayer;
class ImageCanvasLayer;
class ImageCanvasOverlayer;
class OOFCanvasLayer;
class OOFCanvasLayerBase;

#include "common/clip.h"
#include "common/coord_i.h"
#include "common/lock.h"
#include "common/pythonexportable.h"
#include "common/IO/oofCellLocator.h"

class CColor;
class GhostOOFCanvas;
class ImageBase;
class oofImageToGrid;
class oofExcludeVoxels;
class PixelSet;
class VoxelFilter;

#include <vtkAbstractCellLocator.h>
#include <vtkCellCenters.h>
#include <vtkCellLocator.h>
#include <vtkCellType.h>
#include <vtkConeSource.h>
#include <vtkDataSetMapper.h>
#include <vtkDoubleArray.h>
#include <vtkExtractEdges.h>
#include <vtkGlyph3D.h>
#include <vtkIdList.h>
#include <vtkPoints.h>
#include <vtkProp.h>
#include <vtkProp3D.h>
#include <vtkRectilinearGridAlgorithm.h>
#include <vtkScalarsToColors.h>
#include <vtkSmartPointer.h>
#include <vtkSphereSource.h>
#include <vtkTableBasedClipDataSet.h>
#include <vtkUnstructuredGrid.h>


#include <vector>

typedef std::vector<OOFCanvasLayerBase*> CanvasLayerList;

enum ClipState {CLIP_OFF, CLIP_ON, CLIP_UNKNOWN};

// TODO: OOFCanvasLayerBase is derived from PythonExportable because
// it looked like it might be necessary for the ComboCanvasLayer
// class.  It turns out that it's not needed, so perhaps the
// PythonExportable base class should be removed.

class OOFCanvasLayerBase : public PythonExportable<OOFCanvasLayerBase> {
protected:
  GhostOOFCanvas *canvas;
  const std::string name_;	// for debugging mostly
  ClipState clipState;		// is clipping currently being done?
  virtual void start_clipping() = 0;
  virtual void stop_clipping() = 0;
  virtual void set_clip_parity(bool) = 0;
public:
  OOFCanvasLayerBase(GhostOOFCanvas *c, const std::string&);
  virtual ~OOFCanvasLayerBase();
  virtual void destroy() {}
  virtual void setModified() = 0;
  const std::string &name() const { return name_; }
  const std::string &modulename() const;

  void set_clipping(bool, bool);

  virtual void show(bool) {}
  virtual void hide(bool) {}

  virtual bool pickable() { return false; }

  const GhostOOFCanvas *getCanvas() const { return canvas; }

  virtual void writeVTK(const std::string &) {}
};

std::ostream &operator<<(std::ostream&, const OOFCanvasLayerBase&);

typedef std::vector< vtkSmartPointer<vtkProp> > PropVec;

// OOFCanvasLayer is the base class for layers that are not
// overlayers.  Overlayers differ from other layers in that they don't
// build their own vtk pipelines, they just modify another layer's
// pipeline.

class OOFCanvasLayer : public OOFCanvasLayerBase {
private:
  bool showing_;
  PropVec props;
public:
  OOFCanvasLayer(GhostOOFCanvas*, const std::string&);
  virtual ~OOFCanvasLayer();
  void raise_layer(int);
  void raise_to_top();
  void lower_layer(int);

  void installContourMap();
  void updateContourMap();
  virtual vtkScalarsToColors *get_lookupTable();

  void addProp(vtkSmartPointer<vtkProp>);
  void removeProp(vtkSmartPointer<vtkProp>);
  void removeAllProps();

  virtual void show(bool);
  virtual void hide(bool);
  bool showing() const { return showing_; }
  virtual void destroy();

  // Machinery to allow mouse selections.
  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
  virtual vtkSmartPointer<vtkPoints> get_pickable_points();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();
  // TODO: Can pickable() be const?  The generic version uses
  // get_pickable_prop3d, which isn't const.  Can it be?
  virtual bool pickable();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// SimpleCellLayer and its subclasses are meant to be used to display
// a few cells of an unstructured grid.  They don't support picking.

class SimpleCellLayer : public OOFCanvasLayer {
protected:
  // The constructor is protected because only the derived classes
  // should be instantiated.
  SimpleCellLayer(GhostOOFCanvas*, const std::string&);
  vtkSmartPointer<vtkUnstructuredGrid> grid;
  vtkSmartPointer<vtkActor> actor;
  vtkSmartPointer<vtkDataSetMapper> mapper;
  vtkSmartPointer<vtkTableBasedClipDataSet> clipper;
  int number_cells;
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
public:
  virtual ~SimpleCellLayer();
  virtual void setModified();
  virtual void newGrid(vtkSmartPointer<vtkPoints>, int ncells);
  virtual void addCell(VTKCellType type, vtkSmartPointer<vtkIdList> ptIds);
  void clear();
  void set_color(const CColor&);
  void set_opacity(double);
  virtual void set_size(double);
  int get_gridsize() const;
};

class SimpleFilledCellLayer : public SimpleCellLayer {
public:
  SimpleFilledCellLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
};

class SimpleWireframeCellLayer : public SimpleCellLayer {
private:
  vtkSmartPointer<vtkExtractEdges> edgeExtractor;
  void setup();
  const bool extract;
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
public:
  // The bool arg to the constructor says whether or not to extract
  // edges from the grid.  If the grid cell are already edges, the
  // extraction doesn't need to be done (in fact, it can't be done),
  // and the arg should be false.  If it's not given, it's assumed to
  // be true.
  SimpleWireframeCellLayer(GhostOOFCanvas*, bool, const std::string&);
  SimpleWireframeCellLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  void set_lineWidth(double);
  virtual void set_size(double x) { set_lineWidth(x); }
};

// SingleVoxelLayer is used by the PixelInfoDisplay.  PixelInfoDisplay
// would use a SimpleWireframeCellLayer directly, except that it has to
// be able to construct its own vtkPoints object, and
// SimpleWireframeCellLayer gets its vtkPoints from a CSkeleton.

class SingleVoxelLayer : public SimpleWireframeCellLayer {
public:
  SingleVoxelLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  void set_voxel(const ICoord *where, const Coord *size);
};

class SimplePointCellLayer : public SimpleCellLayer {
public:
  SimplePointCellLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  void set_pointSize(double);
  virtual void set_size(double x) { set_pointSize(x); }
};

// Sometimes it's necessary to be able to make picks on a SimpleCellLayer

class PickableFilledCellLayer : public SimpleFilledCellLayer {
private:
  vtkSmartPointer<oofCellLocator> locator;
public:
  PickableFilledCellLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
  virtual vtkSmartPointer<vtkPoints> get_pickable_points();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();
  virtual bool pickable() { return true; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class GlyphedLayer : public SimpleCellLayer {
protected:
  vtkSmartPointer<vtkPolyData> glyphCenters;
  vtkSmartPointer<vtkDoubleArray> glyphDirections;
  vtkSmartPointer<vtkActor> glyphActor;
  vtkSmartPointer<vtkMapper> glyphMapper; // generic
  vtkSmartPointer<vtkGlyph3D> glyph;
  vtkSmartPointer<vtkCellCenters> centerFinder;
  vtkSmartPointer<vtkTableBasedClipDataSet> glyphClipper;
  GlyphedLayer(GhostOOFCanvas*, const std::string&);
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
public:
  void newGrid(vtkSmartPointer<vtkPoints>, int);
  void addDirectedCell(VTKCellType, vtkIdList*, double[]);
  void set_glyphColor(const CColor*);
  virtual void setModified();
  virtual void recomputeDirections() {}
};

class ConeGlyphLayer : public GlyphedLayer {
  // Intermediate base class for GlyphedLayers that use cones.
protected:
  vtkSmartPointer<vtkConeSource> coneSource;
public:
  ConeGlyphLayer(GhostOOFCanvas*, const std::string&);
  void set_coneGeometry(double len, int resolution);
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void recomputeDirections();
};

class FaceGlyphLayer : public ConeGlyphLayer {
protected:
public:
  FaceGlyphLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
};

class EdgeGlyphLayer : public ConeGlyphLayer {
public:
  EdgeGlyphLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  void set_lineWidth(double);
};

class PointGlyphLayer : public GlyphedLayer {
protected:
  vtkSmartPointer<vtkSphereSource> sphereSource;
public:
  PointGlyphLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  void set_sphereGeometry(double size, int resolution);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ImageCanvasLayer : public OOFCanvasLayer {
protected:
  const ImageBase *image;
  vtkSmartPointer<oofImageToGrid> gridifier;
  vtkSmartPointer<oofExcludeVoxels> excluder;
  vtkSmartPointer<vtkTableBasedClipDataSet> clipper;
  vtkSmartPointer<vtkCellLocator> locator;
  vtkSmartPointer<vtkDataSetMapper> mapper;
  vtkSmartPointer<vtkActor> actor;
  VoxelFilter *filter;
  SLock pipelineLock;

  ImageCanvasOverlayer *bottomOverlayer;
  ImageCanvasOverlayer *topOverlayer;

  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);

  // downstreamSocket() returns the vtkAlgorithm that the downstream end
  // of the overlayer pipeline should be connected to.
  vtkSmartPointer<vtkAlgorithm> downstreamSocket() const;
  // overlayerOutput() returns the vtkAlgorithmOutput that is the
  // result of the overlayer pipeline.  If there are no overlayers,
  // it's the vtkRectilinearGrid produced by the gridifier.
  vtkSmartPointer<vtkAlgorithmOutput> overlayerOutput();
  // clipperInput() returns the vtkAlgorithmOutput that should be
  // plugged into the clipper.  It's the same as overlayerOutput()
  // unless there's an excluder.
  vtkSmartPointer<vtkAlgorithmOutput> clipperInput();
  vtkSmartPointer<vtkAlgorithmOutput> connectOverlayers(
					vtkSmartPointer<vtkAlgorithmOutput>);
public:
  ImageCanvasLayer(GhostOOFCanvas*, const std::string&);
  virtual ~ImageCanvasLayer();
  virtual const std::string &classname() const;
  virtual void destroy();
  virtual void setModified();
  void set_image(const ImageBase*, const Coord *location, const Coord *size);
  void set_filter(VoxelFilter*);
  void unset_filter();
  void connectBottomOverlayer(ImageCanvasOverlayer*);
  void connectTopOverlayer(ImageCanvasOverlayer*);
  void noOverlayers();

  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
};

class ImageCanvasOverlayer : public OOFCanvasLayerBase {
protected:
  vtkSmartPointer<vtkRectilinearGridAlgorithm> algorithm;
  vtkSmartPointer<vtkAlgorithmOutput> input;
  virtual void start_clipping() {}
  virtual void stop_clipping() {}
  virtual void set_clip_parity(bool) {}
public:
  ImageCanvasOverlayer(GhostOOFCanvas*, const std::string &,
		       vtkSmartPointer<vtkRectilinearGridAlgorithm>);
  virtual ~ImageCanvasOverlayer();
  virtual void setModified();
  virtual void disconnect();
  virtual void connectToOverlayer(ImageCanvasOverlayer*);
  virtual void connectToAlgorithm(vtkSmartPointer<vtkAlgorithmOutput>);
  virtual vtkSmartPointer<vtkAlgorithmOutput> output();
  friend class ImageCanvasLayer;
};

class OverlayVoxels : public ImageCanvasOverlayer {
public:
  OverlayVoxels(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  void setTintOpacity(double);
  void setColor(const CColor*);
  void setPixelSet(PixelSet*);
  void clearPixelSet();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

vtkSmartPointer<vtkTableBasedClipDataSet> getClipper(const OOFCanvasLayer*);

#endif // CANVASLAYERS_H
