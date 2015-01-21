//
// Test a bug in the C++ module with function arguments
// involving complex datatypes (reported 9/13/96).

%module value
%{

struct Vector {
    double x,y,z;
};

class FooBar {
public:
    Vector r;
    Vector add(Vector s) {
	Vector w;
	w.x = r.x + s.x;
	w.y = r.y + s.y;
	w.z = r.z + s.z;
	return w;
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
    FooBar();
    Vector r;
    Vector add(Vector s) {
	Vector w;
	w.x = r.x + s.x;
	w.y = r.y + s.y;
	w.z = r.z + s.z;
	return w;
    }
};

