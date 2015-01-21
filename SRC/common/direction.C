// -*- C++ -*-
// $RCSfile: direction.C,v $
// $Revision: 1.1.2.10 $
// $Author: langer $
// $Date: 2014/07/29 20:26:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/coord.h"
#include "common/corientation.h"
#include "common/differ.h"
#include "common/direction.h"
#include "common/ooferror.h"
#include "common/smallmatrix.h"
#include "common/tostring.h"

#include <math.h>

// CUnitVectorDirection Direction::rotate(const COrientation &orientation) const {
//   return rotate(orientation.rotation());
// }

const std::string &CDirection::modulename() const {
  static const std::string name("ooflib.SWIG.common.direction");
  return name;
}

CDirection::CDirection() {}

CDirection::~CDirection() {}

std::ostream &operator<<(std::ostream &os, const CDirection &dir) {
  return os << "CDirection(" << *dir.identifier() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static void normalize(double &x, double &y, double &z) {
  double n2 = x*x + y*y + z*z;
  if(n2 == 0)
    throw ErrUserError("Direction vector has zero magnitude!");
  double n = sqrt(n2);
  x /= n;
  y /= n;
  z /= n;
}

CUnitVectorDirection::CUnitVectorDirection(double x, double y, double z)
  : vec(3)
{
  vec[0] = x;
  vec[1] = y;
  vec[2] = z;
  normalize(vec[0], vec[1], vec[2]);
}

CUnitVectorDirection::CUnitVectorDirection(const DoubleVec *xyz)
  : vec(*xyz)
{
  normalize(vec[0], vec[1], vec[2]);
}

CUnitVectorDirection::CUnitVectorDirection(const Coord *coord) {
  vec[0] = coord->x[0];
  vec[1] = coord->x[1];
#if DIM==3
  vec[2] = coord->x[2];
#endif	// DIM==3
}

const std::string &CUnitVectorDirection::classname() const {
  static const std::string name("CUnitVectorDirection");
  return name;
}

double CUnitVectorDirection::theta() const {
  return acos(vec[2]);
}

double CUnitVectorDirection::phi() const {
  return atan2(vec[1], vec[0]);
}

CAngleDirection CUnitVectorDirection::angles() const {
  return CAngleDirection(theta(), phi());
}

Coord *CUnitVectorDirection::coord() const {
  return new Coord(vec[0], vec[1], vec[2]);
}

double CUnitVectorDirection::dot(const Coord *pt) const {
  return vec[0]*(*pt)[0] + vec[1]*(*pt)[1]
#if DIM==3
    + vec[2]*(*pt)[2]
#endif // DIM==3
    ;
}

CUnitVectorDirection CUnitVectorDirection::matmult(const SmallMatrix &rmatrix)
const
{
  DoubleVec prod = rmatrix*vec;
  return CUnitVectorDirection(&prod);
}

std::string *CUnitVectorDirection::identifier() const {
  return new std::string("x=" + to_string(x()) + 
			 " y=" + to_string(y()) + 
			 " z=" + to_string(z()));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &CDirectionX::classname() const {
  static const std::string name("CDirectionX");
  return name;
}

CUnitVectorDirection CDirectionX::unitVector() const {
  return CUnitVectorDirection(1.0, 0.0, 0.0);
}

CAngleDirection CDirectionX::angles() const {
  return CAngleDirection(M_PI/2., 0.0);
}

CUnitVectorDirection CDirectionX::matmult(const SmallMatrix &mat) const {
  return unitVector().matmult(mat);
}

double CDirectionX::dot(const Coord *c) const {
  return (*c)[0];
}

Coord *CDirectionX::coord() const {
  return new Coord(1.0, 0.0, 0.0);
}

std::string *CDirectionX::identifier() const {
  return new std::string("X");
}

//=\\=//

const std::string &CDirectionY::classname() const {
  static const std::string name("CDirectionY");
  return name;
}

CUnitVectorDirection CDirectionY::unitVector() const {
  return CUnitVectorDirection(0.0, 1.0, 0.0);
}

CAngleDirection CDirectionY::angles() const {
  return CAngleDirection(M_PI/2., M_PI/2.);
}

CUnitVectorDirection CDirectionY::matmult(const SmallMatrix &mat) const {
  return unitVector().matmult(mat);
}

double CDirectionY::dot(const Coord *c) const {
  return (*c)[1];
}

Coord *CDirectionY::coord() const {
  return new Coord(0.0, 1.0, 0.0);
}

std::string *CDirectionY::identifier() const {
  return new std::string("Y");
}

//=\\=//

const std::string &CDirectionZ::classname() const {
  static const std::string name("CDirectionZ");
  return name;
}

CUnitVectorDirection CDirectionZ::unitVector() const {
  return CUnitVectorDirection(0.0, 0.0, 1.0);
}

CAngleDirection CDirectionZ::angles() const {
  return CAngleDirection(0., 0.);
}

CUnitVectorDirection CDirectionZ::matmult(const SmallMatrix &mat) const {
  return unitVector().matmult(mat);
}

double CDirectionZ::dot(const Coord *c) const {
  return (*c)[2];
}

Coord *CDirectionZ::coord() const {
  return new Coord(0.0, 0.0, 1.0);
}

std::string *CDirectionZ::identifier() const {
  return new std::string("Z");
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CAngleDirection::CAngleDirection(double theta, double phi)
  : theta_(theta),
    phi_(phi)
{}

const std::string &CAngleDirection::classname() const {
  static const std::string name("CAngleDirection");
  return name;
}

CUnitVectorDirection CAngleDirection::unitVector() const {
  double rxy = sin(theta_);
  return CUnitVectorDirection(rxy*cos(phi_), rxy*sin(phi_), cos(theta_));
}

Coord *CAngleDirection::coord() const {
  return unitVector().coord();
}

double CAngleDirection::dot(const Coord *pt) const {
  return unitVector().dot(pt);
}

CUnitVectorDirection CAngleDirection::matmult(const SmallMatrix &rmatrix) const 
{
  return unitVector().matmult(rmatrix);
}

std::string *CAngleDirection::identifier() const {
  return new std::string("theta=" + to_string(180*theta()/M_PI) +
			 " phi=" + to_string(180*phi()/M_PI));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CUnitVectorDirection operator*(const SmallMatrix &mat, const CDirection &v) {
  return v.matmult(mat);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool CDirection::operator==(const CDirection &other) const {
  CUnitVectorDirection ua = unitVector();
  CUnitVectorDirection ub = other.unitVector();
  return ua == ub;
}

bool CUnitVectorDirection::operator==(const CUnitVectorDirection &other) const {
  return !(differ(x(), other.x()) ||
	   differ(y(), other.y()) ||
	   differ(z(), other.z()));
}

bool CAngleDirection::operator==(const CAngleDirection &other) const {
  return !(differ(theta(),other.theta()) || differ(phi(), other.phi()));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//

bool CDirection::operator<(const CDirection &other) const {
  CUnitVectorDirection ua = unitVector();
  CUnitVectorDirection ub = other.unitVector();
  return ua < ub;
}

bool CUnitVectorDirection::operator<(const CUnitVectorDirection &other) const {
  return (x() < other.x() ||
	  (x() == other.x() && ((y() < other.y()) ||
				(y() == other.y() && z() < other.z())))
	  );
}

// There's no CAngleDirection::operator<(const CAngleDirection&)
// because it would be hard to ensure that it gives the same ordering
// as CUnitVectorDirection::operator<(const CUnitVectorDirection&) on
// the equivalent directions.
