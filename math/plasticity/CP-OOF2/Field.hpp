//
//  Field.hpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Field_hpp
#define Field_hpp

#include <stdio.h>
#include <string>
#include <vector>

using namespace std;



class Field{
    
public:
    
    Field(string const nam,int const idx,int const siz);
    
    string name;
    int index;
    int size;
    std::vector<double> value;
    
};

#endif /* Field_hpp */
