// This file has a CPP macro in it.  SWIG should ignore these

%module macro
%{

%}

#define AMACRO(a,b)     (int (a+b))


int foo(int bar);

/* A multiline macro */

#define plot_circle(x,y,c) \
   if ((x >= xmin) && (x < xmax) && \
       (y >= ymin) && (y < ymax)) \
        pixels[y][x] = c;


double bar(double);
