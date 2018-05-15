//
//  Element.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Element_hpp
#define Element_hpp
#warning "loading Element.hpp"

#include <stdio.h>
#include <vector>
#include <cmath>
#include <iostream>
#include "Material.hpp"
#include "Node.hpp"
#include "GaussPoint.hpp"
#include "ElementData.hpp"
#include "GptPlasticData.hpp"

#include "CrystalInput.hpp"

class Mesh;

class Element {
    
public:
    Element(int id,int node,std::vector<Node*> nodelist);
    void addmaterial(Material *mtl);
    std::vector<Node*> nodes;
    int nnode;
    int ielem;

    virtual void gausspts() = 0;
    
    std::vector<GaussPoint*> gptable;
    
    void make_linear_system(Mesh* mesh);

    //====================================================================
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
    //==========================================================================

    double dshapefnRef(double xi,double zeta,double mu,int node_idx,int refcomp);
    std::vector<std::vector<double>> jacobian;
    void jacobianmtx(double xi,double zeta,double mu);
    std::vector<std::vector<double>> dsfns;
    
    virtual void dsfnsvec(double xi,double zeta,double mu) = 0;

/*
    void dsfnsvec(double xi,double zeta,double mu);
    
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

*/
    int nfieldcomps();
    
    double dshapefn_current(double xi,double zeta,double mu,int node_idx,int refcomp);
    void jacobianmtx_current(double xi,double zeta,double mu);
    double jacobian_current(double xi,double zeta,double mu);

    Material *material;


    double dshapefnRef_tet(double xi,double zeta,double mu,int node_idx,int refcomp);
    std::vector<std::vector<double>> jacobian_tet;
    void jacobianmtx_tet(double xi,double zeta,double mu);
    std::vector<std::vector<double>> dsfns_tet;
    void dsfnsvec_tet(double xi,double zeta,double mu);

    double dsf0d0_tet(double xi,double zeta,double mu);
    double dsf0d1_tet(double xi,double zeta,double mu);
    double dsf0d2_tet(double xi,double zeta,double mu);
    
    double dsf1d0_tet(double xi,double zeta,double mu);
    double dsf1d1_tet(double xi,double zeta,double mu);
    double dsf1d2_tet(double xi,double zeta,double mu);
    
    double dsf2d0_tet(double xi,double zeta,double mu);
    double dsf2d1_tet(double xi,double zeta,double mu);
    double dsf2d2_tet(double xi,double zeta,double mu);
    
    double dsf3d0_tet(double xi,double zeta,double mu);
    double dsf3d1_tet(double xi,double zeta,double mu);
    double dsf3d2_tet(double xi,double zeta,double mu);

private:

    double xi_evaled,zeta_evaled,mu_evaled;
    std::vector<std::vector<double>> dshapefnRefmtx(double xi,double zeta,double mu);
    std::vector<std::vector<double> > jmtx_cache;
    
    std::vector<std::vector<double> > jmtx_cache_current;
    std::vector<std::vector<double>> dshapefn_currentmtx(double xi,double zeta,double mu);

    std::vector<std::vector<double>> dshapefnRefmtx_tet(double xi,double zeta,double mu);
    std::vector<std::vector<double> > jmtx_cache_tet;



};
#endif /* Element_hpp */
