//
//  Mesh.cpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Mesh.hpp"

Mesh::Mesh(int &xelement, int &yelement, int &zelement){
    
    
    dx = 1.0/xelement;
    dy = 1.0/yelement;
    dz = 1.0/zelement;
    nodelist.clear();

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
                nodes.clear();
                elconnectivities[0] = (i*(xelement+1)+j)*(yelement+1)+k;
                elconnectivities[1] = ((i+1)*(xelement+1)+j)*(yelement+1)+k;
                elconnectivities[2] = (i*(xelement+1)+(j+1))*(yelement+1)+k;
                elconnectivities[3] = ((i+1)*(xelement+1)+(j+1))*(yelement+1)+k;
                elconnectivities[4] = (i*(xelement+1)+j)*(yelement+1)+k+1;
                elconnectivities[5] = ((i+1)*(xelement+1)+j)*(yelement+1)+k+1;
                elconnectivities[6] = (i*(xelement+1)+(j+1))*(yelement+1)+k+1;
                elconnectivities[7] = ((i+1)*(xelement+1)+(j+1))*(yelement+1)+k+1;
                
                nelem += 1;
                for (int ki = 0 ; ki < nnode ; ki++){
                    nodes.push_back(nodelist[elconnectivities[ki]]);
                }
                cout<<endl;
                Element el(nelem,nnode,nodes);
                
                ellist.push_back(el);
            }
        }
    }
    
    nelem += 1;
    
    
    
}

void Mesh::addfield(string const name,int const size, double value){
    
    int count = 0;
    for (vector<Node>::iterator ni = nodelist.begin() ; ni!=nodelist.end(); ni++){
        
//    for (int i = 0 ; i < tnode ; i++){
        
        Field newf(name,size*count,size);

//        ni->addfield(&newf);
        
        
        //        nodelist[i].addfield(&newf);
        //        fieldlist.push_back(newf);
        count += 1;
        
    }
    
}
/*
void Mesh::addeqn(string const& name,int const& size){
    
    int counteq = 0;
    for (int i = 0 ; i < sizeof(nodelist) ; i++){
        
        Eqn neweqn(name,size*counteq,size);
        nodelist[i].addeqn(neweqn);
        eqnlist.push_back(neweqn);
        counteq += 1;
        
    }
    
    
}*/

void Mesh::addmaterial(Material *mtl){
    
    for (int i = 0 ; i < sizeof(ellist) ; i++){
        ellist[i].addmaterial(mtl);
    }
    
}

void Mesh::make_stiffness(){
    ///////////////////////////////////////
//    ellist[0].gausspts();
    ///////////////////////////////////////
    
    for (int i = 0 ; i < nelem ; i++){
        ellist[i].gausspts();
        ellist[i].make_linear_system();
    }
    
}



