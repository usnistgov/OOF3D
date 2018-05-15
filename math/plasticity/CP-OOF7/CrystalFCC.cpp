//
//  CrystalFCC.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "CrystalFCC.hpp"
CrystalFCC::CrystalFCC(ConstitutiveModel* cm,MatInput* mi) : CrystalPlasticity(cm) {
    ConstModel->SetSlipSystem(12);
    
    schmid.resize(3,3,ConstModel->n_slip);
    
    cauchy = new CauchyStress("Stress",mi->CijklConst(c11),mi->CijklConst(c12),mi->CijklConst(c44));
    
//    Orientation(mi->Orientation(0), mi->Orientation(1), mi->Orientation(2));
    
//    Cauchy->rotate(qrot);
    
    
};


void CrystalFCC::calculate_schmid_tensor(){
    
    
    int n_dim = 3;
    
    //---------------fcc slip system 1----------
    int ind_slip = 0;
    double cns[3][ConstModel->n_slip];
    double cms[3][ConstModel->n_slip];
    double vec1[1][3];
    double vec2[3][1];
    
    double r2=1.0/pow(2.0,0.5);
    double r3=1.0/pow(3.0,0.5);
    
    
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++){
            schmid(i,j,ind_slip) = tmp1[i][j];
        }
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
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
            tmp_v1[0][i] += qrot(i,j)*vec1[0][j];
            tmp_v2[i][0] += qrot(i,j)*vec2[j][0];
        }
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            tmp1[i][j] = tmp_v1[0][i]*tmp_v2[j][0];
    }
    
    for (int i = 0 ; i<3 ; i++){
        for (int j = 0 ; j < 3 ; j++)
            schmid(i,j,ind_slip) = tmp1[i][j];
    }
    
    
}


