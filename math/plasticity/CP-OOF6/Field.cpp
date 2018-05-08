//
//  Field.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/28/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Field.hpp"

Field::Field(std::string const nam,int const idx,int const siz){
    name = nam;
    index = idx;
    size = siz;
    value.clear();
    for (int i = 0 ; i < size ; i++)
        value.push_back(0.0);
}

void Field::set(int idx,double v){
    this->value[idx] = v;
}

void Field::add(int idx, double v){
    this->value[idx] += v;
}
