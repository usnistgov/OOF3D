// -*- C++ -*-
// $RCSfile: imageformat.h,v $
// $Revision: 1.1.2.4 $
// $Author: langer $
// $Date: 2014/05/20 13:43:34 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef IMAGEFORMAT_H
#define IMAGEFORMAT_H

#include <oofconfig.h>
#include <vtkImageWriter.h>
#include <vtkRenderWindow.h>
#include <vtkSmartPointer.h>

class ImageFormat {
public:
  virtual ~ImageFormat() {}
  virtual void saveCanvas(vtkSmartPointer<vtkRenderWindow>,
			  const std::string&) const = 0;
  virtual const std::string &suffix() const = 0;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class BitmapImageFormat : public ImageFormat {
public:
  virtual ~BitmapImageFormat() {}
  virtual void saveCanvas(vtkSmartPointer<vtkRenderWindow>,
			  const std::string&) const;
  virtual vtkSmartPointer<vtkImageWriter> writer() const = 0;
};

class JPEGImageFormat : public BitmapImageFormat {
private:
  int quality;	 		// 0 (low) to 100 (high)
public:
  JPEGImageFormat(int);
  virtual const std::string &suffix() const;
  virtual vtkSmartPointer<vtkImageWriter> writer() const;
};

class TIFFImageFormat : public BitmapImageFormat {
public:
  TIFFImageFormat() {}
  virtual const std::string &suffix() const;
  virtual vtkSmartPointer<vtkImageWriter> writer() const;
};

class PNGImageFormat : public BitmapImageFormat {
public:
  PNGImageFormat() {}
  virtual const std::string &suffix() const;
  virtual vtkSmartPointer<vtkImageWriter> writer() const;
};

class EPSImageFormat : public BitmapImageFormat {
public:
  EPSImageFormat() {}
  virtual const std::string &suffix() const;
  virtual vtkSmartPointer<vtkImageWriter> writer() const;
};

class PNMImageFormat : public BitmapImageFormat {
public:
  PNMImageFormat() {}
  virtual const std::string &suffix() const;
  virtual vtkSmartPointer<vtkImageWriter> writer() const;
};

class BMPImageFormat : public BitmapImageFormat {
public:
  BMPImageFormat() {}
  virtual const std::string &suffix() const;
  virtual vtkSmartPointer<vtkImageWriter> writer() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// class PDFImageFormat : public ImageFormat {
// public:
//   PDFImageFormat() {}
//   virtual const std::string &suffix() const;
//   virtual void saveCanvas(vtkSmartPointer<vtkRenderWindow>, 
// 			  const std::string&) const;
// };

#endif // IMAGEFORMAT_H
