//
//  CauchyStress.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/29/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef CauchyStress_hpp
#define CauchyStress_hpp

#include <stdio.h>

#include "Flux.hpp"
#include "Cijkl.hpp"
#include <string>


using namespace std;

class CauchyStress : public Flux {
    
public:
    
    CauchyStress();
    
    CauchyStress(string const& name, double& c11,double& c12,double& c44);
    
    Cijkl g_cijkl,C_mat;
    
    void rotate(double **qrot);
    
    
};

#endif /* CauchyStress_hpp */
