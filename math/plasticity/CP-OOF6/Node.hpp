//
//  Node.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Node_hpp
#define Node_hpp

#include <stdio.h>
#include <vector>
#include "Field.hpp"
//#include "Equation.hpp"

class Equation;

class Node{
    
public:
    Node(int id,double x,double y,double z);
    
    int inode;
    double coorx;
    double coory;
    double coorz;
    
    void addfield(Field *field);
    std::vector<Field*> fields;

    void addequation(Equation* equation);
    
    std::vector<Equation*> equations;
    
    int nfieldcomps();



};
#endif /* Node_hpp */
