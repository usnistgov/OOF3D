/* This file should generate a C compiler error.  
   However, the C compiler should report the error for 
   a line in this file, not the wrapper file */

%module error
%{

int a;
int b;

int foo(int a, int b) {
	c = a+b;          /* Error. c not declared */
	return c;
}

%}

int foo(int, int);

