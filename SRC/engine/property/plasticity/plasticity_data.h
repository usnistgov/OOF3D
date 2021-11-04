// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef PLASTICITY_DATA_H
#define PLASTICITY_DATA_H

#include "engine/element.h"
#include "common/smallmatrix.h"
#include "engine/smallmatrix3.h"
#include "engine/symmmatrix3.h"
#include "engine/property/plasticity/constitutive_base.h"
#include <string>
#include <map>



// Utility class, definitely needs optimization, probably should
// be in a different file. 
class Rank4_3DTensor {
private:
  std::vector<double> data;
  static int _index(unsigned int i, unsigned int j,
		    unsigned int k, unsigned int l) {
    return  ((i*3+j)*3+k)*3+l;
  };
public:
  Rank4_3DTensor() : data(81) { this->clear(); };
  Rank4_3DTensor(SmallMatrix &s);
  Rank4_3DTensor(const Rank4_3DTensor&);
  void clear();
  double &operator()(unsigned int i, unsigned int j,
		     unsigned int k, unsigned int l);
  const double &operator()(unsigned int i, unsigned int j,
			   unsigned int k, unsigned int l) const;
  SmallMatrix as_smallmatrix(); // 9x9?  Or 6x6 with magic inner product?
  SmallMatrix as_6matrix();     // 6x6 version.

  friend std::ostream& operator<<(std::ostream &o,
				 const Rank4_3DTensor &t);
};

std::ostream& operator<<(std::ostream &, const Rank4_3DTensor&);


//----------------------------------------------------------
// Data containers for plasticty data. Instantiated
// at gausspoints, and repositories of the non-nodal
// state info.



// Per-gaussponit plastic data, generally needed by all constitutive
// rules. This is the per-gausspoint object contained in the the
// PlasticData container.  It's not expected to be subclassed.
class GptPlasticData {
public:
  GptPlasticData();

  SmallMatrix3 ft;       // Deformation tensor at prior time t
  SmallMatrix3 fpt;      // Plastic part of F at prior time t.
  SmallMatrix3 f_tau;    // Deformation tensor at current time tau.
  SmallMatrix3 fp_tau;   // Plastic part of F at current time tau.
  SmallMatrix3 fe_tau;   // Elastic part of F at current time tau.
  SymmMatrix3 cauchy;   // Cauchy stress (time tau?)
  SmallMatrix3 s_star;   // 2nd PK stress at time tau.
  Rank4_3DTensor w_mat;          // Elastoplastic tangent, at tau, when done.

  friend std::ostream &operator<<(std::ostream&, const GptPlasticData&); 
};


// The ElementData class is a PythonExportable, and in the case where
// it's SWIGged, requires class and module metadata so that Python can
// access derived-class objects from a wrapped base-class pointer.  We
// don't actually do this here, but we might, so an alternate
// mechanism has not been constructed.  These static variables are
// here because the return value of the module and class name
// functions is a reference to a string, and if you just use a
// literal, you end up returning a reference to a temporary.
static std::string elementdataclassname_plastic = "PlasticData";
static std::string elementdataclassname_slip = "SlipData";
static std::string plasticitymodulename = "plasticity";


// PlasticData needs to know about time.  It should have a
// notion of a current time and a previous time, and a way
// of noticing if it's working at a new time.
class PlasticData : public ElementData {
public:
  PlasticData(int o,const Element *e);
  virtual const std::string &classname() const {
    return elementdataclassname_plastic; }
  virtual const std::string &modulename() const {
    return plasticitymodulename; }
  int order;
  std::map<MasterCoord,int> mctogpi_map;
  std::vector<GptPlasticData*> gptdata;
  double dt;
  double current_time;
  double set_time(double);
};


// Base class for constitutive-rule-specific info.  The SlipData
// container has pointers to the base class, individual constitutive
// rules define derived classes that have the relevant data.
class GptSlipData {
public:
  std::vector<double> delta_gamma; 
  std::vector<double> dgamma_dtau;
  std::vector<double> tau_alpha; // Resolved shear stresses.
  GptSlipData(int nslips);
};


class SlipData : public ElementData {
public:
  SlipData(int o, const PlasticConstitutiveRule *r, const Element *e);
  ~SlipData();
  virtual const std::string &classname() const {
    return elementdataclassname_slip; }
  virtual const std::string &modulename() const {
    return plasticitymodulename; }
  int order;
  std::vector<GptSlipData*> gptslipdata;
};



static std::vector<std::vector<int> > voigt9 = {{0,5,4},{8,1,3},{7,6,2}};

#endif
