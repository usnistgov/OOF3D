//
//  main.cpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include <iostream>
#include<vector>
#include "Mesh.hpp"
#include "Node.hpp"
#include "Element.hpp"
#include "Material.hpp"
#include <string>


using namespace std;

int main(int argc, const char * argv[]) {
    
    int n_dim = 3;
    int xelement = 1;
    int yelement = 1;
    int zelement = 1;
    
    Mesh mesh(xelement,yelement,zelement);
    
    double phi = 0.0;
    double theta = 0.0;
    double omega = 0.0;
    string materialtype = "FCC";
    int n_slip = 12;
    
    Material mtl(materialtype,n_slip,n_dim,phi,theta,omega);
    
    mesh.addmaterial(&mtl);
    cout << "Back from addmaterial." << endl;
    
    mesh.addfield("Displacement", n_dim,0.0);
    cout << "Back from addfield." << endl;
    
//    mesh.addeqn("Force",3);
    
    for (int i = 0 ; i <2 ; i++) {
        cout << "Calling make_stiffness i=" << i << endl;
        mesh.make_stiffness();
        cout << "Back from make_stiffness." << endl;
    }
/*
    for(int i=0 ; i < mesh.nelem ; i++){
        cout<<mesh.ellist[i].ielem<<"  ";
        for(int j = 0 ; j < mesh.nnode ; j++){
            
            cout<<mesh.ellist[i].nodes[i].inode<<"   ";
        }
        cout<<endl;
    }
   */
/*    for(int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j < 3 ; j++){
            cout<<mtl.qrot[i][j]<<"   ";
        }
        cout<<endl;
        
    }
    
*/
    cout << "Finished!" << endl;
    return 0;
}
