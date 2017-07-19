//
//  Mesh.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Mesh.hpp"

Mesh::Mesh(int &xelement, int &yelement, int &zelement){
    
    
    dx = 1.0/xelement;
    dy = 1.0/yelement;
    dz = 1.0/zelement;
   
    tnode = -1;
    for (int i = 0 ; i < zelement + 1 ; i++){
        for (int j = 0 ; j < yelement + 1 ; j++){
            for (int k = 0 ; k < xelement + 1 ; k++){
                tnode += 1;
                Node nod(tnode,k*dx,j*dy,i*dz);
                nodelist.push_back(nod);
                
            }
        }
    }
    tnode += 1;
    
    nnode = 8;
    
    elconnectivities.resize(nnode);
    
    nelem = -1;
    for (int i = 0 ; i < zelement ; i++){
        for (int j = 0 ; j < yelement ; j++){
            for (int k = 0 ; k < xelement ; k++){
                elconnectivities[0] = i*(xelement+1)*(yelement+1)+j*(xelement+1)+k;
                elconnectivities[1] = i*(xelement+1)*(yelement+1)+j*(xelement+1)+k+1;
                elconnectivities[2] = i*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k+1;
                elconnectivities[3] = i*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k;
                elconnectivities[4] = (i+1)*(xelement+1)*(yelement+1)+j*(xelement+1)+k;
                elconnectivities[5] = (i+1)*(xelement+1)*(yelement+1)+j*(xelement+1)+k+1;
                elconnectivities[6] = (i+1)*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k+1;
                elconnectivities[7] = (i+1)*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k;
                nelem += 1;
                Element el(nelem,nnode,elconnectivities);
                ellist.push_back(el);
            }
        }
    }
    
    nelem += 1;
    

    
}


void Mesh::addfield(string const& name,int const& size){
    
    int count = 0;
    for (int i = 0 ; i < sizeof(nodelist) ; i++){
        
        Field newf(name,size*count,size);
        nodelist[i].addfield(newf);
        fieldlist.push_back(newf);
        count += 1;
        
    }
    
}

void Mesh::addeqn(string const& name,int const& size){
    
    int counteq = 0;
    for (int i = 0 ; i < sizeof(nodelist) ; i++){
        
        Eqn neweqn(name,size*counteq,size);
        nodelist[i].addeqn(neweqn);
        eqnlist.push_back(neweqn);
        counteq += 1;
        
    }
    

}


void Mesh::addmaterial(Material mtl){
    
    for (int i = 0 ; i < sizeof(ellist) ; i++){
        ellist[i].addmaterial(mtl);
    }
    
}

void Mesh::make_stiffness(){
///////////////////////////////////////
    ellist[0].gausspts();
///////////////////////////////////////
    
    for (int i = 0 ; i < nelem ; i++){
        ellist[i].make_linear_system(this);
    }
 
}
