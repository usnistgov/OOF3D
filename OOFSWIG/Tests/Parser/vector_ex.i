%module vectorop
%{
%}

%extern vector.i
%include vector.c

class Vector2 : public Vector {
public:
  double w;
};


