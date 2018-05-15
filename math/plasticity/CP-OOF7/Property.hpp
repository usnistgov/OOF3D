//
//  Property.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Property_hpp
#define Property_hpp

#include <stdio.h>
#include <string>
#include "Tensor.hpp"
#include "GaussPoint.hpp"


class Material;
class Mesh;
class Element;

class Property {
public:
    std::string tag;
    Property(std::string tg) { tag=tg; };
    virtual void cross_reference(Material *) {};

    virtual void begin_element(Element *, Mesh *) {};
//    virtual void flux_matrix(Element* el, Tensor2d &flux_fderivs,Tensor2d &flux_fderivsg, Vector &fmap,GaussPoint* gpti,int gp_index) {} ;

};
#endif /* Property_hpp */
