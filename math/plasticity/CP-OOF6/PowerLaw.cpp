//
//  PowerLaw.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "PowerLaw.hpp"

//******************************* Container for Power law constitutive model *******************************
GptSlipData::GptSlipData(ConstitutiveModel* CM,MatInput* mi){
    
    // Power Law has three variables "Gammma, dGammma and slip system resistances needed to be updated
    for (int i = 0 ; i < CM->n_slip ; i++){
        res.push_back(mi->MatProp[mi->ctype].prop(init_res));
        dgam.push_back(0.0);
        dgam_dta.push_back(0.0);
        tau_alpha.push_back(0.0);
    }
}
//***********************************************************************************************************


//############################################################################################################
//################################### Power Law Constitutive model ###########################################
//############################################################################################################

PowerLaw::PowerLaw(MatInput* CPIn){
    
    const_w1 = CPIn->MatProp[CPIn->ctype].prop(w1);
    const_w2 = CPIn->MatProp[CPIn->ctype].prop(w2);
    const_ss = CPIn->MatProp[CPIn->ctype].prop(ss);
    const_a = CPIn->MatProp[CPIn->ctype].prop(a);
    const_h0 = CPIn->MatProp[CPIn->ctype].prop(h0);
    const_m = CPIn->MatProp[CPIn->ctype].prop(m);
    const_g0dot = CPIn->MatProp[CPIn->ctype].prop(g0dot);
    const_dt = CPIn->MatProp[CPIn->ctype].prop(dt);
    const_init_res = CPIn->MatProp[CPIn->ctype].prop(init_res);
    
}

void PowerLaw::update_constitutive_model(GptSlipBase* gsdo){
    
    GptSlipData* gp;
    
    gp = dynamic_cast<GptSlipData *>(gsdo);
    //--------- passing res to the local res_ssdt ------
    res_ssdt.resize(n_slip);
    for (int k = 0 ; k < n_slip ; k++)
        res_ssdt[k] = gp->res[k];
    
    
    // --------- 1) Hardening evolution --------------------------
    Hardening(gp);
    for (int k = 0 ; k < n_slip ; k++)
        res_ssdt[k] += res_ssd[k];
    
    //        gp->res[k] += res_ssd[k];
    // ------------------------------------------------------------
    
    
    // --------- 2) Plasric shear strain and its derivatives -------
    PlasticShSt(gp);
    // -------------------------------------------------------------
    
}

//-------------------------------------- Hardening evolution -----------------------------------------
void PowerLaw::Hardening(GptSlipData *gsdo){
    
    double const_qab;
    double ratio_res;
    
    res_ssd.resize(n_slip);
    
    for (int k = 0 ; k < n_slip ; k++){
        res_ssd[k] = 0.0;
        for (int i = 0 ; i < n_slip ; i++){
            if(i == k)
                const_qab = const_w1;
            else
                const_qab = const_w2;
            
            ratio_res=1.0-(res_ssdt[i] /const_ss);//(gsdo->res[i]/const_ss);
            
            res_ssd[k] += const_qab*const_h0*abs(gsdo->dgam[i])*(pow(ratio_res,const_a));
        }
    }
    
}
//------------------------------------------------------------------------------------------------------------

//---------------------------- Plasric shear strain and its derivatives --------------------------------------
void PowerLaw::PlasticShSt(GptSlipData *gsdo){
    
    double ratio_alpha = 0.0;
    double const_sign = 0.0;
    double m_inv = 0.0;
    double res_inv = 0.0;
    for (int k = 0 ; k < n_slip ; k++){
        //        if (gsdo->res[k] >= 1.0){
        if (res_ssdt[k] >= 1.0){
            
            ratio_alpha = gsdo->tau_alpha[k]/res_ssdt[k];//gsdo->res[k];
            
            if (gsdo->tau_alpha[k] >= 0.0)
                const_sign = 1.0;
            else
                const_sign = -1.0;
            
            m_inv = 1.0/const_m;
            gsdo->dgam[k] = const_dt*const_sign*const_g0dot*(pow(abs(ratio_alpha),m_inv));
            /*
             int sd;
             if (abs(gsdo->dgam[k])>1.0e-5) {
             std::cout<<k<<"  "<<gsdo->dgam[k]<<"   "<<gsdo->res[k]<<std::endl;
             cin>>sd;
             }
             */
            res_inv = 1.0/res_ssdt[k];//gsdo->res[k];
            
            gsdo->dgam_dta[k] = const_dt*res_inv*const_g0dot*m_inv*(pow(abs(ratio_alpha),(m_inv-1.0)));
            
        }
        
        else{
            gsdo->dgam[k] = 0.0;
            gsdo->dgam_dta[k] = 0.0;
        }
    }
    
}

//------------------------------------------------------------------------------------------------------------
//############################################################################################################
//############################################################################################################
//############################################################################################################

void PowerLaw::update_evolving_parameters(GptSlipBase *gsdo){
    
    GptSlipData* gp;
    
    gp = dynamic_cast<GptSlipData *>(gsdo);
    
    gp->res = res_ssdt;
    
    
}
