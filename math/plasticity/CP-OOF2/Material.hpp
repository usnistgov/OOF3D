//
//  Material.hpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Material_hpp
#define Material_hpp

#include <stdio.h>
#include <vector>
#include <string>
#include <cmath>

using namespace std;

class Element;

class Material{
    
public:
    
    Material(string materialtype,int const nslip,int const ndim,double const a1,double const a2,double const a3);
    string name;
    int n_slip;
    int n_dim;
    double phi;
    double theta;
    double omega;

    
private:
    
    //    PlasticData *pd;
    double const_pi = acos(-1.0);
    
    
};


#endif /* Material_hpp */
