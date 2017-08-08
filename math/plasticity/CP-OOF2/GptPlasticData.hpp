//
//  GptPlasticData.hpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef GptPlasticData_hpp
#define GptPlasticData_hpp

#include <stdio.h>

#include<vector>
#include "GaussPoint.hpp"

class GptPlasticData {
public:
    GptPlasticData();

    std::vector<std::vector<double>> Ft;
    std::vector<std::vector<double>> Fpt;

};

#endif /* GptPlasticData_hpp */
