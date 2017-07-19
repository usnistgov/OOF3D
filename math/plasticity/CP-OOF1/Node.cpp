//
//  Node.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Node.hpp"

Node::Node(int id,double x,double y,double z){

    inode = id;
    coorx = x;
    coory = y;
    coorz = z;
    
    
}

double Node::addfield(Field field){
    
    fields.push_back(field);
    
    return 0;
}


double Node::addeqn(Eqn eqn){
    
    eqns.push_back(eqn);
    
    return 0;
}
