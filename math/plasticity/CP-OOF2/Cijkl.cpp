//
//  Cijkl.cpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/29/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Cijkl.hpp"

Cijkl::Cijkl() {
    
    for(int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j < 3 ; j++){
            for(int k = 0 ; k < 3 ; k++){
                for(int l = 0 ; l < 3 ; l++)
                    cijkl[i][j][k][l] = 0.0;
            }
        }
    }
}


Cijkl::Cijkl(double c11,double c12, double c44){
    
    double cij[6][6];
    for(int i = 0 ; i < 6 ; i++){
        for(int j = 0 ; j < 6 ; j++){
            cij[i][j] = 0.0;
        }
    }
    
    //---------------- cij for cubic materials
    cij[0][0] = cij[1][1] = cij[2][2] = c11;
    cij[0][1] = cij[0][2] = cij[1][0] = cij[1][2] = cij[2][0] = cij[2][1] = c12;
    cij[3][3] = cij[4][4] = cij[5][5] = c44;
    
    
    //----------------- Get cijkl
    for(int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j < 3 ; j++){
            for(int k = 0 ; k < 3 ; k++){
                for(int l = 0 ; l < 3 ; l++)
                    cijkl[i][j][k][l] = 0.0;
                
            }
        }
    }
    
    for (int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j < 3 ; j++){
            cijkl[i][i][j][j] = cij[i][j];
        }
    }
    
    
    for (int i = 0 ; i < 3 ; i++){
        cijkl[i][i][0][1] = cij[i][3];
        cijkl[i][i][1][0] = cij[i][3];
        cijkl[i][i][1][2] = cij[i][4];
        cijkl[i][i][2][1] = cij[i][4];
        cijkl[i][i][0][2] = cij[i][5];
        cijkl[i][i][2][0] = cij[i][5];
        
        cijkl[0][1][i][i] = cijkl[1][0][i][i] = cij[3][i];
        cijkl[1][2][i][i] = cijkl[2][1][i][i] = cij[4][i];
        cijkl[0][2][i][i] = cijkl[2][0][i][i] = cij[5][i];
    }
    
    cijkl[0][1][0][1] = cijkl[0][1][1][0] = cijkl[1][0][0][1] = cijkl[1][0][1][0] = cij[3][3];
    cijkl[0][1][1][2] = cijkl[0][1][2][1] = cijkl[1][0][1][2] = cijkl[1][0][2][1] = cij[3][4];
    cijkl[0][1][0][2] = cijkl[0][1][2][0] = cijkl[1][0][0][2] = cijkl[1][0][2][0] = cij[3][5];
    cijkl[1][2][0][1] = cijkl[1][2][1][0] = cijkl[2][1][0][1] = cijkl[2][1][1][0] = cij[4][3];
    cijkl[1][2][1][2] = cijkl[1][2][2][1] = cijkl[2][1][1][2] = cijkl[2][1][2][1] = cij[4][4];
    cijkl[1][2][0][2] = cijkl[1][2][2][0] = cijkl[2][1][0][2] = cijkl[2][1][2][0] = cij[4][5];
    cijkl[0][2][0][1] = cijkl[0][2][1][0] = cijkl[2][0][0][1] = cijkl[2][0][1][0] = cij[5][3];
    cijkl[0][2][1][2] = cijkl[0][2][2][1] = cijkl[2][0][1][2] = cijkl[2][0][2][1] = cij[5][4];
    cijkl[0][2][0][2] = cijkl[0][2][2][0] = cijkl[2][0][0][2] = cijkl[2][0][2][0] = cij[5][5];
    
}
Cijkl Cijkl::rotate(double **qrot){
    
    int ndim =3;
    
    Cijkl res = Cijkl();
    
    
    for (int i = 0 ; i < 3 ; i++){
        for (int j = 0 ; j < 3 ; j++){
            for (int k = 0 ; k < 3 ; k++){
                for (int l = 0 ; l < 3 ; l++){
                    res.cijkl[i][j][k][l] = 0.0;
                    for (int m = 0 ; m < 3 ; m++){
                        for (int n = 0 ; n < 3 ; n++){
                            for (int p = 0 ; p < 3 ; p++){
                                for (int q = 0 ; q < 3 ; q++){
                                    
                                    res.cijkl[i][j][k][l] += qrot[i][m]*qrot[j][n]*qrot[k][p]*qrot[l][q]*cijkl[m][n][p][q];
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return res;
}
