// This file tests the %enabledoc and %disabledoc directives

int ea;
/* Comment for 'a' */

int eb;
/* Comment for 'b' */

%disabledoc
int ec;
/* Should be no comment */

int ed;
/* Should be no comment */

%section "Section 1"

int ee;
/* Should be no comment */

%subsection "Section 1.1"
int ef;
/* Should no comment */

%subsubsection "Section 1.1.1"
int eg;
/* Should be no comment */

%enabledoc
%section "Section 2"

int eh;
/* Comment for h */

%subsection "Section 2.1"
int ei;
/* Comment for i */

%subsubsection "Section 2.1.1"
int ej;
/* Comment for j */

%disabledoc
%include after.i
%disabledoc

int ek;
/* Should be ignored */
%enabledoc
int el;
/* Should be ignored */
%enabledoc
int em;
/* Comment for m */

