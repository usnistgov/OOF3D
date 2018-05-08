//
//  GptPlasticData.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/30/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef GptPlasticData_hpp
#define GptPlasticData_hpp

#include <stdio.h>
#include<vector>
#include "GaussPoint.hpp"
#include "Tensor.hpp"

class GptPlasticData {
public:
    GptPlasticData();
    
    Tensor2d Ft;
    Tensor2d Fpt;
    Tensor2d F_tau;
    Tensor2d Fp_tau;
    Tensor2d Fe_tau;
    Tensor2d Cauchy;
    Tensor2d S_star;
    Tensor2d Dep;
    Tensor4d w_mat;

    
};

#endif /* GptPlasticData_hpp */
