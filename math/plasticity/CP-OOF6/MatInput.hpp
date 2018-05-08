//
//  MatInput.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef MatInput_hpp
#define MatInput_hpp

#include <stdio.h>
#include <map>
#include <vector>

#include "CrystalInput.hpp"
#include "MatProperty.hpp"
#include "Tensor.hpp"

struct MatInput{
    
    MatType mtype;
    ConstType ctype;
    std::map<ConstType,MatProperty> MatProp;
    Vector CijklConst;
    Vector Orientation;
    
    
};

#endif /* MatInput_hpp */
