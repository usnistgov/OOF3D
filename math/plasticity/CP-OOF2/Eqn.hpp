//
//  Eqn.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/29/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Eqn_hpp
#define Eqn_hpp

#include <stdio.h>
#include <string>
#include "CauchyStress.hpp"

using namespace std;

class Eqn{
    
public:
    Eqn(string const& nam,int const& idx,int const& siz);
    
    string name;
    int index;
    int size;
    
};

#endif /* Eqn_hpp */
