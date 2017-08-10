//
//  Element.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Element.hpp"

Element::Element(int id,int nnode,std::vector<Node*> nodelist){
    
    ielem = id;
    
    nodes = nodelist;
}

void Element::addmaterial(Material *mtl){
    
    material = mtl;
    
}

