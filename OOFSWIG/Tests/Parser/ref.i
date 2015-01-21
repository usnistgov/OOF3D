//
// Test a bug in the C++ module with function arguments
// involving complex datatypes (reported 9/13/96).

%module ref
%{

struct Vector {
	double x,y,z;
};

class FooBar {
public:
    FooBar(Vector &v) {
	vec = v;
    }
    Vector vec;
    void dump() {
        printf("vec.x = %g, vec.y = %g, vec.z = %g\n", vec.x,vec.y,vec.z);
    }
};

%}

struct Vector {
    Vector();
    ~Vector();
    double x,y,z;
};

class FooBar {
public:
    FooBar(Vector &v) {
	vec = v;
    }
    Vector vec;
    void dump();
};

