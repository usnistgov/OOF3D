//
//  Tensor.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "Tensor.hpp"

//--------------------- first order tensor operators ------------------------------------

Vector::Vector(unsigned int sizeIn)
{
    resize(sizeIn);
}

void Vector::resize(unsigned int sizeIn)
{
    vec.resize(sizeIn);
}

unsigned int Vector::size() const
{
    return vec.size();
}

double& Vector::operator()(unsigned int i)
{
    return vec[i];
}

double Vector::operator()(unsigned int i) const
{
    return vec[i];
}

Vector& Vector::operator=(double val)
{
    for (unsigned int i = 0; i < size(); ++i)
        vec[i] = val;
    return *this;
}


//#################### adding two 2D matrices ####################
Vector& Vector::operator+=(const Vector &b){
    
    int ndim = size();
    
    for (  int i = 0; i < ndim; ++i){
        vec[i] += b(i);
    }
    return *this;
}
//################################################################
//############### making two matrices to add #####################
Vector operator+(const Vector &a,const Vector &b){
    
    Vector result = a;
    
    result += b;
    
    return result;
}
//################################################################

//#################### adding two 2D matrices ####################
Vector& Vector::operator-=(const Vector &b){
    
    int ndim = size();
    
    for (  int i = 0; i < ndim; ++i){
        vec[i] -= b(i);
    }
    return *this;
}
//################################################################
//############### making two matrices to add #####################
Vector operator-(const Vector &a,const Vector &b){
    
    Vector result = a;
    
    result -= b;
    
    return result;
}
//################################################################

//--------------------- first order tensor operators ------------------------------------


//--------------------- Second order tensor operators ------------------------------------

//#################### Initialize a 2D matrix #####################
Tensor2d::Tensor2d( int FirstD , int SecondD ){
    
    resize(FirstD , SecondD );
    
}
//################################################################

//#################### Resize a 2D matrix ########################
void Tensor2d::resize(  int FirstD , int SecondD ){
    
    nFirstD = FirstD;
    nSecondD = SecondD;
    
    tens2d.resize(nFirstD);
    for (  int i = 0; i < nFirstD; ++i){
        tens2d[i].resize(nSecondD);
    }
    
}
//################################################################

//################## () operator for a 2D matrix #################
double& Tensor2d::operator()(int i,   int j ){
    
    return tens2d[i][j];
}
//################################################################

//########### const () operator for a 2D matrix ##################
double Tensor2d::operator()(int i, int j ) const{
    
    return tens2d[i][j];
}
//################################################################

//################## Assign a value a 2D matrix ##################
Tensor2d& Tensor2d::operator=(double val){
    
    for (  int i = 0; i < nFirstD; ++i){
        for (  int j = 0; j < nSecondD; ++j){
            tens2d[i][j] = val;
        }
    }
    return *this;
}
//################################################################

//################## return size of  a 2D matrix #################
int Tensor2d::size() const{
    
    return tens2d.size();
}
//################################################################

//#################### adding two 2D matrices ####################
Tensor2d& Tensor2d::operator+=(const Tensor2d &b){
    
    int ndim = size();
    
    for (  int i = 0; i < ndim; ++i){
        for (  int j = 0; j < ndim; ++j){
            tens2d[i][j] += b(i,j);
        }
    }
    return *this;
}
//################################################################

//#################### subtracting two 2D matrices ####################
Tensor2d& Tensor2d::operator-=(const Tensor2d &b){
    
    int ndim = size();
    
    for (  int i = 0; i < ndim; ++i){
        for (  int j = 0; j < ndim; ++j){
            tens2d[i][j] -= b(i,j);
        }
    }
    return *this;
}
//################################################################

//################# multiplying of two 2D matrices #################
Tensor2d& Tensor2d::operator*=(const Tensor2d &b){
    
    int ndim = size();
    
    Tensor2d tmp = *this;
    
    for (  int i = 0; i < ndim; ++i){
        for (  int j = 0; j < ndim; ++j){
            tens2d[i][j] = 0.0;
            for (  int k = 0; k < ndim; ++k){
                tens2d[i][j] += tmp(i,k)*b(k,j);
            }
        }
    }
    return *this;
}
//################################################################

//############# making two matrices to multiply ##################
Tensor2d operator*(const Tensor2d &a,const Tensor2d &b){
    
    Tensor2d result = a;
    
    result *= b;
    
    return result;
    
}
//################################################################

//############### making two matrices to add #####################
Tensor2d operator+(const Tensor2d &a,const Tensor2d &b){
    
    Tensor2d result = a;
    
    result += b;
    
    return result;
}
//################################################################

//############### making two matrices to subtract #####################
Tensor2d operator-(const Tensor2d &a,const Tensor2d &b){
    
    Tensor2d result = a;
    
    result -= b;
    
    return result;
}
//################################################################

//#################### transpose of a 2D matrix ##################
Tensor2d Tensor2d::operator~(){
    
    int ndim = size();
    
    Tensor2d transpose(ndim,ndim);
    
    for (  int i = 0; i < nFirstD; ++i){
        for (  int j = 0; j < nSecondD; ++j){
            transpose(i,j) = tens2d[j][i];
        }
    }
    return transpose;
}
//################################################################

//############### inverse a 2D matrix of rank 3 ##################
Tensor2d Tensor2d::operator-(){
    
    Tensor2d inverse(3,3);
    
    double det = tens2d[0][0]*tens2d[1][1]*tens2d[2][2]-tens2d[0][0]*tens2d[1][2]*tens2d[2][1]-tens2d[1][0]*tens2d[0][1]\
    *tens2d[2][2]+tens2d[1][0]*tens2d[0][2]*tens2d[2][1]+tens2d[2][0]*tens2d[0][1]*tens2d[1][2]-tens2d[2][0]\
    *tens2d[0][2]*tens2d[1][1];
    
    inverse(0,0) =  ( tens2d[1][1]*tens2d[2][2]-tens2d[1][2]*tens2d[2][1])/det;
    inverse(0,1) = -( tens2d[0][1]*tens2d[2][2]-tens2d[0][2]*tens2d[2][1])/det;
    inverse(0,2) = -(-tens2d[0][1]*tens2d[1][2]+tens2d[0][2]*tens2d[1][1])/det;
    inverse(1,0) = -( tens2d[1][0]*tens2d[2][2]-tens2d[1][2]*tens2d[2][0])/det;
    inverse(1,1) =  ( tens2d[0][0]*tens2d[2][2]-tens2d[0][2]*tens2d[2][0])/det;
    inverse(1,2) = -( tens2d[0][0]*tens2d[1][2]-tens2d[0][2]*tens2d[1][0])/det;
    inverse(2,0) =  ( tens2d[1][0]*tens2d[2][1]-tens2d[1][1]*tens2d[2][0])/det;
    inverse(2,1) = -( tens2d[0][0]*tens2d[2][1]-tens2d[0][1]*tens2d[2][0])/det;
    inverse(2,2) =  ( tens2d[0][0]*tens2d[1][1]-tens2d[0][1]*tens2d[1][0])/det;
    
    
    return inverse;
}
//################################################################

//############### inverse a 2D matrix of rank 6 ##################
Tensor2d Tensor2d::operator--(){
    
    
    Tensor2d inverse(6,6);
    inverse = 0.0;
    int size = 6;
    int ipivot[size];
    double pivot[size];
    int index[size][2];
    
    for(int i = 0 ; i < size ; i++){
        ipivot[i] = 0;
        pivot[i] = 0.0;
        for(int j = 0 ; j < 2 ; j++)
            index[i][j] = 0;
    }
    
    double amax;
    int irow;
    int icolum;
    double swap;
    double t;
    
    
    
    for(int i = 0 ; i < size ; i++){
        
        amax=0.0;
        
        for(int j = 0 ; j < size ; j++){
            if (ipivot[j] != 1){
                for(int k = 0 ; k < size ; k++){
                    if (ipivot[k] <= 1){
                        if (ipivot[k] != 1){
                            if (abs(amax) <= abs(tens2d[j][k])){
                                irow = j;
                                icolum = k;
                                amax = tens2d[j][k];
                            }
                        }
                    }
                }
            }
        }
        
        ipivot[icolum] += 1;
        if (irow != icolum){
            for(int l = 0 ; l < size ; l++){
                swap = tens2d[irow][l];
                tens2d[irow][l] = tens2d[icolum][l];
                tens2d[icolum][l] = swap;
            }
        }
        
        index[i][0] = irow;
        index[i][1] = icolum;
        pivot[i] = tens2d[icolum][icolum];
        tens2d[icolum][icolum] = 1.0;
        
        for(int m = 0 ; m < size ; m++){
            tens2d[icolum][m] = tens2d[icolum][m]/pivot[i];
        }
        for(int n = 0 ; n < size ; n++){
            if (n != icolum){
                t = tens2d[n][icolum];
                tens2d[n][icolum] = 0.0;
                for(int o = 0 ; o < size ; o++){
                    tens2d[n][o] = tens2d[n][o]-tens2d[icolum][o]*t;
                }
            }
        }
    }
    
    
    int ll;
    int jrow;
    int jcolum;
    for(int i = 0 ; i < size ; i++){
        ll = size - i- 1;
        if (index[ll][0] != index[ll][1]){
            jrow = index[ll][0];
            jcolum = index[ll][1];
            for(int k = 0 ; k < size ; k++){
                swap = tens2d[k][jrow];
                tens2d[k][jrow] = tens2d[k][jcolum];
                tens2d[k][jcolum] = swap;
            }
        }
    }
    
    for(int i = 0 ; i < size ; i++){
        for(int j = 0 ; j < size ; j++){
            inverse(i,j) = tens2d[i][j];
        }
    }
    
    return inverse;
}

//################################################################

//--------------------- Second order tensor operators ------------------------------------


//--------------------- Third order tensor operators ------------------------------------

Tensor3d::Tensor3d(){
    
    nFirstD = nSecondD = nThirdD = 0;
}


void Tensor3d::resize(  int FirstD , int SecondD , int ThirdD){
    
    nFirstD = FirstD;
    nSecondD = SecondD;
    nThirdD = ThirdD;
    
    
    tens3d.resize(nFirstD);
    for (  int i = 0; i < nFirstD; ++i){
        tens3d[i].resize(nSecondD);
        for (  int j = 0; j < nSecondD; ++j){
            tens3d[i][j].resize(nThirdD);
        }
    }
    
    *this = 0.0;
}

double& Tensor3d::operator()(int i,   int j , int k ){
    
    return tens3d[i][j][k];
}


Tensor3d& Tensor3d::operator=(double val){
    
    for (  int i = 0; i < nFirstD; ++i){
        for (  int j = 0; j < nSecondD; ++j){
            for (  int k = 0; k < nThirdD; ++k){
                tens3d[i][j][k] = val;
                
            }
        }
    }
    
    
    return *this;
}


//--------------------- Third order tensor operators ------------------------------------

//--------------------- Forth order tensor operators ------------------------------------

//Tensor4d::Tensor4d( int FirstD , int SecondD , int ThirdD , int ForthD ){

//   resize(FirstD , SecondD , ThirdD , ForthD);

//}

Tensor4d::Tensor4d(int dim, double value) {
    resize(dim, dim, dim, dim);
    *this = value;
}

void Tensor4d::resize(  int FirstD , int SecondD , int ThirdD , int ForthD){
    
    nFirstD = FirstD;
    nSecondD = SecondD;
    nThirdD = ThirdD;
    nForthD = ForthD;
    
    
    tens.resize(nFirstD);
    for (  int i = 0; i < nFirstD; ++i){
        tens[i].resize(nSecondD);
        for (  int j = 0; j < nSecondD; ++j){
            tens[i][j].resize(nThirdD);
            for (  int k = 0; k < nThirdD; ++k){
                tens[i][j][k].resize(nForthD);
            }
        }
    }
}


double& Tensor4d::operator()(int i,   int j , int k , int l){
    
    return tens[i][j][k][l];
}

double Tensor4d::operator()(int i, int j , int k , int l) const{
    
    return tens[i][j][k][l];
}

Tensor4d& Tensor4d::operator=(double val){
    
    for (  int i = 0; i < nFirstD; ++i){
        for (  int j = 0; j < nSecondD; ++j){
            for (  int k = 0; k < nThirdD; ++k){
                for (  int l = 0; l < nForthD; ++l){
                    tens[i][j][k][l] = val;
                }
            }
        }
    }
    
    
    return *this;
}


Tensor4d& Tensor4d::operator==(double valu){
    
    
    int ndim = size();
    
    std::vector<std::vector<double>> delta_kron(ndim,std::vector<double>(ndim,0.0));
    
    
    for(int i = 0 ; i < ndim ; i++){
        for(int j = 0 ; j < ndim ; j++){
            for(int k = 0 ; k < ndim ; k++){
                for(int l = 0 ; l < ndim ; l++){
                    tens[i][j][k][l] = 0.0;
                }
            }
        }
    }
    
    for (int i = 0 ; i<ndim ; i++){
        for (int j = 0 ; j < ndim ; j++){
            if(i == j) delta_kron[i][j] = valu;
            else delta_kron[i][j] = 0.0;
        }
    }
    
    
    for(int i = 0 ; i < ndim ; i++){
        for(int j = 0 ; j < ndim ; j++){
            for(int k = 0 ; k < ndim ; k++){
                for(int l = 0 ; l < ndim ; l++){
                    tens[i][j][k][l] = delta_kron[i][k]*delta_kron[j][l]+delta_kron[i][l]*delta_kron[j][k];
                }
            }
        }
    }
    
    for(int i = 0 ; i < ndim ; i++){
        for(int j = 0 ; j < ndim ; j++){
            for(int k = 0 ; k < ndim ; k++){
                for(int l = 0 ; l < ndim ; l++){
                    tens[i][j][k][l] = 0.5*tens[i][j][k][l];
                }
            }
        }
    }
    
    return *this;
}

int Tensor4d::size() const{
    
    return tens.size();
}
Tensor4d& Tensor4d::operator+=(const Tensor4d &b){
    
    
    int ndim = size();
    
    for (  int i = 0; i < ndim; ++i){
        for (  int j = 0; j < ndim; ++j){
            for (  int k = 0; k < ndim; ++k){
                for (  int l = 0; l < ndim; ++l){
                    tens[i][j][k][l] += b(i,j,k,l);
                }
            }
        }
    }
    
    return *this;
    
}

Tensor4d operator+(const Tensor4d &a,const Tensor4d &b){
    
    Tensor4d result = a;
    
    result += b;
    
    return result;
}

//--------------------- Forth order tensor operators ------------------------------------


