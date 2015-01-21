// This file tests the documentation system placing comments after a declaration

%title "Title"
/* This is a title comment */

int foo(int);
/* This is a comment after a function */

int bar(int);
// This is a 
// multiline comment
// appearing after
// a function

%section "Section 1"
/* This is a comment after section 1 */

%subsection "Section 1.1"
/* This is a comment after subsection 1.1 */

%subsection "Section 1.2"
/* This is a comment after subsection 1.2 */

%subsubsection "Section 1.2.1"
/* This is a comment after subsubsection 1.2.1 */

%subsection "Section 1.3"
/* This is a comment after subsection 1.3 */

%subsubsection "Section 1.3.1"
/* This is a comment after subsubsection 1.3.1 */

%section "Section 2"
/* This is a comment after section 2 */

%text %{
This is a some random text thrown in to the file.
%}
/* This comment should not appear */

int grok(int);
/* This is a comment for grok */

/* This comment should be ignored */
%section "Section 3"
/* This is a comment for section 3 */

enum {
	ENUM1,       /* Comment for ENUM1 */
	ENUM2,       /* Comment for ENUM2 */
	ENUM3,       /* Comment for ENUM3 */
	ENUM4 };     /* Comment for ENUM4 */

int   a, /* This is a comment for 'a' */
      b, /* This is a comment for 'b' */
      c, /* This is a comment for 'c' */
      d; /* This is a comment for 'd' */

class AClass {
/* This comment should be attached to the class definition */
public:
  int foo();  /* This is a comment for the foo member function */
  int a;      /* This is a comment for the a data member */
};

double decl(int a,
	    double b,
	    double c,
            double d,
            double e,
            double f);
/* This is comment following a multiline declaration */

