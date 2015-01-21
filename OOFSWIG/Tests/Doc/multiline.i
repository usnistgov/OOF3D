// This file tests some multiline comments

%section "Section 1",after

int foo();
// This is a 
// Multiline comment

double bar();
/* This is a multiline
   block comment */
/* This is another multiline
   block comment...should be ignored */

%section "Section 2",before

// This comment should be ignored

// This comment should be ignored

// This comment should be ignored

// This is a
// multiline comment
// before a declaration
int grok();

/* This is a multiline
   block comment before
   a declaration. (should be ignored) */
/* This is another multiline
   block comment before
   a declaration */
int frob(double);
