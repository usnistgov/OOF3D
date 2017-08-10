//
//  Material.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Material.hpp"
Material::Material(string materialtype,int const nslip,int const ndim,double const a1,double const a2,double const a3){
    
    name = materialtype;
    n_slip = nslip;
    n_dim = ndim;
    phi = a1;
    theta = a2;
    omega = a3;
    
}

