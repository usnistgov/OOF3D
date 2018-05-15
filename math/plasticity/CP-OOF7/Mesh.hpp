//
//  Mesh.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Mesh_hpp
#define Mesh_hpp

#include <stdio.h>
#include <vector>
#include <iostream>
#include<fstream>

#include "Node.hpp"
//#include "Element.hpp"
#include "Material.hpp"
#include "Field.hpp"
#include "Equation.hpp"

//#include "CrystalPlasticity.hpp"


class CrystalPlasticity;

class Mesh{
    
public:
    
    Mesh(std::istream &inFile);

    Mesh(int xelement, int yelement, int zelement);
    
    std::vector<Node*> nodelist;
    int nnode;
    int tnode;
    int nelem;
    std::vector<Element*> ellist;
    int nbw;

    void add_material_to_all(Material *mtl);
    
    void addfield(std::string const name,int const size, double value);
    std::vector<Field*> fieldlist;

    void addeqn(std::string const name,int const size, CrystalPlasticity* cp);
    std::vector<Equation*> equationlist;

    void make_stiffness();
    int neq;
    Tensor2d matrix;
    Vector equations;
    void setSize(int sizeEq);
    
//+++++++++++++++++++++++++++++++++++++++++++++
    void new_setbcs();
    void solvesyseq();
    void solve_nonlinear();
    
//    void userprint(Material* mt);
//    void true_strain(Tensor2d &C);

    std::vector<int> freeeqns;
    Vector f_bc;
    Vector b_rhs;

    int nbc;
    std::vector<int> kbc_n;
    std::vector<int> kbc_d;
    std::vector<double> kbc_v;
    double factor1;
    
    Tensor2d strain;
    double stressvol1;
    double strainvol1;

//+++++++++++++++++++++++++++++++++++++++++++++

    void user_print();
    void true_strain(Tensor2d &C);

private:
    
    double dx;
    double dy;
    double dz;
    std::vector <int> elconnectivities;

    
};
#endif /* Mesh_hpp */
