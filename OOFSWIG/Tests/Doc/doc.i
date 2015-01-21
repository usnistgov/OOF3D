// This file tests the SWIG documentation system

%title "Title"
/* This is the real title */

%module foo

%section "Section 1"
/* This is a test */

int fact(int n);
/* Compute a factorial */

double My_variable;
/* A variable declaration */

%section "Section 2"
/* This section contains some functions to do cool stuff.  This
   text should be attached directly below the section heading. */

%subsection "Functions"
/* Subsection comment */



double grok(double a);

%subsection "Variables"
Matrix *a_variable;

%subsubsection "System variables"
double  avar;
/* avar comment */


%section "Section 3"
/* This is a comment for section 3 */

FILE *fopen(char *, char *);
/* Open a file for reading or writing */

%text %{
This is just some random text thrown into a file.
%}

void fclose(FILE *file);


