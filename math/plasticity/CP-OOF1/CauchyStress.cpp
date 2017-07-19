//
//  CauchyStress.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/11/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "CauchyStress.hpp"


CauchyStress::CauchyStress(string const& name, double& c11,double& c12,double& c44) :
    Flux("Stress","Displacemenr",9), g_cijkl(c11,c12,c44) {}


void CauchyStress::rotate(double **qrot){
    C_mat = g_cijkl.rotate(qrot);
}
