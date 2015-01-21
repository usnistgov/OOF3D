%module cond

// This file tests the SWIG parser on conditionals
// It should wrap 4 functions : bar, grok, frob2, grok2

#ifdef TEST1
int foo(int);

SWIG Should ignore all of this !!!
&&#(&(*!@   This is complete and utter garbage !**)(*()*)(@)(*
#####&&@**!((#############TEESTTTS
/*      #else    SWIG better ignore this! */


#else
double bar(int);
#endif

#ifdef TEST2
int foo2(int);
#ifdef TEST3
int foo3(int);
    #else
double bar2(double);

Even more garbage in an unparsed block. !***@**#[][][][][
(*(*(*)(int,int));
/*
#include "hello"
#endif
int foo4(int);
    #     else
int grok(double);
#ifdef TEST4
double frob(int);

Bunch of junk

#else
double frob2(double);
#endif
int grok2(int);
#endif

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

#if  ! defined(ASYMBOL)
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




