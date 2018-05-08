//
//  SlipData.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/30/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef SlipData_hpp
#define SlipData_hpp

#include <stdio.h>
#include <string>
#include <vector>
#include <iostream>

#include "ElementData.hpp"
#include "Element.hpp"

#include "GaussPoint.hpp"
#include "PowerLaw.hpp"
#include "MatInput.hpp"

class SlipData : public ElementData {
    
public:
    SlipData(const std::string &name , Element *el,ConstitutiveModel* CM,MatInput* mi);
    
    std::vector<GptSlipData> gptslipdata;
    
};

#endif /* SlipData_hpp */
