//
//  GaussPoint.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/28/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef GaussPoint_hpp
#define GaussPoint_hpp

#include <stdio.h>
#include<vector>


class GaussPoint {
    
public:
    
    GaussPoint(double x,double z,double m,double w);
    
    double xi;
    double zeta;
    double mu;
    double weight;
    
};

#endif /* GaussPoint_hpp */
