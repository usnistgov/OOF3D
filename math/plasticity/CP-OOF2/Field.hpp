//
//  Field.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/29/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Field_hpp
#define Field_hpp

#include <stdio.h>
#include <string>

using namespace std;



class Field{
    
public:
    
    Field(string const& nam,int const& idx,int const& siz);
    
    string name;
    int index;
    int size;
    
};


#endif /* Field_hpp */
