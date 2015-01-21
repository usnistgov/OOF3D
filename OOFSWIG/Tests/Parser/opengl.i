%module opengl
%{
%}

#ifdef ORIGINAL
#ifdef STATIC
%include embed.i
#else
%include wish.i
#endif
#endif
%include gl.i
%include glu.i
%include help.i
%include glaux.i
%include carray.i

