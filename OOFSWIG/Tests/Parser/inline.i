%module iline

// This file tests SWIG's inline directive

%inline %{
double inline1(double &a) {
   inlined definition 1
}
double inline2() {
   inlined definition 2
}
double inline3() {
   inlined definition 3
}
int inline4();

int a;

static int foo1(int) {
   A static, but inlined function
}


#define BAR  4
%}

double bar();    // Not inlined
double grok();   // Shouldn't be inlined


%inline double foo() {
   inlined definition 4;
}


