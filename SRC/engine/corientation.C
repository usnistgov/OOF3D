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

#include "common/latticesystem.h"
#include "common/sincos.h"
#include "common/smallmatrix.h"
#include "engine/corientation.h"
#include "engine/ooferror.h"
#include <math.h>

COrientation::COrientation()
  : cachedrot(0)
{}

COrientation::COrientation(const COrientation &other)
  : cachedrot(0)
{
  if(other.cachedrot)
    cachedrot = new SmallMatrix(*other.cachedrot);
}

COrientation::~COrientation() {
  if(cachedrot)
    delete cachedrot;
}

const SmallMatrix &COrientation::rotation() const {
  if(!cachedrot)
    cachedrot = rotation_();
  return *cachedrot;
}

void COrientation::copyMatrix(const COrientation &other) {
  delete cachedrot;
  if(other.cachedrot != nullptr)
    cachedrot = new SmallMatrix(*other.cachedrot);
  else {
    cachedrot = nullptr;
  }
}

COrientABG COrientation::abg() const {
    return COrientABG(rotation()); 
}

COrientBunge COrientation::bunge() const {
  return COrientBunge(rotation()); 
}

COrientQuaternion COrientation::quaternion() const {
  return COrientQuaternion(rotation());
}

COrientX COrientation::X() const {
  return COrientX(rotation()); 
}

COrientXYZ COrientation::XYZ() const {
  return COrientXYZ(rotation());
}

COrientAxis COrientation::axis() const { 
  return COrientAxis(rotation());
}

COrientRodrigues COrientation::rodrigues() const {
  return COrientRodrigues(rotation());
}

double COrientation::misorientation(const COrientation &other,
				    const LatticeSymmetry &lattice)
  const
{
  // The misorientation between two orientations is the angular part
  // of the axis-angle representation of the "difference" between the
  // orientations.  The difference is the product of one orientation
  // and the inverse of the other.

  // If the two angles are identical, be sure to return exactly 0.
  // This is important when autogrouping EBSD data that may already
  // have had noise removed from it.  Compare the angle/axis form of
  // the orientations because that's what the autogroup machinery
  // uses, so it involves less calculation here.
  if(axis() == other.axis())
    return 0.0;

  SmallMatrix transp(rotation()); // copy the matrix
  transp.transpose();		  // and transpose it
  SmallMatrix diff = other.rotation() * transp;

  // When the crystal symmetry allows multiple equivalent
  // orientations, we need to measure the difference between one
  // orientation and all possible equivalent versions of the other,
  // and return the minumum misorientation.
  const std::vector<SmallMatrix> &latticerotations(lattice.matrices());
  double minangle = std::numeric_limits<double>::max();

  for(const SmallMatrix &latrot : latticerotations) {
    COrientAxis axisrot(latrot * diff);
    double angle = fabs(axisrot.angle());
    if(angle < minangle) {
      minangle = angle;
    }
  }
  return minangle;
}

double COrientation::misorientation(const COrientation &other,
				    const std::string &lattice)
  const
{
  // "lattice" is a Schoenflies symbol
  return misorientation(other, *getLatticeSymmetry(lattice));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the weighted average of this orientation and the given
// orientation.  Call this orientation O0 and define the rotation R by
// O1 = R*O0.  Write R as a COrientAxis, R=A(X, theta) where X is the
// axis.  Then if alpha is the relative weight (alpha=0 ==> O0,
// alpha=1 ==> O1), the weighted average is A(X, alpha*theta)*O0.

COrientAxis COrientation::weightedAverage(double w0, double w1,
					  const COrientation &orient1)
  const
{
  return weightedAverage(w0, w1, orient1.rotation());
}

COrientAxis COrientation::weightedAverage(double w0, double w1,
					  const SmallMatrix &m1)
  const
{
  assert(w0 + w1 > 0.0);
  const SmallMatrix &m0 = rotation(); // not a copy
  SmallMatrix m1t(m1);		      // copy
  m1t.transpose();		      // in-place transpose
  COrientAxis r(m0*m1t);
  COrientAxis partial(r.angle()*w1/(w0+w1), r.x(), r.y(), r.z());
  return COrientAxis(partial.rotation()*m0);
}

// If lattice symmetry needs to be taken into account, first choose
// the equivalent O1 that is closest to O0.
// If L*O1 = R*O0 for a lattice symmetry L, R = L*O1*O0^T

COrientAxis COrientation::weightedAverage(double w0, double w1,
					  const COrientation &orient1,
					  const LatticeSymmetry &lattice)
  const
{
  // Find the equivalent orient1 that's closest to this.  The
  // equivalents are L*orient1 for L in the set of lattice symmetry
  // rotations.
  SmallMatrix m0t = rotation();	// copy of matrix for this orientation
  m0t.transpose();
  SmallMatrix m1 = orient1.rotation(); // matrix for orient1
  SmallMatrix diff = m1*m0t;	// O1 * O0^T in matrix form
  
  const std::vector<SmallMatrix> &latticerotations(lattice.matrices());
  double minangle = std::numeric_limits<double>::max();
  int closest = -1;
  for(int i=0; i<latticerotations.size(); i++) {
    COrientAxis axisrot(latticerotations[i]*diff); // L * O1 * O0^T
    double angle = fabs(axisrot.angle());
    if(angle < minangle) {
      minangle = angle;
      closest = i;
    }
  }
  return weightedAverage(w0, w1, latticerotations[closest]*m1);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


COrientABG::COrientABG(const SmallMatrix &matrix) {
  double cosa = matrix(2,2);
  double sina = sqrt(matrix(2,0)*matrix(2,0) + matrix(2,1)*matrix(2,1));
  double sinb, cosb, sing, cosg;
  if(sina != 0.0) {
    // Skip division by sina, it just gets eaten by the arctangent.
    cosb = matrix(2,0);
    sinb = matrix(2,1);
    cosg = -matrix(0,2);
    sing = matrix(1,2);
  }
  else {
    if(cosa > 0.0) {		// i.e., it's 1.0, but there's roundoff.
      cosb = matrix(0,0);
      sinb = matrix(0,1);
      sing = 0.0;
      cosg = 1.0;
    }
    else {			// In this case, cosa must be -1.
      cosb = -matrix(0,0);
      sinb = -matrix(0,1);
      sing = 0.0;
      cosg = 1.0;
    }
  }
  alpha_ = atan2(sina, cosa);
  beta_ = atan2(sinb, cosb);
  gamma_ = atan2(sing, cosg);
}

const COrientation &COrientABG::copyFrom(const COrientation &other) {
  const COrientABG othr(other.abg());
  alpha_ = othr.alpha();
  beta_ = othr.beta();
  gamma_ = othr.gamma();
  copyMatrix(othr);
  return *this;
}

SmallMatrix *COrientABG::rotation_() const {
  double cosa, sina, cosb, sinb, cosg, sing;
  sincos(alpha_, sina, cosa);
  sincos(beta_, sinb, cosb);
  sincos(gamma_, sing, cosg);
  
  SmallMatrix *r = new SmallMatrix(3, 3);
  (*r)(0, 0) =  cosa*cosb*cosg - sinb*sing;
  (*r)(0, 1) =  cosa*sinb*cosg + cosb*sing;
  (*r)(0, 2) = -sina*cosg;
  (*r)(1, 0) = -cosa*cosb*sing - sinb*cosg;
  (*r)(1, 1) = -cosa*sinb*sing + cosb*cosg;
  (*r)(1, 2) =  sina*sing;
  (*r)(2, 0) =  sina*cosb;
  (*r)(2, 1) =  sina*sinb;
  (*r)(2, 2) =  cosa;
  return r;
}

bool COrientABG::operator==(const COrientABG &other) const {
  return alpha_==other.alpha_ && beta_==other.beta_ && gamma_==other.gamma_;
}

bool COrientABG::operator!=(const COrientABG &other) const {
  return alpha_!=other.alpha_ || beta_!=other.beta_ || gamma_!=other.gamma_;
}

void COrientABG::print(std::ostream &os) const {
  os << "COrientABG(alpha=" << alpha()*180/M_PI << ", beta=" << beta()*180/M_PI
     << ", gamma=" << gamma()*180/M_PI << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

COrientBunge::COrientBunge(const SmallMatrix &matrix) {
  double costh = matrix(2,2);
  double sinth = sqrt(matrix(2,0)*matrix(2,0) + matrix(2,1)*matrix(2,1));
  double cosph1, sinph1, cosph2, sinph2;
  if(sinth != 0.0) {
    //  Strictly speaking, should divide by sinth, but they go
    //  into the arctangent, so the common factor would cancel
    //  anyways, so skip it.
    cosph1 = -matrix(1,2);
    sinph1 = matrix(0,2);
    cosph2 = matrix(2,1);
    sinph2 = matrix(2,0);
  }
  else {
    // Same-axis rotation, so let phi2 be zero, and figure out phi1.
    cosph1 = matrix(0,0);
    sinph1 = matrix(1,0);
    cosph2 = 1.0;
    sinph2 = 0.0;
  }
  phi1_ = atan2(sinph1, cosph1);
  theta_ = atan2(sinth, costh);
  phi2_ = atan2(sinph2, cosph2);
};

const COrientation &COrientBunge::copyFrom(const COrientation &other) {
  const COrientBunge othr(other.bunge());
  phi1_ = othr.phi1();
  theta_ = othr.theta();
  phi2_ = othr.phi2();
  copyMatrix(othr);
  return *this;
}

SmallMatrix *COrientBunge::rotation_() const {
  double sinph1, cosph1, sinph2, cosph2, sinth, costh;
  sincos(phi1_, sinph1, cosph1);
  sincos(phi2_, sinph2, cosph2);
  sincos(theta_, sinth, costh);
  SmallMatrix *r = new SmallMatrix(3,3);
  (*r)(0,0) = cosph1*cosph2-sinph1*sinph2*costh;
  (*r)(0,1) = -cosph1*sinph2-sinph1*cosph2*costh;
  (*r)(0,2) = sinph1*sinth;

  (*r)(1,0) = sinph1*cosph2+cosph1*sinph2*costh;
  (*r)(1,1) = -sinph1*sinph2+cosph1*cosph2*costh;
  (*r)(1,2) = -cosph1*sinth;

  (*r)(2,0) = sinph2*sinth;
  (*r)(2,1) = cosph2*sinth;
  (*r)(2,2) = costh;
  return r;
}

void COrientBunge::print(std::ostream &os) const {
  os << "COrientBunge(phi1=" << phi1()*180/M_PI
     << ", theta=" << theta()*180/M_PI
     << ", phi2=" << phi2()*180/M_PI << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

COrientQuaternion::COrientQuaternion(double e0, double e1,
				     double e2, double e3)
{
  q[0] = e0;
  q[1] = e1;
  q[2] = e2;
  q[3] = e3;
  // Un-normalized quaternions are probably dangerous, they
  // result in all the entries in the matrix being too large by a
  // factor of the normalization squared, which means the deduced
  // cosine from the "corner" entry will be wrong.  So, normalize.
  double n2 = norm2();
  if(n2==0.0) { // Presume the user meant "no rotation".
    q[0] = 1.0;
    for(unsigned int i=1; i<4; i++)
      q[i] = 0.0;
  }
  else {
    double norm = 1./sqrt(n2);
    for(unsigned int i=0; i<4; i++)
      q[i] *= norm;
  }
}

COrientQuaternion::COrientQuaternion(const SmallMatrix &matrix) {
  // See https://en.wikipedia.org/wiki/Rotation_matrix#Quaternion
  double t = matrix(0,0) + matrix(1,1) + matrix(2,2);
  if(t > 0) {
    double r = sqrt(1 + t);
    double s = 1/(2*r);
    q[0] = r/2.;
    q[1] = (matrix(1,2) - matrix(2,1))*s;
    q[2] = (matrix(2,0) - matrix(0,2))*s;
    q[3] = (matrix(0,1) - matrix(1,0))*s;
  } // end if t > 0
  else {
    // If the trace is negative (near -1, actually) we could be
    // dividing by something small in the expression above, so don't
    // do that.  This version is copied from
    // http://www.gamasutra.com/view/feature/131686/rotating_objects_using_quaternions.php
    // and implements the algorithm suggested in the wikipedia
    // article.
    int i = 0; 		
    if(matrix(1,1) > matrix(0,0)) i = 1;
    if(matrix(2,2) > matrix(i,i)) i = 2;
    int j = (i+1) % 3;
    int k = (j+1) % 3;
    double s = sqrt(1. + matrix(i,i) - matrix(j,j) - matrix(k,k));
    q[i] = 0.5*s;
    if(s != 0)
      s = 0.5/s;
    q[3] = (matrix(k,j) - matrix(j,k))*s;
    q[j] = (matrix(j,i) + matrix(i,j))*s;
    q[k] = (matrix(k,i) + matrix(i,k))*s;
  }
}

const COrientation &COrientQuaternion::copyFrom(const COrientation &other) {
  const COrientQuaternion othr(other.quaternion());
  for(unsigned int i=0; i<4; i++)
    q[i] = othr.q[i];
  copyMatrix(othr);
  return *this;
}

double COrientQuaternion::norm2() const {
  double sum = 0;
  for(unsigned int i=0; i<4; i++)
    sum += q[i]*q[i];
  return sum;
}

SmallMatrix *COrientQuaternion::rotation_() const {
  SmallMatrix *matrix = new SmallMatrix(3,3);

  double q0 = q[0];
  double q1 = q[1];
  double q2 = q[2];
  double q3 = q[3];

  (*matrix)(0,0) = q0*q0 + q1*q1 - q2*q2 - q3*q3;
  (*matrix)(0,1) = 2.0*(q1*q2 + q0*q3);
  (*matrix)(0,2) = 2.0*(q1*q3 - q0*q2);

  (*matrix)(1,0) = 2.0*(q1*q2 - q0*q3);
  (*matrix)(1,1) = q0*q0 - q1*q1 + q2*q2 - q3*q3;
  (*matrix)(1,2) = 2.0*(q2*q3 + q0*q1);

  (*matrix)(2,0) = 2.0*(q1*q3 + q0*q2);
  (*matrix)(2,1) = 2.0*(q2*q3 - q0*q1);
  (*matrix)(2,2) = q0*q0 - q1*q1 - q2*q2 + q3*q3;

  return matrix;
}

COrientAxis COrientQuaternion::axis() const {
  double vnorm = sqrt(q[1]*q[1] + q[2]*q[2] + q[3]*q[3]); // norm of vector part
  double angle = 2*atan2(vnorm, q[0]);
  return COrientAxis(angle, q[1]/vnorm, q[2]/vnorm, q[3]/vnorm);
}

void COrientQuaternion::print(std::ostream &os) const {
  os << "COrientQuaternion(e0=" << e0() << ", e1=" << e1() << ", e2=" << e2()
     << ", e3=" << e3() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Goldstein's "X" convention.  This may have some other more
// descriptive name, but I don't know what it is.  Rotations are z,x,z.

COrientX::COrientX(const SmallMatrix &matrix) {
  double costh = matrix(2,2);
  double sinth = sqrt(matrix(0,2)*matrix(0,2)+ matrix(1,2)*matrix(1,2));
  double sinps, cosps, sinph, cosph;
  if(sinth != 0.0) {
    // Skip division by sinth in these terms, since the common factor
    // will cancel out in the arctangent anyways.
    cosps = matrix(1,2);
    sinps = matrix(0,2);
    cosph = -matrix(2,1);
    sinph = matrix(2,0);
  }
  else {
    // Same-axis rotation, let psi be zero, figure out phi.
    cosph = matrix(0,0);
    sinph = matrix(0,1);
    cosps = 1.0;
    sinps = 0.0;
  }
  phi_ = atan2(sinph, cosph);
  theta_ = atan2(sinth, costh);
  psi_ = atan2(sinps, cosps);
}

const COrientation &COrientX::copyFrom(const COrientation &other) {
  const COrientX othr(other.X());
  phi_ = othr.phi();
  theta_ = othr.theta();
  psi_ = othr.psi();
  copyMatrix(othr);
  return *this;
}

SmallMatrix *COrientX::rotation_() const {
  double sinph, cosph, sinps, cosps, sinth, costh;
  sincos(phi_, sinph, cosph);
  sincos(theta_, sinth, costh);
  sincos(psi_, sinps, cosps);

  SmallMatrix *matrix = new SmallMatrix(3,3);

  (*matrix)(0,0) = cosps*cosph - costh*sinph*sinps;
  (*matrix)(0,1) = cosps*sinph + costh*cosph*sinps;
  (*matrix)(0,2) = sinps*sinth;

  (*matrix)(1,0) = -sinps*cosph - costh*sinph*cosps;
  (*matrix)(1,1) = -sinps*sinph + costh*cosph*cosps;
  (*matrix)(1,2) = cosps*sinth;

  (*matrix)(2,0) = sinth*sinph;
  (*matrix)(2,1) = -sinth*cosph;
  (*matrix)(2,2) = costh;

  return matrix;
};

void COrientX::print(std::ostream &os) const {
  os << "COrientX(phi=" << phi()*180/M_PI << ", theta=" << theta()*180/M_PI
     << ", psi=" << psi()*180/M_PI << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The "aerodynamic" XYZ convention, with each rotation about a
// different principal axis.  Again the name is from Goldstein.

COrientXYZ::COrientXYZ(const SmallMatrix &matrix) {
  double sinth = matrix(2,0);
  double  costh = sqrt(matrix(2,2)*matrix(2,2)+
		       matrix(2,1)*matrix(2,1));
  double sinph, cosph, sinps, cosps;
  if(costh!=0.0) {
    // Strictly speaking, the sin of phi is this quantity divided by
    // the cosine of theta, but since both terms are divided, and they
    // go into an arctangent routine, we just skip it, and get the
    // same answer.
    sinph = -matrix(2,1);
    cosph = matrix(2,2);
    sinps = -matrix(1,0);
    cosps = matrix(0,0);
  }
  else {
    sinph = matrix(0,1);
    cosph = matrix(1,1);
    sinps = 0.0;
    cosps = 1.0;
  }
  phi_ = atan2(sinph, cosph);
  theta_ = atan2(sinth, costh);
  psi_ = atan2(sinps, cosps);
}

const COrientation &COrientXYZ::copyFrom(const COrientation &other) {
  const COrientXYZ othr(other.XYZ());
  phi_ = othr.phi();
  theta_ = othr.theta();
  psi_ = othr.psi();
  copyMatrix(othr);
  return *this;
}

SmallMatrix *COrientXYZ::rotation_() const {
  double sinph, cosph, sinps, cosps, sinth, costh;
  sincos(phi_, sinph, cosph);
  sincos(theta_, sinth, costh);
  sincos(psi_, sinps, cosps);

  SmallMatrix *matrix = new SmallMatrix(3,3);

  (*matrix)(0,0) = cosps*costh;
  (*matrix)(0,1) = cosps*sinph*sinth+cosph*sinps;
  (*matrix)(0,2) = sinph*sinps-cosph*cosps*sinth;

  (*matrix)(1,0) = -costh*sinps;
  (*matrix)(1,1) = cosph*cosps-sinph*sinps*sinth;
  (*matrix)(1,2) = cosph*sinps*sinth+cosps*sinph;

  (*matrix)(2,0) = sinth;
  (*matrix)(2,1) = -costh*sinph;
  (*matrix)(2,2) = cosph*costh;

  return matrix;
}

void COrientXYZ::print(std::ostream &os) const {
  os << "COrientXYZ(phi=" << phi()*180/M_PI << ", theta=" << theta()*180/M_PI
     << ", psi=" << psi()*180/M_PI << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

COrientAxis::COrientAxis(const SmallMatrix &matrix) {
  COrientQuaternion quat(matrix);
  double sin_half_theta = sqrt(quat.e1()*quat.e1()+quat.e2()*quat.e2()+
			     quat.e3()*quat.e3());
  double cos_half_theta = quat.e0();
  angle_ = 2.0*atan2(sin_half_theta, cos_half_theta);
  // Assume z-axis in the absence of clues.
  if(sin_half_theta == 0.0) {
    x_ = 0.0;
    y_ = 0.0;
    z_ = 1.0;
  }
  else {
    double scale = 1./sin_half_theta;
    x_ = quat.e1()*scale;
    y_ = quat.e2()*scale;
    z_ = quat.e3()*scale;
  }
}

const COrientation &COrientAxis::copyFrom(const COrientation &other) {
  const COrientAxis othr(other.axis());
  angle_ = othr.angle();
  x_ = othr.x();
  y_ = othr.y();
  z_ = othr.z();
  copyMatrix(othr);
  return *this;
}

SmallMatrix *COrientAxis::rotation_() const {
  return quaternion().rotation_();
}

COrientQuaternion COrientAxis::quaternion() const {
  double cos_half_theta, sin_half_theta;
  sincos(0.5*angle_, sin_half_theta, cos_half_theta);
  double norm2 = x_*x_ + y_*y_ + z_*z_;
  assert(norm2 != 0.0);
  double factor = sin_half_theta/sqrt(norm2);
  return COrientQuaternion(cos_half_theta, x_*factor, y_*factor, z_*factor);
}

bool COrientAxis::operator==(const COrientAxis &other) const {
  return angle_==other.angle_ && x_==other.x_ && y_==other.y_ && z_==other.z_;
}

bool COrientAxis::operator!=(const COrientAxis &other) const {
  return angle_!=other.angle_ || x_!=other.x_ || y_!=other.y_ || z_!=other.z_;
}

void COrientAxis::print(std::ostream &os) const {
  os << "COrientAxis(angle=" << angle()*180/M_PI
     << ", x=" << x() << ", y=" << y() << ", z=" << z() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Rodrigues vector. Another way of describing crystal orientations.
// This form is quite popular in the texture community; it is
// particularly useful to describe fiber-texture and poling in
// ferroelectrics. --REG

// The vector points along the axis of the rotation, and its magnitude
// is the tangent of half the angle of the rotation.

COrientRodrigues::COrientRodrigues(const SmallMatrix &matrix) {
  COrientQuaternion quat(matrix);
  double norm;			// secant of half of the rotation angle
  if(quat.e0() != 0.0) {
    norm = 1./quat.e0();
  }
  else {
    // The Rodrigues vector has a singularity at theta = \pm pi.  We
    // want to avoid the singularity, so we set 1/cos(pi/2) = 2.e9.
    // acos(1/2.e9) is within 10^-9 of pi/2, which ought to be good
    // enough precision for an orientation.
    norm = 2.0e9;
  }
  r1_ = quat.e1()*norm;
  r2_ = quat.e2()*norm;
  r3_ = quat.e3()*norm;
  // The above relationship was extracted from A. Heinz, and
  // P. Neumann "Representation of Orientation and Disorientation Data
  // for Cubic, Hexagonal, Tetragonal, and Orthorhombic
  // Crystals". Acta Cryst. (1991) A47, 780-789
}

const COrientation &COrientRodrigues::copyFrom(const COrientation &other) {
  const COrientRodrigues othr(other.rodrigues());
  r1_ = othr.r1_;
  r2_ = othr.r2_;
  r3_ = othr.r3_;
  copyMatrix(othr);
  return *this;
}

SmallMatrix *COrientRodrigues::rotation_() const {
  double mag2 = r1_*r1_ + r2_*r2_ + r3_*r3_;
  double q0 = 1./sqrt(1.0 + mag2);
  return COrientQuaternion(q0, q0*r1_, q0*r2_, q0*r3_).rotation_();
  // The above equations were taken from A. Morawiec, and D. P. Field
  // "Rodrigues parametrization for orientation and misorientation
  // distributions". Phylosophical Magazine A, 1996, Vol. 73, No. 4,
  // 1113-1130
}

void COrientRodrigues::print(std::ostream &os) const {
  os << "COrientRodrigues(r1=" << r1() << ", r2=" << r2() << ", r3=" << r3()
     << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const COrientation &orient) {
  orient.print(os);
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Stuff added to make COrientations usable as OutputVals.

const std::string &COrientation::modulename() const {
  static const std::string nm = "ooflib.SWIG.engine.corientation";
  return nm;
}

static double degrees = 180./M_PI;

// -----------

// The strings in COrientation::arguments are used when constructing
// the OIndex and OIterators that the OutputVal machinery uses when
// getting the components of an output.  The strings are identical to
// the names of the python Parameters for each COrientation
// constructor and the names of the C++ retrieval methods for the
// values.  Can this triplication be eliminated?

const std::vector<std::string> COrientABG::arguments(
					     {"alpha", "beta", "gamma"});

const std::string &COrientABG::classname() const {
  static const std::string nm("COrientABG");
  return nm;
}

COrientABG *COrientABG::clone() const {
  return new COrientABG(*this); 
}

COrientABG *COrientABG::zero() const {
  return new COrientABG(0., 0., 0.);
}

std::vector<double> *COrientABG::value_list() const {
  return new std::vector<double>(
			 {degrees*alpha_, degrees*beta_, degrees*gamma_});
}

// ---------

const std::vector<std::string> COrientBunge::arguments(
					       {"phi1", "theta", "phi2"});

const std::string &COrientBunge::classname() const {
  static const std::string nm("COrientBunge");
  return nm;
}

COrientBunge *COrientBunge::clone() const {
  return new COrientBunge(*this);
};

COrientBunge *COrientBunge::zero() const {
  return new COrientBunge(0., 0., 0.);
}

std::vector<double> *COrientBunge::value_list() const {
  return new std::vector<double>(
			 {degrees*phi1_, degrees*theta_, degrees*phi2_});
}

// ---------

const std::vector<std::string> COrientQuaternion::arguments(
						    {"e0", "e1", "e2", "e3"});

const std::string &COrientQuaternion::classname() const {
  static const std::string nm("COrientQuaternion");
  return nm;
}

COrientQuaternion *COrientQuaternion::clone() const {
  return new COrientQuaternion(*this);
};

COrientQuaternion *COrientQuaternion::zero() const {
  return new COrientQuaternion(0., 0., 0., 0.); 
}

std::vector<double> *COrientQuaternion::value_list() const {
  return new std::vector<double>{q[0], q[1], q[2], q[3]};
}

// --------

const std::vector<std::string> COrientX::arguments({"phi", "theta", "psi"});

const std::string &COrientX::classname() const {
  static const std::string nm("COrientX");
  return nm;
}

COrientX *COrientX::clone() const {
  return new COrientX(*this);
};

COrientX *COrientX::zero() const {
  return new COrientX(0., 0., 0.);
}

std::vector<double> *COrientX::value_list() const {
  return new std::vector<double>({degrees*phi_, degrees*theta_, degrees*psi_});
}

// ---------

const std::vector<std::string> COrientXYZ::arguments({"phi", "theta", "psi"});

const std::string &COrientXYZ::classname() const {
  static const std::string nm("COrientXYZ");
  return nm;
}

COrientXYZ *COrientXYZ::clone() const {
  return new COrientXYZ(*this);
};

COrientXYZ *COrientXYZ::zero() const {
  return new COrientXYZ(0., 0., 0.);
}

std::vector<double> *COrientXYZ::value_list() const {
  return new std::vector<double>({degrees*phi_, degrees*theta_, degrees*psi_});
}

// ---------

const std::vector<std::string> COrientAxis::arguments({"angle", "x", "y", "z"});

const std::string &COrientAxis::classname() const {
  static const std::string nm("COrientAxis");
  return nm;
}

COrientAxis *COrientAxis::clone() const {
  return new COrientAxis(*this);
};

COrientAxis *COrientAxis::zero() const {
  return new COrientAxis(0., 0., 0., 0.);
}

std::vector<double> *COrientAxis::value_list() const {
  return new std::vector<double>({degrees*angle_, x_, y_, z_});
}

// ---------

const std::vector<std::string> COrientRodrigues::arguments({"r1", "r2", "r3"});

const std::string &COrientRodrigues::classname() const {
  static const std::string nm("COrientRodrigues");
  return nm;
}

COrientRodrigues *COrientRodrigues::clone() const {
  return new COrientRodrigues(*this);
};

COrientRodrigues *COrientRodrigues::zero() const {
  return new COrientRodrigues(0., 0., 0.);
}

std::vector<double> *COrientRodrigues::value_list() const {
  return new std::vector<double>({r1_, r2_, r3_});
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: Is there a way to do this automatically, without having to
// list each COrientation subclass here?  This is called by
// OrientationPropertyOutputInit to create an OutputVal of the correct
// type before computing an Output.

COrientation *orientationFactory(const std::string *name) {
  // The names used here are the names used in the
  // OrientationRegistrations in engine/IO/orientationmatrix.py.
  if(*name == "Abg")
    return new COrientABG(0.0, 0.0, 0.0);
  if(*name == "X")
    return new COrientX(0.0, 0.0, 0.0);
  if(*name == "XYZ")
    return new COrientXYZ(0.0, 0.0, 0.0);
  if(*name == "Quaternion")
    return new COrientQuaternion(0.0, 0.0, 0.0, 0.0);
  if(*name == "Axis")
    return new COrientAxis(0.0, 0.0, 0.0, 0.0);
  if(*name == "Rodrigues")
    return new COrientRodrigues(0.0, 0.0, 0.0);
  if(*name == "Bunge")
    return new COrientBunge(0.0, 0.0, 0.0);
  throw ErrProgrammingError("Unrecognized COrientation type! " + *name,
			    __FILE__, __LINE__);
}

COrientation *OrientationPropertyOutputInit::operator()(
				     const NonArithmeticPropertyOutput *output,
				     const FEMesh*,
				     const Element*,
				     const MasterCoord&) const
{
  // Initialize the output with a COrientation in the desired format.
  // In the Properties' output() methods, the orientation will be
  // copied into the object created here, and converted if necessary.
  const std::string *fmt = output->getEnumParam("format");
  return orientationFactory(fmt);
}


