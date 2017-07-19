//
//  GaussPoint.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef GaussPoint_hpp
#define GaussPoint_hpp

#include <stdio.h>
#include<vector>

using namespace std;

class GaussPoint {
    
public:
    
    GaussPoint(double x,double z,double m,double w);
    
    double xi;
    double zeta;
    double mu;
    double weight;
    
};

#endif /* GaussPoint_hpp */
