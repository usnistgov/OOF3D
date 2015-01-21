%module amethod

// Test the add methods construct

struct Foo {
	int x,y,z;
	%addmethods {
		Foo();
		~Foo();
		int bar();
        }
	double a;
};

struct Foo2 {
	%addmethods {
		Foo2();
		~Foo2();
		int grok();
		static int st_func(double a);
	}
	double x,y,z;
};

struct Foo3 {
	%addmethods {
	        double bar(double a) { return a; }
		double ref(Foo &f1, Foo &f2, Foo *f3) { ... do something ... }
		static int grok(int b) {
			... code for a static function ...
		}
}
};

// Try to use addmethods in an inheritance tree

class BarBase {
public:
	int x;
	int foo();
	BarBase();
	~BarBase();
	%addmethods {
	   void added_method(double *a) {
		... code for BarBase::added_method() ... 
	   }
	}
};

class Bar : public BarBase {
public:
	int y;
	Bar();
	~Bar();
};

// Try to get an added method from another file

%import amextern.i

class EE : public EBase {
};

class FF : public EE { };
	 	
// Use addmethods with member data

struct Vector {
%addmethods {
	double x,y,z;
}
};
	






