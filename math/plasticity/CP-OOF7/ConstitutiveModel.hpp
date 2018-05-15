//
//  ConstitutiveModel.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef ConstitutiveModel_hpp
#define ConstitutiveModel_hpp

#include <stdio.h>
#include <cmath>
#include <vector>

#include "MatProperty.hpp"
class GptSlipBase {
    
public:
    
    virtual ~GptSlipBase() {};
    
};

class ConstitutiveModel{
    
public:
    
    void SetSlipSystem(int nslip);
    int n_slip;
    
    virtual void update_constitutive_model(GptSlipBase *gsdo) = 0;
    
    virtual void update_evolving_parameters(GptSlipBase *gsdo) = 0;


};

#endif /* ConstitutiveModel_hpp */
