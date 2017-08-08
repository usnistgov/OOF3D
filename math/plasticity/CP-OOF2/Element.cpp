//
//  Element.cpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Element.hpp"
#include "Material.hpp"

Element::Element(int id,int nnode,std::vector<Node> &nodelist){
    
    ielem = id;
    
    nodes = nodelist;
    /*    lnode.resize(nnode);
     for (int i = 0 ; i < nnode ; i++){
     lnode[i] = elconnectivities[i];
     }
     */
}

void Element::addmaterial(Material *mtl){
    
    material = mtl;
    
}


void Element::make_linear_system(){
    
    gptable.clear();
    gausspts();
    material->begin_element(this);
    
}

void Element::gausspts(){
    
    
    mpt = pow((1.0/3.0),0.5);
    pts[0] = -mpt, pts[1] = mpt;
    wts[0] = 1.0 , wts[1] = 1.0;
    
    int n = 2;
    
    int stuff;
    for(int i = 0 ; i < 2 ; i ++){
        for(int j = 0 ; j < 2 ; j ++){
            for(int k = 0 ; k < 2 ; k ++){
                GaussPoint gp(pts[i],pts[j],pts[k],wts[k]*wts[j]*wts[i]);
                gptable.push_back(gp);
            }
        }
    }
    
    
    
}


int Element::appendData(ElementData *x)  {
    el_data.push_back(x);
    return el_data.size()-1;
}

void Element::setData(int i, ElementData *x)  {
    el_data[i]=x;
}

ElementData *Element::getData(int i)  {
    return el_data[i];
}


// This call does retrieval-by-name, and so should be used
// as infrequently as can be managed.
ElementData *Element::getDataByName(const std::string &name)  {
    int i=getIndexByName(name);
    if (i>=0)
        return getData(i);
    else
        return 0;
}

// Overwrites the data indexed under the indicated name, appends
// it, whichever.
void Element::setDataByName(ElementData *x,const std::string &name)  {
    int i=getIndexByName(x->name());
    if (i>=0)
        // NB Does this overwrite have implications for reference counts
        // of the referred-to Python data?
        setData(i,x);
    else
        appendData(x);
}


// Retrieval by name should be done infrequently, to avoid the search.
int Element::getIndexByName(const std::string &searchname)  {
    for(std::vector<ElementData*>::size_type i=0; i<el_data.size(); i++) {
        if (el_data[i]->name() == searchname) {
            return i;
        }
    }
    // Not found -- this is permissible, return something.
    return -1;
}



// Deletion functions do not remove the pointed-to object, they just
// remove the ElementData* from the element object's local array.
void Element::delData(int i)  {
    std::vector<ElementData*>::iterator it = el_data.begin();
    it += i;
    el_data.erase(it);
}

void Element::delDataByName(const std::string &name)  {
    std::vector<ElementData*>::iterator it = el_data.begin();
    int i=getIndexByName(name);
    it += i;
    el_data.erase(it);
}

void Element::clearData()  {
    el_data.clear();
}

//------------------------------------------------------------------
std::vector<vector<double>> Element::dshapefnRef(double xi,double zeta,double mu){
    
    
    
    jacobianmtx(xi,zeta,mu);
    
    
    
    double det = jacobian[0][0]*jacobian[1][1]*jacobian[2][2]-jacobian[0][0]*jacobian[1][2]*jacobian[2][1]-jacobian[1][0]*jacobian[0][1]\
    *jacobian[2][2]+jacobian[1][0]*jacobian[0][2]*jacobian[2][1]+jacobian[2][0]*jacobian[0][1]*jacobian[1][2]-jacobian[2][0]\
    *jacobian[0][2]*jacobian[1][1];
    
    double jinv[3][3];
    jinv[0][0] =  ( jacobian[1][1]*jacobian[2][2]-jacobian[1][2]*jacobian[2][1])/det;
    jinv[0][1] = -( jacobian[0][1]*jacobian[2][2]-jacobian[0][2]*jacobian[2][1])/det;
    jinv[0][2] = -(-jacobian[0][1]*jacobian[1][2]+jacobian[0][2]*jacobian[1][1])/det;
    jinv[1][0] = -( jacobian[1][0]*jacobian[2][2]-jacobian[1][2]*jacobian[2][0])/det;
    jinv[1][1] =  ( jacobian[0][0]*jacobian[2][2]-jacobian[0][2]*jacobian[2][0])/det;
    jinv[1][2] = -( jacobian[0][0]*jacobian[1][2]-jacobian[0][2]*jacobian[1][0])/det;
    jinv[2][0] =  ( jacobian[1][0]*jacobian[2][1]-jacobian[1][1]*jacobian[2][0])/det;
    jinv[2][1] = -( jacobian[0][0]*jacobian[2][1]-jacobian[0][1]*jacobian[2][0])/det;
    jinv[2][2] =  ( jacobian[0][0]*jacobian[1][1]-jacobian[0][1]*jacobian[1][0])/det;
    
    
    
    std::vector<double> dfdmaster(3,0.0);
    
    std::vector<vector<double>> dfdreft;
    
    std::vector<double> dfdref(3,0.0);
    
    for (int i = 0 ; i < 8 ; i++){
        dfdmaster[0] = dsfns[i][0];
        dfdmaster[1] = dsfns[i][1];
        dfdmaster[2] = dsfns[i][2];
        
        
        for (int ix = 0 ; ix < 3 ; ix++){
            dfdref[ix] = 0.0;
            for (int jx = 0 ; jx < 3 ; jx++){
                dfdref[ix] += jinv[ix][jx]*dfdmaster[jx];
            }
        }
        
        
        dfdreft.push_back(dfdref);
        
    }
    
    return dfdreft;
}



void Element::jacobianmtx(double xi,double zeta,double mu){
    
    dsfnsvec(xi,zeta,mu);
    
    jacobian.clear();
    std::vector<double> jac{0.0,0.0,0.0};
    
    for (int i = 0 ; i < 3 ; i++){
        jacobian.push_back(jac);
    }
    
    for (int i = 0 ; i < 8 ; i++){
        jacobian[0][0] += dsfns[i][0]*nodes[i].coorx;
        jacobian[0][1] += dsfns[i][0]*nodes[i].coory;
        jacobian[0][2] += dsfns[i][0]*nodes[i].coorz;
        
        jacobian[1][0] += dsfns[i][1]*nodes[i].coorx;
        jacobian[1][1] += dsfns[i][1]*nodes[i].coory;
        jacobian[1][2] += dsfns[i][1]*nodes[i].coorz;
        
        jacobian[2][0] += dsfns[i][2]*nodes[i].coorx;
        jacobian[2][1] += dsfns[i][2]*nodes[i].coory;
        jacobian[2][2] += dsfns[i][2]*nodes[i].coorz;
    }
    
}

void Element::dsfnsvec(double xi,double zeta,double mu){
    
    
    std::vector<double> ds{0.0,0.0,0.0};
    
    for (int i = 0 ; i < 8 ; i++){
        dsfns.push_back(ds);
    }
    
    dsfns[0][0] = dsf0d0(xi,zeta,mu);
    dsfns[0][1] = dsf0d1(xi,zeta,mu);
    dsfns[0][2] = dsf0d2(xi,zeta,mu);
    dsfns[1][0] = dsf1d0(xi,zeta,mu);
    dsfns[1][1] = dsf1d1(xi,zeta,mu);
    dsfns[1][2] = dsf1d2(xi,zeta,mu);
    dsfns[2][0] = dsf2d0(xi,zeta,mu);
    dsfns[2][1] = dsf2d1(xi,zeta,mu);
    dsfns[2][2] = dsf2d2(xi,zeta,mu);
    dsfns[3][0] = dsf3d0(xi,zeta,mu);
    dsfns[3][1] = dsf3d1(xi,zeta,mu);
    dsfns[3][2] = dsf3d2(xi,zeta,mu);
    dsfns[4][0] = dsf4d0(xi,zeta,mu);
    dsfns[4][1] = dsf4d1(xi,zeta,mu);
    dsfns[4][2] = dsf4d2(xi,zeta,mu);
    dsfns[5][0] = dsf5d0(xi,zeta,mu);
    dsfns[5][1] = dsf5d1(xi,zeta,mu);
    dsfns[5][2] = dsf5d2(xi,zeta,mu);
    dsfns[6][0] = dsf6d0(xi,zeta,mu);
    dsfns[6][1] = dsf6d1(xi,zeta,mu);
    dsfns[6][2] = dsf6d2(xi,zeta,mu);
    dsfns[7][0] = dsf7d0(xi,zeta,mu);
    dsfns[7][1] = dsf7d1(xi,zeta,mu);
    dsfns[7][2] = dsf7d2(xi,zeta,mu);
    
    
}

double Element::dsf0d0(double xi,double zeta,double mu){
    return -0.125*(zeta-1.0)*(mu-1.0);
}
double Element::dsf0d1(double xi,double zeta,double mu){
    return -0.125*(xi-1.0)*(mu-1.0);
}
double Element::dsf0d2(double xi,double zeta,double mu){
    return -0.125*(xi-1.0)*(zeta-1.0);
}


double Element::dsf1d0(double xi,double zeta,double mu){
    return +0.125*(zeta-1.0)*(mu+1.0);
}
double Element::dsf1d1(double xi,double zeta,double mu){
    return +0.125*(xi-1.0)*(mu+1.0);
}
double Element::dsf1d2(double xi,double zeta,double mu){
    return +0.125*(xi-1.0)*(zeta-1.0);
}


double Element::dsf2d0(double xi,double zeta,double mu){
    return +0.125*(zeta+1.0)*(mu-1.0);
}
double Element::dsf2d1(double xi,double zeta,double mu){
    return +0.125*(xi-1.0)*(mu-1.0);
}
double Element::dsf2d2(double xi,double zeta,double mu){
    return +0.125*(xi-1.0)*(zeta+1.0);
}


double Element::dsf3d0(double xi,double zeta,double mu){
    return -0.125*(zeta+1.0)*(mu+1.0);
}
double Element::dsf3d1(double xi,double zeta,double mu){
    return -0.125*(xi-1.0)*(mu+1.0);
}
double Element::dsf3d2(double xi,double zeta,double mu){
    return -0.125*(xi-1.0)*(zeta+1.0);
}


double Element::dsf4d0(double xi,double zeta,double mu){
    return +0.125*(zeta-1.0)*(mu-1.0);
}
double Element::dsf4d1(double xi,double zeta,double mu){
    return +0.125*(xi+1.0)*(mu-1.0);
}
double Element::dsf4d2(double xi,double zeta,double mu){
    return +0.125*(xi+1.0)*(zeta-1.0);
}


double Element::dsf5d0(double xi,double zeta,double mu){
    return -0.125*(zeta-1.0)*(mu+1.0);
}
double Element::dsf5d1(double xi,double zeta,double mu){
    return -0.125*(xi+1.0)*(mu+1.0);
}
double Element::dsf5d2(double xi,double zeta,double mu){
    return -0.125*(xi+1.0)*(zeta-1.0);
}


double Element::dsf6d0(double xi,double zeta,double mu){
    return -0.125*(zeta+1.0)*(mu-1.0);
}
double Element::dsf6d1(double xi,double zeta,double mu){
    return -0.125*(xi+1.0)*(mu-1.0);
}
double Element::dsf6d2(double xi,double zeta,double mu){
    return -0.125*(xi+1.0)*(zeta+1.0);
}


double Element::dsf7d0(double xi,double zeta,double mu){
    return +0.125*(zeta+1.0)*(mu+1.0);
}
double Element::dsf7d1(double xi,double zeta,double mu){
    return +0.125*(xi+1.0)*(mu+1.0);
}
double Element::dsf7d2(double xi,double zeta,double mu){
    return +0.125*(xi+1.0)*(zeta+1.0);
}















