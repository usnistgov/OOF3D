// This file tests the documentation system placing comments before a declaration

/* This is a title comment */
%title "Title",before

/* This is a comment before a function */
int foo(int);

// This is a 
// multiline comment
// appearing before
// a function
int bar(int);

/* This is a comment before section 1 */
%section "Section 1"

/* This is a comment before subsection 1.1 */
%subsection "Section 1.1"

/* This is a comment before subsection 1.2 */
%subsection "Section 1.2"

/* This is a comment before subsubsection 1.2.1 */
%subsubsection "Section 1.2.1"

/* This is a comment before subsection 1.3 */
%subsection "Section 1.3"

/* This is a comment before subsubsection 1.3.1 */
%subsubsection "Section 1.3.1"

/* This is a comment before section 2 */
%section "Section 2"

/* This comment should not appear */
%text %{
This is a some random text thrown in to the file.
%}

/* This is a comment for grok */
int grok(int);

/* This is a comment for section 3 */
%section "Section 3"
/* This comment should be ignored */

enum {
/* Comment for ENUM1 */	ENUM1, 
/* Comment for ENUM2 */	ENUM2,       
/* Comment for ENUM3 */	ENUM3,       
/* Comment for ENUM4 */	ENUM4 };     

int  /* This is a comment for 'a' */ a, 
/* This is a comment for 'b' */      b, 
/* This is a comment for 'c' */      c, 
/* This is a comment for 'd' */      d; 

/* This comment should be attached to the class definition */
class AClass {

public:
/* This is a comment for the foo member function */
  int foo();  
/* This is a comment for the a data member */
  int a;      
};


/* These are a bunch of comments that should be pruned */

/* Comment 1 */

/* Comment 2 */

/* Comment 3 */

/* Comment 4 */

/* Comment 5 */

/* Commment before section 4 */
%section "Section 4"

/* Comment 6 */

/* Comment 7 */

/* Comment 8 */

/* Comment 9 */

/* Comment before section 5 */
%section "Section 5"

/* Comment before function frob */
double frob(double);
