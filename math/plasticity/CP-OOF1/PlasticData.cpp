//
//  PlasticData.cpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/22/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "PlasticData.hpp"

PlasticData::PlasticData(const std::string &name,Element *el) : ElementData("plastic_data") {
    for (vector<GaussPoint>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++) {
        GptPlasticData gppd = GptPlasticData();
        fp.push_back(gppd);
    }
}
