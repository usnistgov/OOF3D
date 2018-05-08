//
//  GptPlasticData.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/30/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "GptPlasticData.hpp"
GptPlasticData::GptPlasticData(){
    
    std::vector<double> ft{0.0,0.0,0.0};
    std::vector<double> dep{0.0,0.0,0.0,0.0,0.0,0.0};
    
    Ft.resize(3,3);
    Fpt.resize(3,3);
    F_tau.resize(3,3);
    Fp_tau.resize(3,3);
    Fe_tau.resize(3,3);
    Cauchy.resize(3,3);
    S_star.resize(3,3);
    w_mat.resize(3,3,3,3);
    Ft = Fpt = F_tau = Fp_tau = Fe_tau = Cauchy = S_star = 0.0;
    
    Dep = 0.0;
    w_mat = 0.0;
    
    Ft(0,0) = Ft(1,1) = Ft(2,2) = 1.0;
    Fpt(0,0) = Fpt(1,1) = Fpt(2,2) = 1.0;
    F_tau(0,0) = F_tau(1,1) = F_tau(2,2) = 1.0;
    
}
