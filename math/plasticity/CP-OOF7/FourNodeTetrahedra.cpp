//
//  FourNodeTetrahedra.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 5/11/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "FourNodeTetrahedra.hpp"

void FourNodeTetrahedra::gausspts(){
    
    
    ptsi[0] = 0.25, ptsi[1] = 0.25, ptsi[2] = 0.25;
    wts[0] = 1.0/6.0 ;
    
    int n = 2;
    
    int i_count = 0;
    GaussPoint *gp =new GaussPoint(ptsi[0],ptsi[1],ptsi[2],wts[0]);
    
    gptable.push_back(gp);

    
}

void FourNodeTetrahedra::dsfnsvec(double xi,double zeta,double mu){
    
    
    std::vector<double> ds{0.0,0.0,0.0};
    
    for (int i = 0 ; i < 4 ; i++){
        dsfns.push_back(ds);
    }
    
    dsfns[0][0] = dsf0d0(xi,zeta,mu);
    dsfns[0][1] = dsf0d1(xi,zeta,mu);
    dsfns[0][2] = dsf0d2(xi,zeta,mu);
    dsfns[1][0] = dsf1d0(xi,zeta,mu);
    dsfns[1][1] = dsf1d1(xi,zeta,mu);
    dsfns[1][2] = dsf1d2(xi,zeta,mu);
    dsfns[2][0] = dsf2d0(xi,zeta,mu);
    dsfns[2][1] = dsf2d1(xi,zeta,mu);
    dsfns[2][2] = dsf2d2(xi,zeta,mu);
    dsfns[3][0] = dsf3d0(xi,zeta,mu);
    dsfns[3][1] = dsf3d1(xi,zeta,mu);
    dsfns[3][2] = dsf3d2(xi,zeta,mu);
    
    
}

double FourNodeTetrahedra::dsf0d0(double xi,double zeta,double mu){
    return 1.0;
}
double FourNodeTetrahedra::dsf0d1(double xi,double zeta,double mu){
    return 0.0;
}
double FourNodeTetrahedra::dsf0d2(double xi,double zeta,double mu){
    return 0.0;
}


double FourNodeTetrahedra::dsf1d0(double xi,double zeta,double mu){
    return 0.0;
}
double FourNodeTetrahedra::dsf1d1(double xi,double zeta,double mu){
    return 1.0;
}
double FourNodeTetrahedra::dsf1d2(double xi,double zeta,double mu){
    return 0.0;
}


double FourNodeTetrahedra::dsf2d0(double xi,double zeta,double mu){
    return 0.0;
}
double FourNodeTetrahedra::dsf2d1(double xi,double zeta,double mu){
    return 0.0;
}
double FourNodeTetrahedra::dsf2d2(double xi,double zeta,double mu){
    return 1.0;
}


double FourNodeTetrahedra::dsf3d0(double xi,double zeta,double mu){
    return -1.0;
}
double FourNodeTetrahedra::dsf3d1(double xi,double zeta,double mu){
    return -1.0;
}
double FourNodeTetrahedra::dsf3d2(double xi,double zeta,double mu){
    return -1.0;
}

