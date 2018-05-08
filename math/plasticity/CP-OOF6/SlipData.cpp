//
//  SlipData.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/30/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "SlipData.hpp"
SlipData::SlipData(const std::string &name,Element *el,ConstitutiveModel* CM,MatInput* mi) : ElementData("slip_data") {
    
    for (std::vector<GaussPoint*>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++) {
        GptSlipData gpslip = GptSlipData(CM,mi);
        gptslipdata.push_back(gpslip);
        
    }
}
