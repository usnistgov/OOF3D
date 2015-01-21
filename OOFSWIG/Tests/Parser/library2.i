//
// This file tests the SWIG library
// Should not lock up, should not generate any duplicates
%module library
%{
%}

%include library.i
%include function.i
%include variable.i
%include constant.i
%include cpp_func.i
%include cpp_data.i
%include cpp_inherit.i
%include cpp_const.i
%include rename.i


