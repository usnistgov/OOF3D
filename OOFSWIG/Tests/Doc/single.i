// This file tests comments on the same line as declarations. 
// They should be associated with the correct declaration
// regardless of mode

int        a;          /* A comment to the right */

/* A comment to the left */    int b;

/* A comment before */
int        c;         /* A comment to the right */

int        d;         /* A comment to the right */
/* A comment after */


