//
//  PlasticData.cpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#include "PlasticData.hpp"

PlasticData::PlasticData(const std::string &name,Element *el) : ElementData("plastic_data") {
    for (vector<GaussPoint*>::iterator gpti = el->gptable.begin() ; gpti!=el->gptable.end(); gpti++) {
        GptPlasticData gppd = GptPlasticData();
        fp.push_back(gppd);
        //        el->array.push_back(gppd);
        gptdata.push_back(gppd);
        
        //        for (int i = 0 ; i < el->array.size() ; i++)
        //           cout<<i<<"   "<<el->array[i].ft[0]<<endl;
    }
}
