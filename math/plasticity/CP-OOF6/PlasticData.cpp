//
//  PlasticData.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/30/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "PlasticData.hpp"
PlasticData::PlasticData(const std::string &name,Element *el) : ElementData("plastic_data") {
    
    for (std::vector<GaussPoint*>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++) {
        GptPlasticData gppd = GptPlasticData();
        fp.push_back(gppd);
        gptdata.push_back(gppd);
        
    }
}
