%module vector
%{

typedef double Real;
#include "vector.h"

/* Create a big array of vectors */

Vector *array_Vector(int nv) {
    Vector *v;
    v = (Vector *) malloc(nv*sizeof(Vector));
    return v;
}

/* Get a vector out of the array */

Vector *get_Vector(Vector *a, int i) {
    return &a[i];
}

void set_Vector(Vector *a, int i, Vector *v) {
    a[i] = *v;
}


/* Move pointer to next vector */

Vector *Vector_next(Vector *a) {
    return a + 1;
}

/* Print out vector */

char *Vector___str__(Vector *a) {
    static char s[256];
    sprintf(s,"x = %f, y = %f, z = %f", a->x, a->y, a->z);
    return s;
}

Vector *Vector_get(Vector *v, int i) {
	return v+i;
}

void Vector___setitem__(Vector *v, int i, Vector *val) {
	v[i] = *val;
}

%}

typedef double Real;
typedef struct Vector {
    Vector();	
   ~Vector();
    Real x,y,z;
//
// Betcha you didn't know that SWIG let's you add methods to C
// structures!
%addmethods {
    Vector *next();
%name(__getitem__)    Vector *get(int i);
    void   __setitem__(int i, Vector *val);
    char  *__str__();
}
} Vector;

Vector *array_Vector(int nv);
Vector *get_Vector(Vector *a, int i);
void set_Vector(Vector *a, int i, Vector *v);

