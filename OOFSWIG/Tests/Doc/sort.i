// This file tests SWIG's sorting ability

%title "Sorted Documentation",sort
/* This file tests SWIG's documentation sorting */

%section "X Section"

int  f;
int  d;
double zip();

%section "C Section"

// Test case-insensitivity

int   before;
int   LATER;
int   A;
int   B;

%subsection "K subsection"

%subsection "D subsection"

%subsubsection "M subsubsection"

%subsubsection "G subsubsection"

%subsection "Y subsection"

%section "F Section"
/* Comment for F section */

%section "Not sorted",nosort
/* This section isn't sorted */

double nd;  /* Comment for nd */
double nc;  /* Comment for nc */
double nb;
double na;

%section "Q Section"
/* This section is should be sorted even though last one wasn't */

double qd,qc,qb,qa;

