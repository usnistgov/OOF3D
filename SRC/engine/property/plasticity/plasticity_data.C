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
#include "engine/property/plasticity/plasticity_data.h"
#include "engine/property/plasticity/constitutive_base.h"

GptPlasticData::GptPlasticData() :
  ft(),fpt(),f_tau(),fp_tau(),fe_tau(),cauchy(),s_star()
  // Constructors above not needed now that SmallMatrix3 exist
  // and has a default constructor.
{
  ft(0,0) = ft(1,1) = ft(2,2) = 1.0;
  fpt(0,0) = fpt(1,1) = fpt(2,2) = 1.0;
  f_tau(0,0) = f_tau(1,1) = f_tau(2,2) = 1.0;
}

// The order selects which gpt array to iterate over.  It's passed in,
// but it's very important that this be done consistently.

// Constructor should make two time-steps, "new" and "old".
PlasticData::PlasticData(int ord, const Element *el) :
  ElementData("plastic_data"), order(ord), current_time(0.0), dt(0.0)
{
  for (GaussPointIterator gpt = el->integrator(order);
       !gpt.end(); ++gpt) {
    GptPlasticData *gppd = new GptPlasticData();
    MasterCoord mc = gpt.gausspoint().mastercoord();
    mctogpi_map[mc]=gpt.index();
    gptdata.push_back(gppd);
  }
}


std::ostream &operator<<(std::ostream &o, const GptPlasticData &gppd) {
  o << "GptPlasticData: " << std::endl;
  o << "- ft = " << gppd.ft;
  o << "- fpt = " << gppd.fpt; 
  o << "- f_tau = " << gppd.f_tau;
  o << "- fp_tau = " << gppd.fp_tau;
  o << std::endl;
}


double PlasticData::set_time(double time) {
  // std::cerr << "PlasticData set_time called with " << time << std::endl;
  if (time!=current_time) {
    dt = time-current_time;
    current_time = time;
    // std::cerr << "PD set_time updating current time, delta is " << dt << std::endl;
    return dt;
  }
  else {
    // std::cerr << "PD set_time Not updating current time." << std::endl;
    return dt;
  }
}

GptSlipData::GptSlipData(int nslips) {
  for(int i=0;i<nslips;++i) {
    delta_gamma.push_back(0.0);
    dgamma_dtau.push_back(0.0);
    tau_alpha.push_back(0.0);
  }
}

SlipData::SlipData(int ord, const PlasticConstitutiveRule *r,
		   const Element *e) : ElementData("slip_data"), order(ord)
{
  for (GaussPointIterator gpti = e->integrator(order);
       !gpti.end(); ++gpti) {
    GptSlipData *gpslip = r->getSlipData(); // Pointer to new object.
    gptslipdata.push_back(gpslip);
  }
}

// We own the pointed-to GptSlipData objects -- clean them up when we die.
SlipData::~SlipData() {
  for (std::vector<GptSlipData*>::iterator i = gptslipdata.begin();
       i!=gptslipdata.end(); ++i) {
    delete (*i);
  }
}

Rank4_3DTensor::Rank4_3DTensor(SmallMatrix &s) {
  data = std::vector<double>(81,0.0);
  if ((s.rows()!=9) || (s.cols()!=9))
    throw ErrProgrammingError("Attempt to construct Rank4_3DTensor with malformed SmallMatrix.", __FILE__,__LINE__);

  for(int i=0;i<3;++i)
    for(int j=0;j<3;++j)
      for(int k=0;k<3;++k)
	for(int l=0;l<3;++l) {
	  data[_index(i,j,k,l)] = s(voigt9[i][j],voigt9[k][l]);
	};
}
  
Rank4_3DTensor::Rank4_3DTensor(const Rank4_3DTensor& other) {
  data = other.data;
}

SmallMatrix Rank4_3DTensor::as_smallmatrix() {
  SmallMatrix res = SmallMatrix(9);
  for(int i=0;i<3;++i)
    for(int j=0;j<3;++j)
      for(int k=0;k<3;++k)
	for(int l=0;l<3;++l) {
	  res(voigt9[i][j],voigt9[k][l]) = data[_index(i,j,k,l)];
	};
  return res;
}

SmallMatrix Rank4_3DTensor::as_6matrix() {
    
  SmallMatrix res = SmallMatrix(6);
    
  for(int i = 0 ; i < 3 ; i++){
    for(int j = 0 ; j < 3 ; j++){
      res(i,j) = data[_index(i,i,j,j)];
    }
  }

  // OK not to symmetrize here, summing is correct.
  for(int i = 0 ; i < 3 ; i++){
    res(i,3) = data[_index(i,i,0,1)]+data[_index(i,i,1,0)];
    res(i,4) = data[_index(i,i,1,2)]+data[_index(i,i,2,1)];
    res(i,5) = data[_index(i,i,0,2)]+data[_index(i,i,2,0)];
  }
    
    
  for(int j = 0 ; j < 3 ; j++){
    res(3,j) = data[_index(0,1,j,j)];
    res(4,j) = data[_index(1,2,j,j)];
    res(5,j) = data[_index(0,2,j,j)];
  }
    
  res(3,3) = data[_index(0,1,0,1)]+data[_index(0,1,1,0)];
  res(3,4) = data[_index(0,1,1,2)]+data[_index(0,1,2,1)];
  res(3,5) = data[_index(0,1,0,2)]+data[_index(0,1,2,0)];

  res(4,3) = data[_index(1,2,0,1)]+data[_index(1,2,1,0)];
  res(4,4) = data[_index(1,2,1,2)]+data[_index(1,2,2,1)];
  res(4,5) = data[_index(1,2,0,2)]+data[_index(1,2,2,0)];
  
  res(5,3) = data[_index(0,2,0,1)]+data[_index(0,2,1,0)];
  res(5,4) = data[_index(0,2,1,2)]+data[_index(0,2,2,1)];
  res(5,5) = data[_index(0,2,0,2)]+data[_index(0,2,2,0)];
  
  return res;
}

void Rank4_3DTensor::clear() {
  for(std::vector<double>::iterator di = data.begin();
      di!=data.end(); ++di)
    (*di) = 0.0;
}  

double &Rank4_3DTensor::operator()(unsigned int i, unsigned int j,
				   unsigned int k, unsigned int l) {
  return data[_index(i,j,k,l)];
}

const double &Rank4_3DTensor::operator()(unsigned int i, unsigned int j,
				   unsigned int k, unsigned int l) const {
  return data[_index(i,j,k,l)];
}

std::ostream& operator<<(std::ostream &o, const Rank4_3DTensor &t) {
  for(int i=0;i<3;++i)
    for(int j=0;j<3;++j)
      for(int k=0;k<3;++k)
	for(int l=0;l<3;++l)
	  o << i << ", " << j << ", " << k << ", " << l <<
	    ": " << t.data[t._index(i,j,k,l)] << std::endl;
  return o;
}



