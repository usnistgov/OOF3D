//
//  Field.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/28/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Field_hpp
#define Field_hpp

#include <stdio.h>
#include <string>
#include <vector>




class Field{
    
public:
    
    Field(std::string const nam,int const idx,int const siz);
    void set(int idx,double v);
    void add(int idx, double v);
    
    std::string name;
    int index;
    int size;
    std::vector<double> value;
    
};

#endif /* Field_hpp */
