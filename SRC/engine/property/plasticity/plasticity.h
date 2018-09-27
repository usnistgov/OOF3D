// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// Plasticity property, v0.1.  This implements quasi-static crystal
// plasticity, and requires a fixed-step non-adaptive time-stepper
// and a large-deformation equation.

// Operationally speaking it works like a nonlinear elasticity, the
// way in which it contributes to the stiffness matrix is through the
// stress flux, but the stress derivatives are the elasto-plastic ones
// that take into account the additional yield that would occur if you
// incremented the displacements.  The plastic constitutive rule is a
// parameter to this object, not yet written.

// Crystal plasticity classes are richer than that, though, they also
// know the crystallography, and can construct the Schmid tensors for
// common crystal classes.

// The base class knows the Cijkl, and that there are slip systems,
// derived classes know the specific slip systems, and the plastic
// data objects which have the gausspoint-specific, per-time-step
// information about the accumulated slip on each of these systems.

// Constitutive models know how to compute the slip increment given
// the stress, and have additional per-time-step gausspoint-specific
// data about the state of various local variables, like hardening.

// At the moment, there's no top-level "generic" way of doing this,
// but there probably should be.  That's a TODO.

// TODO: We might want to use a different property sub-class
// to ensure the right kind of equation does the derivatives.


#ifndef PLASTICITY_H
#define PLASTICITY_H

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/element.h"
#include "engine/property/elasticity/cijkl.h"
#include "common/pythonexportable.h"
#include "common/smallmatrix.h"
#include <string>

// TODO: cijkl is in a different hierarchy, needs to be higher?
// Or, plasticity should be a sub-type of elasticity, logically
// speaking?

class CSubProblem;
class Element;
class ElementFuncNodeIterator;
class FEMesh;
class Flux;
class Material;
class OutputVal;
class Position;
class PropertyOutput;
class SymmetricTensorFlux;
class TwoVectorField;
class ThreeVectorField;
class SmallSystem;
class PlasticConstitutiveRule;
class SmallMatrix;

class OrientationPropBase;

class PlasticConstitutiveRule;

class Plasticity : public FluxProperty {
public:
  Plasticity(PyObject *rg, const std::string &nm,
	     const Cijkl &c, PlasticConstitutiveRule *r, const int slips);
  virtual ~Plasticity() {}
  virtual void begin_element(const CSubProblem*, const Element*); 
  virtual void flux_matrix(const FEMesh *mesh,
			   const Element *element,
			   const ElementFuncNodeIterator &nu,
			   const Flux *flux,
			   const MasterPosition &x,
			   double time,
			   SmallSystem *fluxmtx) const;
  virtual void static_flux_value(const FEMesh*, const Element*,
				 const Flux*,
				 const MasterPosition&,
				 double time,
				 SmallSystem*) const;
  virtual int integration_order(const CSubProblem *, const Element*) const;
  virtual bool constant_in_space() const { return true; }
  virtual void precompute(FEMesh*);
  virtual void cross_reference(Material*);
  
  const Cijkl cijkl(const FEMesh*, const Element*,
		    const MasterPosition&);

  // Outputs -- plastic strain at gpts, total strain, elastic strain...
  
protected:
  FEMesh *mesh; // Set in precompute, used in begin_element.
  const int nslips;
  // TODO: 2D version?
  ThreeVectorField *displacement;
  SymmetricTensorFlux *stress_flux;
  SmallMatrix *_normalized_outer_product(double*, double*);
  SmallMatrix *_rotate_schmid_tensor(SmallMatrix*, const COrientation *);

  const OrientationPropBase *orientation;
  const Cijkl xtal_cijkl_;
  Cijkl lab_cijkl_;
  std::vector<SmallMatrix*> xtal_schmid_tensors;
  std::vector<SmallMatrix*> lab_schmid_tensors;
  const PlasticConstitutiveRule *rule;
};


class FCCPlasticity : public Plasticity {
public:
  FCCPlasticity(PyObject *rg, const std::string &nm,
		const Cijkl &c, PlasticConstitutiveRule *rule);
  virtual ~FCCPlasticity() {}
  //
};


//-------------------------------------------------------------------//
// Data containers.
//-------------------------------------------------------------------//

// Per-gaussponit plastic data, generally needed by all constitutive
// rules. This is the per-gausspoint object contained in the the
// PlasticData container.  It' snot expected to be subclassed.
class GptPlasticData {
public:
  GptPlasticData();

  SmallMatrix ft;       // Deformation tensor at prior time t
  SmallMatrix fpt;      // Plastic part of F at prior time t.
  SmallMatrix f_tau;    // Deformation tensor at current time tau.
  SmallMatrix fp_tau;   // Plastic part of F at current time tau.
  SmallMatrix fe_tau;   // Elastic part of F at current time tau.
  SmallMatrix cauchy;   // Cauchy stress (time tau?)
  SmallMatrix s_star;   // 2nd PK stress at time tau?
  SmallMatrix d_ep;     // Elastoplastic modules D.
  Cijkl w_mat;          // Elastoplastic tangent.
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


class PlasticData : public ElementData {
public:
  PlasticData(int o,const Element *e);
  virtual const std::string &classname() const {
    return elementdataclassname_plastic; }
  virtual const std::string &modulename() const {
    return plasticitymodulename; }
  int order;
  std::vector<GptPlasticData> fp;
  std::vector<GptPlasticData> gptdata;
};


// Base class for constitutive-rule-specific info.  The SlipData
// container has pointers to the base class, individual constitutive
// rules define derived classes that have the relevant data.
class GptSlipData {
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

};

#endif // PLASTICITY_H
