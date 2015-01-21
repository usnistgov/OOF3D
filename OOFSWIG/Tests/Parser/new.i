// Test out the %new directive

%module foo

%new char *return_string();

class Foo {
public:
	Foo();
	~Foo();
	%new Foo *create_foo();
};

%new Foo *create_foo2();
