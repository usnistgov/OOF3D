//
//  Mesh.hpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.hts reserved.
//

#ifndef Mesh_hpp
#define Mesh_hpp

#include <stdio.h>
#include<vector>
#include <string>
#include <iostream>

#include "Node.hpp"
#include "Element.hpp"
#include "Material.hpp"
#include "Field.hpp"




using namespace std;

class Mesh{
    
public:
    
    Mesh(int &xelement, int &yelement, int &zelement);
    void addmaterial(Material *mtl);
    void addfield(string const name,int const size, double value);
    void make_stiffness();


    
    vector<Node*> nodelist;
    int nnode;
    int tnode;
    int nelem;
    
    // vector<Node*> nodes; // nodes members are the element conectivities.

    
    vector<Element*> ellist;
    
    
private:
    
    double dx;
    double dy;
    double dz;
    vector <int> elconnectivities;

};


#endif /* Mesh_hpp */
