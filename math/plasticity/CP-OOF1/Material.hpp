//
//  Material.hpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Material_hpp
#define Material_hpp

#include <iostream>

#include <stdio.h>
#include <vector>
#include <string>
#include<cmath>
#include "CauchyStress.hpp"

#include "PlasticData.hpp"

#include "Element.hpp"

#include <map>

using namespace std;

class Material{
    
public:
    
//    Material();
    Material(string const materialtype,int nslip,double const a1,double const a2,double const a3);
    
    double Orientation(double phi,double theta,double omega);
    
//    double precompute(CauchyStress f);
    double precompute();
    
    double make_linear_system();
    
    double begin_element(Element *el);
    double end_element();
    
    double calc_schmid(string crystal_type,int n_slip);
    
    string name;
    int n_slip;
    double phi;
    double theta;
    double omega;
    double const_pi = acos(-1.0);
    
    int const ndim = 3;


    double **qrot;
    double **F_t;
    double **F_tau;
    
    double ***schmid;
    
    
private:
    
    PlasticData *pd;
    
    
    
};

#endif /* Material_hpp */
