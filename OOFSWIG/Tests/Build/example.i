/* File : example.i */
%module example
%{
/* Put headers and other declarations here */
%}

extern double My_variable;
extern int    fact(int);

// Build a static version depending on what language we're using

#ifdef STATIC

#ifdef TCL
%include tclsh.i
#endif

#ifdef WISH
%include wish.i
#endif

#ifdef PERL5
%include perlmain.i
#endif

#ifdef PYTHON
%include embed.i
#endif

#endif


