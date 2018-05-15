//
//  Material.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Material.hpp"

void Material::begin_element(Element *e, Mesh *m) {
    
    for (std::vector<Property*>::iterator pi = props.begin(); pi!=props.end(); ++pi) {
        (*pi)->begin_element(e,m);
    }
    
}

void Material::add_flux_property(Flux *f) {
    fluxprops.push_back(f);
    add_property(f); // add_property pushes back flux into the props.
}

void Material::cross_reference() {

    for (std::vector<Property*>::iterator pi = props.begin(); pi!=props.end(); ++pi)
        (*pi)->cross_reference(this);

}

Property * Material::get_by_tag(std::string tag) {
    for (std::vector<Property*>::iterator pi = props.begin(); pi!=props.end(); ++pi)
        if ((*pi)->tag == tag )
            return (*pi);
    return NULL;
}

void Material::make_linear_system(Element *el,Mesh *mesh){
    el->gptable.clear();
    el->gausspts();
    
    for (std::vector<GaussPoint*>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++){

        for (std::vector<Flux*>::iterator fi = fluxprops.begin(); fi!=fluxprops.end(); ++fi){
            (*fi)->make_linear_system(el,(*gpti),std::distance(el->gptable.begin(), gpti));
            

            int icount = 0;
            for (std::vector<Node*>::iterator nd = el->nodes.begin() ; nd != el->nodes.end() ; nd++){
                for ( std::vector<Equation*>::iterator eqn = (*nd)->equations.begin() ; eqn != (*nd)->equations.end() ; eqn++){
                    (*eqn)->make_linear_system(icount,el,(*gpti),(*fi)->flux_vector,(*fi)->flux_fderivs,(*fi)->flux_fderivsg,(*fi)->fmap,mesh);
                }
                icount += 1;
            }
            

        }
        
   
        
    }


}
