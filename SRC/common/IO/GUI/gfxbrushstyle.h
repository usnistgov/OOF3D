// -*- C++ -*-
// $RCSfile: gfxbrushstyle.h,v $
// $Revision: 1.4.18.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GFXBRUSHSTYLE_H
#define GFXBRUSHSTYLE_H

#include <oofconfig.h>

#include "common/coord_i.h"
#include "common/brushstyle.h"
#include <gdk/gdk.h>
#include <gtk/gtk.h>
#include <libgnomecanvas/libgnomecanvas.h>

// Each BrushStyle subclass defined in common/brushstyle.h should have
// a GfxBrushStyle class derived from it here.  The drawStyle()
// routine draws the brush's "rubberband" while the user is moving the
// mouse.  The classes defined here must be swigged in
// gfxbrushstyle.swg, and the brushstyle registration must be modified
// in gfxbrushstyle.spy.

class GfxBrushStyle {
public:
  virtual ~GfxBrushStyle() {}
  virtual void drawStyle(GnomeCanvasItem*, GdkBitmap*, GdkBitmap*,
			 const guint32&, const guint32&, const Coord&) = 0;
};

class GfxCircleBrush : public GfxBrushStyle, public CircleBrush {
public:
  GfxCircleBrush(double r) : CircleBrush(r) {}
  virtual void drawStyle(GnomeCanvasItem*, GdkBitmap*, GdkBitmap*,
			 const guint32&, const guint32&, const Coord&);
};

class GfxSquareBrush : public GfxBrushStyle, public SquareBrush {
public:
  GfxSquareBrush(double hs) : SquareBrush(hs) {}
  virtual void drawStyle(GnomeCanvasItem*, GdkBitmap*, GdkBitmap*,
			 const guint32&, const guint32&, const Coord&);
};

#endif // GFXBRUSHSTYLE_H
