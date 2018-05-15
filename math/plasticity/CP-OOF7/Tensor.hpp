//
//  Tensor.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Tensor_hpp
#define Tensor_hpp

#include <stdio.h>
#include <vector>
#include <iostream>
#include <cmath>

//--------------------- first order tensor operators ------------------------------------
class Vector{
    
public:
    
    Vector(unsigned int sizeIn = 0);
    void resize(unsigned int sizeIn);
    unsigned int size() const;
    unsigned int rows() const {return size();}
    double& operator()(unsigned int i);
    double operator()(unsigned int i) const;
    Vector& operator=(double val);
    Vector& operator+=(const Vector &b);
    Vector& operator-=(const Vector &b);
    
private:
    
    std::vector<double> vec;
    
    
    
};
Vector operator+(const Vector &a,const Vector &b);
Vector operator-(const Vector &a,const Vector &b);


//--------------------- Second order tensor operators ------------------------------------
class Tensor2d{
    
public:
    Tensor2d(int FirstD = 0, int SecondD = 0);
    void resize(int FirstD = 0, int SecondD = 0);
    double& operator()(int i, int j);
    double operator()(int i, int j) const;
    Tensor2d& operator=(double val);
    Tensor2d& operator+=(const Tensor2d &b);
    Tensor2d& operator-=(const Tensor2d &b);
    Tensor2d& operator*=(const Tensor2d &b);
    Tensor2d operator~();
    Tensor2d operator-();
    Tensor2d operator--();
    
    int size() const;
    
    
    
private:
    std::vector<std::vector<double>> tens2d;
    int nFirstD;
    int nSecondD;
    
};
Tensor2d operator+(const Tensor2d &a,const Tensor2d &b);
Tensor2d operator-(const Tensor2d &a,const Tensor2d &b);
Tensor2d operator*(const Tensor2d &a,const Tensor2d &b);

//--------------------- Second order tensor operators ------------------------------------

//--------------------- Third order tensor operators ------------------------------------
class Tensor3d{
    
public:
    Tensor3d();
    void resize(int FirstD = 0, int SecondD = 0 , int ThirdD = 0);
    double& operator()(int i, int j , int k );
    double operator()(int i, int j , int k ) const;
    Tensor3d& operator=(double val);
    
private:
    std::vector<std::vector<std::vector<double>>> tens3d;
    int nFirstD;
    int nSecondD;
    int nThirdD;
    
};
//--------------------- Third order tensor operators ------------------------------------

//--------------------- Forth order tensor operators ------------------------------------
class Tensor4d{
public:
    //  Tensor4d(int FirstD = 0, int SecondD = 0 , int ThirdD = 0 , int ForthD = 0);
    Tensor4d( int dim = 0 , double value = 0.0);
    void resize(int FirstD = 0, int SecondD = 0 , int ThirdD = 0 , int ForthD = 0);
    double& operator()(int i, int j , int k , int l);
    double operator()(int i, int j , int k , int l) const;
    Tensor4d& operator=(double val);
    Tensor4d& operator==(double valu);
    Tensor4d& operator+=(const Tensor4d &b);
    int size() const;
    
private:
    std::vector<std::vector<std::vector<std::vector <double>>>> tens;
    int nFirstD;
    int nSecondD;
    int nThirdD;
    int nForthD;
};

Tensor4d operator+(const Tensor4d &a,const Tensor4d &b);
//--------------------- Forth order tensor operators ------------------------------------




#endif /* Tensor_hpp */
