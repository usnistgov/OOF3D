//
//  main.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include <iostream>
#include<vector>
#include "Mesh.hpp"
#include "Node.hpp"
#include "Element.hpp"
#include "Material.hpp"
#include <string>
#include "CauchyStress.hpp"
#include "Flux.hpp"


using namespace std;

int main() {

    int ndim = 3;
    int xelement = 2;
    int yelement = 2;
    int zelement = 2;
    
    Mesh mesh(xelement,yelement,zelement);
    
/*    double c11 = 2.0;
    double c12 = 1.3;
    double c44 = 1.0;

    
    CauchyStress f("Stress",c11,c12,c44);
*/    
    double phi = 30.0;
    double theta = 0.0;
    double omega = 0.0;
    string materialtype = "FCC";
    int n_slip = 12;
    
    Material mtl(materialtype,n_slip,phi,theta,omega);
    

    
//    mtl.precompute(f);
    mtl.precompute();
 

    mesh.addmaterial(mtl);
 

    mesh.addfield("Displacement", ndim);
    
    mesh.addeqn("Force",3);
    
    
    mesh.make_stiffness();
    
    for(int i=0 ; i < mesh.nelem ; i++){
        cout<<mesh.ellist[i].ielem<<"  ";
        for(int j = 0 ; j < mesh.nnode ; j++){
            
            cout<<mesh.ellist[i].lnode[j]<<"   ";
        }
        cout<<endl;
    }
    
    for(int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j < 3 ; j++){
            cout<<mtl.qrot[i][j]<<"   ";
        }
        cout<<endl;
        
    }
   
    
    
    
    

    
    return 0;
}
