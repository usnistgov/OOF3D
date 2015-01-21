%module name
%{

%}

#else
int foo;

#endif


#ifdef BAR
double My_var;
#else
float My_var;
#else
int My_var;
#endif

double bar;


