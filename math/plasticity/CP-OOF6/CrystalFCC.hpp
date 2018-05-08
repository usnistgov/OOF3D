//
//  CrystalFCC.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef CrystalFCC_hpp
#define CrystalFCC_hpp

#include <stdio.h>

#include "CrystalPlasticity.hpp"
#include "MatInput.hpp"
#include "ConstitutiveModel.hpp"
#include "CauchyStress.hpp"

class CrystalFCC : public CrystalPlasticity {
    
public:
    
    CrystalFCC(ConstitutiveModel* cm,MatInput* mi);
    virtual void calculate_schmid_tensor();
 //   virtual void begin_element(Element *, Mesh *);
    
    
    
    
};

#endif /* CrystalFCC_hpp */
