//
//  CrystalPlasticity.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "CrystalPlasticity.hpp"

#include "PowerLaw.hpp"
#include "CrystalFCC.hpp"
#include "Orientation.hpp"
#include "Material.hpp"


//%%%%%%%%%%%%%%%%%%%%%% Material Factory for crystal structure and constitutive model %%%%%%%%%%%%%%%%%%%%%%%%

CrystalPlasticity* PlasticityType(MatInput *CPIn){
    
    
    CrystalPlasticity *cp;
    ConstitutiveModel* cm;
    
    //------------ Assigning the constitutive model --------------------
    switch (CPIn->ctype){
        case ConstDefault:
            break;
            
        case ConstPowerLaw:
            cm = new PowerLaw(CPIn);
            break;
    }
    //------------ Assigning the crystal structure to the material --------------------
    
    switch (CPIn->mtype){
        case mDefault:
            break;
            
        case mFCC:
            cp = new CrystalFCC(cm,CPIn);

            
            cp->cpi = CPIn;
            
//            cp->calculate_schmid_tensor();
            
            break;
    }
    
    return cp;
    
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Material Factory for crystal orientation %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

OrientationProp *OrientationType(MatInput *CPIn){
    OrientationProp *o = new OrientationProp(CPIn->Orientation(phi),CPIn->Orientation(theta),CPIn->Orientation(omega));

    return o;
}
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

//++++++ cross_refernce is overwritten method from Proeprty class to cross reference orientation and crystal++++++++++
void CrystalPlasticity::cross_reference(Material *mtl) {
    OrientationProp *op = dynamic_cast<OrientationProp*>(mtl->get_by_tag("Orientation"));
    Orientation(op);
    calculate_schmid_tensor();
    cauchy->rotate(qrot);
    
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
void CrystalPlasticity::Orientation(OrientationProp *o){
    
    double phi = (o->phi)*const_pi/180.0;
    double theta = (o->theta)*const_pi/180.0;
    double omega = (o->omega)*const_pi/180.0;
    
    double sp = sin(phi);
    double cp = cos(phi);
    double st = sin(theta);
    double ct = cos(theta);
    double so = sin(omega);
    double co = cos(omega);
    
    qrot.resize(3,3);
    qrot = 0.0;
    qrot(0,0) = co*cp-so*sp*ct;
    qrot(1,0) = co*sp+so*ct*cp;
    qrot(2,0) = so*st;
    qrot(0,1) = -so*cp-sp*co*ct;
    qrot(1,1) = -so*sp+ct*co*cp;
    qrot(2,1) = co*st;
    qrot(0,2) = sp*st;
    qrot(1,2) = -st*cp;
    qrot(2,2) = ct;
    
    
    
}

//################################## Crystal Plasticity Main Computation #######################################
//void CrystalPlasticity::CrystalPlasticity_Flux(Element *el, Mesh *mesh){

void CrystalPlasticity::begin_element(Element *el, Mesh* mesh){
    ////////////////////////////////// store and retrive data //////////////////////////
    ElementData *ed = el->getDataByName("plastic_data");
    ElementData *eds = el->getDataByName("slip_data");
    

    nslip = ConstModel->n_slip;
    
    
    if (ed == 0){
        
        pd = new PlasticData("plastic_data",el);  // Plastic Data container "same for all constitutive models"
        el->setDataByName(pd,"plastic_data");
        
    }
    else {
        
        pd = dynamic_cast<PlasticData *>(ed);
        
        int gsize = pd->gptdata.size();
        for (int ig = 0 ; ig < gsize ; ig++){
            pd->gptdata[ig].Ft = pd->gptdata[ig].F_tau;
            pd->gptdata[ig].Fpt = pd->gptdata[ig].Fp_tau;
        }
        
        
    }
    
    if (eds == 0){
        
        ConstitutiveModel* CM0 = ConstModel;
        sd = new SlipData("slip_data",el,CM0,cpi); // Slip Data Container "changes with constitutive model"
        el->setDataByName(sd,"slip_data");
        
    }
    else {
        
        sd = dynamic_cast<SlipData *>(eds);
        
    }
    
    Tensor2d XYZ(8,n_dim);
    Tensor2d xyz(8,n_dim);
    
    //$$$$$$$$$$$$$$$$ Set the reference and current positions of the nodes within an element $$$$$$$$$$$$$$$$$$$$$
    for (std::vector<Node*>::iterator ni = el->nodes.begin() ; ni!=el->nodes.end(); ni++){
        XYZ(std::distance(el->nodes.begin(), ni),0) = (*ni)->coorx;
        XYZ(std::distance(el->nodes.begin(), ni),1) = (*ni)->coory;
        XYZ(std::distance(el->nodes.begin(), ni),2) = (*ni)->coorz;
        
        xyz(std::distance(el->nodes.begin(), ni),0) = (*ni)->coorx + (*ni)->fields[0]->value[0] ;
        xyz(std::distance(el->nodes.begin(), ni),1) = (*ni)->coory + (*ni)->fields[0]->value[1] ;
        xyz(std::distance(el->nodes.begin(), ni),2) = (*ni)->coorz + (*ni)->fields[0]->value[2] ;
        
    }
    //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
    //################################# Calculation of A, B, C matrices and trial stress ############################
    A_mat.resize(n_dim,n_dim);
    A_mat = 0.0;
    B_alpha.resize(n_dim,n_dim,nslip) , C_alpha.resize(n_dim,n_dim,nslip);
    
    S_trial.resize(n_dim,n_dim);
    
    shpg.resize(n_dim,8);

    for (std::vector<GaussPoint*>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++){
        for (int i = 0 ; i < 3 ; i++){
            for (int j = 0 ; j < 8 ; j++){
                shpg(i,j) = el->dshapefnRef((*gpti)->xi,(*gpti)->zeta, (*gpti)->mu,j,i);
            }
        }
        
        upd = &pd->gptdata[std::distance(el->gptable.begin(), gpti)];
        usd = &sd->gptslipdata[std::distance(el->gptable.begin(), gpti)];

        calc_F(xyz,shpg,8);
        

        //------------------- Calculate matrix [A]
        calc_A();
        //------------------  Calculate matrix [B_alpha]
        calc_B();
        //---------------- Calculate the matrix C_alpha for each slip system
        calc_C();
        //----------------- Calculate the trial elastic stress S_trial
        stress_trial();

//############################################################################################################
        
//&&&&&&&&&&&&&&&& Solving nonlinear equation to find 2PK stress then Fp_tau and Cauchy stress &&&&&&&&&&&&&&&
        
        iterSecPio();
        
//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        
//%%%%%%%%%%%%%%%%%%%%%%%%% Calculation of elasto plastic modulus or elastic Jacobian %%%%%%%%%%%%%%%%%%%%%%%%
        
        W_mat();
        
        
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    }

    
    
    
    
    
}

void CrystalPlasticity::calc_F(Tensor2d coorElement, Tensor2d shpg,int nnode){
    
    
    double dxt_dx0 = 0.0;
    double dxt_dy0 = 0.0;
    double dxt_dz0 = 0.0;
    double dyt_dx0 = 0.0;
    double dyt_dy0 = 0.0;
    double dyt_dz0 = 0.0;
    double dzt_dx0 = 0.0;
    double dzt_dy0 = 0.0;
    double dzt_dz0 = 0.0;
    
    
    
    for(int i = 0 ; i < nnode ; i++){
        
        dxt_dx0 += shpg(0,i)*coorElement(i,0);
        dxt_dy0 += shpg(1,i)*coorElement(i,0);
        dxt_dz0 += shpg(2,i)*coorElement(i,0);
        
        dyt_dx0 += shpg(0,i)*coorElement(i,1);
        dyt_dy0 += shpg(1,i)*coorElement(i,1);
        dyt_dz0 += shpg(2,i)*coorElement(i,1);
        
        dzt_dx0 += shpg(0,i)*coorElement(i,2);
        dzt_dy0 += shpg(1,i)*coorElement(i,2);
        dzt_dz0 += shpg(2,i)*coorElement(i,2);
    }
    
    
    
    
    
    upd->F_tau(0,0) = dxt_dx0;
    upd->F_tau(0,1) = dxt_dy0;
    upd->F_tau(0,2) = dxt_dz0;
    upd->F_tau(1,0) = dyt_dx0;
    upd->F_tau(1,1) = dyt_dy0;
    upd->F_tau(1,2) = dyt_dz0;
    upd->F_tau(2,0) = dzt_dx0;
    upd->F_tau(2,1) = dzt_dy0;
    upd->F_tau(2,2) = dzt_dz0;
    
    
}


//################################## Crystal Plasticity Main Computation #######################################


//////////////////////// Calculation of matrix A,B and C ///////////////////////////////

//########################## Calculate matrix [A] ##############################
void CrystalPlasticity::calc_A(){
    
    
    Tensor2d FpI_t(n_dim,n_dim);
    Tensor2d FpIT_t(n_dim,n_dim);
    Tensor2d FT_tau(n_dim,n_dim);
    Tensor2d TMP1(n_dim,n_dim);
    Tensor2d TMP2(n_dim,n_dim);
    
    FpI_t = -upd->Fpt;
    FpIT_t = ~FpI_t;
    FT_tau = ~upd->F_tau;
    TMP1 = upd->F_tau * FpI_t;
    TMP2 = FT_tau * TMP1;
    A_mat = FpIT_t * TMP2;
    
    
}
//########################## End of A_mat ##################################


//################ Calculate matrix [B_alpha] ##############################
void CrystalPlasticity::calc_B(){
    
    
    Tensor2d TMP11(n_dim,n_dim);
    Tensor2d TMP12(n_dim,n_dim);
    Tensor2d TMP20(n_dim,n_dim);
    Tensor2d TMP21(n_dim,n_dim);
    
    
    for(int i = 0 ; i < nslip ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                TMP11(j,k) = schmid(j,k,i);
                TMP12(j,k) = schmid(k,j,i);
                
            }
        }
        
        
        TMP20 = A_mat * TMP11;
        TMP21 = TMP12 * A_mat;
        
        for(int j1 = 0 ; j1 < n_dim ; j1++){
            for(int k1 = 0 ; k1 < n_dim ; k1++){
                B_alpha(j1,k1,i) = TMP20(j1,k1)+TMP21(j1,k1);
            }
        }
    }
    
    
    
}
//###################### End of B_alpha #####################################



//################ Calculate the matrix C_ALPHA for each slip system ###########
void CrystalPlasticity::calc_C(){
    
    
    
    for (int k = 0 ; k < nslip ; k++){
        for(int i = 0 ; i < n_dim ; i++){
            for(int j = 0 ; j < n_dim ; j++){
                //                C_alpha[i][j][k] = 0.0;
                C_alpha(i,j,k) = 0.0;
                for(int m = 0 ; m < n_dim ; m++){
                    for(int n = 0 ; n < n_dim ; n++){
                        C_alpha(i,j,k) += cauchy->C_mat(i,j,m,n)*0.5*B_alpha(m,n,k);
                    }
                }
            }
        }
    }
    
    
}
//####################### End of C_alpha ####################################
//////////////////////// end of Calculation of matrix A,B and C ///////////////////////////////
//############# Calculate the trial elastic stress S_trial ##################
void CrystalPlasticity::stress_trial(){
    
    Tensor2d delta_kron(n_dim,n_dim);
    
    delta_kron = 0.0;
    
    delta_kron(0,0) = delta_kron(1,1) = delta_kron(2,2) = 1.0;
    
    
    
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            S_trial(i,j) = 0.0;
            for(int m = 0 ; m < n_dim ; m++){
                for(int n = 0 ; n < n_dim ; n++){
                    S_trial(i,j) += cauchy->C_mat(i,j,m,n)*0.5*(A_mat(m,n)-delta_kron(m,n));
                    
                }
            }
        }
    }
    
    
    
}
//########################## End of S_trial ####################################


//###################################################################################
//###################################################################################
//################                    #########                         #############
//################                    #########                         #############
//################                    #########                         #############
//################          ###################        ##########       #############
//################          ###################        ##########       #############
//################          ###################        ##########       #############
//################          ###################                         #############
//################                    #########                         #############
//################                    #########        ##############################
//################                    #########        ##############################
//#############################################        ##############################
//###################################################################################

void CrystalPlasticity::iterSecPio(){
    
    std::cout.precision(17);
    
    
    
    for(int i = 0 ; i < nslip ; i++)
        usd->tau_alpha[i] = usd->dgam[i] = usd->dgam_dta[i] = 0.0;
    
    // ----------- 1) first time to update plastic shear strain with the constitutive model -----------
    resolvedshear(S_trial);
    
    
    ConstModel->update_constitutive_model(usd);
    
    
    // ------------------------------------------------------------------------------------------------
    
    
    // -------------------- Calculation of first value of 2nd PKS-----------------
    SPKStress();
    
    // ----------------------------------------------------------------------------
    
    delta_kron4d.resize(3,3,3,3);
    
    
    delta_kron4d == 1.0;
    
    int niter = 20;
    int iitr = 0;
    double ratio_norm = 1.0e10;
    
    //$$$$$$$$$$$$$$$$$$$$$$$$ Iteration to calculate 2PK stress or update Fp_tau $$$$$$$$$$$$$$$$$$$$$$$
    while (iitr <= niter and abs(ratio_norm) >= 0.001){
        
        //###################### update slip system properties (gamma , hardening) ###########
        for(int i = 0 ; i < nslip ; i++)
            usd->tau_alpha[i] = 0.0;
        
        // ----------- 2) second time to update plastic shear strain with the constitutive model -----------
        resolvedshear(upd->S_star);
        ConstModel->update_constitutive_model(usd);
        
        //#####################################################################################
        // --------------------------- Newton-Raphson method to solve 2PK stress ----------------------------
        GT_mat.resize(n_dim,n_dim,nslip);
        GTMat();    //------ calculate GT_mat
        
        RJ_mat.resize(n_dim,n_dim,n_dim,n_dim);
        
        RJ_mat = 0.0;
        RJMat();
        
        
        
        RJ_mat += delta_kron4d;
        
        RJ_reduced.resize(6,6);
        RJ_reduced = 0.0;
        
        RJ_reduced = reduce_mat(RJ_mat); //--- deflate 4th order 3d tensor to 6by6 2d matrix ----
        
        
        RJ_reduced = --RJ_reduced;      //--- Inverse sixth order tensor ------
        
        
        Tensor2d TMP1s(n_dim,n_dim);
        
        for(int i = 0 ; i < n_dim ; i++){
            for(int j = 0 ; j < n_dim ; j++){
                TMP1s(i,j) = 0.0;
                for(int k = 0 ; k < nslip ; k++){
                    TMP1s(i,j) += usd->dgam[k]*C_alpha(i,j,k); //--- Plastic part of 2PK stress ------
                }
            }
        }
        
        
        
        TMP1s += upd->S_star - S_trial; //------- updated 2PK stress --------------
        
        //====================  compare the updated 2PK with the old one with L2 norm method ===============
        Vector GN_vec(6) , S_vec(6);
        GN_vec = reduce_vec(TMP1s);
        S_vec = reduce_vec(upd->S_star);
        
        Vector TMP_RG(6) , TMP_vec(6);
        for(int i = 0 ; i < 6 ; i++){
            TMP_RG(i) = 0.0;
            for(int j = 0 ; j < 6 ; j++){
                TMP_RG(i) += RJ_reduced(i,j)*GN_vec(j);
            }
        }
        
        TMP_vec = S_vec;
        
        S_vec -= TMP_RG;
        
        upd->S_star = inflate_vec(S_vec);
        
        double dot_product_S_vec = 0.0;
        for(int i = 0 ; i < 6 ; i++)
            dot_product_S_vec += S_vec(i)*S_vec(i);
        
        double rnorm_s_vec = pow(dot_product_S_vec,0.5);
        
        
        double dot_product_TMP_vec = 0.0;
        for(int i = 0 ; i < 6 ; i++)
            dot_product_TMP_vec += TMP_vec(i)*TMP_vec(i);
        
        double rnorm_tmp_vec = pow(dot_product_TMP_vec,0.5);
        
        if (abs(rnorm_tmp_vec) < 1.0)
            ratio_norm = 0.0;
        else
            ratio_norm = (rnorm_s_vec-rnorm_tmp_vec)/rnorm_tmp_vec;
        /*
         if (abs(ratio_norm) > 0.0){
         
         std::cout<<"ratio_norm = "<<rnorm_s_vec<<"  "<<rnorm_tmp_vec<<"   "<<ratio_norm<<std::endl;
         int stuff;
         cin>>stuff;
         }
         */
        //==============================================================================================
        
        
        iitr += 1;
        //-------------------------------------------------------------------------------------
    }
    //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
    // ----------- 3) third time to update plastic shear strain with the constitutive model -----------
    resolvedshear(upd->S_star);
    ConstModel->update_constitutive_model(usd);
    
    ConstModel->update_evolving_parameters(usd);
    
    //    usd->res = ConstModel->res_ssdt;
    
    //&&&&&&&&&&&&&&&&&&&&& Calculation of Velocity Gradient &&&&&&&&&&&&&&&&&&&&&&&&&&
    
    Tensor2d Lp(n_dim,n_dim);
    
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            Lp(i,j) = 0.0;
            for(int k = 0 ; k < nslip ; k++){
                Lp(i,j) += usd->dgam[k]*schmid(i,j,k);
            }
        }
    }
    
    //&&&&&&&&&&&&&&&&&&&&&&&&&&& Calculation of Fp-tau   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    Tensor2d Iden(3,3);
    
    Iden = 0.0;
    Iden(0,0) = Iden(1,1) = Iden(2,2) = 1.0;
    
    Lp += Iden;
    
    upd->Fp_tau = Lp * upd->Fpt;
    
    
    double det_Fp_tau=(upd->Fp_tau(0,0)*upd->Fp_tau(1,1)*upd->Fp_tau(2,2)\
                       -upd->Fp_tau(0,0)*upd->Fp_tau(1,2)*upd->Fp_tau(2,1)-upd->Fp_tau(1,0)\
                       *upd->Fp_tau(0,1)*upd->Fp_tau(2,2) +upd->Fp_tau(1,0)*upd->Fp_tau(0,2)\
                       *upd->Fp_tau(2,1)+upd->Fp_tau(2,0)*upd->Fp_tau(0,1)*upd->Fp_tau(1,2)\
                       -upd->Fp_tau(2,0)*upd->Fp_tau(0,2)*upd->Fp_tau(1,1));
    
    double oby3 = 1.0/3.0;
    for(int i = 0 ; i < 3 ; i++)
        for(int j = 0 ; j < 3 ; j++)
            upd->Fp_tau(i,j) = upd->Fp_tau(i,j)/(pow(det_Fp_tau,oby3));
    
    //&&&&&&&&&&&&&&&&&&&&&&&&& Calculation of the new Cauchy Stress &&&&&&&&&&&&&&&&&&&&&
    
    Tensor2d Fp_tauI(n_dim,n_dim);
    
    Fp_tauI = -upd->Fp_tau;
    
    upd->Fe_tau = upd->F_tau*Fp_tauI;
    
    Tensor2d Fe_tauT(n_dim,n_dim);
    
    Fe_tauT = ~upd->Fe_tau;
    
    Tensor2d TMPSFeT(n_dim,n_dim);
    
    TMPSFeT = upd->S_star * Fe_tauT;
    
    upd->Cauchy = upd->Fe_tau * TMPSFeT;
    
    
    double det_F_tau=(upd->F_tau(0,0)*upd->F_tau(1,1)*upd->F_tau(2,2)-upd->F_tau(0,0)*upd->F_tau(1,2)\
                      *upd->F_tau(2,1)-upd->F_tau(1,0)*upd->F_tau(0,1)*upd->F_tau(2,2)\
                      +upd->F_tau(1,0)*upd->F_tau(0,2)*upd->F_tau(2,1)+upd->F_tau(2,0)\
                      *upd->F_tau(0,1)*upd->F_tau(1,2)-upd->F_tau(2,0)*upd->F_tau(0,2)*upd->F_tau(1,1));
    
    
    for(int i = 0 ; i < 3 ; i++)
        for(int j = 0 ; j < 3 ; j++)
            upd->Cauchy(i,j) = upd->Cauchy(i,j)/det_F_tau;
    
    
    //&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    
}

//################  Resolved Shear Stress ##########
void CrystalPlasticity::resolvedshear(Tensor2d &Stress){
    
    
    for(int k = 0 ; k < nslip ; k++){
        usd->tau_alpha[k] = 0.0;
        for(int i = 0 ; i < n_dim ; i++){
            for(int j = 0 ; j < n_dim ; j++){
                usd->tau_alpha[k] += Stress(i,j)*schmid(i,j,k);
            }
        }
    }
    
    
}
//#################### End of Resolved Shear Stress ##############
//################################################################
void CrystalPlasticity::SPKStress(){
    
    Tensor2d TMP1(n_dim,n_dim);
    
    
    for(int it = 0 ; it < n_dim ; it++){
        for(int jt = 0 ; jt < n_dim ; jt++){
            TMP1(it,jt) = 0.0;
            for(int kt = 0 ; kt < nslip ; kt++){
                TMP1(it,jt) += usd->dgam[kt]*C_alpha(it,jt,kt);
                
            }
        }
    }
    
    for(int it = 0 ; it < n_dim ; it++){
        for(int jt = 0 ; jt < n_dim ; jt++){
            upd->S_star(it,jt) = S_trial(it,jt)-TMP1(it,jt);
        }
    }
    
}
//################################################################

//################################################################
void CrystalPlasticity::GTMat(){
    
    
    for(int k = 0 ; k < nslip ; k++){
        for(int i = 0 ; i < n_dim ; i++){
            for(int j = 0 ; j < n_dim ; j++){
                GT_mat(i,j,k) = 0.5*(schmid(i,j,k) + schmid(j,i,k))*usd->dgam_dta[k];
            }
        }
    }
    
}
//################################################################

//################################################################
void CrystalPlasticity::RJMat(){
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int m = 0 ; m < n_dim ; m++){
                for(int n = 0 ; n < n_dim ; n++){
                    RJ_mat(i,j,m,n) = 0.0;
                    for(int k = 0 ; k < nslip ; k++){
                        RJ_mat(i,j,m,n) += C_alpha(i,j,k)*GT_mat(m,n,k);
                    }
                }
            }
        }
    }
    
    
}
//################################################################


//################################################################
Tensor2d CrystalPlasticity::reduce_mat(Tensor4d as_mat){
    
    Tensor2d as_redu;
    as_redu.resize(6,6);
    
    for(int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j < 3 ; j++){
            as_redu(i,j) = as_mat(i,i,j,j);
        }
    }
    
    for(int i = 0 ; i < 3 ; i++){
        as_redu(i,3) = as_mat(i,i,0,1)+as_mat(i,i,1,0);
        as_redu(i,4) = as_mat(i,i,1,2)+as_mat(i,i,2,1);
        as_redu(i,5) = as_mat(i,i,0,2)+as_mat(i,i,2,0);
    }
    
    
    for(int j = 0 ; j < 3 ; j++){
        as_redu(3,j) = as_mat(0,1,j,j);
        as_redu(4,j) = as_mat(1,2,j,j);
        as_redu(5,j) = as_mat(0,2,j,j);
    }
    
    as_redu(3,3) = as_mat(0,1,0,1)+as_mat(0,1,1,0);
    as_redu(3,4) = as_mat(0,1,1,2)+as_mat(0,1,2,1);
    as_redu(3,5) = as_mat(0,1,0,2)+as_mat(0,1,2,0);
    
    as_redu(4,3) = as_mat(1,2,0,1)+as_mat(1,2,1,0);
    as_redu(4,4) = as_mat(1,2,1,2)+as_mat(1,2,2,1);
    as_redu(4,5) = as_mat(1,2,0,2)+as_mat(1,2,2,0);
    
    as_redu(5,3) = as_mat(0,2,0,1)+as_mat(0,2,1,0);
    as_redu(5,4) = as_mat(0,2,1,2)+as_mat(0,2,2,1);
    as_redu(5,5) = as_mat(0,2,0,2)+as_mat(0,2,2,0);
    
    return as_redu;
    
}

//#################  Reduce 2nd order 3*3 tensor to 1st 6 vector ########
Vector CrystalPlasticity::reduce_vec(Tensor2d as_star){
    
    Vector as_vec(6);
    for(int i = 0 ; i < 3 ; i++)
        as_vec(i) = as_star(i,i);
    
    as_vec(3) = 0.5*(as_star(0,1)+as_star(1,0));
    as_vec(4) = 0.5*(as_star(1,2)+as_star(2,1));
    as_vec(5) = 0.5*(as_star(0,2)+as_star(2,0));
    
    return as_vec;
    
}
//#################  end of Reduce 2nd order 3*3 tensor to 1st 6 vector ########

//######### Inflate 1st 6 vector to 2nd 3*3 tensor ################
Tensor2d CrystalPlasticity::inflate_vec(Vector as_vec){
    
    Tensor2d as_star(n_dim,n_dim);
    
    for(int i = 0 ; i < 3 ; i++)
        as_star(i,i) = as_vec(i);
    
    as_star(0,1) = as_vec(3);
    as_star(1,2) = as_vec(4);
    as_star(0,2) = as_vec(5);
    
    as_star(1,0) = as_vec(3);
    as_star(2,1) = as_vec(4);
    as_star(2,0) = as_vec(5);
    
    return as_star;
    
}
//######### end of Inflate 1st 6 vector to 2nd 3*3 tensor ################


//################################################################
void CrystalPlasticity::W_mat(){
    
    polardecomp();
    
    //#------ Calculation of L_mat-------
    Tensor4d L_mat(n_dim,0.0);
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    L_mat(i,j,k,l) = 0.0;
                    for(int m = 0 ; m < n_dim ; m++){
                        L_mat(i,j,k,l) += upd->Fe_tau(k,i)*Stretch(l,m)*upd->Fe_tau(m,j)+upd->Fe_tau(m,i)*Stretch(m,k)*upd->Fe_tau(l,j);
                    }
                }
            }
        }
    }
    
    
    //#--------- Calculation of D_mat ---------
    Tensor4d D_mat(n_dim,0.0);
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    D_mat(i,j,k,l) = 0.0;
                    for(int m = 0 ; m < n_dim ; m++){
                        for(int n = 0 ; n < n_dim ; n++){
                            D_mat(i,j,k,l) += 0.5*cauchy->C_mat(i,j,m,n)*L_mat(m,n,k,l);
                        }
                    }
                }
            }
        }
    }
    
    
    //#-------------- Calculation of G_alpha----------------------
    double G_alpha[n_dim][n_dim][n_dim][n_dim][nslip];
    
    for(int alpha = 0 ; alpha < nslip ; alpha++){
        for(int m = 0 ; m < n_dim ; m++){
            for(int n = 0 ; n < n_dim ; n++){
                for(int k = 0 ; k < n_dim ; k++){
                    for(int l = 0 ; l < n_dim ; l++){
                        G_alpha[m][n][k][l][alpha] = 0.0;
                        for(int p = 0 ; p < n_dim ; p++){
                            G_alpha[m][n][k][l][alpha] += L_mat(m,p,k,l)*schmid(p,n,alpha)+schmid(m,p,alpha)*L_mat(p,n,k,l);
                        }
                    }
                }
            }
        }
    }
    //#--------- Calculation of J_alpha ---------
    double J_alpha[n_dim][n_dim][n_dim][n_dim][nslip];
    
    for(int alpha = 0 ; alpha < nslip ; alpha++){
        for(int i = 0 ; i < n_dim ; i++){
            for(int j = 0 ; j < n_dim ; j++){
                for(int k = 0 ; k < n_dim ; k++){
                    for(int l = 0 ; l < n_dim ; l++){
                        J_alpha[i][j][k][l][alpha] = 0.0;
                        for(int m = 0 ; m < n_dim ; m++){
                            for(int n = 0 ; n < n_dim ; n++){
                                J_alpha[i][j][k][l][alpha] += 0.5*cauchy->C_mat(i,j,m,n)*G_alpha[m][n][k][l][alpha];
                            }
                        }
                    }
                }
            }
        }
    }
    
    //#------------- Calculation of Q_mat -------------------
    Tensor4d K_inv(n_dim,0.0);
    K_inv = inflate_ten(RJ_reduced);
    
    
    Tensor4d TMP_4d(n_dim,0.0);
    for(int m = 0 ; m < n_dim ; m++){
        for(int n = 0 ; n < n_dim ; n++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    TMP_4d(m,n,k,l) = 0.0;
                    for(int alpha = 0 ; alpha < nslip ; alpha++){
                        TMP_4d(m,n,k,l) += usd->dgam[alpha]*J_alpha[m][n][k][l][alpha];
                    }
                    
                }
            }
        }
    }
    
    
    Tensor4d Q_mat(n_dim,0.0);
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    Q_mat(i,j,k,l) = 0.0;
                    for(int m = 0 ; m < n_dim ; m++){
                        for(int n = 0 ; n < n_dim ; n++){
                            Q_mat(i,j,k,l) += K_inv(i,j,m,n)*(D_mat(m,n,k,l)-TMP_4d(m,n,k,l));
                        }
                    }
                    
                }
            }
        }
    }
    
    
    //#-------------- Calculation of R_alpha -----------------
    Tensor3d R_alpha;
    R_alpha.resize(n_dim,n_dim,nslip);
    for(int alpha = 0 ; alpha < nslip ; alpha++){
        for(int i = 0 ; i < n_dim ; i++){
            for(int j = 0 ; j < n_dim ; j++){
                R_alpha(i,j,alpha) = 0.0;
                for(int k = 0 ; k < n_dim ; k++){
                    for(int l = 0 ; l < n_dim ; l++){
                        R_alpha(i,j,alpha) += GT_mat(k,l,alpha)*Q_mat(k,l,i,j);
                    }
                }
            }
        }
    }
    
    //#------------- Calculation of S_mat---------------------
    for(int k = 0 ; k < n_dim ; k++){
        for(int l = 0 ; l < n_dim ; l++){
            for(int p = 0 ; p < n_dim ; p++){
                for(int j = 0 ; j < n_dim ; j++){
                    TMP_4d(k,l,p,j) = 0.0;
                    for(int alpha = 0 ; alpha < nslip ; alpha++){
                        TMP_4d(k,l,p,j) += R_alpha(k,l,alpha)*schmid(p,j,alpha);
                    }
                }
            }
        }
    }
    
    Tensor2d TMP_2d(n_dim,n_dim);
    for(int p = 0 ; p < n_dim ; p++){
        for(int j = 0 ; j < n_dim ; j++){
            TMP_2d(p,j) = 0.0;
            for(int alpha = 0 ; alpha < nslip ; alpha++){
                TMP_2d(p,j) += usd->dgam[alpha]*schmid(p,j,alpha);
            }
        }
    }
    
    Tensor4d S_mat(n_dim,0.0);
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    S_mat(i,j,k,l) = Rotation(i,k)*upd->Fe_tau(l,j);
                }
            }
        }
    }
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    for(int p = 0 ; p < n_dim ; p++){
                        S_mat(i,j,k,l) -= Rotation(i,k)*upd->Fe_tau(l,p)*TMP_2d(p,j);
                    }
                }
            }
        }
    }
    
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    for(int m = 0 ; m < n_dim ; m++){
                        for(int n = 0 ; n < n_dim ; n++){
                            for(int p = 0 ; p < n_dim ; p++){
                                S_mat(i,j,k,l) -= Rotation(i,m)*Stretch(m,n)*upd->Fe_tau(n,p)*TMP_4d(k,l,p,j);
                            }
                        }
                    }
                }
            }
        }
    }
    
    
    //#------------------ Calculation of inverse of Fe ----------------
    
    Tensor2d Fe_tau_inv(n_dim,n_dim);
    
    Fe_tau_inv = -upd->Fe_tau;
    
//    w_mat.resize(n_dim,n_dim,n_dim,n_dim);
//    w_mat = 0.0;
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    upd->w_mat(i,j,k,l) = 0.0;
                    for(int m = 0 ; m < n_dim ; m++){
                        for(int n = 0 ; n < n_dim ; n++){
                            upd->w_mat(i,j,k,l) += S_mat(i,m,k,l)*upd->S_star(m,n)*upd->Fe_tau(j,n);
                        }
                    }
                }
            }
        }
    }
    
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    for(int m = 0 ; m < n_dim ; m++){
                        for(int n = 0 ; n < n_dim ; n++){
                            upd->w_mat(i,j,k,l) += upd->Fe_tau(i,m)*Q_mat(m,n,k,l)*upd->Fe_tau(j,n);
                        }
                    }
                }
            }
        }
    }
    
    
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    for(int m = 0 ; m < n_dim ; m++){
                        for(int n = 0 ; n < n_dim ; n++){
                            upd->w_mat(i,j,k,l) += upd->Fe_tau(i,m)*upd->S_star(m,n)*S_mat(j,n,k,l);
                        }
                    }
                }
            }
        }
    }
    
    Tensor2d TMP_sf(n_dim,n_dim);
    
    for(int k = 0 ; k < n_dim ; k++){
        for(int l = 0 ; l < n_dim ; l++){
            TMP_sf(k,l) = 0.0;
            for(int p = 0 ; p < n_dim ; p++){
                for(int q = 0 ; q < n_dim ; q++){
                    TMP_sf(k,l) += S_mat(p,q,k,l)*Fe_tau_inv(q,p);
                }
            }
        }
    }
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    for(int m = 0 ; m < n_dim ; m++){
                        for(int n = 0 ; n < n_dim ; n++){
                            upd->w_mat(i,j,k,l) -= upd->Fe_tau(i,m)*upd->S_star(m,n)*upd->Fe_tau(j,n)*TMP_sf(k,l);
                        }
                    }
                }
            }
        }
    }
    
    double det_Fe_tau=(upd->Fe_tau(0,0)*upd->Fe_tau(1,1)*upd->Fe_tau(2,2)-upd->Fe_tau(0,0)*\
                       upd->Fe_tau(1,2)*upd->Fe_tau(2,1)-upd->Fe_tau(1,0)*upd->Fe_tau(0,1)*upd->Fe_tau(2,2)\
                       +upd->Fe_tau(1,0)*upd->Fe_tau(0,2)*upd->Fe_tau(2,1)+upd->Fe_tau(2,0)*\
                       upd->Fe_tau(0,1)*upd->Fe_tau(1,2)-upd->Fe_tau(2,0)*upd->Fe_tau(0,2)*upd->Fe_tau(1,1));
    
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            for(int k = 0 ; k < n_dim ; k++){
                for(int l = 0 ; l < n_dim ; l++){
                    upd->w_mat(i,j,k,l) = upd->w_mat(i,j,k,l)/det_Fe_tau;
                }
            }
        }
    }
    
    Dep = reduce_wmat(upd->w_mat);
    
    
}
//################################################################
void CrystalPlasticity::polardecomp(){
    
    Tensor2d F_tI(n_dim,n_dim) , F_REL(n_dim,n_dim) , F_REL_T(n_dim,n_dim);
    
    Stretch.resize(n_dim,n_dim) , Rotation.resize(n_dim,n_dim);
    
    Stretch = 0.0;
    Rotation = 0.0;
    
    F_tI = -upd->Ft;
    
    
    F_REL = upd->F_tau*F_tI;
    
    //#----------------------- square root of a positive matrix U=sqrt(C) ------------
    
    Tensor2d C(n_dim,n_dim) , Csquare(n_dim,n_dim) , Iden(n_dim,n_dim) , invU(n_dim,n_dim);
    
    Iden = 0.0;
    Iden(0,0) = Iden(1,1) = Iden(2,2) = 1.0;
    
    F_REL_T = ~F_REL;
    //#----------------------- C = FTF --------------------------------------
    C = F_REL_T*F_REL;
    //#---------------------- C^2 ------------------------------------------
    Csquare = C*C;
    
    double o3=1.0/3.0;
    double root3 = pow(3.0,0.5);
    double c1212 = C(0,1)*C(0,1);
    double c1313 = C(0,2)*C(0,2);
    double c2323 = C(1,2)*C(1,2);
    double c2313 = C(1,2)*C(0,2);
    double c1223 = C(0,1)*C(1,2);
    double c1213 = C(0,1)*C(0,2);
    double s11 = C(1,1)*C(2,2)-c2323;
    double ui1 = o3*(C(0,0)+C(1,1)+C(2,2));
    double ui2 = s11+C(0,0)*C(1,1)+C(2,2)*C(0,0)-c1212-c1313;
    double ui3 = C(0,0)*s11+C(0,1)*(c2313-C(0,1)*C(2,2))+C(0,2)*(c1223-C(1,1)*C(0,2));
    double ui1s = ui1*ui1;
    double q = pow(-fmin((o3*ui2-ui1s),0.0),0.5);
    double r = 0.5*(ui3-ui1*ui2)+ui1*ui1s;
    double xmod = q*q*q;
    
    double sign;
    if (xmod-1.0e30 > 0.0)
        sign = 1.0;
    else
        sign = -1.0;
    
    double scl1 = 0.5 + 0.5*sign;
    
    if (xmod-abs(r) > 0.0)
        sign = 1.0;
    else
        sign = -1.0;
    
    double scl2 = 0.5 + 0.5*sign;
    double scl0 = fmin(scl1,scl2);
    scl1 = 1.0 - scl0;
    
    double xmodscl1;
    if(scl1 == 0)
        xmodscl1 = xmod;
    else
        xmodscl1=xmod+scl1;
    
    
    
    double sdetm = acos(r/(xmodscl1))*o3;
    
    q = scl0*q;
    double ct3=q*cos(sdetm);
    double st3=q*root3*sin(sdetm);
    sdetm = scl1*pow(fmax(0.0,r),0.5);
    double aa = 2.0*(ct3+sdetm)+ui1;
    double bb = -ct3+st3-sdetm+ui1;
    double cc = -ct3-st3-sdetm+ui1;
    double lamda1 = pow(fmax(aa,0.0),0.5);
    double lamda2 = pow(fmax(bb,0.0),0.5);
    double lamda3 = pow(fmax(cc,0.0),0.5);
    
    double Iu = lamda1 + lamda2 + lamda3;
    double IIu = lamda1*lamda2 + lamda1*lamda3 + lamda2*lamda3;
    double IIIu = lamda1*lamda2*lamda3;
    
    
    for (int i = 0 ; i < 3 ; i++){
        for (int j = 0 ; j < 3 ; j++){
            Stretch(i,j) = Iu*IIIu*Iden(i,j)+(pow(Iu,2)-IIu)*C(i,j)-Csquare(i,j);
            Stretch(i,j) = Stretch(i,j)/(Iu*IIu-IIIu);
        }
    }
    
    for (int i = 0 ; i < 3 ; i++){
        for (int j = 0 ; j < 3 ; j++){
            invU(i,j) = (IIu*Iden(i,j)-Iu*Stretch(i,j)+C(i,j))/IIIu;
        }
    }
    
    //#----------------------- R = FU^-1 -----------------------------
    
    Rotation = F_REL * invU;
    
    
    //#---------------------- End of Polar Decomposition ---------------
    
}
//################################################################
Tensor4d CrystalPlasticity::inflate_ten(Tensor2d as_ten){
    
    Tensor4d as_mat(n_dim,0.0);
    
    for(int i = 0 ; i < n_dim ; i++)
        for(int j = 0 ; j < n_dim ; j++)
            as_mat(i,i,j,j) = as_ten(i,j);
    
    
    
    for(int i = 0 ; i < n_dim ; i++){
        as_mat(i,i,0,1) = as_mat(i,i,1,0) = 0.5*as_ten(i,3);
        as_mat(i,i,1,2) = as_mat(i,i,2,1) = 0.5*as_ten(i,4);
        as_mat(i,i,0,2) = as_mat(i,i,2,0) = 0.5*as_ten(i,5);
    }
    
    for(int j = 0 ; j < n_dim ; j++){
        as_mat(0,1,j,j) = as_mat(1,0,j,j) = as_ten(3,j);
        as_mat(1,2,j,j) = as_mat(2,1,j,j) = as_ten(4,j);
        as_mat(0,2,j,j) = as_mat(2,0,j,j) = as_ten(5,j);
    }
    
    as_mat(0,1,0,1) = as_mat(0,1,1,0) = as_mat(1,0,0,1) = as_mat(1,0,1,0) = 0.5*as_ten(3,3);
    as_mat(0,1,1,2) = as_mat(0,1,2,1) = as_mat(1,0,1,2) = as_mat(1,0,2,1) = 0.5*as_ten(3,4);
    as_mat(0,1,0,2) = as_mat(0,1,2,0) = as_mat(1,0,0,2) = as_mat(1,0,2,0) = 0.5*as_ten(3,5);
    
    as_mat(1,2,0,1) = as_mat(1,2,1,0) = as_mat(2,1,0,1) = as_mat(2,1,1,0) = 0.5*as_ten(4,3);
    as_mat(1,2,1,2) = as_mat(1,2,2,1) = as_mat(2,1,1,2) = as_mat(2,1,2,1) = 0.5*as_ten(4,4);
    as_mat(1,2,0,2) = as_mat(1,2,2,0) = as_mat(2,1,0,2) = as_mat(2,1,2,0) = 0.5*as_ten(4,5);
    
    as_mat(0,2,0,1) = as_mat(0,2,1,0) = as_mat(2,0,0,1) = as_mat(2,0,1,0) = 0.5*as_ten(5,3);
    as_mat(0,2,1,2) = as_mat(0,2,2,1) = as_mat(2,0,1,2) = as_mat(2,0,2,1) = 0.5*as_ten(5,4);
    as_mat(0,2,0,2) = as_mat(0,2,2,0) = as_mat(2,0,0,2) = as_mat(2,0,2,0) = 0.5*as_ten(5,5);
    
    return as_mat;
}
//################################################################
Tensor2d CrystalPlasticity::reduce_wmat(Tensor4d as_mat){
    
    Tensor2d as_redu(6,6);
    for(int i = 0 ; i < n_dim ; i++){
        for(int j = 0 ; j < n_dim ; j++){
            as_redu (i,j) = as_mat(i,i,j,j);
        }
    }
    
    for(int i = 0 ; i < 3 ; i++){
        as_redu(i,3) = (as_mat(i,i,0,1)+as_mat(i,i,1,0))/2.0;
        as_redu(i,4) = (as_mat(i,i,1,2)+as_mat(i,i,2,1))/2.0;
        as_redu(i,5) = (as_mat(i,i,0,2)+as_mat(i,i,2,0))/2.0;
    }
 
    
    for(int j = 0 ; j < 3 ; j++){
        as_redu(3,j) = as_mat(0,1,j,j);
        as_redu(4,j) = as_mat(1,2,j,j);
        as_redu(5,j) = as_mat(0,2,j,j);
    }
    
    as_redu(3,3) = (as_mat(0,1,0,1)+as_mat(0,1,1,0))/2.0;
    as_redu(3,4) = (as_mat(0,1,1,2)+as_mat(0,1,2,1))/2.0;
    as_redu(3,5) = (as_mat(0,1,0,2)+as_mat(0,1,2,0))/2.0;
    
    as_redu(4,3) = (as_mat(1,2,0,1)+as_mat(1,2,1,0))/2.0;
    as_redu(4,4) = (as_mat(1,2,1,2)+as_mat(1,2,2,1))/2.0;
    as_redu(4,5) = (as_mat(1,2,0,2)+as_mat(1,2,2,0))/2.0;
    
    as_redu(5,3) = (as_mat(0,2,0,1)+as_mat(0,2,1,0))/2.0;
    as_redu(5,4) = (as_mat(0,2,1,2)+as_mat(0,2,2,1))/2.0;
    as_redu(5,5) = (as_mat(0,2,0,2)+as_mat(0,2,2,0))/2.0;
    
    
    return as_redu;
    
}
//################################################################
//################################################################
//################################################################
//################################################################
//################################################################
//################################################################
//################################################################
//################################################################
//################################################################


void CrystalPlasticity::make_linear_system(Element *el,GaussPoint* gpti, int gp_index){
    
    
    int cols = el->nfieldcomps();
    int rows = dim;
    
    flux_vector.resize(rows);
    flux_fderivs.resize(rows,cols);
    flux_fderivsg.resize(rows,cols);
    
    
    flux_vector = 0.0;
    flux_fderivs = 0.0;
    flux_fderivsg = 0.0;
    
    fmap.resize(cols);
    
    // Populate the flux matrix, whose rows are components of the flux,
    // and columns are field components for this element.
    int col_offset = 0;
    int f_offset , local_cdx;
    Tensor2d gstress(3,3);
    double dsfn;
    int cndx = 0;
    Tensor2d dukl(3,3);
    
    GptPlasticData* gpdo;
    gpdo = &pd->gptdata[gp_index];

    for (std::vector<Node*>::iterator ni = el->nodes.begin() ; ni != el->nodes.end() ; ni++){
        f_offset = 0;
        for (std::vector<Field*>::iterator f = (*ni)->fields.begin() ; f != (*ni)->fields.end() ; f++){
            for (int comp = 0 ; comp < (*f)->size ; comp++){
                local_cdx = col_offset + f_offset + comp;
                fmap(local_cdx) = (*f)->index + comp;
                gstress = 0.0;
                for( int l = 0 ; l < 3 ; l++){
                    for( int i = 0 ; i < 3 ; i++){
                        gstress(i,comp) = gpdo->Cauchy(i,l);
                    }
                    dsfn = el->dshapefn_current(gpti->xi, gpti->zeta, gpti->mu,cndx,l);
                    for (int ii = 0 ; ii < 3 ; ii++){
                        for (int jj = 0 ; jj < 3 ; jj++){
                            dukl(ii,jj) = gpdo->w_mat(comp,l,ii,jj);
                        }
                    }
                    //<<<<<<<<<<<<<<<<<<<<<<<<< Flux derivatives for material part in stiffness matrix >>>>>>>>>>>>>>>>>>>>>>>>>>
                    for (int flux_comp = 0 ; flux_comp < this->dim ; flux_comp++){
                        flux_fderivs(flux_comp,local_cdx) += dukl(t_row[flux_comp],t_col[flux_comp])*dsfn;
                    }
                    //>>>>>>>>>>>>>>>>>>>>>>>> Flux derivatives for geometric part in stiffness matrix >>>>>>>>>>>>>>>>>>>>>>>>>>
                    for (int flux_compg = 0 ; flux_compg < this->dim ; flux_compg++){
                        flux_fderivsg(flux_compg,local_cdx) += gstress(t_rowg[flux_compg],t_colg[flux_compg])*dsfn;
                    }
                }
            }
            f_offset += (*f)->size;
        }
        col_offset += f_offset;
        cndx += 1;
    }

    
//--------------------------------------- flux vector -----------------------------------------
    std::vector<int> t_row = {0,1,2,1,0,0,1,2,2};
    std::vector<int> t_col = {0,1,2,2,2,1,0,0,1};
    
    for (int flux_comp = 0 ; flux_comp < rows ; flux_comp++){
        flux_vector(flux_comp) = gpdo->Cauchy(t_row[flux_comp],t_col[flux_comp]);
    }

//--------------------------------------- flux vector -----------------------------------------


}


//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ user_print ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
void CrystalPlasticity::user_print(GaussPoint *gpti, int gp_index){
    
    cauchy_stress.resize(3,3);
    cauchy_stress = 0.0;
    deformation_gradient.resize(3,3);
    deformation_gradient = 0.0;
    
    GptPlasticData* gpdo;
    gpdo = &pd->gptdata[gp_index];
    
    cauchy_stress = gpdo->Cauchy;
    deformation_gradient = gpdo->F_tau;
    
    

    
}
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

