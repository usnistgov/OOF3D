//
//  Element.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Element_hpp
#define Element_hpp

#include <stdio.h>
#include <vector>
#include <cmath>
#include <iostream>
#include "ElementData.hpp"
#include "GaussPoint.hpp"

#include "GptPlasticData.hpp"

//#include "Material.hpp"
#include "Node.hpp"


class Material;


class Element {
    
public:
    Element(int id,int nnode,std::vector<Node> &nodelist);
    
    void addmaterial(Material *mtl);

    std::vector<Node> nodes;

    void make_linear_system();
    
    void gausspts();
    
    int ielem;
    std::vector<int>lnode;
    vector<GaussPoint> gptable;
    
//    vector<double> array;
    

    std::vector<ElementData*> el_data;
    
    int appendData(ElementData *x) ;
    void setData(int i, ElementData *x);
    
    
    ElementData *getData(int i) ;
    // This call does retrieval-by-name, and so should be used
    // as infrequently as can be managed.
    ElementData *getDataByName(const std::string &name);
    // Overwrites the data indexed under the indicated name, appends
    // it, whichever.
    //    void setDataByName(ElementData *x);
    void setDataByName(ElementData *x,const std::string &name);
    
    // Retrieval by name should be done infrequently, to avoid the search.
    int getIndexByName(const std::string &searchname) ;
    
    
    // Deletion functions do not remove the pointed-to object, they just
    // remove the ElementData* from the element object's local array.
    void delData(int i) ;
    void delDataByName(const std::string &name);
    void clearData();
    
    
    std::vector<std::vector<double>> dshapefnRef(double xi,double zeta,double mu);
    void jacobianmtx(double xi,double zeta,double mu);
    void dsfnsvec(double xi,double zeta,double mu);
    
    std::vector<vector<double>> dsfns;
    std::vector<vector<double>> jacobian;
    
    
    double dsf0d0(double xi,double zeta,double mu);
    double dsf0d1(double xi,double zeta,double mu);
    double dsf0d2(double xi,double zeta,double mu);
    
    double dsf1d0(double xi,double zeta,double mu);
    double dsf1d1(double xi,double zeta,double mu);
    double dsf1d2(double xi,double zeta,double mu);
    
    double dsf2d0(double xi,double zeta,double mu);
    double dsf2d1(double xi,double zeta,double mu);
    double dsf2d2(double xi,double zeta,double mu);
    
    double dsf3d0(double xi,double zeta,double mu);
    double dsf3d1(double xi,double zeta,double mu);
    double dsf3d2(double xi,double zeta,double mu);
    
    double dsf4d0(double xi,double zeta,double mu);
    double dsf4d1(double xi,double zeta,double mu);
    double dsf4d2(double xi,double zeta,double mu);
    
    double dsf5d0(double xi,double zeta,double mu);
    double dsf5d1(double xi,double zeta,double mu);
    double dsf5d2(double xi,double zeta,double mu);
    
    double dsf6d0(double xi,double zeta,double mu);
    double dsf6d1(double xi,double zeta,double mu);
    double dsf6d2(double xi,double zeta,double mu);
    
    double dsf7d0(double xi,double zeta,double mu);
    double dsf7d1(double xi,double zeta,double mu);
    double dsf7d2(double xi,double zeta,double mu);

    
private:
    
    Material *material;
    double mpt;
    double pts[2];
    double wts[2];


};

#endif /* Element_hpp */
