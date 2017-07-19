//
//  Mesh.hpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Mesh_hpp
#define Mesh_hpp

#include <stdio.h>
#include "Node.hpp"
#include<vector>
#include "Element.hpp"
#include <iostream>
#include <string>
#include "Field.hpp"
#include "CauchyStress.hpp"
#include "Eqn.hpp"
#include "Material.hpp"

using namespace std;

class Mesh{
    
public:
    
    Mesh(int &xelement, int &yelement, int &zelement);
    void addfield(string const& name,int const& size);
    void addeqn(string const& name,int const& size);
    void addmaterial(Material mtl);
    
    void make_stiffness();
    
    vector<Node> nodelist;
    int nnode;
    int tnode;
    int nelem;
    vector <Field> fieldlist;
    vector <Eqn> eqnlist;
    vector <Element> ellist;
    
    
private:
    
    double dx;
    double dy;
    double dz;
    vector <int> elconnectivities;

    
};

#endif /* Mesh_hpp */
