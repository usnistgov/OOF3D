/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
C++ CLASS DECLARATION : class a
C++ CLASS DECLARATION : class b
C++ CLASS DECLARATION : class c
C++ CLASS DECLARATION : class d
C++ CLASS DECLARATION : class foo
C++ CLASS DECLARATION : class foo1
C++ CLASS DECLARATION : class foo2
C++ CLASS DECLARATION : class foo3
C++ CLASS DECLARATION : class foo4
C++ CLASS DECLARATION : class foo5
C++ CLASS DECLARATION : class foo6
C++ CLASS DECLARATION : class foo7
C++ CLASS DECLARATION : class foo8
C++ CLASS DECLARATION : class A
C++ CLASS DECLARATION : class B
C++ CLASS DECLARATION : class C
C++ CLASS DECLARATION : class D
C++ CLASS START : class a  ========================================

C++ CLASS END ===================================================

C++ CLASS START : class b  ========================================

C++ CLASS END ===================================================

C++ CLASS START : class c  ========================================

C++ CLASS END ===================================================

C++ CLASS START : class d  ========================================

C++ CLASS END ===================================================

C++ CLASS START : class foo  ========================================

inheriting from baseclass : a b c d
static void *SwigfooToa(void *ptr) {
    foo *src;
    a *dest;
    src = (foo *) ptr;
    dest = (a *) src;
    return (void *) dest;
}

static void *SwigfooTob(void *ptr) {
    foo *src;
    b *dest;
    src = (foo *) ptr;
    dest = (b *) src;
    return (void *) dest;
}

static void *SwigfooToc(void *ptr) {
    foo *src;
    c *dest;
    src = (foo *) ptr;
    dest = (c *) src;
    return (void *) dest;
}

static void *SwigfooTod(void *ptr) {
    foo *src;
    d *dest;
    src = (foo *) ptr;
    dest = (d *) src;
    return (void *) dest;
}

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo1  ========================================

inheriting from baseclass : a
static void *Swigfoo1Toa(void *ptr) {
    foo1 *src;
    a *dest;
    src = (foo1 *) ptr;
    dest = (a *) src;
    return (void *) dest;
}

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo2  ========================================

inheriting from baseclass : a
static void *Swigfoo2Toa(void *ptr) {
    foo2 *src;
    a *dest;
    src = (foo2 *) ptr;
    dest = (a *) src;
    return (void *) dest;
}

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo3  ========================================

inheriting from baseclass : a b c
static void *Swigfoo3Toa(void *ptr) {
    foo3 *src;
    a *dest;
    src = (foo3 *) ptr;
    dest = (a *) src;
    return (void *) dest;
}

static void *Swigfoo3Tob(void *ptr) {
    foo3 *src;
    b *dest;
    src = (foo3 *) ptr;
    dest = (b *) src;
    return (void *) dest;
}

static void *Swigfoo3Toc(void *ptr) {
    foo3 *src;
    c *dest;
    src = (foo3 *) ptr;
    dest = (c *) src;
    return (void *) dest;
}

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo4  ========================================

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo5  ========================================

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo6  ========================================

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo7  ========================================

        MEMBER FUNC   : double bar();

C++ CLASS END ===================================================

C++ CLASS START : class foo8  ========================================

inheriting from baseclass : a b c
static void *Swigfoo8Toa(void *ptr) {
    foo8 *src;
    a *dest;
    src = (foo8 *) ptr;
    dest = (a *) src;
    return (void *) dest;
}

static void *Swigfoo8Tob(void *ptr) {
    foo8 *src;
    b *dest;
    src = (foo8 *) ptr;
    dest = (b *) src;
    return (void *) dest;
}

static void *Swigfoo8Toc(void *ptr) {
    foo8 *src;
    c *dest;
    src = (foo8 *) ptr;
    dest = (c *) src;
    return (void *) dest;
}

C++ CLASS END ===================================================

C++ CLASS START : class A  ========================================

C++ CLASS END ===================================================

C++ CLASS START : class B  ========================================

inheriting from baseclass : A
static void *SwigBToA(void *ptr) {
    B *src;
    A *dest;
    src = (B *) ptr;
    dest = (A *) src;
    return (void *) dest;
}

C++ CLASS END ===================================================

C++ CLASS START : class C  ========================================

inheriting from baseclass : A
static void *SwigCToA(void *ptr) {
    C *src;
    A *dest;
    src = (C *) ptr;
    dest = (A *) src;
    return (void *) dest;
}

C++ CLASS END ===================================================

C++ CLASS START : class D  ========================================

inheriting from baseclass : B C
static void *SwigDToB(void *ptr) {
    D *src;
    B *dest;
    src = (D *) ptr;
    dest = (B *) src;
    return (void *) dest;
}

static void *SwigDToA(void *ptr) {
    D *src;
    A *dest;
    src = (D *) ptr;
    dest = (A *) src;
    return (void *) dest;
}

static void *SwigDToC(void *ptr) {
    D *src;
    C *dest;
    src = (D *) ptr;
    dest = (C *) src;
    return (void *) dest;
}

C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_a","_class_foo8",Swigfoo8Toa},
    { "_a","_foo8",Swigfoo8Toa},
    { "_a","_class_foo3",Swigfoo3Toa},
    { "_a","_foo3",Swigfoo3Toa},
    { "_a","_class_foo2",Swigfoo2Toa},
    { "_a","_foo2",Swigfoo2Toa},
    { "_a","_class_foo1",Swigfoo1Toa},
    { "_a","_foo1",Swigfoo1Toa},
    { "_a","_class_foo",SwigfooToa},
    { "_a","_foo",SwigfooToa},
    { "_a","_class_a",0},
    { "_foo2","_class_foo2",0},
    { "_signed_long","_long",0},
    { "_b","_class_foo8",Swigfoo8Tob},
    { "_b","_foo8",Swigfoo8Tob},
    { "_b","_class_foo3",Swigfoo3Tob},
    { "_b","_foo3",Swigfoo3Tob},
    { "_b","_class_foo",SwigfooTob},
    { "_b","_foo",SwigfooTob},
    { "_b","_class_b",0},
    { "_foo3","_class_foo3",0},
    { "_c","_class_foo8",Swigfoo8Toc},
    { "_c","_foo8",Swigfoo8Toc},
    { "_c","_class_foo3",Swigfoo3Toc},
    { "_c","_foo3",Swigfoo3Toc},
    { "_c","_class_foo",SwigfooToc},
    { "_c","_foo",SwigfooToc},
    { "_c","_class_c",0},
    { "_foo4","_class_foo4",0},
    { "_class_A","_class_D",SwigDToA},
    { "_class_A","_D",SwigDToA},
    { "_class_A","_class_C",SwigCToA},
    { "_class_A","_C",SwigCToA},
    { "_class_A","_class_B",SwigBToA},
    { "_class_A","_B",SwigBToA},
    { "_class_A","_A",0},
    { "_d","_class_foo",SwigfooTod},
    { "_d","_foo",SwigfooTod},
    { "_d","_class_d",0},
    { "_foo5","_class_foo5",0},
    { "_class_B","_class_D",SwigDToB},
    { "_class_B","_D",SwigDToB},
    { "_class_B","_B",0},
    { "_foo6","_class_foo6",0},
    { "_class_C","_class_D",SwigDToC},
    { "_class_C","_D",SwigDToC},
    { "_class_C","_C",0},
    { "_foo7","_class_foo7",0},
    { "_class_D","_D",0},
    { "_foo8","_class_foo8",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_class_foo1","_foo1",0},
    { "_class_a","_class_foo8",Swigfoo8Toa},
    { "_class_a","_foo8",Swigfoo8Toa},
    { "_class_a","_class_foo3",Swigfoo3Toa},
    { "_class_a","_foo3",Swigfoo3Toa},
    { "_class_a","_class_foo2",Swigfoo2Toa},
    { "_class_a","_foo2",Swigfoo2Toa},
    { "_class_a","_class_foo1",Swigfoo1Toa},
    { "_class_a","_foo1",Swigfoo1Toa},
    { "_class_a","_class_foo",SwigfooToa},
    { "_class_a","_foo",SwigfooToa},
    { "_class_a","_a",0},
    { "_class_foo2","_foo2",0},
    { "_class_b","_class_foo8",Swigfoo8Tob},
    { "_class_b","_foo8",Swigfoo8Tob},
    { "_class_b","_class_foo3",Swigfoo3Tob},
    { "_class_b","_foo3",Swigfoo3Tob},
    { "_class_b","_class_foo",SwigfooTob},
    { "_class_b","_foo",SwigfooTob},
    { "_class_b","_b",0},
    { "_class_foo3","_foo3",0},
    { "_class_c","_class_foo8",Swigfoo8Toc},
    { "_class_c","_foo8",Swigfoo8Toc},
    { "_class_c","_class_foo3",Swigfoo3Toc},
    { "_class_c","_foo3",Swigfoo3Toc},
    { "_class_c","_class_foo",SwigfooToc},
    { "_class_c","_foo",SwigfooToc},
    { "_class_c","_c",0},
    { "_class_foo4","_foo4",0},
    { "_class_d","_class_foo",SwigfooTod},
    { "_class_d","_foo",SwigfooTod},
    { "_class_d","_d",0},
    { "_class_foo5","_foo5",0},
    { "_class_foo6","_foo6",0},
    { "_class_foo7","_foo7",0},
    { "_class_foo8","_foo8",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_foo","_class_foo",0},
    { "_A","_class_D",SwigDToA},
    { "_A","_D",SwigDToA},
    { "_A","_class_C",SwigCToA},
    { "_A","_C",SwigCToA},
    { "_A","_class_B",SwigBToA},
    { "_A","_B",SwigBToA},
    { "_A","_class_A",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_B","_class_D",SwigDToB},
    { "_B","_D",SwigDToB},
    { "_B","_class_B",0},
    { "_C","_class_D",SwigDToC},
    { "_C","_D",SwigDToC},
    { "_C","_class_C",0},
    { "_D","_class_D",0},
    { "_class_foo","_foo",0},
    { "_foo1","_class_foo1",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {

     // C++ CLASS START : class a
     // C++ CLASS END 


     // C++ CLASS START : class b
     // C++ CLASS END 


     // C++ CLASS START : class c
     // C++ CLASS END 


     // C++ CLASS START : class d
     // C++ CLASS END 


     // C++ CLASS START : class foo
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo1
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo2
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo3
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo4
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo5
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo6
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo7
     ADD MEMBER FUN : bar --> double bar();
     // C++ CLASS END 


     // C++ CLASS START : class foo8
     // C++ CLASS END 


     // C++ CLASS START : class A
     // C++ CLASS END 


     // C++ CLASS START : class B
     // C++ CLASS END 


     // C++ CLASS START : class C
     // C++ CLASS END 


     // C++ CLASS START : class D
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
