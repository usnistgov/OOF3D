//
//  ElementData.hpp
//  CPOOF
//
//  Created by Keshavarzhadad, Shahriyar on 8/10/17.
//  Copyright © 2017 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef ElementData_hpp
#define ElementData_hpp

#include <stdio.h>
#include <string>

class ElementData {
private:
    const std::string name_;
public:
    ElementData(const std::string &nm) : name_(nm) {}
    std::string name() { return name_; }
    virtual ~ElementData() {}
};


#endif /* ElementData_hpp */
