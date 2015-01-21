%module doc
%{

%}

// This file tests the disable/enable features for documentation

int foo(int a);

%disabledoc
double bar(double b);
%enabledoc

double grok(int a);
%disabledoc
int frob(int a);
%disabledoc
double foobar(double b);
%enabledoc
double spam(int c);    // This should still be disabled (by scoping)
%enabledoc

int spif(double d);    // This should be enabled.
