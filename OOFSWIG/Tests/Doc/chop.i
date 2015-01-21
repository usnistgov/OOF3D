// This file tests the chopping of comments

%title "Chop"
/* This file tests chopping of comment blocks */

%localstyle before,chop_left=3,chop_top=1,chop_bottom=1,chop_right=3

/************************************************************
 * This is a block comment.                                 *
 *                                                          *
 * It should get chopped so that only text remains.         *
 ************************************************************/
int foobar(int);

/* This comment should not be chopped because it's too short */
int grok(double);


