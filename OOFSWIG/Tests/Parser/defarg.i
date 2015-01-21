// Testing of default argument parsing

%module defarg

int foo(int, double a = 3, char *str = "Hello");
int bar(double a, char *ptr = 0, char c = 'a', void *p = NULL);

class Foo {
public:
   enum SWIG {LAGER,ALE,STOUT};
   void test(double a, SWIG value=Foo::LAGER);
   void test2(double a, SWIG value=STOUT);
};

void grok(Foo *f);

// Try some C++ references

void ref(String &s = STR);
