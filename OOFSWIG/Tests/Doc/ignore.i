// This file tests SWIG's ability to ignore comments

%title "Ignore"
/* This file contains comments that should be ignored */

%section "Section 1",ignore

int a;
/* This comment is ignored */

int b;
/* This comment is ignored */

%section "Section 2"
/* Section 2 comment.  Not ignored */

int c;
/* This is comment for 'c' */

int d;
/* This is a comment for 'd' */

%section "Section 3",ignore
/* This comment is ignored */

int e;
/* This comment is ignored */

int f;
/* This comment is ignored */
