//
//  PowerLaw.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef PowerLaw_hpp
#define PowerLaw_hpp

#include <stdio.h>
#include <vector>

#include "ConstitutiveModel.hpp"
#include "MatInput.hpp"
#include "GaussPoint.hpp"

class GptSlipData : public GptSlipBase {
public:
    GptSlipData(ConstitutiveModel* CM,MatInput* mi);
    
    std::vector<double> res;
    std::vector<double> dgam;
    std::vector<double> dgam_dta;
    std::vector<double> tau_alpha;
    
};



class PowerLaw : public ConstitutiveModel {
    
public:
    
    PowerLaw(MatInput* CPIn);
    
    virtual void update_constitutive_model(GptSlipBase* gsdo);
    void Hardening(GptSlipData* gsdo);
    void PlasticShSt(GptSlipData* gsdo);

    virtual void update_evolving_parameters(GptSlipBase *gsdo); // This is a method to update incremental parameters such as slip system resistance which is called when the iteration of 2PK is done and we would like to update res

private:
    
    double const_w1, const_w2, const_ss , const_a, const_h0 , const_m , const_g0dot , const_dt,const_init_res;
    std::vector<double> res_ssd;
    
    std::vector<double> res_ssdt;

};
#endif /* PowerLaw_hpp */
