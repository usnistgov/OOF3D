%module fr
%{

%}

// Test recognition of friends.  Friends should be ignored.

class foobar {
public:

friend int bar(int, double);
friend operator!=(const char &, const char &) {
    }
};
	
