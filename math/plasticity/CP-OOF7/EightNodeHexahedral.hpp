//
//  EightNodeHexahedral.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 5/11/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef EightNodeHexahedral_hpp
#define EightNodeHexahedral_hpp

#include <stdio.h>
#include "Element.hpp"

class EightNodeHexahedral : public Element{
    
public:
    
    EightNodeHexahedral (int id,int nnode,std::vector<Node*> nodelist) : Element(id,nnode,nodelist) {};
    virtual void gausspts();
    
    double mpt;
    double ptsi[8];
    double pts[2];
    double wts[2];
    
    virtual void dsfnsvec(double xi,double zeta,double mu);
    
    double dsf0d0(double xi,double zeta,double mu);
    double dsf0d1(double xi,double zeta,double mu);
    double dsf0d2(double xi,double zeta,double mu);
    
    double dsf1d0(double xi,double zeta,double mu);
    double dsf1d1(double xi,double zeta,double mu);
    double dsf1d2(double xi,double zeta,double mu);
    
    double dsf2d0(double xi,double zeta,double mu);
    double dsf2d1(double xi,double zeta,double mu);
    double dsf2d2(double xi,double zeta,double mu);
    
    double dsf3d0(double xi,double zeta,double mu);
    double dsf3d1(double xi,double zeta,double mu);
    double dsf3d2(double xi,double zeta,double mu);
    
    double dsf4d0(double xi,double zeta,double mu);
    double dsf4d1(double xi,double zeta,double mu);
    double dsf4d2(double xi,double zeta,double mu);
    
    double dsf5d0(double xi,double zeta,double mu);
    double dsf5d1(double xi,double zeta,double mu);
    double dsf5d2(double xi,double zeta,double mu);
    
    double dsf6d0(double xi,double zeta,double mu);
    double dsf6d1(double xi,double zeta,double mu);
    double dsf6d2(double xi,double zeta,double mu);
    
    double dsf7d0(double xi,double zeta,double mu);
    double dsf7d1(double xi,double zeta,double mu);
    double dsf7d2(double xi,double zeta,double mu);

    
};



#endif /* EightNodeHexahedral_hpp */
