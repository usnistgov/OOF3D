// This tests the placement of a conditional in an enumeration list

enum test {
	value1,
	value2,
#ifdef ALL
	value3,
	value4,
	value5,
	value6,
#else
	value7,
	value8,
	value9,
#endif
	value10,
	value11 };

