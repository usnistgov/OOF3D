//
//  Node.hpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Node_hpp
#define Node_hpp

#include <stdio.h>
#include <vector>
#include "Field.hpp"


using namespace std;

class Node{
    
public:
    Node(int id,double x,double y,double z);
    void addfield(Field *field);

    int inode;
    double coorx;
    double coory;
    double coorz;
    
    vector<Field*> fields;

    
    
};

#endif /* Node_hpp */
