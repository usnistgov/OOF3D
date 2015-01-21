// -*- C++ -*-
// $RCSfile: evenlyilluminate.C,v $
// $Revision: 1.10.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:37 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "oofimage.h"
#include "common/doublearray.h"

static double togray(const CColor &color) { return color.getGray(); }

void OOFImage::evenly_illuminate(int windowsize) {
  DoubleArray gray = convert(togray);

  int windowArea = (2*windowsize+1)*(2*windowsize+1);
  ICoord diagonalUR(windowsize+1, windowsize+1);
  ICoord diagonalLL(-windowsize, -windowsize);

  const ICoord xhat(1, 0);
  const ICoord yhat(0, 1);

  double globalavg = 0.0;	// average gray value of whole image
  for(DoubleArray::iterator i=gray.begin(); i!= gray.end(); ++i)
    globalavg += *i;
  globalavg /= gray.width()*gray.height();

  ICoord lastPixel;
  bool first = true;
  double windowtotal = 0.0;	// sum of gray values in moving window
  for(DoubleArray::iterator i=gray.begin(); i!=gray.end(); ++i) {
    ICoord center = i.coord();
    DoubleArray window(gray.subarray(center+diagonalLL, center+diagonalUR));
    if(first || center - lastPixel != xhat) {			// first pixel
      windowtotal = 0.0;
      for(DoubleArray::iterator j=window.begin(); j!=window.end(); ++j)
	windowtotal += *j;
      // The actual window may contain fewer than windowArea pixels
      // because it may lie partly outside the image.  Pretend that
      // the region outside the image is filled with average pixels.
      windowtotal += globalavg * (windowArea - window.width()*window.height());
      first = false;
    }
    else {			// not the first pixel
      if(center - lastPixel == xhat) {
	// window has moved one pixel in the x direction, update w/o recalc.
	ICoord moverR = center+diagonalUR-xhat-yhat;
	ICoord moverL = center+diagonalLL;
	for(int k=0; k<2*windowsize+1; k++) {
	  if(gray.contains(moverL))
	    windowtotal -= gray[moverL];
	  else
	    windowtotal -= globalavg;
	  if(gray.contains(moverR))
	    windowtotal += gray[moverR];
	  else
	    windowtotal += globalavg;
	  moverR -= yhat;
	  moverL += yhat;
	}
      }
      if(windowtotal != 0.0) {
	CColor color = (*this)[center];
	double regionGrayAvg = windowtotal/windowArea;
	double scale = globalavg/regionGrayAvg;
	color.dim(scale);
	set(center, color);
      }
    }
    lastPixel = center;
  }
}
