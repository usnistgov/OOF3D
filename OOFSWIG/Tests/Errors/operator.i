%module op
%{
%}

// SWIG should recognize operator overloading, but should ignore it...

class foobar {
public:
	foobar &operator[](int i);
	const char &operator[](int) {
	    a bunch of random code here
	}
};

foobar& foobar::operator[](int i);

