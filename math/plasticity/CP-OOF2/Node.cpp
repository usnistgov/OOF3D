//
//  Node.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Node.hpp"
Node::Node(int id,double x,double y,double z){
    
    inode = id;
    coorx = x;
    coory = y;
    coorz = z;
    
    
}

void Node::addfield(Field *field){
    
    fields.push_back(field);
    
}
