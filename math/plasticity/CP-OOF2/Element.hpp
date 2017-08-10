//
//  Element.hpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Element_hpp
#define Element_hpp

#include <stdio.h>
#include <vector>
#include <cmath>
#include <iostream>
#include "Node.hpp"


class Material;


class Element {
    
public:
    Element(int id,int nnode,std::vector<Node*> nodelist);
    void addmaterial(Material *mtl);


    
    std::vector<Node*> nodes;
    int ielem;

    
   
private:
    
    Material *material;
    double mpt;
    double pts[2];
    double wts[2];

    
    
    
};

#endif /* Element_hpp */
