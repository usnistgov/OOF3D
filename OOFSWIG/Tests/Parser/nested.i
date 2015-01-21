// Check SWIG's parsing of nested structures

%module nested

%inline %{

struct ValueStruct {  
                  unsigned int dataType;
                  union foo {
			int       intval;
			double    doubleval;
			char     *charval;
			void     *ptrvalue;
			long      longval;
		} u;
		double bar;
};

%}




