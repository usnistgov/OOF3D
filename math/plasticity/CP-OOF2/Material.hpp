//
//  Material.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Material_hpp
#define Material_hpp

#include <stdio.h>
#include <vector>
#include <string>
#include "ElementData.hpp"
//#include "Element.hpp"
#include "PlasticData.hpp"
#include "CauchyStress.hpp"

using namespace std;

class Element;

class Material{
    
public:
    
    Material(string materialtype,int const nslip,int const ndim,double const a1,double const a2,double const a3);
    
    void begin_element(Element *el);
    void Orientation(double phi,double theta,double omega);
    void calc_schmid(string crystal_type,int n_slip);

    string name;
    int n_slip;
    int n_dim;
    double phi;
    double theta;
    double omega;
    
    double **qrot;
    double ***schmid;

   
private:
    
//    PlasticData *pd;
    double const_pi = acos(-1.0);

    PlasticData *pd;

};
#endif /* Material_hpp */
