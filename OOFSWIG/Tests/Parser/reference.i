%module ref

// Test the parsing of C++ references

double bar(double &a);

double &foobar(double &a, double &);

extern double foo(double &a);
extern double &foobar2(double &a, double &);

// Make sure C++ references don't get confused with the other kind of reference

extern int dot_product(Vector a, Vector b);

// Make sure %val works with a C++ reference

extern double mutt(%val double &a);



