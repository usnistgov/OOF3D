/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"


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


typedef union {
			int       intval;
			double    doubleval;
			char     *charval;
			void     *ptrvalue;
			long      longval;
		} ValueStruct_u;

C++ CLASS DECLARATION : struct ValueStruct
C++ CLASS DECLARATION : union ValueStruct_u
C++ CLASS START : struct ValueStruct  ========================================

        ATTRIBUTE     : unsigned int  dataType; 
        ATTRIBUTE     : double  bar; 
        ATTRIBUTE     : ValueStruct_u  u; 
C++ CLASS END ===================================================

C++ CLASS START : union ValueStruct_u  ========================================

        ATTRIBUTE     : int  intval; 
        ATTRIBUTE     : double  doubleval; 
        ATTRIBUTE     : char * charval; 
        ATTRIBUTE     : void * ptrvalue; 
        ATTRIBUTE     : long  longval; 
C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_ValueStruct","_struct_ValueStruct",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_unsigned_long","_long",0},
    { "_struct_ValueStruct","_ValueStruct",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {

     // C++ CLASS START : struct ValueStruct
     ADD MEMBER     : dataType --> unsigned int  dataType; 
     ADD MEMBER     : bar --> double  bar; 
     ADD MEMBER     : u --> ValueStruct_u  u; 
     // C++ CLASS END 


     // C++ CLASS START : union ValueStruct_u
     ADD MEMBER     : intval --> int  intval; 
     ADD MEMBER     : doubleval --> double  doubleval; 
     ADD MEMBER     : charval --> char * charval; 
     ADD MEMBER     : ptrvalue --> void * ptrvalue; 
     ADD MEMBER     : longval --> long  longval; 
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
