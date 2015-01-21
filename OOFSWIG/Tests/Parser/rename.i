//
// This file tests the SWIG %name() directive
//
%module rename

%name(new_variable) int my_variable;
%name(add) double sum(double,double);

class Foo2 {
public:
%name(new_var) double var;
%name(new_static_var) static double static_var;
%name(add)       int    sum(int a, int b) { return a+b;}
%name(product)  static int    mul(int a, int b) { return a*b;}
enum swig {%name(LAGER) lager, %name(ALE) ale, %name(STOUT) stout,
           %name(PILSNER) pilsner};

// Overloaded member functions

int       foo(double, double);
%name(foochar) void      foo(char *);

// Overloaded static functions

static int  bar(double);
%name(barchar) static void bar(char *);
static int bar(int);

};

%name(MyClass) class Class {
public:
	int member_data;
	double member_func();
        void pointer(Class *c);
        Class *retptr(void);
};

// Test using class above

Class *retClass(void);

// Find out what happens when we inherit

class Foo3 : public Foo2 { };

class Foo4 : public Foo3 { };

class Bar : public Class { };

// Check if %name works around a #define now

#ifdef SWIG
%name(NewName)
#endif
void OldName(double);
void SameName(int);


// Try out the new %rename directive

%rename old_name new_name;

// Now some declarations

int foo10(double);
int old_name(double);

class C {
public:
	int old_name(int a);
};

