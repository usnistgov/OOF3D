//
//  Equation.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/28/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Equation.hpp"
#include "CrystalPlasticity.hpp"
Equation::Equation(std::string const nam, int const id, int const siz,CrystalPlasticity* cp){
    
    name = nam;
    index = id;
    size = siz;
   flux = cp;
//    flux = dynamic_cast<CrystalPlasticity *>(cp);
}

void Equation::make_linear_system(int ndx, Element *el, GaussPoint *gpt, Vector &flux_vector, Tensor2d &flux_fderivs, Tensor2d &flux_fderivsg, Vector &fmap,Mesh* mesh){
    
    std::vector<int> jvec = {0,0,0,1,1,1,2,2,2};
    int row , j , col;
    double res , eqval , cres;
    
    for (int fxcomp = 0 ; fxcomp < this->flux->dim ; fxcomp++){
        
        res = eqval = cres = 0.0;
        row = this->index + this->flux->t_row[fxcomp];
        j = this->flux->t_col[fxcomp];
        res = el->dshapefn_current(gpt->xi, gpt->zeta, gpt->mu,ndx,j);
        res *= (-1.0)*el->jacobian_current(gpt->xi,gpt->zeta,gpt->mu)*gpt->weight;
        //######### eqval is the equation value to calculate the residual stresses
        eqval = res*flux_vector(fxcomp);
        
        try{
            mesh-> equations(row) += eqval;
        }
        catch(int er){
            mesh->equations(row) = eqval;
        }
//        int mapsize = sizeof(fmap);
        int mapsize = fmap.size();

        for (int fxcol = 0 ;  fxcol < mapsize ; fxcol++){
            col = fmap(fxcol);
            cres = res * flux_fderivs(fxcomp,fxcol);
            try{
                mesh->matrix(row,col) += cres;
            }
            catch(int er1){
                mesh->matrix(row,col) = cres;
            }
        }
    }
    
    
    int rowg , jg;
    double resg , cresg;
    for (int fxcomp = 0 ; fxcomp < this->flux->dim ; fxcomp++){
        
        rowg = this->index + this->flux->t_colg[fxcomp];
        jg = this->flux->t_rowg[fxcomp];
        
        
        resg = el->dshapefn_current(gpt->xi, gpt->zeta, gpt->mu,ndx,jg);
        resg *= (-1.0)*el->jacobian_current(gpt->xi,gpt->zeta,gpt->mu)*gpt->weight;
        
//        int mapsize = sizeof(fmap);
        int mapsize = fmap.size();

        for (int fxcol = 0 ; fxcol < mapsize ; fxcol++){
            col = fmap(fxcol);
            cresg = resg * flux_fderivsg(fxcomp,fxcol);
            
            mesh->matrix(rowg,col) += cresg;
        }
    }
    
    
}

