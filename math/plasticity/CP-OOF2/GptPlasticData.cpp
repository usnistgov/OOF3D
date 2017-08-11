//
//  GptPlasticData.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "GptPlasticData.hpp"
GptPlasticData::GptPlasticData(){
    
    std::vector<double> ft{0.0,0.0,0.0};
    
    for (int i = 0 ; i < 3 ; i++){
        Ft.push_back(ft);
        Fpt.push_back(ft);
    }
    
    Ft[0][0] = Ft[1][1] = Ft[2][2] = 1.0;
    Fpt[0][0] = Fpt[1][1] = Fpt[2][2] = 1.0;
    
}
