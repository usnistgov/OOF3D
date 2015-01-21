// This is only a start of template support

%module temp

// A function involving templated parameters

void foo(vector<complex> *cv, vector<int> *ci);
void foo2(vector<complex> &cv, vector<int> &ci);

// Multi-valued templates
void foo3(pair<complex, double> *a, triple<int,int,double> *b);

// Make sure our stripping function works

void foo4(pair<unsigned int,    double> *a, triple<const      unsigned    int, double,    complex> *b);

// This should gracefully generate an error message

template<class T> class vector {
	T *v;
	int sz;
public:
	vector(int);
	T& operator[](int);
	T& elem(int i) { return v[i]; }
};

// This should parse okay

int bar(void);

template<class E, int size> class buffer;

int bar1(void);

// A template function

template<class T> void sort(vector<T>);

int bar2(void);



