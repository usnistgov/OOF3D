//
//  Material.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/9/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Material.hpp"
Material::Material(string materialtype,int const nslip,int const ndim,double const a1,double const a2,double const a3){
    
    name = materialtype;
    n_slip = nslip;
    n_dim = ndim;
    phi = a1;
    theta = a2;
    omega = a3;
    
}

void Material::begin_element(Element *el){
    
    
    double c11 = 2.0;
    double c12 = 1.3;
    double c44 = 1.0;
    
    CauchyStress *f = new CauchyStress("Stress",c11,c12,c44);
    
    Orientation(phi, theta, omega);
    
////////////////////////////////// store and retrive data //////////////////////////
    ElementData *ed = el->getDataByName("plastic_data");
    
    if (ed == 0){
        
        //el->gptdata.clear();
        
        
        pd = new PlasticData("plastic_data",el);
        el->setDataByName(pd,"plastic_data");
        
    }
    else {
        
        pd = dynamic_cast<PlasticData *>(ed);
        for(int i = 0 ; i < 3 ; i++)
            for(int j = 0 ; j < 3 ; j++)
                cout<<pd->gptdata[7].Fpt[i][j]<<"   ";
        
        //        cout<<pd->fp[7].ft[8]<<"  ";
        
    }
    
    //    std::vector<vector<double>> XYZ(8,vector<double>(3,0.0));
    //    std::vector<vector<double>> xyz(8,vector<double>(3,0.0));
    
    

    std::vector<vector<double>> SHP;
    for (vector<GaussPoint*>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++){
        SHP = el->dshapefnRef((*gpti)->xi,(*gpti)->zeta, (*gpti)->mu);
//        for (int i = 0 ; i < 8 ; i++)
//            cout<<SHP[i][0]<<endl;

    }
}


void Material::Orientation(double phi, double theta, double omega){
    
    phi = phi*const_pi/180.0;
    theta = theta*const_pi/180.0;
    omega = omega*const_pi/180.0;
    
    double sp = sin(phi);
    double cp = cos(phi);
    double st = sin(theta);
    double ct = cos(theta);
    double so = sin(omega);
    double co = cos(omega);
    
    qrot = new double*[3];
    for(int i = 0 ; i < 3 ; i++)
        qrot[i] = new double[3];
    
    qrot[0][0] = co*cp-so*sp*ct;
    qrot[1][0] = co*sp+so*ct*cp;
    qrot[2][0] = so*st;
    qrot[0][1] = -so*cp-sp*co*ct;
    qrot[1][1] = -so*sp+ct*co*cp;
    qrot[2][1] = co*st;
    qrot[0][2] = sp*st;
    qrot[1][2] = -st*cp;
    qrot[2][2] = ct;
    
}

