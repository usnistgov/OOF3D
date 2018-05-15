//
//  CauchyStress.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "CauchyStress.hpp"
CauchyStress::CauchyStress(std::string const& name, double& c11,double& c12,double& c44) :
 g_cijkl(c11,c12,c44) {}

CauchyStress::CauchyStress(std::string const& name)  {}

void CauchyStress::rotate(Tensor2d &qrot){
    C_mat = g_cijkl.rotate(qrot);
}
