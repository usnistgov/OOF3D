// This file contains C preprocessor directives that SWIG should successful ignore

%module cpp_ignore

// A Macro

#define  foo(a,b)          (a+b)

// Some erroneous defines

#define  LBRACE      _{ 
#define  DEF_VALUE   {{0,0},{1,2},{3,4}}
#define  FOOBAR      #&&&*!((@))(#JJAJKSKK!@((#JS  S))A  @JJ# 

int a;

#define ASYMBOL
// An include

#include "foobar.h"

// Misc C++ directives
#line  45,"input.i"
#error

// Should have no effect

#


// Test #undef

#undef ASYMBOL

#define ASYMBOL

// Test the #if defined() macro 

#if  defined(ASYMBOL)
double b;
#if ! defined(ASYMBOL)
double not_defined;
#elif defined(ASYMBOL)
double not_defined_2;
#endif
#elif defined(BSYMBOL)
double c;
#else
double d;
#endif



