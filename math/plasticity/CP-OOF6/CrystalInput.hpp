//
//  CrystalInput.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef CrystalInput_hpp
#define CrystalInput_hpp

#include <stdio.h>
typedef enum {mDefault, mFCC} MatType;
typedef enum {ConstDefault, ConstPowerLaw} ConstType;
typedef enum {w1 , w2 , ss , a, h0,m,g0dot,dt,init_res,endconst} MatConst;
typedef enum {c11,c12,c44,numconst} CijklConst;
typedef enum {phi, theta, omega} Orientations;

#endif /* CrystalInput_hpp */
