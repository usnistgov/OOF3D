//
//  Equation.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/28/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Equation_hpp
#define Equation_hpp

#include <stdio.h>
#include <string>
#include <vector>

#include "Flux.hpp"
#include "Element.hpp"
#include "Tensor.hpp"
#include "Mesh.hpp"


class CrystalPlasticity;

class Equation{
public:
    Equation(std::string const nam, int const id, int const siz,CrystalPlasticity* cp);
    void make_linear_system(int ndx,Element* el,GaussPoint* gpt,Vector &flux_vector,Tensor2d  &flux_fderivs,Tensor2d &flux_fderivsg,Vector &fmap, Mesh* mesh);

 
    std::string name;
    int index;
    int size;
    Flux* flux;
    
};

#endif /* Equation_hpp */
