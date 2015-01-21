%module ebase

class EBase {
public:
	EBase();
	~EBase();
	%addmethods {
		void emethod(double a);
	}
};

%addmethods EBase {
	void emethod2(double b) {	
		... code for emethod2() ...
        }
};

