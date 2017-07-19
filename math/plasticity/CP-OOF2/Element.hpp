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

class Material;


class Element {
    
public:
    Element(int id,int nnode,std::vector<int> &elconnectivities);
    
    void addmaterial(Material mtl);

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
    
private:
    
    Material *material;
    double mpt;
    double pts[2];
    double wts[2];


};

#endif /* Element_hpp */
