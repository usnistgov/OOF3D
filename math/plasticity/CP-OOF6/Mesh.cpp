//
//  Mesh.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Mesh.hpp"

Mesh::Mesh(int xelement, int yelement, int zelement){
    
    
    dx = 1.0/xelement;
    dy = 1.0/yelement;
    dz = 1.0/zelement;
    nodelist.clear();
    
    tnode = -1;
    for (int i = 0 ; i < zelement + 1 ; i++){
        for (int j = 0 ; j < yelement + 1 ; j++){
            for (int k = 0 ; k < xelement + 1 ; k++){
                tnode += 1;
                Node *nod = new Node(tnode,k*dx,j*dy,i*dz);
                nodelist.push_back(nod);
                
            }
        }
    }
    tnode += 1;
    
    nnode = 8;
    
    elconnectivities.resize(nnode);
    
    nelem = -1;
    for (int i = 0 ; i < zelement ; i++){
        for (int j = 0 ; j < yelement ; j++){
            for (int k = 0 ; k < xelement ; k++){
                std::vector<Node*> nodes(0);
                elconnectivities[0] = i*(xelement+1)*(yelement+1)+j*(xelement+1)+k;
                elconnectivities[1] = i*(xelement+1)*(yelement+1)+j*(xelement+1)+k+1;
                elconnectivities[2] = i*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k+1;
                elconnectivities[3] = i*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k;
                elconnectivities[4] = (i+1)*(xelement+1)*(yelement+1)+j*(xelement+1)+k;
                elconnectivities[5] = (i+1)*(xelement+1)*(yelement+1)+j*(xelement+1)+k+1;
                elconnectivities[6] = (i+1)*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k+1;
                elconnectivities[7] = (i+1)*(xelement+1)*(yelement+1)+(j+1)*(xelement+1)+k;
                
                for (int kj = 0 ; kj < 8 ; kj++)
                    std::cout<<elconnectivities[kj]<<"   ";
                nelem += 1;
                for (int ki = 0 ; ki < nnode ; ki++){
                    nodes.push_back(nodelist[elconnectivities[ki]]);
                }
                std::cout<<std::endl;
                Element *el = new Element(nelem,nnode,nodes);
                
                ellist.push_back(el);
            }
        }
    }
    
    nelem += 1;
    
    
    // This is for solving systme equaions -------
    
    nbw = 0;
    std::vector<int> lnode;
    
    for(std::vector<Element*>::iterator el = ellist.begin() ; el != ellist.end() ; el++){
        lnode.clear();
        for (int i = 0 ; i < 8 ; i++)
            lnode.push_back((*el)->nodes[i]->inode);
        auto nb1 = max_element(begin(lnode), end(lnode));
        auto nb2 = min_element(begin(lnode), end(lnode));
        
        
        int nb = 3*((*nb1)-(*nb2)+1);
        if (nb > nbw)
            nbw = nb;
    }
    //-----------------------------------------------
    
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
void Mesh::add_material_to_all(Material *mtl){
    
    for (std::vector<Element*>::iterator eli = ellist.begin() ; eli!=ellist.end(); eli++){
        
        (*eli)->addmaterial(mtl);
    }
    
}
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
void Mesh::addfield(std::string const name,int const size, double value){
    
    int count = 0;
    for (std::vector<Node*>::iterator ni = nodelist.begin() ; ni!=nodelist.end(); ni++){
        
        //    for (int i = 0 ; i < tnode ; i++){
        
        Field *newf = new Field(name,size*count,size);
        
        (*ni)->addfield(newf);
        
        fieldlist.push_back(newf);
        count += 1;
        
    }
    
}

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//==============================================================================
void Mesh::addeqn(const std::string name, const int size, CrystalPlasticity *cp){
    
    int count = 0;
    for (std::vector<Node*>::iterator ni = nodelist.begin() ; ni!=nodelist.end(); ni++){
        
        Equation* neweqn = new Equation(name, count*size, size, cp);
        (*ni)->addequation(neweqn);
        equationlist.push_back(neweqn);
        count += 1;
    }
    
    
}
//==============================================================================

//$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
void Mesh::make_stiffness(){
    
    setSize(sizeof(equationlist));
    matrix.resize(neq,neq);
    matrix = 0.0;
    
    equations.resize(neq);
    equations = 0.0;
    for (std::vector<Element*>::iterator eli = ellist.begin() ; eli!=ellist.end(); eli++){
        (*eli)->gausspts();
        (*eli)->make_linear_system(this);
    }
 /*
    for (int i = 0 ; i <neq ; i++)
        for (int j = 0 ; j <neq ; j++)
            std::cout<<i<<"  "<<j<<"  "<<matrix(i,j)<<std::endl;
    
*/
}


//$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

void Mesh::setSize(int sizeEq){
    
    neq = sizeEq;
}

//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&







//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

void Mesh::new_setbcs(){
    
    f_bc.resize(neq);
    f_bc = 0.0;
    b_rhs.resize(neq);
    b_rhs = 0.0;
    freeeqns.resize(neq);
    for (int i = 0 ; i < neq ; i++)
        freeeqns[i] = 1;
    
    for(int ibc = 0 ; ibc < nbc ; ibc++){
        f_bc(3*kbc_n[ibc]+kbc_d[ibc]-1) = kbc_v[ibc];
    }
    
    for(int ibc = 0 ; ibc < nbc ; ibc++){
        int jbc = 3*kbc_n[ibc]+kbc_d[ibc]-1;
        freeeqns[jbc] = 0;
    }
    
}

void Mesh::solvesyseq(){
    
    Tensor2d matrixm;
    matrixm.resize(neq,neq);
    matrixm = 0.0;
    
    
    for(int ibc = 0 ; ibc < nbc ; ibc++){
        int jbc = 3*kbc_n[ibc]+kbc_d[ibc]-1;
        b_rhs(jbc) = matrix(jbc,jbc)*1.0e20*factor1*f_bc(jbc);
        matrix(jbc,jbc) = matrix(jbc,jbc)*1.0e20;
    }
    
    
    
    //#--------- storing first nbw rows---------
    for(int i = 0 ; i < neq-nbw+1 ; i++){
        int k = -1;
        for(int j = i ; j < i+nbw ; j++){
            k = k+1;
            matrixm(i,k) = matrix(i,j);
        }
    }
    //#--------- storing nbw+1 to neq rows---------
    for(int i = neq-nbw+1 ; i < neq ; i++){
        for(int j = 0 ; j < neq-i ; j++){
            matrixm(i,j) = matrix(i,j+i);
        }
    }
    
    //#------ End of storing total stiffness matrix into neq by nbw matrix ------
    //#------- Solve system equations bt Gauss elimination method-------
    for(int i = 0 ; i < neq-1 ; i++){
        int nbk = fmin(neq-i,nbw);
        for(int j = i+1 ; j < nbk+i ; j++){
            int j1=j-i;
            double c = matrixm(i,j1)/matrixm(i,0);
            for(int l = j ; l < nbk+i ; l++){
                int l1=l-j;
                int l2=l-i;
                matrixm(j,l1) += -c*matrixm(i,l2);
            }
            
            b_rhs(j) += -c*b_rhs(i);
        }
    }
    
    b_rhs(neq-1) = b_rhs(neq-1)/matrixm(neq-1,0);
    
    for(int ii = 0 ; ii < neq-1 ; ii++){
        int i = neq-ii-2;
        int nbi = fmin(neq-i,nbw);
        double up = 0.0;
        for(int j = 1 ; j < nbi ; j++){
            up += matrixm(i,j)*b_rhs(i+j-1+1);
        }
        b_rhs(i) = (b_rhs(i)-up)/matrixm(i,0);
    }
    
    
}


void Mesh::solve_nonlinear(){
    
    
    solvesyseq();
    
    int in = 0;
    for (std::vector<Node*>::iterator n = nodelist.begin() ; n != nodelist.end() ; n++){
        for (int k = 0 ; k < (*n)->fields[0]->size ; k++){
            (*n)->fields[0]->add(k,b_rhs(3*((*n)->inode)+k));
        }
        in += 1;
    }
    
    
    //--------------------- start convergence loop -----------------------
    
    int iconv = 0;
    int nconv = 5;
    double ratio_norm = 1.0e10;
    Vector magiter;
    magiter.resize(nconv);
    magiter = 0.0;
    
    double  gf_nod , unb_nod;
    double norm_gs , norm_us;
    while (iconv <= nconv-1 and abs(ratio_norm) >= 1.0e-9){
        
        if (iconv > 0){
            
            for (int i = 0 ; i < neq ; i++)
                b_rhs(i) = -1.0*equations(i);
            
            f_bc = 0.0;
            
            
            
            solvesyseq();
            
            int in = 0;
            for (std::vector<Node*>::iterator n = nodelist.begin() ; n != nodelist.end() ; n++){
                for (int k = 0 ; k < (*n)->fields[0]->size ; k++){
                    (*n)->fields[0]->add(k,b_rhs(3*((*n)->inode)+k));
                }
                in += 1;
            }
            
            
        }
        
        
        make_stiffness();
        ratio_norm = 0.0;
        
        gf_nod = unb_nod = 0.0;
        
        
        for (int i = 0 ; i < neq ; i++){
            gf_nod += equations(i)*equations(i);
        }
        
        for (int i = 0 ; i < neq ; i++){
            if (freeeqns[i] > 0){
                unb_nod += equations(i)*equations(i);
            }
            
        }
        
        norm_gs = pow(gf_nod , 0.5);
        norm_us = pow(unb_nod , 0.5);
        
        ratio_norm = norm_us/norm_gs;
        
        std::cout<<iconv<<"  "<<norm_us<<"  "<<norm_gs<<"  "<<ratio_norm<<std::endl;
        
        
        
        /*
         for (std::vector<Node*>::iterator n = nodelist.begin() ; n !=nodelist.end() ; n++){
         std::cout<<(*n)->inode<<"  "<<0<<" "<<(*n)->fields[0]->value[0]<<std::endl;
         std::cout<<(*n)->inode<<"  "<<1<<" "<<(*n)->fields[0]->value[1]<<std::endl;
         std::cout<<(*n)->inode<<"  "<<2<<" "<<(*n)->fields[0]->value[2]<<std::endl;
         
         }
         
         int sdt;
         cin>>sdt;
         */
        
        iconv += 1;
        
        
    }
    
    
}


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

void Mesh::user_print(){
    
    double volg = 0.0;
    double volt = 0.0;
    stressvol1 = 0.0;
    strainvol1 = 0.0;
    int ndim = 3;
    strain.resize(ndim,ndim);
    strain = 0.0;
    
    
    Tensor2d TMP1(ndim,ndim);
    Tensor2d TMPt(ndim,ndim);
    Tensor2d TMP3(ndim,ndim);
    
    TMP1 = TMPt = TMP3 = 0.0;

    for (std::vector<Element*>::iterator eli = ellist.begin() ; eli!=ellist.end(); eli++){
        
        Property *pl = ((*eli)->material)->get_by_tag("Plasticity");
        Flux *plf = dynamic_cast<Flux*>(pl);
        
        int ig = 0;
        for (std::vector<GaussPoint*>::iterator gpti = (*eli)->gptable.begin() ; gpti!=(*eli)->gptable.end(); gpti++){
            volg = (*eli)->jacobian_current((*gpti)->xi,(*gpti)->zeta,(*gpti)->mu)*(*gpti)->weight;
            plf->user_print(*gpti,std::distance((*eli)->gptable.begin(), gpti));
            stressvol1 += plf->cauchy_stress(1,1)*volg;
            TMP1 = plf->deformation_gradient;
            
            TMPt = ~TMP1;
            for(int i = 0 ; i < ndim ; i++){
                for(int j = 0 ; j < ndim ; j++){
                    TMP3(i,j) = 0.0;
                    for(int k = 0 ; k < ndim ; k++){
                        TMP3(i,j) += TMPt(i,k)*TMP1(k,j);
                    }
                }
            }
            true_strain(TMP3);
            strainvol1 += strain(1,1)*volg;
            volt += volg;
            ig += 1;
        }
    }
    
    stressvol1 = stressvol1 / volt;
    strainvol1 = strainvol1 / volt;
//    std::cout<<strainvol1<<"  "<<stressvol1<<std::endl;
//    int stuff;
//    std::cin>>stuff;

}

//############################## Calculate logarithmic or true strain ###########################
void Mesh::true_strain(Tensor2d &C){
    
    int ndim = 3;
    
    Tensor2d v(ndim,ndim);
    Vector beta(ndim);
    
    
    double p1 = pow(C(0,1),2) + pow(C(0,2),2) + pow(C(1,2),2);
    
    if (p1 < 1.0e-10){
        for (int ivec = 0 ; ivec < ndim ; ivec++){
            beta(ivec) = C(ivec,ivec);
            v(ivec,ivec) = 1.0;
        }
    }
    else if (p1 >= 1.0e-10){
        
        double q = 0.0;
        
        for(int i = 0 ; i < ndim ; i++){
            q += C(i,i);
        }
        q = q/3.0;
        
        Tensor2d Iden(ndim,ndim);
        Tensor2d tmp1(ndim,ndim);
        Tensor2d tmp2(ndim,ndim);
        Tensor2d tmp3(ndim,ndim);
        Tensor2d b(ndim,ndim);
        
        Iden = tmp1 = tmp2 = tmp3 = b = 0.0;
        
        Iden(0,0) = Iden(1,1) = Iden(2,2) = 1.0;
        
        for(int i = 0 ; i < ndim ; i++)
            for(int j = 0 ; j < ndim ; j++)
                tmp1(i,j) = C(i,j)-q*Iden(i,j);
        
        
        for(int i = 0 ; i < ndim ; i++){
            for(int j = 0 ; j < ndim ; j++){
                tmp2(i,j) = 0.0;
                for(int k = 0 ; k < ndim ; k++){
                    tmp2(i,j) += tmp1(i,k)*tmp1(k,j);
                }
                
                tmp2(i,j) = tmp2(i,j)/6.0;
            }
        }
        
        double p = 0.0;
        for(int i = 0 ; i < ndim ; i++){
            p += tmp2(i,i);
        }
        p = pow(p,0.5);
        
        for(int i = 0 ; i < ndim ; i++)
            for(int j = 0 ; j < ndim ; j++)
                b(i,j) = tmp1(i,j)/p;
        
        double det_b = b(0,0)*b(1,1)*b(2,2)-b(0,0)*b(1,2)*b(2,1)-b(1,0)*b(0,1)\
        *b(2,2)+b(1,0)*b(0,2)*b(2,1)+b(2,0)*b(0,1)*b(1,2)-b(2,0)\
        *b(0,2)*b(1,1);
        
        double r = det_b/2.0;
        double phi = 0.0;
        double const_pi = acos(-1.0);
        if (r <= -1.0)
            phi = const_pi/3.0;
        else if (r >= 1.0)
            phi = 0.0;
        else if (r > -1.0 and r < 1.0)
            phi = acos(r)/3.0;
        
        
        beta(0) = q + 2.0 * p * cos(phi);
        beta(1) = q + 2.0 * p * cos(phi + (2.0 * const_pi / 3.0));
        beta(2) = 3.0 * q - beta(0) - beta(1);
        
        double alpha = 0.0;
        double alpha1 = 0.0;
        double alpha2 = 0.0;
        double alpha21 = 0.0;
        double alpha22 = 0.0;
        double alpha3 = 0.0;
        
        for (int ivec = 0 ; ivec < ndim ; ivec++){
            for(int i = 0 ; i < ndim ; i++)
                for(int j = 0 ; j < ndim ; j++)
                    tmp3(i,j) = C(i,j)-beta(ivec)*Iden(i,j);
            
            if (tmp3(2,2) != 0.0){
                alpha1 = 1.0;
                alpha21 = -tmp3(1,0)+(tmp3(1,2)*tmp3(2,0)/tmp3(2,2));
                alpha22 = tmp3(1,1)-(tmp3(1,2)*tmp3(2,1)/tmp3(2,2));
                alpha2 = alpha21/alpha22;
                alpha3 = (-tmp3(2,0)/tmp3(2,2))-(tmp3(2,1)/tmp3(2,2))*alpha2;
            }
            if (tmp3(2,2) == 0.0 and tmp3(2,1) != 0.0){
                alpha1 = 1.0;
                alpha2 = -tmp3(2,0)/tmp3(2,1);
                if (tmp3(1,2) != 0.0){
                    alpha3 = (tmp3(1,0)-tmp3(1,1)*alpha2)/tmp3(1,2);
                }
                else if (tmp3(1,2) == 0.0 and tmp3(0,2) != 0.0){
                    alpha3 = (tmp3(0,0)-tmp3(0,1)*alpha2)/tmp3(1,2);
                }
                else if (tmp3(1,2) == 0.0 and tmp3(0,2) == 0.0){
                    alpha3 = 0.0;
                }
            }
            
            if (tmp3(2,2) == 0.0 and tmp3(2,1) == 0.0 and tmp3(2,1) != 0.0){
                alpha1 = 0.0;
                if (tmp3(1,2) != 0.0){
                    alpha2 = 1.0;
                    alpha3 = -tmp3(1,1)/tmp3(1,2);
                }
                else if (tmp3(1,2) == 0.0 and tmp3(0,2) != 0.0){
                    alpha2 = 0.0;
                    alpha3 = 1.0;
                }
            }
            
            alpha = pow((pow(alpha1,2)+pow(alpha2,2)+pow(alpha3,2)),0.5);
            alpha1 = alpha1/alpha ;
            alpha2 = alpha2/alpha ;
            alpha3 = alpha3/alpha;
            v(ivec,0) = alpha1 ;
            v(ivec,1) = alpha2 ;
            v(ivec,2) = alpha3;
            
        }
    }
    
    Tensor2d tmpv1(ndim,ndim);
    Tensor2d tmpv2(ndim,ndim);
    Tensor2d tmpv3(ndim,ndim);
    
    tmpv1 = tmpv2 = tmpv3 = 0.0;
    
    for(int i = 0 ; i < ndim ; i++)
        for(int j = 0 ; j < ndim ; j++)
            tmpv1(i,j) = v(0,i)*v(0,j);
    
    for(int i = 0 ; i < ndim ; i++)
        for(int j = 0 ; j < ndim ; j++)
            tmpv2(i,j) = v(1,i)*v(1,j);
    
    for(int i = 0 ; i < ndim ; i++)
        for(int j = 0 ; j < ndim ; j++)
            tmpv3(i,j) = v(2,i)*v(2,j);
    
    for(int i = 0 ; i < ndim ; i++)
        for(int j = 0 ; j < ndim ; j++)
            strain(i,j) = 0.5*log(beta(0))*tmpv1(i,j)+0.5*log(beta(1))*tmpv2(i,j)+0.5*log(beta(2))*tmpv3(i,j);
    
}


