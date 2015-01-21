%module array
%{

%}

// Test array parsing

extern int foo(int a[4], int b[4][4], int c[4][4][3]);
extern int func(int argc, char *argv[]);

typedef  float MATRIX4[4][4];

extern float matrix(MATRIX4 a);

extern float matrixofmatrix(MATRIX4 a[4]);

