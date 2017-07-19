//
//  Mesh.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Mesh_hpp
#define Mesh_hpp

#include <stdio.h>
#include<vector>
#include <string>

#include "Node.hpp"
#include "Element.hpp"
#include "Material.hpp"
//#include "Field.hpp"
//#include "Eqn.hpp"



using namespace std;

class Mesh{
    
public:
    
    Mesh(int &xelement, int &yelement, int &zelement);
//    void addfield(string const& name,int const& size);
//    void addeqn(string const& name,int const& size);
    void addmaterial(Material mtl);

    void make_stiffness();
    
    vector<Node> nodelist;
    int nnode;
    int tnode;
    int nelem;
    
    vector<Element> ellist;
//    vector <Field> fieldlist;
//    vector <Eqn> eqnlist;
    
    
private:
    
    double dx;
    double dy;
    double dz;
    vector <int> elconnectivities;
    
};





#endif /* Mesh_hpp */
