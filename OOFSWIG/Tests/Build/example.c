/* Simple example from documentation */
/* File : example.c */

#ifdef SWIG
%module example
#endif


double My_variable = 3.0;

int fact(int n) {
  if (n <= 1) return 1;
  else return n*fact(n-1);
}

int mod(int n, int m) {
  return (n % m);
}
