//
//  Node.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
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

void Node::addequation(Equation *equation){
    equations.push_back(equation);
}

int Node::nfieldcomps(){
    
    int res = 0;
    
    for (std::vector<Field*>::iterator nf = fields.begin() ; nf != fields.end() ; nf++){
        res +=  (*nf)->size;
    }
    
    return res;
    
}

