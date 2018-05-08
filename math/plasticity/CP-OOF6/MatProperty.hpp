//
//  MatProperty.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef MatProperty_hpp
#define MatProperty_hpp

#include <stdio.h>
#include <map>
#include "Tensor.hpp"

class MatProperty {
    
public:
    
    void setSize(int sizeIn);
    Vector prop;
};

#endif /* MatProperty_hpp */
