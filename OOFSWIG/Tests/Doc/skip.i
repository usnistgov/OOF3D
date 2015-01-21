// Tests the documentation systems 'skip' capability

%section "Comments following a declaration",after,skip=1

int a;

/* This comment should be ignored */

int b;

/* This comment should be ignored */

int c;
/* Comment for 'c' */

%section "Comments before a declaration",before,skip=1

/* This comment should be ignored */

int d;

/* This comment should be ignored */

int e;

/* This comment is for 'f' */
int f;

%section "Larger skip value",before,skip=2

/* Comment for 'g' */

int g;

/* Comment for 'h' */

int h;

/* This comment should be ignored */


int i;

/* This comment is for 'j' */
int j;

