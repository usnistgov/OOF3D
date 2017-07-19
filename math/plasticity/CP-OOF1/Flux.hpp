//
//  Flux.hpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/11/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Flux_hpp
#define Flux_hpp

#include <stdio.h>
#include <string>

using namespace std;

class Flux{
    
public:
    
//    Flux();
    Flux(string const& nam,string const& fname,int const& dimension);
    

    string name;
    string fieldname;
    int dim;
    
};

#endif /* Flux_hpp */
