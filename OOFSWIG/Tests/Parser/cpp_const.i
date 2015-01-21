//
// cpp_const.i
// Test SWIG's parsing of C++ style constants
//
%module cpp_const

class Foo {
public:
	enum my_months {JAN = 1, FEB = 2, MAR = 3, APR = 4, MAY = 5,
		     JUN = 6, JUL = 7, AUG = 8, SEP = 9, OCT = 10,
		     NOV = 11, DEC = 12};
	enum fruits {PEAR, APPLE, BANANA, PEACH};
	enum values {VAL1 = 0x01, VAL2 = 0x02, VAL3 = 0x03, };
	const double MAX = 50;
};

enum fruit {PEAR, APPLE};   // Not a repeated value (not in scope)

const double PI = 3.141592654;
const int    N = 1000;
const char  *VERSION = "1.0";




