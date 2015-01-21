
// Miscellaneous C++ declarations that SWIG should be able to handle

%module cpp_misc

// Ignored "inline" directive

inline int misc1(int);

// Extra "const" added

int misc2(int, int) const;

// Now in a class definition

class Misc {
public:
	inline int misc3(double);
	double misc4(double,float) const;
};

// Constructor initializer

class Foo {
	int x,y;
public:
	Foo(int x, int y) : x(x), y(y), z(x+2,3,4) { };
};

