//
//  Node.hpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Node_hpp
#define Node_hpp

#include <stdio.h>
#include "Field.hpp"
#include <vector>
#include "Eqn.hpp"


using namespace std;

class Node{
    
public:
    Node(int id,double x,double y,double z);
    
    double addfield(Field field);

    double addeqn(Eqn eqn);

    
    int inode;
    double coorx;
    double coory;
    double coorz;
    
    vector<Field> fields;
    vector<Eqn> eqns;
    
    
    
    
    
};
#endif /* Node_hpp */
