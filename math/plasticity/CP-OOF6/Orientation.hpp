//
//  Orientation.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef Orientation_hpp
#define Orientation_hpp

#include <stdio.h>

#include "Property.hpp"

class OrientationProp : public Property {
public:
    double phi,theta,omega;
    OrientationProp(double phi, double theta, double omega) : Property("Orientation"), phi(phi),theta(theta),omega(omega) {}
};
#endif /* Orientation_hpp */
