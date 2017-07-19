//
//  GptPlasticData.cpp
//  sr
//
//  Created by Keshavarzhadad, Shahriyar on 6/28/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "GptPlasticData.hpp"

GptPlasticData::GptPlasticData(){
    
    ft.clear();
    ft.push_back(1.0) , ft.push_back(0.0) , ft.push_back(0.0);
    ft.push_back(0.0) , ft.push_back(1.0) , ft.push_back(0.0);
    ft.push_back(0.0) , ft.push_back(0.0) , ft.push_back(1.0);
    
//    ft = {1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0};
}
