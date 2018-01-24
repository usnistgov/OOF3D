// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CANVASLAYERS_SWG
#define CANVASLAYERS_SWG

%module canvaslayers
%include "common/typemaps.swg"
%extern "common/coord.swg"
%extern "common/direction.swg"
%extern "common/geometry.swg"

%{
#include "common/ccolor.h"
#include "common/IO/canvaslayers.h"
#include "common/IO/vtkutils.h"
#include "common/pixelgroup.h"
%}

%pragma(python) include="canvaslayers.spy"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"
%pragma(python) code="from ooflib.SWIG.common.direction import CUnitVectorDirectionPtr"

%typemap(python, out) OOFCanvasLayerBase* {
  $target = $source->pythonObject();
}

class OOFCanvasLayerBase {
public:
  ~OOFCanvasLayerBase();
  void destroy();
  void setModified();
  void show(bool);
  void hide(bool);
  bool pickable();
  bool showing();
  void writeVTK(char*);

  bool visibleBoundingBox(vtkRendererPtr, CRectangularPrism *outPrism);
  void setCoincidentTopologyParams(double, double);
};

class OOFCanvasLayer : public OOFCanvasLayerBase { 
public:
  // void raise_layer(int);
  // void raise_to_top();
  // void lower_layer(int);
  // void add_to_renderer();
  // void remove_from_renderer();
  void setEmpty(bool);
  void setModified();
  void installContourMap();
};

class PlaneAndArrowLayer: public OOFCanvasLayer {
public:
  PlaneAndArrowLayer(GhostOOFCanvas*, const char*, bool);
  vtkActorPtr get_planeActor();
  vtkActorPtr get_arrowActor();
  void set_visibility(bool);
  void set_arrowShaftRadius(double);
  void set_arrowTipRadius(double);
  void set_arrowLength(double);
  void set_arrowColor(const CColor&);
  void set_planeColor(const CColor&);
  void set_planeOpacity(double);

  void rotate(Coord* Point, double);
  void translate(Coord *Point);
  void offset(double);
  void scale(double);
  
  %new Coord *get_center();
  %new Coord *get_normal_Coord3D();
  %new CUnitVectorDirection *get_normal();
  double get_offset();

  void set_scale(double);
  void set_normal(const CDirection*);
  void set_center(Coord* Point);
};

class BoxAndArrowLayer : public OOFCanvasLayer {
public:
  BoxAndArrowLayer(GhostOOFCanvas*, const char*);
  %new Coord *get_cellCenter(int);
  %new Coord *get_cellNormal_Coord3D(int);
  void reset();
  void set_box(Coord *Point);
  void set_totalVisibility(bool);
  void set_arrowVisibility(bool);
  void set_arrowShaftRadius(double);
  void set_arrowTipRadius(double);
  void set_arrowLength(double);
  void set_arrowColor(const CColor&);
  void set_pointSize(float);
  void set_lineWidth(float);
  void set_lineColor(const CColor&);
  void set_faceColor(const CColor&);
  void set_faceOpacity(double);
  void set_position(Coord *Point);
  void offset_cell(int, double); 
};

class SimpleCellLayer : public OOFCanvasLayer {
public:
  void newGrid(vtkPointsPtr, int);
  void addCell(VTKCellType, vtkIdListPtr);
  // void reinitialize(int);
  // void doneAddingCells();
  void set_color(const CColor&);
  void set_opacity(double);
  void clear();
};

class SimpleFilledCellLayer : public SimpleCellLayer {
public:
  SimpleFilledCellLayer(GhostOOFCanvas*, const char*);
};

class SimpleWireframeCellLayer : public SimpleCellLayer {
public:
  SimpleWireframeCellLayer(GhostOOFCanvas*, bool, const char*);
  void set_lineWidth(double);
};

class LineSegmentLayer : public SimpleWireframeCellLayer {
public:
  LineSegmentLayer(GhostOOFCanvas*, const char*);
  void set_nSegs(int);
  void addSegment(Coord *Point, Coord *Point);
};

class SimplePointCellLayer : public SimpleCellLayer {
public:
  SimplePointCellLayer(GhostOOFCanvas*, const char*);
  void set_pointSize(double);
};

class SingleVoxelLayer : public SimpleWireframeCellLayer {
public:
  SingleVoxelLayer(GhostOOFCanvas*, const char*);
  void set_voxel(const ICoord *iPoint, const Coord *Point);
};

class ImageCanvasLayer : public OOFCanvasLayer {
public:
  ImageCanvasLayer(GhostOOFCanvas*, const char*);
  void set_image(ImageBase*, Coord *Point, Coord *Point);
  void set_filter(VoxelFilter*);
  void filterModified();
  void connectBottomOverlayer(ImageCanvasOverlayer*);
  void connectTopOverlayer(ImageCanvasOverlayer*);
  void noOverlayers();
  void set_opacity(double);
};

class ImageCanvasOverlayer : public OOFCanvasLayerBase {
public:
  ~ImageCanvasOverlayer();
  void connectToOverlayer(ImageCanvasOverlayer*);
  void disconnect();
};

class OverlayVoxels : public ImageCanvasOverlayer {
public:
  OverlayVoxels(GhostOOFCanvas*, const char*);
  void setTintOpacity(double);
  void setColor(CColor*);
  void setPixelSet(PixelSet*);
  void clearPixelSet();
};

class GlyphedLayer : public SimpleCellLayer {
public:
  void addDirectedCell(VTKCellType, vtkIdListPtr, double *doubleDIMArray);
  void set_glyphColor(CColor*);
  void recomputeDirections();
};

class ConeGlyphLayer : public GlyphedLayer {
public:
  void set_coneGeometry(double, int);
}

class FaceGlyphLayer : public ConeGlyphLayer {
public:
  FaceGlyphLayer(GhostOOFCanvas*, const char*);
};

class EdgeGlyphLayer : public ConeGlyphLayer {
public:
  EdgeGlyphLayer(GhostOOFCanvas*, const char*);
  void set_lineWidth(double);
};

class PointGlyphLayer : public GlyphedLayer {
public:
  PointGlyphLayer(GhostOOFCanvas*, const char*);
  void set_sphereGeometry(double, int);
};



// class GlyphedLayer : public SimpleCellLayer {
// public:
//   GlyphedLayer(GhostOOFCanvas*, const char*);
//   void addDirectedCell(VTKCellType, vtkIdListPtr, double *doubleDIMArray);
//   void set_lineWidth(double);
//   void set_glyphColor(const CColor&);
//   void set_glyphGeometry(double, int);
//   void set_face_mode();
//   void set_edge_mode();
//   void set_point_mode();
// };



// class ImageCanvasOverlay : public OOFCanvasLayerBase {
// public:
//   // ImageCanvasOverlay(GhostOOFCanvas*, const char*);
//   // void disconnect();
// };

// class ResampleImageOverlay : public ImageCanvasOverlay {
// public:
//   ResampleImageOverlay(GhostOOFCanvas*, const char*);
//   void set_bitmap(BitmapOverlay*);
//   void set_color(CColor*);
//   void set_tintOpacity(double);
//   void set_voxelOpacity(double);
// };

// class ImageCanvasLayer : public OOFCanvasLayer {
// public:
//   ImageCanvasLayer(GhostOOFCanvas*, const char*);
//   void set_image(ImageBase*, const Coord *Point, const Coord *Point);
//   void set_opacity(double);
//   void addOverlayer(ImageCanvasOverlay*);
//   void clearOverlayers();
//   void disassemblePipeline();
//   void rebuildPipeline();
// };


#endif // CANVASLAYERS_SWG
