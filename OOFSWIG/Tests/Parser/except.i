// Test parsing of C++ exception specifications

%module except


// Test the SWIG exception typemap

%except(tcl) {
    try {
          $function
    }
    catch (X) {
	...
    }
}

int f1(double) throw();
int f2(double) throw(X,Y);
int f3(int) throw(X) {
     ... a bunch of code ...
}

class Foo {
public:
	int f1(double) throw();
	int f2(double) throw(X,Y);
	int f3(double) throw(X) {
	     ... member code ...
	}
};

