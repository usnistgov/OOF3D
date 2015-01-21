// This file tests SWIG's ability to keep text declarations associated with
// function calls.

%module text

%section "Test section",pre,sort

int foo(double);

%text %{
The foo function does something cool.
%}

int bar(double);

%text %{
The bar function does something even cooler.
%}

int grok(int);

%text %{
Who knows what this function does.
%}


