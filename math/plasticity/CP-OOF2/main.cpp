//
//  main.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include <iostream>
#include<vector>
#include <string>
#include "Mesh.hpp"
#include "Material.hpp"


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
    
    mesh.addfield("Displacement", n_dim,0.0);
    



    
    return 0;
}
