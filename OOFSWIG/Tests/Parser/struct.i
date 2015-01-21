%module structs

// This module tests all sorts of different styles of structure definitions

struct Struct {
	double d;
	int    i;
	float  f;
	char   *c;
};

union Value {
	double d;
	int    i;
	float  f;
	char   *c;
};

class Object {
public:
	double d;
	int    i;
	float  f;
	char   *c;
	double  foo();
	Object();
	~Object();
};

typedef struct Struct1 {
	double d;
	int    i;
	float  f;
	char   *c;
} Struct1;

typedef union Value1 {
	double d;
	int    i;
	float  f;
	char   *c;
} Value1;

typedef class Object1 {
public:
	double d;
	int    i;
	float  f;
	char   *c;
	double  foo();
	Object1();
	~Object1();
} Object1;


/* Unnamed structures */

typedef struct {
	double d;
	int    i;
	float  f;
	char   *c;
} Struct2;

typedef union {
	double d;
	int    i;
	float  f;
	char   *c;
} Value2;

typedef class {
public:
	double d;
	int    i;
	float  f;
	char   *c;
	double  foo();
	Object2();
	~Object2();
} Object2;


/* Renamed structures */

%name(MyStruct) struct Struct3 {
	double d;
	int    i;
	float  f;
	char   *c;
};

%name(MyValue) union Value3 {
	double d;
	int    i;
	float  f;
	char   *c;
};

%name(MyObject) class Object3 {
public:
	double d;
	int    i;
	float  f;
	char   *c;
	double  foo();
	Object3();
	~Object3();
};

%name(MyStruct1) typedef struct Struct4 {
	double d;
	int    i;
	float  f;
	char   *c;
} Struct4;

%name(MyValue1) typedef union Value4 {
	double d;
	int    i;
	float  f;
	char   *c;
} Value4;

%name(MyObject1) typedef class Object4 {
public:
	double d;
	int    i;
	float  f;
	char   *c;
	double  foo();
	Object4();
	~Object4();
} Object4;


/* Unnamed structures */

%name(MyStruct2) typedef struct {
	double d;
	int    i;
	float  f;
	char   *c;
} Struct5;

%name(MyValue2) typedef union {
	double d;
	int    i;
	float  f;
	char   *c;
} Value5;

%name(MyObject2) typedef class {
public:
	double d;
	int    i;
	float  f;
	char   *c;
	double  foo();
	Object5();
	~Object5();
} Object5;




