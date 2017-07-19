//
//  Material.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Material.hpp"
/*
Material::Material(){
    
}
 
 */

Material::Material(string const materialtype,int nslip,double const a1,double const a2,double const a3){
    
    name = materialtype;
    n_slip = nslip;
    phi = a1;
    theta = a2;
    omega = a3;
    
    
    
    
}


double Material::Orientation(double phi, double theta, double omega){
    
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

    
    return 0;
}

double Material::precompute(){
    
//    Orientation(phi, theta, omega);

//    fl.rotate(qrot);
    
    return 0;
}


double Material::make_linear_system(){
    
    return 0;
}


double Material::begin_element(Element *el){
    

    double c11 = 2.0;
    double c12 = 1.3;
    double c44 = 1.0;
    
    
    CauchyStress f("Stress",c11,c12,c44);

    Orientation(phi, theta, omega);
    
    f.rotate(qrot);

    
    calc_schmid(name,n_slip);
    
    
////////////////////////////////// store and retrive data //////////////////////////
    ElementData *ed = el->getDataByName("plastic_data");
    if (el == 0){
        pd = new PlasticData("plastic_data",el);
        el->setDataByName(pd,"plastic_data");
    }
    else {
        pd = dynamic_cast<PlasticData *>(ed);
    }
    
//\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
    
    F_tau = new double*[ndim];
    F_t = new double*[ndim];
    
    for(int i = 0 ; i < ndim ; i++){
        F_t[i] = new double[ndim];
    }
    
    
    for(int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j < 3 ; j++){
            F_t[i][j] = 1.0;
        }
    }
    
    
    
    return 0;

    
}

double Material::end_element(){
  
    
    
    
//    map<string ,double(***)> garray;
    
//    garray.insert(pair<string ,double(***)>("F_t",F_t));
    
/*    for (map<string ,double(**)>::iterator it = array.begin(); it != array.end() ; it++){
        cout<<it -> first<<endl;
        for (int i = 0 ; i < ndim ; i++){
            for (int j = 0 ; j < 3; j++){
                cout<<array["F_t"][i][j]<<"   ";
            }
        }
        cout<< endl;
    }
*/
    
    
    return 0;
}

double Material::calc_schmid(string crystal_type,int n_slip){
    
    schmid = new double**[ndim];
    for (int i = 0 ; i < ndim ; i++){
        schmid[i] = new double*[ndim];
        for (int j = 0 ; j < 3; j++)
        schmid[i][j] = new double[n_slip];
    }

    if (crystal_type == "fcc" or crystal_type == "ni3al"){
        
        for(int k = 0 ; k < n_slip ; k++){
            for(int i = 0 ; i < 3 ; i++){
                for(int j = 0 ; j < 3 ; j++){
                    schmid[i][j][k] = 0.0;
                }
            }
        }
        
        
        //---------------fcc slip system 1----------
        int ind_slip = 0;
        double cns[3][n_slip];
        double cms[3][n_slip];
        double vec1[1][3];
        double vec2[3][1];
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        double tmp_v1[1][3];
        double tmp_v2[3][1];
        double tmp1[3][3];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
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
        
        for (int ij = 0 ; ij < 3 ; ij++)
        vec2[ij][0] = cns[ij][ind_slip];
        
        
        for (int ik = 0 ; ik < 3 ; ik++)
        vec1[0][ik] = cms[ik][ind_slip];
        
        for (int i = 0 ; i<3 ; i++){
            tmp_v1[0][i] = 0.0 , tmp_v2[i][0] = 0.0;
            for (int j = 0 ; j < 3 ; j++){
                tmp_v1[0][i] += qrot[i][j]*vec1[0][j];
                tmp_v2[i][0] += qrot[i][j]*vec2[j][0];
            }
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
        }
        
        for (int i = 0 ; i<3 ; i++){
            for (int j = 0 ; j < 3 ; j++)
            schmid[i][j][ind_slip] = tmp1[i][j];
        }
        
        
        
    }
    return 0;
    
}





