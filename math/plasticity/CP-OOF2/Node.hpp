//
//  Node.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Node_hpp
#define Node_hpp

#include <stdio.h>
#include <vector>
#include "Field.hpp"
//#include "Eqn.hpp"


using namespace std;

class Node{
    
public:
    Node(int id,double x,double y,double z);
    
    
//    void addfield(Field *field);
    
    
//    void addeqn(Eqn eqn);
    
    int inode;
    double coorx;
    double coory;
    double coorz;
    
    vector<Field*> fields;
    
    
    
    
//    vector<Eqn> eqns;
 
    
};



#endif /* Node_hpp */
