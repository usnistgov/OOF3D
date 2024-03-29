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

#include "common/IO/imageformat.h"
#include "common/IO/oofcerr.h"

#include <vtkBMPWriter.h>
#include <vtkGL2PSExporter.h>
#include <vtkJPEGWriter.h>
#include <vtkPNGWriter.h>
#include <vtkPNMWriter.h>
#include <vtkPostScriptWriter.h>
#include <vtkTIFFWriter.h>
#include <vtkWindowToImageFilter.h>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void BitmapImageFormat::saveCanvas(vtkSmartPointer<vtkRenderWindow> window,
				   const std::string &filename)
  const
{
  vtkSmartPointer<vtkWindowToImageFilter> w2i =
    vtkSmartPointer<vtkWindowToImageFilter>::New();
  w2i->SetInput(window);
  vtkSmartPointer<vtkImageWriter> righter = writer();
  righter->SetInputConnection(w2i->GetOutputPort());
  righter->SetFileName(filename.c_str());
  window->Render();		// necessary?
  w2i->Update();		// necessary?
  righter->Write();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

JPEGImageFormat::JPEGImageFormat(int quality)
  : quality(quality)
{}

const std::string &JPEGImageFormat::suffix() const {
  static const std::string sfx("jpg");
  return sfx;
}

vtkSmartPointer<vtkImageWriter> JPEGImageFormat::writer() const {
  vtkSmartPointer<vtkJPEGWriter> w = vtkSmartPointer<vtkJPEGWriter>::New();
  w->SetQuality(quality);
  return w;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &TIFFImageFormat::suffix() const {
  static const std::string sfx("tif");
  return sfx;
}

vtkSmartPointer<vtkImageWriter> TIFFImageFormat::writer() const {
  vtkSmartPointer<vtkImageWriter> w = vtkSmartPointer<vtkTIFFWriter>::New();
  return w;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &PNGImageFormat::suffix() const {
  static const std::string sfx("png");
  return sfx;
}

vtkSmartPointer<vtkImageWriter> PNGImageFormat::writer() const {
  vtkSmartPointer<vtkImageWriter> w = vtkSmartPointer<vtkPNGWriter>::New();
  return w;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The EPS output produced by vtkPostScriptWriter is a bitmap, not
// scalable vector graphics.  vtkGL2PSExporter is capable of producing
// scalable output in principle, but it works very badly.  See
// PDFImageFormat.

const std::string &EPSImageFormat::suffix() const {
  static const std::string sfx("eps");
  return sfx;
}

vtkSmartPointer<vtkImageWriter> EPSImageFormat::writer() const {
  vtkSmartPointer<vtkImageWriter> w = 
    vtkSmartPointer<vtkPostScriptWriter>::New();
  return w;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &PNMImageFormat::suffix() const {
  static const std::string sfx("pnm");
  return sfx;
}

vtkSmartPointer<vtkImageWriter> PNMImageFormat::writer() const {
  vtkSmartPointer<vtkImageWriter> w = 
    vtkSmartPointer<vtkPNMWriter>::New();
  return w;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &BMPImageFormat::suffix() const {
  static const std::string sfx("bmp");
  return sfx;
}

vtkSmartPointer<vtkImageWriter> BMPImageFormat::writer() const {
  vtkSmartPointer<vtkImageWriter> w = 
    vtkSmartPointer<vtkBMPWriter>::New();
  return w;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &PDFImageFormat::suffix() const {
  // This is a hack because vtkGL2PSExporter adds the suffix itself.
  static const std::string &sfx("");
  return sfx;
}

void PDFImageFormat::saveCanvas(vtkSmartPointer<vtkRenderWindow> window,
				const std::string &filename)
  const
{
  // TODO: I'm not at all sure that the parameters set below are the
  // best.  This doesn't work if the GUI's not running.
  vtkSmartPointer<vtkGL2PSExporter> exporter =
    vtkSmartPointer<vtkGL2PSExporter>::New();
  exporter->SetRenderWindow(window);
  exporter->SetFileFormatToPDF();
  exporter->SetFilePrefix(filename.c_str());
  exporter->SetSortToBSP();
  exporter->CompressOn();
  exporter->OcclusionCullOff();
  exporter->SimpleLineOffsetOff();
  //exporter->SimpleLineOffsetOn();
  exporter->TextOn();
  //exporter->Write3DPropsAsRasterImageOn();
  exporter->Write();
}

