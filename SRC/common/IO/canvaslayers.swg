// -*- C++ -*-
// $RCSfile: canvaslayers.swg,v $
// $Revision: 1.1.2.31 $
// $Author: langer $
// $Date: 2014/12/05 21:29:11 $

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

%{
#include "common/ccolor.h"
#include "common/IO/canvaslayers.h"
#include "common/IO/vtkutils.h"
#include "common/pixelgroup.h"
%}

%pragma(python) include="canvaslayers.spy"

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
  void writeVTK(char*);
};

class OOFCanvasLayer : public OOFCanvasLayerBase { 
public:
  // void raise_layer(int);
  // void raise_to_top();
  // void lower_layer(int);
  // void add_to_renderer();
  // void remove_from_renderer();
  void setModified();
  void installContourMap();
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
  long get_gridsize();
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
  void connectBottomOverlayer(ImageCanvasOverlayer*);
  void connectTopOverlayer(ImageCanvasOverlayer*);
  void noOverlayers();
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
