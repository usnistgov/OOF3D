// -*- C++ -*-

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
class BoxWidgetLayer;
class FilledGridCanvasLayer;
class ImageCanvasLayer;
class ImageCanvasOverlayer;
class OOFCanvasLayer;
class OOFCanvasLayerBase;
class PlaneAndArrowLayer;

#include "common/clip.h"
#include "common/coord_i.h"
#include "common/lock.h"
#include "common/pythonexportable.h"
#include "common/IO/oofCellLocator.h"

class CColor;
class CRectangularPrism;
class GhostOOFCanvas;
class ImageBase;
class oofImageToGrid;
class oofExcludeVoxels;
class PixelSet;
class VoxelFilter;

#include <vtkAbstractCellLocator.h>
#include <vtkActorCollection.h>
#include <vtkArrowSource.h>
#include <vtkAssembly.h>
#include <vtkCellCenters.h>
#include <vtkCellLocator.h>
#include <vtkCellType.h>
#include <vtkConeSource.h>
#include <vtkCubeSource.h>
#include <vtkDataSetMapper.h>
#include <vtkDoubleArray.h>
#include <vtkExtractEdges.h>
#include <vtkGlyph3D.h>
#include <vtkIdList.h>
#include <vtkPoints.h>
#include <vtkPolyDataMapper.h>
#include <vtkProp.h>
#include <vtkProp3D.h>
#include <vtkRectilinearGridAlgorithm.h>
#include <vtkScalarsToColors.h>
#include <vtkSmartPointer.h>
#include <vtkSphereSource.h>
#include <vtkTransformPolyDataFilter.h>
#include <vtkTransform.h>
#include <vtkTableBasedClipDataSet.h>
#include <vtkUnstructuredGrid.h>

#include <vector>

typedef std::vector<OOFCanvasLayer*> CanvasLayerList;

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
  virtual bool showing() const { return false; }
  virtual void setCoincidentTopologyParams(double, double) = 0;

  // TODO: Why isn't pickable() const?
  virtual bool pickable() { return false; }

  const GhostOOFCanvas *getCanvas() const { return canvas; }

  // visibleBoundingBox returns false if none of the layer is visible
  // inside the given camera frustum.  It returns true and sets the
  // CRectangularPrism to the bounding box of the visible region if
  // any of the layer is within the frustum.
  //    visibleBoundingBox is used to choose the center of rotation for
  // view modifications.  Layers that don't display anything relevant
  // for that purpose don't have to redefine it.  The base class
  // implementation just returns false.
  virtual bool visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
				  CRectangularPrism*) const;

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
   // showing_ is set by show() and hide(), which also toggle the vtk
   // Visibility flags.
  bool showing_;
  bool empty_;
  PropVec props;
  // setPropVisibility toggles vtk visibility, without touching the
  // OOFCanvasLayer state.
  void setPropVisibility(bool);
public:
  OOFCanvasLayer(GhostOOFCanvas*, const std::string&);
  virtual ~OOFCanvasLayer();

  void installContourMap();
  void updateContourMap();
  virtual vtkScalarsToColors *get_lookupTable();

  void addProp(vtkSmartPointer<vtkProp>);
  void removeProp(vtkSmartPointer<vtkProp>);
  void removeAllProps();
  // setEmpty should be called when nothing will be drawn.  See the
  // comment in the .C file.
  void setEmpty(bool);
  bool getEmpty() const { return empty_; } // for debugging

  virtual void show(bool);
  virtual void hide(bool);
  virtual bool showing() const { return showing_; }
  virtual void destroy();

  // Machinery to allow mouse selections.
  virtual vtkSmartPointer<vtkActorCollection> get_pickable_actors();
  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
  virtual vtkSmartPointer<vtkPoints> get_pickable_points();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();
  // TODO: Can pickable() be const?  The generic version uses
  // get_pickable_prop3d, which isn't const.  Can it be?
  virtual bool pickable();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// PlaneAndArrowLayer is used to display a plane (represented
// by a vtk plane) and its normal vector (represented by a vtk arrow).
// This layer is pickable.

// This class is used in clipplaneclickanddragdisplay.py to allow the
// user to easily edit clipping planes inside the OOF3D canvas.

class PlaneAndArrowLayer : public OOFCanvasLayer {
protected:
  vtkSmartPointer<vtkCubeSource> planeSource;
  vtkSmartPointer<vtkArrowSource> arrowSource;
  vtkSmartPointer<vtkTransform> scaling;
  vtkSmartPointer<vtkTransform> arrowScaling;
  vtkSmartPointer<vtkTransform> rotation;
  vtkSmartPointer<vtkTransform> translation;
  vtkSmartPointer<vtkTransform> planeTransform;
  vtkSmartPointer<vtkTransform> arrowTransform;
  vtkSmartPointer<vtkTransformPolyDataFilter> planeFilter;
  vtkSmartPointer<vtkTransformPolyDataFilter> arrowFilter;
  vtkSmartPointer<vtkPolyDataMapper> planeMapper;
  vtkSmartPointer<vtkPolyDataMapper> arrowMapper;
  vtkSmartPointer<vtkActor> planeActor;
  vtkSmartPointer<vtkActor> arrowActor;
  int arrowParity;		// 1 or -1, multiplies arrowScaling
public:
  PlaneAndArrowLayer(GhostOOFCanvas*, const std::string&, bool);
  ~PlaneAndArrowLayer();
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
  virtual void setModified();
  virtual const std::string &classname() const;
  vtkSmartPointer<vtkActor> get_planeActor();
  vtkSmartPointer<vtkActor> get_arrowActor();
  virtual bool pickable() { return true; }
  virtual vtkSmartPointer<vtkActorCollection> get_pickable_actors();
  void set_arrowShaftRadius(double);
  void set_arrowTipRadius(double);
  void set_arrowLength(double);
  void set_arrowColor(const CColor&);
  void set_planeColor(const CColor&);
  void set_planeOpacity(double);
  void rotate(const Coord3D*, double);
  void translate(const Coord3D*);
  void offset(double);
  void scale(double);
  Coord3D *get_center();
  Coord3D *get_normal_Coord3D();
  CUnitVectorDirection *get_normal();
  double get_offset();
  void set_scale(double);
  void set_normal(const CDirection*);
  void set_center(const Coord3D*);
  virtual void setCoincidentTopologyParams(double, double);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class BoxWidgetLayer : public OOFCanvasLayer {
protected:
  vtkSmartPointer<vtkUnstructuredGrid> grid;
  vtkSmartPointer<vtkPoints> points;
  vtkSmartPointer<vtkDataSetMapper> boxMapper;
  vtkSmartPointer<vtkActor> boxActor;
  vtkSmartPointer<oofCellLocator> locator;
public:
  BoxWidgetLayer(GhostOOFCanvas*, const std::string&);
  ~BoxWidgetLayer();
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
  virtual void setModified();
  virtual const std::string &classname() const;
  virtual bool pickable() { return true; }
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();
  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkPoints> get_pickable_points();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();
  Coord3D *get_cellCenter(vtkIdType);
  Coord3D *get_cellNormal_Coord3D(vtkIdType);
  void reset();
  void set_box(const Coord3D*);
  void set_box(const CRectangularPrism*);
  CRectangularPrism *get_box() const;
  void set_pointSize(float);
  void set_lineWidth(float);
  void set_lineColor(const CColor&);
  void set_faceColor(const CColor&);
  void set_opacity(double);
  void set_position(const Coord3D*);
  void offset_cell(vtkIdType, double);
  virtual void setCoincidentTopologyParams(double, double);
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
  virtual bool visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
				  CRectangularPrism*) const;
  virtual void setCoincidentTopologyParams(double, double);
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

class LineSegmentLayer : public SimpleWireframeCellLayer {
private:
  virtual void newGrid(vtkSmartPointer<vtkPoints>, int) {}
public:
  LineSegmentLayer(GhostOOFCanvas*, const std::string&);
  virtual const std::string &classname() const;
  void set_nSegs(int);	// use instead of newGrid
  void addSegment(const Coord*, const Coord*);
  virtual bool pickable() { return false; }
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

  // clipperInput() returns the vtkAlgorithmOutput that should be
  // plugged into the clipper.
  vtkSmartPointer<vtkAlgorithmOutput> clipperInput();
public:
  ImageCanvasLayer(GhostOOFCanvas*, const std::string&);
  virtual ~ImageCanvasLayer();
  virtual const std::string &classname() const;
  virtual void destroy();
  virtual void setModified();
  void filterModified();
  void set_image(const ImageBase*, const Coord *location, const Coord *size);
  void set_filter(VoxelFilter*);
  void unset_filter();
  void set_opacity(double);

  virtual vtkSmartPointer<vtkProp3D> get_pickable_prop3d();
  virtual vtkSmartPointer<vtkAbstractCellLocator> get_locator();
  virtual vtkSmartPointer<vtkDataSet> get_pickable_dataset();

  virtual bool visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
				  CRectangularPrism*) const;

  virtual void setCoincidentTopologyParams(double, double);

  vtkSmartPointer<vtkAlgorithmOutput> griddedImage();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class MonochromeVoxelLayer : public OOFCanvasLayer {
protected:
  ImageCanvasLayer *imageLayer;
  vtkSmartPointer<oofExcludeVoxels> excluder;
  vtkSmartPointer<vtkTableBasedClipDataSet> clipper;
  vtkSmartPointer<vtkDataSetMapper> mapper;
  vtkSmartPointer<vtkActor> actor;
  VoxelFilter *filter;
public:
  MonochromeVoxelLayer(GhostOOFCanvas*, const std::string&);
  virtual ~MonochromeVoxelLayer();
  virtual const std::string &classname() const;
  virtual void setModified();
  void set_opacity(double);
  void set_color(const CColor&);
  void set_filter(VoxelFilter*);
  void set_image_layer(ImageCanvasLayer*);
  virtual void start_clipping();
  virtual void stop_clipping();
  virtual void set_clip_parity(bool);
  virtual void setCoincidentTopologyParams(double, double);
  virtual bool pickable() { return false; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

vtkSmartPointer<vtkTableBasedClipDataSet> getClipper(const OOFCanvasLayer*);

bool getVisibleBoundingBox(vtkDataSet*, vtkSmartPointer<vtkRenderer>,
			   CRectangularPrism*);
#endif // CANVASLAYERS_H
