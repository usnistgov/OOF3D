//
//  PlasticData.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/30/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef PlasticData_hpp
#define PlasticData_hpp

#include <stdio.h>
#include <string>
#include <vector>
#include <iostream>

#include "ElementData.hpp"
#include "Element.hpp"

#include "GptPlasticData.hpp"
#include "GaussPoint.hpp"

class PlasticData : public ElementData {
public:
    PlasticData(const std::string &name , Element *el);
    std::vector<GptPlasticData> fp;
    
    std::vector<GptPlasticData> gptdata;
    
};


#endif /* PlasticData_hpp */
