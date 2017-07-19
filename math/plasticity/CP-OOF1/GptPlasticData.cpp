//
//  GptPlasticData.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/26/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "GptPlasticData.hpp"

GptPlasticData::GptPlasticData(){
    
    fp.resize(9);
    for (int i = 0 ; i <9 ; i++)
        fp[i] = 0.0;
    fp[0] = fp[4] = fp[8] = 1.0;
}
