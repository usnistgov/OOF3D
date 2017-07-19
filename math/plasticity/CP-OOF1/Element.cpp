//
//  Element.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Element.hpp"

Element::Element(int id,int &nnode,vector<int> &elconnectivities){
    
    ielem = id;
    lnode.resize(nnode);
    for (int i = 0 ; i < nnode ; i++){
        lnode[i] = elconnectivities[i];
    }
    
}


double Element::addmaterial(Material mtl){
    
    Material material = mtl;
    
    return 0;
}


double Element::make_linear_system(Mesh m){
    
//    gausspts();
    
    material.begin_element(this);
    
    for (int i = 0 ; i < 8 ; i++){
        material.make_linear_system();
    }
    
    material.end_element();

    return 0;
}

double Element::gausspts(){
  
    
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
    

    
    return 0;
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

