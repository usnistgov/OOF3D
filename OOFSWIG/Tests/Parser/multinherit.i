// Tests SWIG's parsing of multiple inheritance structures

class a {
    int x;
};

class b {
    int y;
};

class c {
    int z;
};

class d {
    int w;
};

class foo : public a, public b, public c, public d {
public:
     double bar();
};

// Tests parsing of virtual public

class foo1 : virtual public a {
public:
    double bar();
};

class foo2 : public virtual a {
public:
    double bar();
};

class foo3 : public a, public virtual b, virtual public c {
public:
     double bar();
};

// Private inheritance, not supported

class foo4 : private a {
public :
	double bar();
};

// Protected inheritance, not supported

class foo5 : protected a {
public :
        double bar();
};

// Missing access specifier should generate errors

class foo6 : a {
public :
	double bar();
};

class foo7 : virtual a {
public :
	double bar();
};

// A mix of everything (just to make sure the parser isn't hosed)

class foo8 : public a,
             virtual public b,
             public virtual c,
             private d,
             virtual private e,
             private virtual f,
             protected g,
             virtual protected h,
             protected virtual i,
             j,
             virtual k {
public:
};


// The evil diamond

class A { };
class B : public A { };
class C : public A { };
class D : public B, public C { };


