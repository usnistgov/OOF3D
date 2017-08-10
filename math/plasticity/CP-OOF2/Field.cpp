//
//  Field.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Field.hpp"

Field::Field(string const nam,int const idx,int const siz){
    
    name = nam;
    index = idx;
    size = siz;
    value.clear();
    for (int i = 0 ; i < size ; i++)
        value.push_back(0.0);
    
    
    
}
