//
//  Material.cpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
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
    
    
    CauchyStress f("Stress",c11,c12,c44);

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
    for (vector<GaussPoint>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++){
        SHP = el->dshapefnRef(gpti->xi,gpti->zeta, gpti->mu);
        
    }

    
//\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
    
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


void Material::calc_schmid(string crystal_type,int n_slip){
    
    schmid = new double**[n_dim];
    for (int i = 0 ; i < n_dim ; i++){
        schmid[i] = new double*[n_dim];
        for (int j = 0 ; j < n_dim; j++)
            schmid[i][j] = new double[n_slip];
    }
    
    if (crystal_type == "fcc" or crystal_type == "ni3al"){
        
        for(int k = 0 ; k < n_slip ; k++){
            for(int i = 0 ; i < n_dim ; i++){
                for(int j = 0 ; j < n_dim ; j++){
                    schmid[i][j][k] = 0.0;
                }
            }
        }
        
        
        //---------------fcc slip system 1----------
        int ind_slip = 0;
        double cns[n_dim][n_slip];
        double cms[n_dim][n_slip];
        double vec1[1][n_dim];
        double vec2[n_dim][1];
        double r1=1.0;
        double r2=1.0/pow(2.0,0.5);
        double r3=1.0/pow(3.0,0.5);
        double r6=1.0/pow(6.0,0.5);
        
        cns[0][ind_slip] = r3;
        cns[1][ind_slip] = r3;
        cns[2][ind_slip] = r3;
        
        cms[0][ind_slip] = 0.0;
        cms[1][ind_slip] = r2;
        cms[2][ind_slip] = -r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        double tmp_v1[1][n_dim];
        double tmp_v2[n_dim][1];
        double tmp1[n_dim][n_dim];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 2----------
        
        ind_slip = 1;
        cns[0][ind_slip] = r3;
        cns[1][ind_slip] = r3;
        cns[2][ind_slip] = r3;
        
        cms[0][ind_slip] = -r2;
        cms[1][ind_slip] = 0.0;
        cms[2][ind_slip] = r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 3----------
        ind_slip = 2;
        cns[0][ind_slip] = r3;
        cns[1][ind_slip] = r3;
        cns[2][ind_slip] = r3;
        
        cms[0][ind_slip] = r2;
        cms[1][ind_slip] = -r2;
        cms[2][ind_slip] = 0.0;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 4----------
        ind_slip = 3;
        cns[0][ind_slip] = r3;
        cns[1][ind_slip] = -r3;
        cns[2][ind_slip] = -r3;
        
        cms[0][ind_slip] = 0.0;
        cms[1][ind_slip] = -r2;
        cms[2][ind_slip] = r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 5----------
        ind_slip = 4;
        cns[0][ind_slip] = r3;
        cns[1][ind_slip] = -r3;
        cns[2][ind_slip] = -r3;
        
        cms[0][ind_slip] = -r2;
        cms[1][ind_slip] = 0.0;
        cms[2][ind_slip] = -r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 6----------
        ind_slip = 5;
        cns[0][ind_slip] = r3;
        cns[1][ind_slip] = -r3;
        cns[2][ind_slip] = -r3;
        
        cms[0][ind_slip] = r2;
        cms[1][ind_slip] = r2;
        cms[2][ind_slip] = 0.0;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 7----------
        ind_slip = 6;
        cns[0][ind_slip] = -r3;
        cns[1][ind_slip] = r3;
        cns[2][ind_slip] = -r3;
        
        cms[0][ind_slip] = 0.0;
        cms[1][ind_slip] = r2;
        cms[2][ind_slip] = r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 8----------
        ind_slip = 7;
        cns[0][ind_slip] = -r3;
        cns[1][ind_slip] = r3;
        cns[2][ind_slip] = -r3;
        
        cms[0][ind_slip] = r2;
        cms[1][ind_slip] = 0.0;
        cms[2][ind_slip] = -r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 9----------
        ind_slip = 8;
        cns[0][ind_slip] = -r3;
        cns[1][ind_slip] = r3;
        cns[2][ind_slip] = -r3;
        
        cms[0][ind_slip] = -r2;
        cms[1][ind_slip] = -r2;
        cms[2][ind_slip] = 0.0;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 10----------
        ind_slip = 9;
        cns[0][ind_slip] = -r3;
        cns[1][ind_slip] = -r3;
        cns[2][ind_slip] = r3;
        
        cms[0][ind_slip] = 0.0;
        cms[1][ind_slip] = -r2;
        cms[2][ind_slip] = -r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 11----------
        ind_slip = 10;
        cns[0][ind_slip] = -r3;
        cns[1][ind_slip] = -r3;
        cns[2][ind_slip] = r3;
        
        cms[0][ind_slip] = r2;
        cms[1][ind_slip] = 0.0;
        cms[2][ind_slip] = r2;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        //---------------fcc slip system 12----------
        ind_slip = 11;
        cns[0][ind_slip] = -r3;
        cns[1][ind_slip] = -r3;
        cns[2][ind_slip] = r3;
        
        cms[0][ind_slip] = -r2;
        cms[1][ind_slip] = r2;
        cms[2][ind_slip] = 0.0;
        
        for (int ij = 0 ; ij < n_dim ; ij++)
            vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < n_dim ; ik++)
            vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<n_dim ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < n_dim ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<n_dim ; i++){
            for (int j = 0 ; j < n_dim ; j++)
                schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        
        
    }
    
}






