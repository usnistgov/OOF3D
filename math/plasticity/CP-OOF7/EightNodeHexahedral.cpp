//
//  EightNodeHexahedral.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 5/11/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//
#warning "Starting EightNodeHexahedral.cpp"
#include "EightNodeHexahedral.hpp"

void EightNodeHexahedral::gausspts(){
    
    
    mpt = 1.0/pow(3.0,0.5);
    ptsi[0] = -mpt, ptsi[1] = mpt, ptsi[2] = mpt, ptsi[3] = -mpt, ptsi[4] = -mpt, ptsi[5] = mpt, ptsi[6] = mpt, ptsi[7] = -mpt;
    pts[0] = -mpt, pts[1] = mpt;
    wts[0] = 1.0 , wts[1] = 1.0;
    
    int n = 2;
    
    int i_count = 0;
    for(int k = 0 ; k < 2 ; k ++){
        for(int j = 0 ; j < 2 ; j ++){
            for(int i = 0 ; i < 2 ; i ++){
                GaussPoint *gp =new GaussPoint(ptsi[i_count],pts[j],pts[k],wts[k]*wts[j]*wts[i]);
                
                i_count += 1;
                gptable.push_back(gp);
            }
        }
    }
    
    
}


void EightNodeHexahedral::dsfnsvec(double xi,double zeta,double mu){
    
    
    std::vector<double> ds{0.0,0.0,0.0};
    
    for (int i = 0 ; i < 8 ; i++){
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
    dsfns[4][0] = dsf4d0(xi,zeta,mu);
    dsfns[4][1] = dsf4d1(xi,zeta,mu);
    dsfns[4][2] = dsf4d2(xi,zeta,mu);
    dsfns[5][0] = dsf5d0(xi,zeta,mu);
    dsfns[5][1] = dsf5d1(xi,zeta,mu);
    dsfns[5][2] = dsf5d2(xi,zeta,mu);
    dsfns[6][0] = dsf6d0(xi,zeta,mu);
    dsfns[6][1] = dsf6d1(xi,zeta,mu);
    dsfns[6][2] = dsf6d2(xi,zeta,mu);
    dsfns[7][0] = dsf7d0(xi,zeta,mu);
    dsfns[7][1] = dsf7d1(xi,zeta,mu);
    dsfns[7][2] = dsf7d2(xi,zeta,mu);
    
    
}

double EightNodeHexahedral::dsf0d0(double xi,double zeta,double mu){
    return -0.125*(1.0-zeta)*(1.0-mu);
}
double EightNodeHexahedral::dsf0d1(double xi,double zeta,double mu){
    return -0.125*(1.0-xi)*(1.0-mu);
}
double EightNodeHexahedral::dsf0d2(double xi,double zeta,double mu){
    return -0.125*(1.0-xi)*(1.0-zeta);
}


double EightNodeHexahedral::dsf1d0(double xi,double zeta,double mu){
    return +0.125*(1.0-zeta)*(1.0-mu);
}
double EightNodeHexahedral::dsf1d1(double xi,double zeta,double mu){
    return -0.125*(1.0+xi)*(1.0-mu);
}
double EightNodeHexahedral::dsf1d2(double xi,double zeta,double mu){
    return -0.125*(1.0+xi)*(1.0-zeta);
}


double EightNodeHexahedral::dsf2d0(double xi,double zeta,double mu){
    return +0.125*(1.0+zeta)*(1.0-mu);
}
double EightNodeHexahedral::dsf2d1(double xi,double zeta,double mu){
    return +0.125*(1.0+xi)*(1.0-mu);
}
double EightNodeHexahedral::dsf2d2(double xi,double zeta,double mu){
    return -0.125*(1.0+xi)*(1.0+zeta);
}


double EightNodeHexahedral::dsf3d0(double xi,double zeta,double mu){
    return -0.125*(1.0+zeta)*(1.0-mu);
}
double EightNodeHexahedral::dsf3d1(double xi,double zeta,double mu){
    return +0.125*(1.0-xi)*(1.0-mu);
}
double EightNodeHexahedral::dsf3d2(double xi,double zeta,double mu){
    return -0.125*(1.0-xi)*(1.0+zeta);
}

double EightNodeHexahedral::dsf4d0(double xi,double zeta,double mu){
    return -0.125*(1.0-zeta)*(1.0+mu);
}
double EightNodeHexahedral::dsf4d1(double xi,double zeta,double mu){
    return -0.125*(1.0-xi)*(1.0+mu);
}
double EightNodeHexahedral::dsf4d2(double xi,double zeta,double mu){
    return +0.125*(1.0-xi)*(1.0-zeta);
}

double EightNodeHexahedral::dsf5d0(double xi,double zeta,double mu){
    return +0.125*(1.0-zeta)*(1.0+mu);
}
double EightNodeHexahedral::dsf5d1(double xi,double zeta,double mu){
    return -0.125*(1.0+xi)*(1.0+mu);
}
double EightNodeHexahedral::dsf5d2(double xi,double zeta,double mu){
    return +0.125*(1.0+xi)*(1.0-zeta);
}

double EightNodeHexahedral::dsf6d0(double xi,double zeta,double mu){
    return +0.125*(1.0+zeta)*(1.0+mu);
}
double EightNodeHexahedral::dsf6d1(double xi,double zeta,double mu){
    return +0.125*(1.0+xi)*(1.0+mu);
}
double EightNodeHexahedral::dsf6d2(double xi,double zeta,double mu){
    return +0.125*(1.0+xi)*(1.0+zeta);
}

double EightNodeHexahedral::dsf7d0(double xi,double zeta,double mu){
    return -0.125*(1.0+zeta)*(1.0+mu);
}
double EightNodeHexahedral::dsf7d1(double xi,double zeta,double mu){
    return +0.125*(1.0-xi)*(1.0+mu);
}
double EightNodeHexahedral::dsf7d2(double xi,double zeta,double mu){
    return +0.125*(1.0-xi)*(1.0+zeta);
}

