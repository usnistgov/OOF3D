
// This file tests the parsing of '0' constants with modifiers
// Bug reported by David Ascher : 9/25/96

%module zero
%{
%}

#define foo      0L
#define bar      0l
#define foobar   0U
#define barfoo   0u
#define grok     0UL
#define frob     0ul

const long FOO =  0L;


