#include "vector.h"

/* Define a bunch of operations on vectors */

Vector add(Vector v1, Vector v2) {
    Vector v;
    v.x = v1.x + v2.x;
    v.y = v1.y + v2.y;
    v.z = v1.z + v2.z;
    return v;
}

Vector sub(Vector v1, Vector v2) {
    Vector v;
    v.x = v1.x - v2.x;
    v.y = v1.y - v2.y;
    v.z = v1.z - v2.z;
    return v;
}

Vector cross(Vector v1, Vector v2) {
    Vector v;
    v.x = v1.y*v2.z - v1.z*v2.y;
    v.y = v1.x*v2.z - v1.z*v2.x;
    v.z = v1.x*v2.y - v2.x*v1.y;
    return v;
}

double dot(Vector v1, Vector v2) {
    double d;
    d = v1.x*v2.x + v1.y*v2.y + v1.z*v2.z;
    return d;
}

Vector mul(double a, Vector v1) {
    Vector v;
    v.x = a*v1.x;
    v.y = a*v1.y;
    v.z = a*v1.z;
    return v;
}





