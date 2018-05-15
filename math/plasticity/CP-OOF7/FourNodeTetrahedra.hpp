//
//  FourNodeTetrahedra.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 5/11/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef FourNodeTetrahedra_hpp
#define FourNodeTetrahedra_hpp

#include <stdio.h>
#include "Element.hpp"

class FourNodeTetrahedra : public Element{
    
public:
    
    FourNodeTetrahedra(int id,int nnode,std::vector<Node*> nodelist) : Element(id,nnode,nodelist) {};
    virtual void gausspts();
    
    double ptsi[3];
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


};
#endif /* FourNodeTetrahedra_hpp */

