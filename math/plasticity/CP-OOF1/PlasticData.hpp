//
//  PlasticData.hpp
//  node
//
//  Created by Keshavarzhadad, Shahriyar on 6/22/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef PlasticData_hpp
#define PlasticData_hpp

#include <stdio.h>
#include <string>
#include <vector>

#include "ElementData.hpp"
#include "Element.hpp"

#include "GaussPoint.hpp"
#include "GptPlasticData.hpp"

class PlasticData : public ElementData {
public:
    PlasticData(const std::string &name , Element *el);
    std::vector<GptPlasticData> fp;
};

#endif /* PlasticData_hpp */
