//
// cpp_data.i
// This file tests SWIG's parsing of C++ member data
//
%module cpp_data

class Data {
public:
	int               d_int;
	short             d_short;
	long              d_long;
	unsigned int      d_uint;
	unsigned short    d_ushort;
	unsigned long     d_ulong;
	unsigned char     d_uchar;
	signed char       d_schar;
	float             d_float;
	double            d_double;
	char             *d_string;
	char              d_char;
	int               *p_int;
	short             *p_short;
	long              *p_long;
	unsigned int      *p_uint;
	unsigned short    *p_ushort;
	unsigned long     *p_ulong;
	unsigned char     *p_uchar;
	signed char       *p_schar;
	float             *p_float;
	double            *p_double;

static  int                s_int;
static  short              s_short;
static  long               s_long;
static  float              s_float;
static  double             s_double;
static  char              *s_string;

	Vector             vec;
	Vector            &rvec;
};




