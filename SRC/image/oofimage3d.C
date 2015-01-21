// -*- C++ -*-
// $RCSfile: oofimage3d.C,v $
// $Revision: 1.5.8.60 $
// $Author: langer $
// $Date: 2014/12/14 22:49:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "image/oofimage3d.h"
#ifdef HAVE_MPI
#include "common/mpitools.h"
#endif ////HAVE_MPI

#include "common/IO/oofcerr.h"
#include "common/boolarray.h"
#include "common/coord.h"
#include "common/ooferror.h"
#include "common/printvec.h"	// debugging
#include "common/progress.h"
#include "common/tostring.h"

#include <iostream>
#include <math.h>
#include <set>

#include <vtkBMPReader.h>
#include <vtkBMPWriter.h>
#include <vtkImageAppendComponents.h>
#include <vtkImageExport.h>
#include <vtkImageExtractComponents.h>
#include <vtkImageFlip.h>
#include <vtkImageGaussianSmooth.h>
#include <vtkImageImport.h>
#include <vtkImageLuminance.h>
#include <vtkImageMathematics.h>
#include <vtkImageMedian3D.h>
#include <vtkImagePermute.h>
#include <vtkImageReader2.h>
#include <vtkImageReader2Factory.h>
#include <vtkImageShiftScale.h>
#include <vtkImageThreshold.h>
#include <vtkJPEGWriter.h>
#include <vtkPNGWriter.h>
#include <vtkPNMWriter.h>
#include <vtkPointData.h>
#include <vtkPostScriptWriter.h>
#include <vtkStringArray.h>
#include <vtkTIFFReader.h>
#include <vtkTIFFWriter.h>
#include <vtk_tiff.h>		// for ORIENTATION_BOTLEFT


OOFImage3D::OOFImage3D(const std::string &name,
		       const std::vector<std::string> *files, 
		       const Coord *size)
  : name_(name)
{
  vtkSmartPointer<vtkImageReader2Factory> factory =
    vtkSmartPointer<vtkImageReader2Factory>::New();

  // Create an ImageReader, and read the first file to get its xy size.
  const char *f = (*files)[0].c_str();
  vtkSmartPointer<vtkImageReader2> imageReader;
  // The documentation for vtkImageReader2Factory::CreateImageReader2
  // says that the caller must call Delete on the returned object.
  // That means that the reference count is one more than we think it
  // is, so we use vtkSmartPointer::TakeReference here.
  imageReader.TakeReference(factory->CreateImageReader2(f));

  imageReader->SetFileName(f);
  imageReader->ReleaseDataFlagOn();
  imageReader->Update();

  // The extent vector gives the integer coords of the first and last
  // voxels, in the order (x0, x1, y0, y1, z0, z1).
  int extent[6]; 
  imageReader->GetDataExtent(extent); // get x and y extent from first file
  extent[4] = 0;		      // set z extent
  extent[5] = files->size() - 1;
  imageReader->SetDataExtent(extent);

  sizeInPixels_ = ICoord(extent[1] - extent[0] + 1,
  			 extent[3] - extent[2] + 1,
  			 extent[5] - extent[4] + 1);

  // Set physical size.  Components that are negative weren't provided
  // by the user.
  size_ = *size;
  double spacing[3];
  int nauto = 0;		// How many dimensions weren't provided?
  int given = -1;		// The dimension that was provided, if one was.
  for(int i=0; i<3; i++) {
    if((*size)[i] < 0) {
      ++nauto;
    }
    else
      given = i;
  }
  // If no dimensions were given, each pixel is 1x1x1.
  if(nauto == 3) {
    for(int i=0; i<3; i++) {
      spacing[i] = 1.0;
      size_[i] = sizeInPixels_[i];
    }
  }
  // If only one dimension was given, assume pixels are cubes, with a
  // size that makes the given dimension come out right.
  if(nauto == 2) {
    double pxlsize = (*size)[given]/sizeInPixels_[given];
    for(int i=0; i<3; i++) {
	spacing[i] = pxlsize;
	if(i != given)
	  size_[i] = pxlsize * sizeInPixels_[i];
    }
  }
  // If two dimensions were given, the user is being difficult.
  if(nauto == 1)
    throw ErrSetupError(
	"It is impossible to set just one image dimension automatically.");
  // All three dimensions were given.
  if(nauto == 0) {
    for(int i=0; i<3; i++) {
      spacing[i] = (*size)[i]/sizeInPixels_[i];
    }
  }
  imageReader->SetDataSpacing(spacing);
  
  // Some image types require special treatment.
  vtkTIFFReader *tf = vtkTIFFReader::SafeDownCast(imageReader);
  if(tf) 
    tf->SetOrientationType(ORIENTATION_BOTLEFT);
  vtkBMPReader *bmp = vtkBMPReader::SafeDownCast(imageReader);
  if(bmp)
    bmp->Allow8BitBMPOn();

  // Convert std::vector of names to a vtkStringArray.
  vtkSmartPointer<vtkStringArray> names =
    vtkSmartPointer<vtkStringArray>::New();
  names->SetNumberOfValues(files->size());
  for(unsigned int i=0; i<files->size(); i++) {
    names->SetValue(i, (*files)[i].c_str());
  }
  imageReader->SetFileNames(names);

  // TODO 3.1: Check that images are all the same size, and raise an
  // exception if they're not.  Or at least figure out how to catch
  // the exception raised by vtk (if there is one) instead of
  // crashing.

  imageReader->SetDataScalarTypeToUnsignedChar();
  image = imageReader->GetOutput();

  image->Update();		// The actual reading takes place here.

  // For certain image formats such as PNG, the bit depth may be
  // greater than 8 and the reader will return a vtkImageData object
  // with a scalar type other than unsigned char.  We need to scale
  // the data and make it an unsigned char type.
  if(image->GetScalarType() != VTK_UNSIGNED_CHAR) {
    vtkSmartPointer<vtkImageShiftScale> shiftscale = 
      vtkSmartPointer<vtkImageShiftScale>::New();
    shiftscale->SetInput(image);
    shiftscale->SetShift(0);
    shiftscale->SetScale(255.0/image->GetScalarTypeMax());
    shiftscale->SetOutputScalarTypeToUnsignedChar();
    image = shiftscale->GetOutput();
    image->Update();
  }
  // Make sure that the image has three channels.  TODO OPT: If this uses
  // too much memory, we could allow gray scale images to have only
  // one channel, but we'd either have to do something clever in
  // oofOverlayVoxels.C, or require that the overlay color also be
  // gray.  Also, getPixels() would be need to be smarter.
  image = ImageBase::getRGB(image);
  image->Update();
} // end OOFImage constructor


OOFImage3D::~OOFImage3D() {}


OOFImage3D::OOFImage3D(const std::string &name)
  : name_(name)
{}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Constructor that takes color values from a vector of unsigned
// chars.  Used when loading images embedded in an OOF data file.

OOFImage3D::OOFImage3D(const std::string &name,
		       const Coord &size, const ICoord &isize,
		       const std::vector<unsigned char> *data) 
  : name_(name)
{
  assert((int) data->size() == 3*isize[0]*isize[1]*isize[2]);

  vtkSmartPointer<vtkImageImport> importer =
    vtkSmartPointer<vtkImageImport>::New();
  importer->SetDataSpacing(
		   size[0]/isize[0], size[1]/isize[1], size[2]/isize[2]);
  importer->SetDataOrigin(0, 0, 0);
  importer->SetWholeExtent(0, isize[0]-1, 0, isize[1]-1, 0, isize[2]-1);
  importer->SetDataExtentToWholeExtent();
  importer->SetDataScalarTypeToUnsignedChar();
  importer->SetNumberOfScalarComponents(3);
  importer->CopyImportVoidPointer((void*)(&(*data)[0]), data->size());
  image = importer->GetOutput();
  // TODO OPT: Check that importer is being destroyed.  Would
  // image->ShallowCopy(importer->GetOutput()) help?
  image->Update();
  getPixelSizeFromImage();	// sets sizeInPixels_
  setSize(&size);		// sets size_ and adjusts spacing
}

// Wrapper for the above constructor, so that we can call it from
// Python.

OOFImage3D *newImageFromData(const std::string &name,
			     const Coord *size,
			     const ICoord *isize,
			     const std::vector<unsigned char> *data)
{
  return new OOFImage3D(name, *size, *isize, data);
}

// getPixels() is the inverse of newImageFromData().

std::vector<unsigned char> *OOFImage3D::getPixels() {
  int n = 3*sizeInPixels_[0]*sizeInPixels_[1]*sizeInPixels_[2];
  std::vector<unsigned char> *pxls = new std::vector<unsigned char>(n);
  vtkSmartPointer<vtkImageExport> exporter =
    vtkSmartPointer<vtkImageExport>::New();
  exporter->SetInputConnection(image->GetProducerPort());
  exporter->ImageLowerLeftOn();
  exporter->Export(&(*pxls)[0]);
  // TODO OPT: Check that exporter is being destroyed.
  return pxls;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ICoord OOFImage3D::pixelFromPoint(const Coord *point) const {
  double xx = (*point)[0]/size_[0]*sizeInPixels_[0];
  double yy = (*point)[1]/size_[1]*sizeInPixels_[1];
  double zz = (*point)[2]/size_[2]*sizeInPixels_[2];
  if (xx == sizeInPixels_[0])
    xx = sizeInPixels_[0] - 1.0;
  if (yy == sizeInPixels_[1])
    yy = sizeInPixels_[1] - 1.0;
  if (zz == sizeInPixels_[2])
    zz = sizeInPixels_[2] - 1.0;

  return ICoord((int) floor(xx), (int) floor(yy), (int) floor(zz));
}

bool OOFImage3D::pixelInBounds(const ICoord *pxl) const {
  int xx = (*pxl)[0];
  int yy = (*pxl)[1];
  int zz = (*pxl)[2];
  if ( (xx<0) || (xx>=sizeInPixels_[0]) || 
       (yy<0) || (yy>=sizeInPixels_[1]) || 
       (zz<0) || (zz>=sizeInPixels_[2])  )
    return false;
  return true;
}

void OOFImage3D::getPixelSizeFromImage() {
  const int *sighs = image->GetDimensions();
  sizeInPixels_ = ICoord(sighs[0], sighs[1], sighs[2]);
}

OOFImage3D *OOFImage3D::clone(const std::string &nm) const {
  OOFImage3D *copy = new OOFImage3D(nm);
  copy->image = vtkSmartPointer<vtkImageData>::New();
  copy->image->DeepCopy(image);
  copy->image->Update();
  copy->getPixelSizeFromImage();	 
  copy->size_ = size_;
  copy->setMicrostructure(microstructure);
  return copy;
}

void OOFImage3D::save(const std::string &filepattern, const std::string &format)
{
  vtkSmartPointer<vtkImageWriter> writer;
  if(format == "bmp")
    writer = vtkSmartPointer<vtkBMPWriter>::New();
  else if(format == "jpg")
    writer = vtkSmartPointer<vtkJPEGWriter>::New();
  else if(format == "png")
    writer = vtkSmartPointer<vtkPNGWriter>::New();
  else if(format == "pnm")
    writer = vtkSmartPointer<vtkPNMWriter>::New();
  else if(format == "ps")
    writer = vtkSmartPointer<vtkPostScriptWriter>::New();
  else if(format == "tiff")
    writer = vtkSmartPointer<vtkTIFFWriter>::New();
  else
    throw ErrUserError("Unrecognized image format!");

  writer->SetFilePattern(filepattern.c_str());
  writer->SetInputConnection(image->GetProducerPort());
  //writer->Update();		// is this necessary?
  writer->Write();
}

const CColor OOFImage3D::operator[](const ICoord &c) const {
  // It's important to cast to unsigned char* and then to
  // double. Casting directly to double* will give the wrong value.
  unsigned char* ptr = (unsigned char*)
    image->GetScalarPointer(c[0], c[1], c[2]);
  if(image->GetNumberOfScalarComponents() == 1) {
    double g = *ptr/255.;
    return CColor(g, g, g);
  }
  return CColor(ptr[0]/255., ptr[1]/255., ptr[2]/255.);
}

bool OOFImage3D::compare(const OOFImage3D &other, double tol) const {
  if (sizeInPixels_ != other.sizeInPixels_) {
    oofcerr << "OOFImage3D::compare: size mismatch: "
	    << sizeInPixels_ << " != " << other.sizeInPixels_ << std::endl;
    return false;
  }

  for(int i=0;i<sizeInPixels_[0];i++) {
    for(int j=0;j<sizeInPixels_[1];j++) {
      for(int k=0;j<sizeInPixels_[2];j++) {
	CColor c0 = (*this)[ICoord(i,j,k)];
	CColor c1 = other[ICoord(i,j,k)];
	if (!c0.compare(c1, tol)) {
	  oofcerr << "OOFImage3D::compare: color mismatch: " 
		  << ICoord(i,j,k) << " " << c0 << " != " << c1
		  << std::endl;
	  return false;
	}
      }
    }
  }
  return true;
}

void OOFImage3D::imageChanged() {
  ++timestamp;			// marks image as changed
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Modifiers.  These operate in-place on OOFImage3D::image.

void OOFImage3D::gray() {
  vtkSmartPointer<vtkImageLuminance> luminance 
    = vtkSmartPointer<vtkImageLuminance>::New();
  luminance->SetInputConnection(image->GetProducerPort());
  image = luminance->GetOutput();
  image->Update();
  imageChanged();
}

void OOFImage3D::threshold(double T) {
  vtkSmartPointer<vtkImageLuminance> luminance 
    = vtkSmartPointer<vtkImageLuminance>::New();
  luminance->SetInputConnection(image->GetProducerPort());
  vtkSmartPointer<vtkImageData> gray = luminance->GetOutput();
	
  vtkSmartPointer<vtkImageThreshold> thold1 =
    vtkSmartPointer<vtkImageThreshold>::New();
  thold1->ThresholdByUpper(T*255);
  thold1->SetOutValue(0);
  thold1->SetInputConnection(gray->GetProducerPort());
	
  vtkSmartPointer<vtkImageThreshold> thold2 = 
    vtkSmartPointer<vtkImageThreshold>::New();
  thold2->ThresholdByLower(T*255);
  thold2->SetOutValue(255);
  thold2->SetInputConnection(thold1->GetOutputPort());

  image = thold2->GetOutput();
  image->Update();
  imageChanged();
}

void OOFImage3D::blur(double radius, double sigma) {

  vtkSmartPointer<vtkImageGaussianSmooth> gauss 
    = vtkSmartPointer<vtkImageGaussianSmooth>::New();
  gauss->SetRadiusFactors(radius, radius, radius);
  gauss->SetStandardDeviation(sigma, sigma, sigma);
  gauss->SetInputConnection(image->GetProducerPort());
  image = gauss->GetOutput();
  image->Update();
  imageChanged();
}


void OOFImage3D::dim(double factor) {
  vtkSmartPointer<vtkImageMathematics> dimmer
    = vtkSmartPointer<vtkImageMathematics>::New();
  dimmer->SetOperationToMultiplyByK();
  dimmer->SetConstantK(factor);
  dimmer->SetInputConnection(image->GetProducerPort());
  image = dimmer->GetOutput();
  image->SetScalarTypeToUnsignedChar();
  image->Update();
  imageChanged();
}

void OOFImage3D::fade(double factor) {
  vtkSmartPointer<vtkImageMathematics> fade1 =
    vtkSmartPointer<vtkImageMathematics>::New();
  fade1->SetOperationToMultiplyByK();
  fade1->SetConstantK(1.0-factor);
  fade1->SetInputConnection(image->GetProducerPort());
	
  vtkSmartPointer<vtkImageMathematics> fade2 = 
    vtkSmartPointer<vtkImageMathematics>::New();
  fade2->SetOperationToAddConstant();
  fade2->SetConstantC(255*factor);
  fade2->SetInputConnection(fade1->GetOutputPort());
	
  image = fade2->GetOutput();
  image->SetScalarTypeToUnsignedChar();
  image->Update();
  imageChanged();
}


void OOFImage3D::negate(double dummy) {
  vtkSmartPointer<vtkImageMathematics> negator =
    vtkSmartPointer<vtkImageMathematics>::New();
  negator->SetOperationToMultiplyByK();
  negator->SetConstantK(-1.0);
  negator->SetInputConnection(image->GetProducerPort());

  vtkSmartPointer<vtkImageMathematics> corrector =
    vtkSmartPointer<vtkImageMathematics>::New();
  corrector->SetOperationToAddConstant();
  corrector->SetConstantC(255);
  corrector->SetInputConnection(negator->GetOutputPort());

  image = corrector->GetOutput();
  image->SetScalarTypeToUnsignedChar();
  image->Update();
  imageChanged();
}

void OOFImage3D::medianFilter(int radius) {
  // This can be slow. Could use a progress bar.
  // padImage(-1);
  vtkSmartPointer<vtkImageMedian3D> median
    = vtkSmartPointer<vtkImageMedian3D>::New();

  median->SetKernelSize(radius*2, radius*2, radius*2);
  median->SetInputConnection(image->GetProducerPort());
	
  image = median->GetOutput();
  image->Update();
  imageChanged();
}

void OOFImage3D::normalize() {
  vtkSmartPointer<vtkImageAppendComponents> appender 
    = vtkSmartPointer<vtkImageAppendComponents>::New();

  for(int i=0; i<3; i++) {
    vtkSmartPointer<vtkImageExtractComponents> extractor =
      vtkSmartPointer<vtkImageExtractComponents>::New();
    extractor->SetInputConnection(image->GetProducerPort());
    extractor->SetComponents(i);
    extractor->Update();
		
    const double *minmax = extractor->GetOutput()->GetScalarRange();
		
    vtkSmartPointer<vtkImageMathematics> adder = 
      vtkSmartPointer<vtkImageMathematics>::New();
    adder->SetInputConnection(extractor->GetOutputPort());
    adder->SetOperationToAddConstant();
    if(minmax[0] > 0 && minmax[0] != minmax[1]) {
      adder->SetConstantC(256-minmax[0]);
    }
    else{
      adder->SetConstantC(0);
    }

    vtkSmartPointer<vtkImageMathematics> mult =
      vtkSmartPointer<vtkImageMathematics>::New();
    mult->SetInputConnection(adder->GetOutputPort());
    mult->SetOperationToMultiplyByK();
    if(minmax[0] != minmax[1]) {
      double K = 255.0/(minmax[1]-minmax[0]);
      mult->SetConstantK(K);
    }
    else {
      mult->SetConstantK(1.0);
    }
    mult->GetOutput()->SetScalarTypeToUnsignedChar();

    appender->AddInputConnection(mult->GetOutputPort());
  }

  image = appender->GetOutput();
  image->Update();
  imageChanged();
}

void OOFImage3D::contrast(double factor) {
  // Replace x by [X + factor*(x-X)] where X is the midpoint of the
  // original range of x values.  vtkImageShiftScale applies the shift
  // before the scale, so we have to rewrite the result as
  // factor*[x + (1-factor)*X/factor]

  //  image->Update();

  const double *minmax = image->GetScalarRange();
  double X = 0.5*(minmax[1] + minmax[0]);
  double shift = (1.-factor)*X/factor;

  vtkSmartPointer<vtkImageShiftScale> scale 
    = vtkSmartPointer<vtkImageShiftScale>::New();
  scale->SetInput(image);
  scale->SetShift(shift); 
  scale->SetScale(factor);
  scale->ClampOverflowOn();
  scale->SetOutputScalarTypeToUnsignedChar();
  
  image = scale->GetOutput();
  image->Update();
  imageChanged();
}
	
void OOFImage3D::flip(const std::string &axis) {
  // axis is a string like 'x' or 'xy'.
  for(unsigned int i=0; i<axis.size(); i++) {
    vtkSmartPointer<vtkImageFlip> flipper =
      vtkSmartPointer<vtkImageFlip>::New();
    flipper->SetFilteredAxis((int)axis[i]-(int)'x');
    flipper->SetInputConnection(image->GetProducerPort());
    image = flipper->GetOutput();
    image->Update();
  }
  imageChanged();
}

void OOFImage3D::permuteAxes(const std::string &axes) {
  // axes is a permutation of "xyz" in 3D or "xy" in 2D
  int iaxes[3];
  for(int i=0; i<DIM; i++)
    iaxes[i] = axes[i] - 'x';
#if DIM==2
  iaxes[2] = 2;
#endif // DIM==2
  vtkSmartPointer<vtkImagePermute> permute =
    vtkSmartPointer<vtkImagePermute>::New();
  permute->SetFilteredAxes(iaxes);
  permute->SetInputConnection(image->GetProducerPort());
  image = permute->GetOutput();
  image->Update();
  imageChanged();
}


// This is kind of slow for very large images.  It might make sense to
// have a progress bar.
void OOFImage3D::getColorPoints(const CColor &ref, 
				const ColorDifference &diff,
				BoolArray &selected)
  const
{
  //   for(ConstOOFImage3DIterator i=this->begin(); i!=this->end(); ++i)
  //     if (diff.contains(ref, *i)) selected[i.coord()] = true;

  int i,j,k;
  ICoord coord;
  for (i=0; i<sizeInPixels_[0]; i++) {
    for (j=0; j<sizeInPixels_[1]; j++) {
      for (k=0; k<sizeInPixels_[2]; k++) {
	coord = ICoord(i,j,k);
	if (diff.contains(ref, operator[](coord)))
	  selected[coord] = true;
      }
    }
  }

}


