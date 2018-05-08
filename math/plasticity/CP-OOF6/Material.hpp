//
//  Material.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Material_hpp
#define Material_hpp

#include <stdio.h>
#include <vector>
#include <string>
#include "Property.hpp"
#include "CrystalPlasticity.hpp"
#include "Flux.hpp"
#include "Equation.hpp"

class Mesh;
class Element;


class Material {
public:
    std::vector<Flux*> fluxprops;
    void add_flux_property(Flux *f);

    std::vector<Property*> props;
    void add_property(Property *p) { props.push_back(p); };
    void cross_reference();

    Property *get_by_tag(std::string tag);
    
    void begin_element(Element *e, Mesh *m);
    
    void make_linear_system(Element *el, Mesh *mesh);
    


};
#endif /* Material_hpp */
