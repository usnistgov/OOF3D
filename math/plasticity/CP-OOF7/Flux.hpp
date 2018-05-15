//
//  Flux.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Flux_hpp
#define Flux_hpp

#include <stdio.h>
#include <string>
#include <iostream>
#include <cmath>

#include "Tensor.hpp"
#include "Property.hpp"
#include "GptPlasticData.hpp"
#include "CauchyStress.hpp"
#include "GaussPoint.hpp"

//#include "ElementData.hpp"
//#include "PlasticData.hpp"

//#include "PlasticData.hpp"

class Element;
class Mesh;

class Flux  : public Property {
    
public:
    
    Flux(std::string const nam,std::string const fname, std::string tag, int const dimension);

    std::string name;
    std::string fieldname;
    int dim;
    int nslip;
    
//    virtual void flux_begin_element(Element *el, Mesh* mesh) = 0;
//    PlasticData *pd;

    virtual void make_linear_system(Element* el,GaussPoint* gpti,int gp_index) = 0;
    
    Tensor2d flux_fderivs;
    Tensor2d flux_fderivsg;
    Vector flux_vector;
    Vector fmap;
    std::vector<int> t_row = {0,1,2,1,0,0,1,2,2};
    std::vector<int> t_col = {0,1,2,2,2,1,0,0,1};
    std::vector<int> t_rowg = {0,1,2,0,1,2,0,1,2};
    std::vector<int> t_colg = {0,0,0,1,1,1,2,2,2};
    
//============================ user_print =========================
    virtual void user_print(GaussPoint* gpti,int gp_index) {};
    
    Tensor2d cauchy_stress;
    Tensor2d deformation_gradient;
//==================================================================

};

#endif /* Flux_hpp */
