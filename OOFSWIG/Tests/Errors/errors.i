//
// This file tests various types of errors that
// SWIG should properly deal with
// 

%{

%}

//  Linkage to complex datatype

Vector   v;

// Renaming more than one declaration.

%name new_int {int old_int, a, b, c;}

%name(new_int1) int old_int1, a1, b1, c1;

// Returning a complex type by value

Vector foo(void);

// Redeclaration of functions

int  fact(int);
int  fact(int);

// Recursive inclusion (should not lock the system up)

%include errors.i

// Type errors in constants

#define  I_CONS       3.1423 | 0x4f

// Redeclaration of %title and %init functions
// (should be ignored)

%title "Hello world"
%init My_Init

//
// Nonexistent include file

%include bogus.i

//
// Missing type information.

variable;
bar(int);

//
// Array notation

int foo1(int a[]);

// Function pointer

int foo2(int (*a)(void *, int, double), double);
int foo3(int);
int foo4(int (*)(void *, int, double), double);






