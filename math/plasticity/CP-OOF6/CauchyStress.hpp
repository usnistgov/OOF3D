//
//  CauchyStress.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef CauchyStress_hpp
#define CauchyStress_hpp

#include <stdio.h>
#include <string>
#include <iostream>

#include "Cijkl.hpp"
#include "Tensor.hpp"

class CauchyStress {
    
public:
    
    
    CauchyStress(std::string const& name, double& c11,double& c12,double& c44);
    
    CauchyStress(std::string const& name);
    
    Cijkl g_cijkl,C_mat;
    
    void rotate(Tensor2d &qrot);
    
    
};


#endif /* CauchyStress_hpp */
