//
//  CauchyStress.hpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef CauchyStress_hpp
#define CauchyStress_hpp

#include <stdio.h>
#include <string>

#include "Flux.hpp"
#include "Cijkl.hpp"



using namespace std;

class CauchyStress : public Flux {
    
public:
    
    
    CauchyStress(string const& name, double& c11,double& c12,double& c44);
    
    Cijkl g_cijkl,C_mat;
    
    void rotate(double **qrot);

    
    
};


#endif /* CauchyStress_hpp */
