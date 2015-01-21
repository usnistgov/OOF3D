//
// cpp_inherit.i
// This file tests SWIG handling of inheritance and virtual
// functions.
%module shape

class Shape {
private:
	int count;
public:
        virtual ~Shape() { };
        Shape() { count = 1;}
        void ref() { count++;}
	void deref() { count--; if (!count) delete this; }
        int  get_ref() { return count;}
	int  color;
virtual void print() = 0;
        char *name;


};

class TwoD : public Shape {
private:
	double x,y;
public:
        ~TwoD() { };
	void set_center(double _x, double _y) {x = _x; y= _y;}
virtual double  area() = 0;
virtual double  perimeter() = 0;
virtual void    print() = 0;
  void print_center() { printf("x = %g, y = %g\n", x, y);}
};

class ThreeD : public Shape {
private:
	double x,y,z;
public:
  ~ThreeD() { };
  void set_center(double _x, double _y, double _z) {
    x= _x; y = _y; z = _z;
  }
  virtual double volume() = 0;
  virtual double surface() = 0;
  virtual void print() = 0;
  void print_center() { printf("x = %g, y = %g, z= %g\n", x, y, z);}
};

class Circle : public TwoD {
private:
  double radius;
public:
  Circle(double _r) { radius = _r; name = "Circle";}
  double area() { return 3.1415926*radius*radius;}
  double perimeter() {return 2*3.1415926*radius;}
  void   print() { printf("Circle : radius = %g\n", radius);}
};

class Square : public TwoD {
private:
  double width;
public:
  Square(double _w) { width = _w; name = "Square";}
  double area() {return width*width;}
  double perimeter() {return 4*width;}
  void   print() {printf("Square : width = %g\n", width);}
};

class Sphere : public ThreeD {
private:
  double radius;
public:
  Sphere(double _r) { radius = _r; name = "Sphere";}
  double volume() {return (4.0/3)*3.1415926*radius*radius*radius;}
  double surface() {return 4*3.1415926*radius*radius;}
  void   print() {printf("Sphere : radius = %g\n", radius);}
};

class Cube : public ThreeD {
private:
  double width;
public:
  Cube(double _w) {width = _w; name = "Cube";}
  double volume() {return width*width*width;}
  double surface() {return 6*width*width;}
  void print() {printf("Cube : width = %g\n", width);}
};
			

// Check inheritance of enums and datatypes

class ENUM {
public:
   enum Enum1 { ALE, LAGER, STOUT, PILSNER };
   void foo(Enum1 e);
   typedef double Real;
   Real bar(Real);
};

class ENUM1 : public ENUM {
public:
   void foo2(Enum1 e);
   Real bar2(Real);
};
	
// Check inheritance of readonly variables

class ROnlyBase {
public:
%readonly
   int x;
%readwrite;
   int y;
};

class ROnly : public ROnlyBase {};
