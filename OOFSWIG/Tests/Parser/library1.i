//
// This file tests the SWIG library
// Should not lock up, should not generate any duplicates
%module library
%{
%}

%include library1.i
%include library2.i
%include library3.i
%include library4.i
%include function.i
%include variable.i
%include constant.i

