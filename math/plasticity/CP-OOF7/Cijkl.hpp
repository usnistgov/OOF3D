//
//  Cijkl.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Cijkl_hpp
#define Cijkl_hpp

#include <stdio.h>
#include "Tensor.hpp"

class Cijkl {
public:
    Cijkl(double c11,double c12, double c44);
    Cijkl();
    
    double operator()(int,int,int,int) const;
    double &operator()(int,int,int,int);
    
    Cijkl rotate(Tensor2d &qrot);
private:
    
    Tensor4d cijkl;
};


#endif /* Cijkl_hpp */
