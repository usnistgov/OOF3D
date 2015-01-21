/* A Bison parser, made by GNU Bison 3.0.2.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2013 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.0.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* Copy the first part of user declarations.  */
#line 1 "parser.y" /* yacc.c:339  */

/*******************************************************************************
 * Simplified Wrapper and Interface Generator  (SWIG)
 * 
 * Author : David Beazley
 *
 * Department of Computer Science        
 * University of Chicago
 * 1100 E 58th Street
 * Chicago, IL  60637
 * beazley@cs.uchicago.edu
 *
 * Please read the file LICENSE for the copyright and terms by which SWIG
 * can be used and distributed.
 *******************************************************************************/
/***********************************************************************
 * $Header: /users/langer/FE/CVSoof/OOF2/OOFSWIG/SWIG/parser.y,v 1.1.2.2 2014/06/27 20:28:32 langer Exp $
 *
 * parser.y
 *
 * YACC parser for parsing function declarations.
 *
 * *** DISCLAIMER ***
 *
 * This is the most ugly, incredibly henious, and completely unintelligible
 * file in SWIG.  While it started out simple, it has grown into a
 * monster that is almost unmaintainable.   A complete parser rewrite is
 * currently in progress that should make this file about 1/4 the size
 * that it is now.   Needless to say, don't modify this file or even look
 * at it for that matter!
 ***********************************************************************/

#define yylex yylex

extern "C" int yylex();
void   yyerror (const char *s);       
    
extern int  line_number;
extern int  start_line;
extern void skip_brace(void);
extern void skip_define(void);
extern void skip_decl(void);
extern int  skip_cond(int);
extern void skip_to_end(void);
extern void skip_template(void);
extern void scanner_check_typedef(void);
extern void scanner_ignore_typedef(void);
extern void scanner_clear_start(void);
extern void start_inline(char *, int);
extern void format_string(char *);
extern void swig_pragma(char *, char *);

#include "internal.h"

#ifdef NEED_ALLOC
void *alloca(unsigned n) {
  return((void *) malloc(n));
}
#else
// This redefinition is apparently needed on a number of machines,
// particularly HPUX
#undef  alloca
#define alloca  malloc
#endif

// Initialization flags.   These indicate whether or not certain
// features have been initialized.  These were added to allow
// interface files without the block (required in previous
// versions).

static int     module_init = 0;    /* Indicates whether the %module name was given */
static int     title_init = 0;     /* Indicates whether %title directive has been given */
static int     doc_init = 0;    

static int     lang_init = 0;      /* Indicates if the language has been initialized */

static int            i;
       int            Error = 0;
static char           temp_name[128];
static DataType      *temp_typeptr, temp_type;
static char           yy_rename[256];
static int            Rename_true = 0;
static DataType      *Active_type = 0;         // Used to support variable lists
static int            Active_extern = 0;       // Whether or not list is external
static int            Active_static = 0;
static DataType       *Active_typedef = 0;     // Used for typedef lists
static int            InArray = 0;             // Used when an array declaration is found 
static int            in_then = 0;
static int            in_else = 0;       
static int            allow = 1;               // Used during conditional compilation
static int            doc_scope = 0;           // Documentation scoping
static String         ArrayString;             // Array type attached to parameter names
static String         ArrayBackup;             // Array backup string
static char           *DefArg = 0;             // Default argument hack
static char           *ConstChar = 0;          // Used to store raw character constants
static ParmList       *tm_parm = 0;            // Parameter list used to hold typemap parameters
static Hash            name_hash;              // Hash table containing renamings
       char           *objc_construct = (char*)"new"; // Objective-C constructor
       char           *objc_destruct = (char*)"free"; // Objective-C destructor

/* Some macros for building constants */

#define E_BINARY(TARGET, SRC1, SRC2, OP)  \
        TARGET = new char[strlen(SRC1) + strlen(SRC2) +strlen(OP)+1];\
	sprintf(TARGET,"%s%s%s",SRC1,OP,SRC2);

/* C++ modes */

#define  CPLUS_PUBLIC    1
#define  CPLUS_PRIVATE   2
#define  CPLUS_PROTECTED 3

int     cplus_mode;

// Declarations of some functions for handling C++ 

extern void cplus_open_class(const char *name, char *rname,const char *ctype);
extern void cplus_member_func(char *, char *, DataType *, ParmList *, int);
extern void cplus_constructor(char *, char *, ParmList *);
extern void cplus_destructor(char *, char *);
extern void cplus_variable(char *, char *, DataType *);
extern void cplus_static_func(char *, char *, DataType *, ParmList *);
extern void cplus_declare_const(const char *,const char *, DataType *,const char *);
extern void cplus_class_close(char *);
extern void cplus_inherit(int, char **);
extern void cplus_cleanup(void);
extern void cplus_static_var(char *, char *, DataType *);
extern void cplus_register_type(char *);
extern void cplus_register_scope(Hash *);
extern void cplus_inherit_scope(int, char **);
extern void cplus_add_pragma(char *, char *, char *);
extern DocEntry *cplus_set_class(char *);
extern void cplus_unset_class();
extern void cplus_abort();
  
// ----------------------------------------------------------------------
// static init_language()
//
// Initialize the target language.
// Does nothing if this function has already been called.
// ----------------------------------------------------------------------

static void init_language() {
  if (!lang_init) {
    lang->initialize();
    
    // Initialize the documentation system

    if (!doctitle) {
      doctitle = new DocTitle(title,0);
    }
    if (!doc_init)
      doctitle->usage = title;

    doc_stack[0] = doctitle;
    doc_stack_top = 0;
    
    int oldignore = IgnoreDoc;
    IgnoreDoc = 1;
    if (ConfigFile) {
      include_file(ConfigFile);
    }
    IgnoreDoc = oldignore;
  }
  lang_init = 1;
  title_init = 1;
}

// ----------------------------------------------------------------------
// int promote(int t1, int t2)
//
// Promote types (for constant expressions)
// ----------------------------------------------------------------------

int promote(int t1, int t2) {

  if ((t1 == T_ERROR) || (t2 == T_ERROR)) return T_ERROR;
  if ((t1 == T_DOUBLE) || (t2 == T_DOUBLE)) return T_DOUBLE;
  if ((t1 == T_FLOAT) || (t2 == T_FLOAT)) return T_FLOAT;
  if ((t1 == T_ULONG) || (t2 == T_ULONG)) return T_ULONG;
  if ((t1 == T_LONG) || (t2 == T_LONG)) return T_LONG;
  if ((t1 == T_UINT) || (t2 == T_UINT)) return T_UINT;
  if ((t1 == T_INT) || (t2 == T_INT)) return T_INT;
  if ((t1 == T_USHORT) || (t2 == T_USHORT)) return T_SHORT;
  if ((t1 == T_SHORT) || (t2 == T_SHORT)) return T_SHORT;
  if ((t1 == T_UCHAR) || (t2 == T_UCHAR)) return T_UCHAR;
  if (t1 != t2) {
    fprintf(stderr,"%s : Line %d. Type mismatch in constant expression\n",
	    input_file, line_number);
    FatalError();
  }
  return t1;
}

/* Generate the scripting name of an object.  Takes %name directive into 
   account among other things */

static char *make_name(char *name) {
  // Check to see if the name is in the hash
  char *nn = (char *) name_hash.lookup(name);
  if (nn) return nn;        // Yep, return it.

  if (Rename_true) {
    Rename_true = 0;
    return yy_rename;
  } else {
    // Now check to see if the name contains a $
    if (strchr(name,'$')) {
      static String temp;
      temp = "";
      temp << name;
      temp.replace("$","_S_");
      return temp;
    } else {
      return name;
    }
  }
}

/* Return the parent of a documentation entry.   If wrapping externally, this is 0 */

static DocEntry *doc_parent() {
  if (!WrapExtern) 
    return doc_stack[doc_stack_top];
  else
    return 0;
}

// ----------------------------------------------------------------------
// create_function(int ext, char *name, DataType *t, ParmList *l)
//
// Creates a function and manages documentation creation.  Really
// only used internally to the parser.
// ----------------------------------------------------------------------

void create_function(int ext, char *name, DataType *t, ParmList *l) {
  if (Active_static) return;     // Static declaration. Ignore

  init_language();
  if (WrapExtern) return;        // External wrapper file. Ignore

  char *iname = make_name(name);

  // Check if symbol already exists

  if (add_symbol(iname, t, (char *) 0)) {
    fprintf(stderr,"%s : Line %d. Function %s multiply defined (2nd definition ignored).\n",
	    input_file, line_number, iname);
  } else {
    Stat_func++;
    if (Verbose) {
      fprintf(stderr,"Wrapping function : ");
      emit_extern_func(name, t, l, 0, stderr);
    }

    // If extern, make an extern declaration in the SWIG wrapper file

    if (ext) 
      emit_extern_func(name, t, l, ext, f_header);
    else if (ForceExtern) {
      emit_extern_func(name, t, l, 1, f_header);
    }

    // If this function has been declared inline, produce a function

    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
    lang->create_function(name, iname, t, l);
    l->check_defined();
    t->check_defined();
  }
  scanner_clear_start();
}

// -------------------------------------------------------------------
// create_variable(int ext, char *name, DataType *t)
//
// Create a link to a global variable.
// -------------------------------------------------------------------

void create_variable(int ext, char *name, DataType *t) {

  if (WrapExtern) return;        // External wrapper file. Ignore
  int oldstatus = Status;

  if (Active_static) return;  // If static ignore
				   
  init_language();

  char *iname = make_name(name);
  if (add_symbol(iname, t, (char *) 0)) {
    fprintf(stderr,"%s : Line %d. Variable %s multiply defined (2nd definition ignored).\n",
	    input_file, line_number, iname);
  } else {
    Stat_var++;
    if (Verbose) {
      fprintf(stderr,"Wrapping variable : ");
      emit_extern_var(name, t, 0, stderr);
    }

    // If externed, output an external declaration

    if (ext) 
      emit_extern_var(name, t, ext, f_header);
    else if (ForceExtern) {
      emit_extern_var(name, t, 1, f_header);
    }

    // If variable datatype is read-only, we'll force it to be readonly
    if (t->status & STAT_READONLY) Status = Status | STAT_READONLY;

    // Now dump it out
    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
    lang->link_variable(name, iname, t);
    t->check_defined();
    Status = oldstatus;
  }
  scanner_clear_start();
}

// ------------------------------------------------------------------
// create_constant(char *name, DataType *type, char *value)
//
// Creates a new constant.
// -------------------------------------------------------------------

void create_constant(char *name, DataType *type, char *value) {

  if (Active_static) return;
  if (WrapExtern) return;        // External wrapper file. Ignore
  init_language();

  if (Rename_true) {
    fprintf(stderr,"%s : Line %d. %%name directive ignored with #define\n",
	    input_file, line_number);
    Rename_true = 0;
  }

  if ((type->type == T_CHAR) && (!type->is_pointer))
    type->is_pointer++;
  
  if (!value) value = copy_string(name);
  sprintf(temp_name,"const:%s", name);
  if (add_symbol(temp_name, type, value)) {
    fprintf(stderr,"%s : Line %d. Constant %s multiply defined. (2nd definition ignored)\n",
	    input_file, line_number, name);
  } else {
    // Update symbols value if already defined.
    update_symbol(name, type, value);

    if (!WrapExtern) {    // Only wrap the constant if not in %extern mode
      Stat_const++;
      if (Verbose) 
	fprintf(stderr,"Creating constant %s = %s\n", name, value);

      doc_entry = new DocDecl(name,doc_stack[doc_stack_top]);	   
      lang->declare_const(name, name, type, value);
      type->check_defined();
    }
  }
  scanner_clear_start();
}


/* Print out array brackets */
void print_array() {
  int i;
  for (i = 0; i < InArray; i++)
    fprintf(stderr,"[]");
}

/* manipulate small stack for managing if-then-else */

static int then_data[100];
static int else_data[100];
static int allow_data[100];
static int te_index = 0;
static int prev_allow = 1;

void if_push() {
  then_data[te_index] = in_then;
  else_data[te_index] = in_else;
  allow_data[te_index] = allow;
  prev_allow = allow;
  te_index++;
  if (te_index >= 100) {
    fprintf(stderr,"SWIG.  Internal parser error. if-then-else stack overflow.\n");
    SWIG_exit(1);
  }
}

void if_pop() {
  if (te_index > 0) {
    te_index--;
    in_then = then_data[te_index];
    in_else = else_data[te_index];
    allow = allow_data[te_index];
    if (te_index > 0) {
      prev_allow = allow_data[te_index-1];
    } else {
      prev_allow = 1;
    }
  }
}

// Structures for handling code fragments built for nested classes

struct Nested {
  String   code;         // Associated code fragment
  int      line;         // line number where it starts
  char     *name;        // Name associated with this nested class
  DataType *type;        // Datatype associated with the name
  Nested   *next;        // Next code fragment in list
};

// Some internal variables for saving nested class information

static Nested      *nested_list = 0;

// Add a function to the nested list

static void add_nested(Nested *n) {
  Nested *n1;
  if (!nested_list) nested_list = n;
  else {
    n1 = nested_list;
    while (n1->next) n1 = n1->next;
    n1->next = n;
  }
}

// Dump all of the nested class declarations to the inline processor
// However.  We need to do a few name replacements and other munging
// first.  This function must be called before closing a class!

static void dump_nested(char *parent) {
  Nested *n,*n1;
  n = nested_list;
  int oldstatus = Status;

  Status = STAT_READONLY;
  while (n) {
    // Token replace the name of the parent class
    n->code.replace("$classname",parent);

    // Fix up the name of the datatype (for building typedefs and other stuff)
    sprintf(n->type->name,"%s_%s",parent,n->name);
    
    // Add the appropriate declaration to the C++ processor
    doc_entry = new DocDecl(n->name,doc_stack[doc_stack_top]);
    cplus_variable(n->name,(char *) 0, n->type);

    // Dump the code to the scanner
    if (Verbose)
      fprintf(stderr,"Splitting from %s : (line %d) \n%s\n", parent,n->line, n->code.get());

    fprintf(f_header,"\n%s\n", n->code.get());
    start_inline(n->code.get(),n->line);

    n1 = n->next;
    delete n;
    n = n1;
  }
  nested_list = 0;
  Status = oldstatus;
}    


#line 534 "y.tab.c" /* yacc.c:339  */

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* In a future release of Bison, this section will be replaced
   by #include "y.tab.h".  */
#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    ID = 258,
    HBLOCK = 259,
    WRAPPER = 260,
    POUND = 261,
    STRING = 262,
    NUM_INT = 263,
    NUM_FLOAT = 264,
    CHARCONST = 265,
    NUM_UNSIGNED = 266,
    NUM_LONG = 267,
    NUM_ULONG = 268,
    TYPEDEF = 269,
    TYPE_INT = 270,
    TYPE_UNSIGNED = 271,
    TYPE_SHORT = 272,
    TYPE_LONG = 273,
    TYPE_FLOAT = 274,
    TYPE_DOUBLE = 275,
    TYPE_CHAR = 276,
    TYPE_VOID = 277,
    TYPE_SIGNED = 278,
    TYPE_BOOL = 279,
    TYPE_TYPEDEF = 280,
    LPAREN = 281,
    RPAREN = 282,
    COMMA = 283,
    SEMI = 284,
    EXTERN = 285,
    INIT = 286,
    LBRACE = 287,
    RBRACE = 288,
    DEFINE = 289,
    PERIOD = 290,
    CONST = 291,
    STRUCT = 292,
    UNION = 293,
    EQUAL = 294,
    SIZEOF = 295,
    MODULE = 296,
    LBRACKET = 297,
    RBRACKET = 298,
    WEXTERN = 299,
    ILLEGAL = 300,
    READONLY = 301,
    READWRITE = 302,
    NAME = 303,
    RENAME = 304,
    INCLUDE = 305,
    CHECKOUT = 306,
    ADDMETHODS = 307,
    PRAGMA = 308,
    CVALUE = 309,
    COUT = 310,
    ENUM = 311,
    ENDDEF = 312,
    MACRO = 313,
    CLASS = 314,
    PRIVATE = 315,
    PUBLIC = 316,
    PROTECTED = 317,
    COLON = 318,
    STATIC = 319,
    VIRTUAL = 320,
    FRIEND = 321,
    OPERATOR = 322,
    THROW = 323,
    TEMPLATE = 324,
    NATIVE = 325,
    INLINE = 326,
    IFDEF = 327,
    IFNDEF = 328,
    ENDIF = 329,
    ELSE = 330,
    UNDEF = 331,
    IF = 332,
    DEFINED = 333,
    ELIF = 334,
    RAW_MODE = 335,
    ALPHA_MODE = 336,
    TEXT = 337,
    DOC_DISABLE = 338,
    DOC_ENABLE = 339,
    STYLE = 340,
    LOCALSTYLE = 341,
    TYPEMAP = 342,
    EXCEPT = 343,
    IMPORT = 344,
    ECHO = 345,
    NEW = 346,
    APPLY = 347,
    CLEAR = 348,
    DOCONLY = 349,
    TITLE = 350,
    SECTION = 351,
    SUBSECTION = 352,
    SUBSUBSECTION = 353,
    LESSTHAN = 354,
    GREATERTHAN = 355,
    USERDIRECTIVE = 356,
    OC_INTERFACE = 357,
    OC_END = 358,
    OC_PUBLIC = 359,
    OC_PRIVATE = 360,
    OC_PROTECTED = 361,
    OC_CLASS = 362,
    OC_IMPLEMENT = 363,
    OC_PROTOCOL = 364,
    OR = 365,
    XOR = 366,
    AND = 367,
    LSHIFT = 368,
    RSHIFT = 369,
    PLUS = 370,
    MINUS = 371,
    STAR = 372,
    SLASH = 373,
    UMINUS = 374,
    NOT = 375,
    LNOT = 376,
    DCOLON = 377
  };
#endif
/* Tokens.  */
#define ID 258
#define HBLOCK 259
#define WRAPPER 260
#define POUND 261
#define STRING 262
#define NUM_INT 263
#define NUM_FLOAT 264
#define CHARCONST 265
#define NUM_UNSIGNED 266
#define NUM_LONG 267
#define NUM_ULONG 268
#define TYPEDEF 269
#define TYPE_INT 270
#define TYPE_UNSIGNED 271
#define TYPE_SHORT 272
#define TYPE_LONG 273
#define TYPE_FLOAT 274
#define TYPE_DOUBLE 275
#define TYPE_CHAR 276
#define TYPE_VOID 277
#define TYPE_SIGNED 278
#define TYPE_BOOL 279
#define TYPE_TYPEDEF 280
#define LPAREN 281
#define RPAREN 282
#define COMMA 283
#define SEMI 284
#define EXTERN 285
#define INIT 286
#define LBRACE 287
#define RBRACE 288
#define DEFINE 289
#define PERIOD 290
#define CONST 291
#define STRUCT 292
#define UNION 293
#define EQUAL 294
#define SIZEOF 295
#define MODULE 296
#define LBRACKET 297
#define RBRACKET 298
#define WEXTERN 299
#define ILLEGAL 300
#define READONLY 301
#define READWRITE 302
#define NAME 303
#define RENAME 304
#define INCLUDE 305
#define CHECKOUT 306
#define ADDMETHODS 307
#define PRAGMA 308
#define CVALUE 309
#define COUT 310
#define ENUM 311
#define ENDDEF 312
#define MACRO 313
#define CLASS 314
#define PRIVATE 315
#define PUBLIC 316
#define PROTECTED 317
#define COLON 318
#define STATIC 319
#define VIRTUAL 320
#define FRIEND 321
#define OPERATOR 322
#define THROW 323
#define TEMPLATE 324
#define NATIVE 325
#define INLINE 326
#define IFDEF 327
#define IFNDEF 328
#define ENDIF 329
#define ELSE 330
#define UNDEF 331
#define IF 332
#define DEFINED 333
#define ELIF 334
#define RAW_MODE 335
#define ALPHA_MODE 336
#define TEXT 337
#define DOC_DISABLE 338
#define DOC_ENABLE 339
#define STYLE 340
#define LOCALSTYLE 341
#define TYPEMAP 342
#define EXCEPT 343
#define IMPORT 344
#define ECHO 345
#define NEW 346
#define APPLY 347
#define CLEAR 348
#define DOCONLY 349
#define TITLE 350
#define SECTION 351
#define SUBSECTION 352
#define SUBSUBSECTION 353
#define LESSTHAN 354
#define GREATERTHAN 355
#define USERDIRECTIVE 356
#define OC_INTERFACE 357
#define OC_END 358
#define OC_PUBLIC 359
#define OC_PRIVATE 360
#define OC_PROTECTED 361
#define OC_CLASS 362
#define OC_IMPLEMENT 363
#define OC_PROTOCOL 364
#define OR 365
#define XOR 366
#define AND 367
#define LSHIFT 368
#define RSHIFT 369
#define PLUS 370
#define MINUS 371
#define STAR 372
#define SLASH 373
#define UMINUS 374
#define NOT 375
#define LNOT 376
#define DCOLON 377

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE YYSTYPE;
union YYSTYPE
{
#line 475 "parser.y" /* yacc.c:355  */
         
  char        *id;
  struct Declaration {
    char *id;
    int   is_pointer;
    int   is_reference;
  } decl;
  struct InitList {
    char **names;
    int    count;
  } ilist;
  struct DocList {
    char **names;
    char **values;
    int  count;
  } dlist;
  struct Define {
    char *id;
    int   type;
  } dtype;
  DataType     *type;
  Parm         *p;
  TMParm       *tmparm;
  ParmList     *pl;
  int           ivalue;

#line 845 "y.tab.c" /* yacc.c:355  */
};
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */

/* Copy the second part of user declarations.  */

#line 860 "y.tab.c" /* yacc.c:358  */

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

#if !defined _Noreturn \
     && (!defined __STDC_VERSION__ || __STDC_VERSION__ < 201112)
# if defined _MSC_VER && 1200 <= _MSC_VER
#  define _Noreturn __declspec (noreturn)
# else
#  define _Noreturn YY_ATTRIBUTE ((__noreturn__))
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  3
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   2151

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  123
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  136
/* YYNRULES -- Number of rules.  */
#define YYNRULES  428
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  907

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   377

#define YYTRANSLATE(YYX)                                                \
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, without out-of-bounds checking.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   120,   121,   122
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   559,   559,   559,   582,   586,   590,   601,   618,   636,
     646,   657,   657,   688,   696,   696,   708,   717,   717,   733,
     746,   746,   759,   774,   797,   797,   812,   819,   825,   833,
     842,   842,   850,   850,   862,   874,   895,   943,   973,  1009,
    1046,  1054,  1062,  1066,  1075,  1079,  1090,  1100,  1109,  1119,
    1125,  1132,  1138,  1160,  1176,  1195,  1202,  1208,  1208,  1223,
    1223,  1223,  1243,  1256,  1275,  1287,  1305,  1320,  1341,  1352,
    1369,  1376,  1383,  1388,  1394,  1395,  1396,  1397,  1415,  1416,
    1420,  1424,  1440,  1453,  1459,  1473,  1492,  1492,  1508,  1530,
    1554,  1554,  1583,  1595,  1606,  1626,  1652,  1675,  1694,  1704,
    1730,  1759,  1768,  1775,  1781,  1789,  1793,  1801,  1802,  1802,
    1829,  1829,  1842,  1845,  1848,  1856,  1857,  1858,  1870,  1879,
    1885,  1888,  1893,  1896,  1901,  1916,  1942,  1961,  1973,  1984,
    1994,  2003,  2008,  2014,  2021,  2022,  2028,  2032,  2034,  2037,
    2038,  2041,  2044,  2051,  2055,  2060,  2070,  2071,  2075,  2079,
    2086,  2089,  2097,  2100,  2103,  2106,  2109,  2112,  2115,  2118,
    2121,  2125,  2129,  2140,  2155,  2160,  2165,  2174,  2180,  2190,
    2193,  2196,  2199,  2202,  2205,  2208,  2211,  2214,  2218,  2222,
    2226,  2231,  2240,  2243,  2249,  2255,  2261,  2271,  2274,  2280,
    2286,  2292,  2300,  2301,  2304,  2304,  2310,  2317,  2329,  2335,
    2345,  2346,  2352,  2353,  2357,  2362,  2362,  2369,  2370,  2373,
    2385,  2396,  2400,  2404,  2408,  2412,  2416,  2421,  2426,  2438,
    2445,  2451,  2457,  2464,  2471,  2482,  2494,  2506,  2518,  2530,
    2537,  2547,  2558,  2559,  2565,  2565,  2633,  2667,  2633,  2734,
    2757,  2734,  2798,  2809,  2830,  2850,  2858,  2866,  2866,  2884,
    2885,  2886,  2889,  2890,  2892,  2890,  2895,  2895,  2906,  2909,
    2933,  2956,  2977,  2997,  3017,  3017,  3070,  3101,  3101,  3124,
    3144,  3155,  3166,  3177,  3185,  3185,  3192,  3192,  3210,  3215,
    3221,  3229,  3235,  3240,  3244,  3249,  3252,  3275,  3275,  3301,
    3301,  3326,  3333,  3338,  3343,  3348,  3349,  3352,  3353,  3356,
    3357,  3358,  3361,  3362,  3362,  3387,  3387,  3415,  3418,  3421,
    3422,  3423,  3426,  3427,  3430,  3445,  3461,  3476,  3492,  3493,
    3496,  3499,  3505,  3518,  3527,  3532,  3537,  3546,  3555,  3566,
    3567,  3568,  3572,  3573,  3574,  3577,  3578,  3579,  3584,  3587,
    3590,  3591,  3594,  3595,  3598,  3599,  3602,  3603,  3611,  3611,
    3644,  3644,  3660,  3661,  3662,  3677,  3678,  3682,  3688,  3693,
    3694,  3694,  3697,  3697,  3700,  3700,  3703,  3703,  3717,  3720,
    3727,  3749,  3771,  3771,  3776,  3796,  3818,  3821,  3822,  3822,
    3827,  3827,  3831,  3831,  3845,  3848,  3868,  3889,  3890,  3893,
    3896,  3900,  3908,  3912,  3920,  3926,  3931,  3932,  3943,  3953,
    3960,  3967,  3970,  3973,  3983,  3986,  3991,  3997,  4001,  4004,
    4017,  4031,  4044,  4059,  4063,  4063,  4072,  4072,  4082,  4088,
    4091,  4096,  4097,  4103,  4104,  4107,  4108,  4109,  4141
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 0
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "ID", "HBLOCK", "WRAPPER", "POUND",
  "STRING", "NUM_INT", "NUM_FLOAT", "CHARCONST", "NUM_UNSIGNED",
  "NUM_LONG", "NUM_ULONG", "TYPEDEF", "TYPE_INT", "TYPE_UNSIGNED",
  "TYPE_SHORT", "TYPE_LONG", "TYPE_FLOAT", "TYPE_DOUBLE", "TYPE_CHAR",
  "TYPE_VOID", "TYPE_SIGNED", "TYPE_BOOL", "TYPE_TYPEDEF", "LPAREN",
  "RPAREN", "COMMA", "SEMI", "EXTERN", "INIT", "LBRACE", "RBRACE",
  "DEFINE", "PERIOD", "CONST", "STRUCT", "UNION", "EQUAL", "SIZEOF",
  "MODULE", "LBRACKET", "RBRACKET", "WEXTERN", "ILLEGAL", "READONLY",
  "READWRITE", "NAME", "RENAME", "INCLUDE", "CHECKOUT", "ADDMETHODS",
  "PRAGMA", "CVALUE", "COUT", "ENUM", "ENDDEF", "MACRO", "CLASS",
  "PRIVATE", "PUBLIC", "PROTECTED", "COLON", "STATIC", "VIRTUAL", "FRIEND",
  "OPERATOR", "THROW", "TEMPLATE", "NATIVE", "INLINE", "IFDEF", "IFNDEF",
  "ENDIF", "ELSE", "UNDEF", "IF", "DEFINED", "ELIF", "RAW_MODE",
  "ALPHA_MODE", "TEXT", "DOC_DISABLE", "DOC_ENABLE", "STYLE", "LOCALSTYLE",
  "TYPEMAP", "EXCEPT", "IMPORT", "ECHO", "NEW", "APPLY", "CLEAR",
  "DOCONLY", "TITLE", "SECTION", "SUBSECTION", "SUBSUBSECTION", "LESSTHAN",
  "GREATERTHAN", "USERDIRECTIVE", "OC_INTERFACE", "OC_END", "OC_PUBLIC",
  "OC_PRIVATE", "OC_PROTECTED", "OC_CLASS", "OC_IMPLEMENT", "OC_PROTOCOL",
  "OR", "XOR", "AND", "LSHIFT", "RSHIFT", "PLUS", "MINUS", "STAR", "SLASH",
  "UMINUS", "NOT", "LNOT", "DCOLON", "$accept", "program", "$@1",
  "command", "statement", "$@2", "$@3", "$@4", "$@5", "$@6", "$@7", "$@8",
  "$@9", "$@10", "$@11", "doc_enable", "typedef_decl", "$@12", "$@13",
  "typedeflist", "cond_compile", "cpp_const_expr", "pragma", "stail",
  "$@14", "$@15", "definetail", "extern", "func_end", "parms", "ptail",
  "parm", "parm_type", "pname", "def_args", "parm_specifier",
  "parm_specifier_list", "declaration", "stars", "array", "array2", "type",
  "strict_type", "opt_signed", "opt_unsigned", "opt_int", "definetype",
  "$@16", "initlist", "ename", "enumlist", "edecl", "$@17", "etype",
  "expr", "cpp", "cpp_class", "$@18", "$@19", "$@20", "$@21", "$@22",
  "cpp_other", "$@23", "added_members", "cpp_members", "$@24", "$@25",
  "$@26", "cpp_member", "$@27", "$@28", "$@29", "$@30", "cpp_pragma",
  "$@31", "$@32", "nested_decl", "type_extra", "cpp_tail", "$@33", "$@34",
  "cpp_end", "cpp_vend", "cpp_enumlist", "cpp_edecl", "inherit",
  "base_list", "base_specifier", "access_specifier", "cpptype",
  "cpp_const", "ctor_end", "ctor_initializer", "mem_initializer_list",
  "mem_initializer", "expr_list", "objective_c", "$@35", "$@36",
  "objc_inherit", "objc_protolist", "objc_data", "$@37", "$@38", "$@39",
  "$@40", "objc_vars", "objc_var", "$@41", "objc_vartail", "objc_methods",
  "$@42", "$@43", "$@44", "objc_method", "objc_end", "objc_ret_type",
  "objc_arg_type", "objc_args", "objc_separator", "stylelist", "styletail",
  "stylearg", "tm_method", "tm_list", "tm_tail", "typemap_parm",
  "typemap_name", "$@45", "$@46", "typemap_args", "idstring",
  "user_directive", "uservalue", "empty", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371,   372,   373,   374,
     375,   376,   377
};
# endif

#define YYPACT_NINF -796

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-796)))

#define YYTABLE_NINF -429

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
    -796,    70,  -796,  -796,   967,  -796,  -796,  -796,   166,  -796,
    1847,  -796,   201,   177,    86,   209,   356,  -796,  -796,   197,
     267,   356,   356,   274,    53,  1871,  -796,   294,  1732,   332,
     354,  -796,  -796,   391,    20,    20,  -796,  -796,   392,  -796,
    -796,   418,   418,   406,   423,   356,   400,  -796,  1895,  1895,
    -796,   451,   462,   477,   486,   198,   447,   504,  -796,  -796,
    -796,  -796,  -796,  -796,  -796,  1686,  -796,  -796,  -796,  -796,
    -796,  -796,  -796,   -39,  -796,   426,   507,   507,  -796,  -796,
    -796,  -796,   485,  -796,   430,  1895,  -796,  -796,   536,  -796,
     549,    31,   212,   516,  -796,  -796,  1973,  -796,  -796,  -796,
    -796,  -796,   282,   553,  -796,  -796,   532,   529,   568,   551,
     426,   507,   507,   559,   560,   563,   565,   485,   567,   430,
    1895,   576,    55,   569,   593,   600,  -796,    55,   609,  -796,
    -796,  -796,   192,    20,  -796,  -796,  -796,   529,  -796,  -796,
     153,   610,  -796,  -796,  -796,  -796,  -796,  1210,   194,   575,
     585,   587,  -796,  -796,  -796,  -796,   589,   590,  1662,   583,
    -796,     1,  -796,     3,   536,   617,   508,   596,   620,    55,
     602,   626,  -796,   627,  -796,  -796,  -796,   507,   507,  -796,
    -796,  -796,  -796,  -796,  -796,  -796,  -796,   507,   507,  -796,
    -796,  -796,  -796,  -796,   603,   605,  -796,  -796,  -796,   515,
     594,   195,    21,  -796,  -796,   611,  -796,   584,  -796,  -796,
    -796,  -796,   586,  1833,   611,   615,  -796,   631,  -796,   506,
    -796,  -796,   500,   636,   640,   641,   642,   646,   647,  -796,
      46,   558,   650,   651,   653,  -796,  -796,   678,  -796,  -796,
     655,  -796,   663,   667,  -796,   339,   885,   842,   322,   322,
    -796,  -796,  -796,  -796,  1895,  -796,  1895,  -796,  -796,   668,
    -796,   668,   668,   668,  -796,  -796,   664,  -796,  -796,   673,
     674,  -796,  -796,  1662,   255,  -796,  -796,   698,   701,  -796,
    -796,   505,   675,  -796,  -796,  -796,  1662,  -796,     0,   588,
     237,  -796,  -796,  -796,  -796,  -796,  -796,    48,   681,  -796,
     595,   279,   679,  -796,  1320,  1100,   710,  -796,  -796,   606,
    -796,  -796,  -796,  -796,  -796,  2031,   699,  1833,  1833,   835,
    -796,   205,  -796,  1451,  -796,  -796,   724,   728,  1662,  -796,
       5,  -796,  -796,   702,  1662,   708,   668,   154,  1895,   442,
    1662,  -796,  -796,   718,   322,   594,   819,  -796,  -796,   720,
     715,   587,   747,   716,   273,  1662,  -796,  -796,  -796,  -796,
     312,   508,    48,  -796,    48,  -796,  -796,   726,   430,   722,
    -796,  -796,  -796,   729,  1662,    36,     5,  -796,  -796,   723,
     573,   730,    55,  -796,  -796,   681,    48,  -796,  -796,  -796,
    -796,   309,   732,  -796,    42,  -796,  -796,    41,  1895,  -796,
    -796,  -796,   735,   733,   319,   536,   695,   703,   705,  1895,
    1756,  -796,  -796,   759,  -796,  -796,  -796,    66,   738,   736,
    1320,  -796,   235,  -796,  -796,  -796,   768,  -796,   426,   507,
     507,  -796,  -796,  -796,  -796,   485,  -796,   430,  1895,   748,
     779,   771,  1895,  -796,  -796,  1833,  1833,  1833,  1833,  1833,
    1833,  1833,  1833,  1833,   375,   769,  1895,  -796,   751,   751,
     745,  1320,   125,  -796,   529,   529,   752,    30,   772,  -796,
    -796,  1919,   755,  -796,  -796,   758,   385,  -796,  -796,   720,
    -796,   760,  -796,   594,  -796,  -796,  -796,   529,  -796,  -796,
     674,  -796,  -796,    48,  -796,  -796,   430,  -796,  1397,   573,
      23,   761,   449,  -796,  -796,  -796,   750,   573,   397,  -796,
    -796,   764,   369,  -796,   765,  -796,   788,   279,  -796,   791,
    1320,  1320,  1617,   792,  -796,   529,   795,   767,  -796,  -796,
    -796,    55,   797,    55,  1540,   775,   617,   275,   376,   737,
    -796,   685,    55,  -796,   483,  -796,  -796,  -796,  -796,  -796,
    -796,  -796,  -796,  1833,  -796,  -796,   778,   604,   625,   540,
     443,   443,   429,   429,  -796,  -796,   276,  -796,    55,   804,
    1895,   807,  -796,   809,  -796,  -796,  -796,   789,   782,  -796,
     435,  -796,  -796,   790,    23,  -796,   813,  -796,  -796,   541,
       2,    55,    23,  1895,  -796,  -796,  1895,  -796,   794,  -796,
    -796,  -796,   798,  -796,  -796,   800,  -796,  -796,  -796,    55,
     785,  1397,   793,  -796,   420,  -796,   801,  -796,  -796,    23,
    1662,  -796,   541,  1320,  -796,  -796,   573,   821,  1662,  -796,
    -796,   803,  -796,  -796,  -796,   799,  -796,  -796,   808,   810,
    1320,  -796,   811,  -796,   814,   815,   817,  -796,  1662,  1662,
    -796,     5,  -796,  -796,  -796,  -796,  -796,  -796,    55,  -796,
    -796,   776,   725,   377,    14,  -796,  -796,   435,   841,  -796,
    -796,  -796,  -796,   820,  -796,    55,  -796,  -796,  -796,   830,
    -796,   820,   441,   828,  1662,   833,   438,  1397,   843,  1397,
    1397,  1397,   594,   438,  -796,    55,   831,  -796,   832,  1662,
     541,  -796,   820,   836,  -796,   834,   379,  -796,  -796,   839,
    1662,    55,    23,  -796,   837,   866,   527,  1662,   545,   844,
    1662,   845,   847,   545,  -796,   681,    55,   846,  -796,   849,
     210,  -796,   210,  -796,   850,   125,  -796,   541,   359,  1662,
    -796,  -796,  1895,  -796,   851,  1662,   777,  -796,   852,  -796,
    -796,  -796,  -796,   780,   395,  -796,  -796,   859,  -796,   541,
     858,  -796,  -796,  -796,   835,   681,   869,   886,  -796,   853,
    -796,  -796,   529,   873,   888,   527,   433,  -796,  -796,   890,
      55,  -796,  -796,    23,   892,    23,    23,  -796,  -796,  -796,
     895,  -796,  -796,  -796,   862,  -796,  -796,  -796,  -796,   889,
    -796,  -796,   893,  -796,  1662,     5,   900,   909,  -796,   915,
    -796,  -796,  -796,   793,  -796,  -796,  -796,  -796,  -796,  -796,
     914,   681,   951,   450,  -796,  1320,  -796,   379,   952,  -796,
     527,   927,    23,   312,  -796,   492,    23,  -796,  -796,  -796,
    -796,  1662,   954,  -796,   435,  -796,   932,  -796,   931,  -796,
    -796,  1801,  -796,  -796,  -796,   935,   936,  -796,  -796,  -796,
    -796,  -796,   938,  -796,  -796,  -796,  -796,     5,  -796,  -796,
    -796,   472,   939,  -796,  -796,    23,   541,  -796,  -796,   554,
     951,   960,   545,  -796,  -796,  -796,   533,  -796,  -796,  -796,
    -796,   835,   556,  -796,   930,  -796,   545,   945,   541,  -796,
    1833,   379,  -796,  -796,  -796,   835,  -796
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint16 yydefact[] =
{
       2,     0,   428,     1,     0,     5,    77,    45,     0,    10,
       0,    74,   115,     0,     0,     0,     0,    26,    27,     0,
       0,     0,     0,     0,     0,     0,   246,     0,     0,     0,
       0,    98,    97,     0,     0,     0,    41,    40,     0,    84,
      85,     0,     0,     0,     0,     0,     0,    30,     0,     0,
      51,     0,     0,     0,     0,     0,     0,     0,   352,   353,
       4,    42,    44,    79,    80,     0,    75,   232,   233,    76,
      83,   116,    46,   428,   152,   428,   428,   428,   157,   158,
     155,   159,   428,   156,   428,     0,   333,   334,   428,   332,
       0,     0,     0,   117,   428,    47,     0,    55,   428,   421,
     422,     7,     0,     0,     6,     9,     0,   428,     0,   152,
     428,   428,   428,   157,   158,   155,   159,   428,   156,   428,
       0,     0,     0,     0,     0,     0,    48,     0,     0,    95,
      96,    56,     0,     0,    99,   100,    43,   428,    81,    82,
       0,     0,    73,    71,     8,    49,    50,     0,   428,     0,
       0,   428,   428,   428,   428,   428,     0,     0,   428,     0,
     424,   428,   428,   428,   428,     0,   428,     0,     0,     0,
       0,     0,   357,     0,   163,   358,   188,   428,   428,   191,
     161,   187,   192,   153,   193,   154,   183,   428,   428,   186,
     160,   182,   162,   164,   168,     0,   201,   167,   143,     0,
      86,     0,   165,   239,   428,    52,   199,     0,   196,   197,
     113,    54,     0,     0,    53,     0,    32,     0,   247,     0,
     105,   403,     0,   161,   153,   154,   160,   162,   164,   168,
     428,     0,   165,     0,     0,   165,   102,     0,   103,   428,
     404,   405,     0,     0,    31,   428,   428,     0,   428,   428,
     416,   409,   418,   420,     0,    69,     0,   406,   408,    36,
     400,    37,    38,    39,   425,   426,     0,   139,   140,     0,
     428,   123,   142,     0,   428,   120,   427,     0,     0,   348,
     428,     0,     0,   145,   147,   146,   428,   144,   428,     0,
     165,   166,   189,   190,   184,   185,    59,   428,   428,    90,
       0,     0,     0,   321,     0,     0,     0,   114,   112,   218,
     211,   212,   213,   214,   215,     0,     0,     0,     0,   195,
      28,   428,    29,   428,   402,   401,     0,     0,   428,   150,
     428,   151,    16,   428,   428,     0,   398,     0,     0,     0,
     428,   414,   413,     0,   428,   428,     0,   411,   410,   428,
       0,   428,     0,     0,     0,     0,   119,   122,   124,   141,
     428,     0,   428,   125,   428,   132,   133,     0,   428,     0,
     356,   354,    57,     0,   428,     0,   428,    13,   242,     0,
     428,     0,     0,    87,    94,   428,   428,   324,   330,   329,
     331,     0,   320,   322,     0,   236,   256,   428,     0,   296,
     278,   279,     0,     0,     0,   428,     0,     0,     0,     0,
       0,   280,   274,     0,   295,   283,   282,   428,     0,     0,
       0,   284,     0,   258,    78,   198,     0,   169,   428,   428,
     428,   174,   175,   172,   176,   428,   173,   428,     0,     0,
       0,     0,     0,   229,   230,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,   115,     0,    33,   428,   428,
       0,     0,     0,   251,   428,   428,     0,   194,     0,    14,
     138,     0,     0,   101,   404,     0,     0,    72,    70,   428,
     419,     0,   148,   428,   417,    68,   407,   428,   129,   423,
     428,   130,   131,   428,   127,   126,   428,   355,     0,   428,
     428,     0,     0,   245,    11,   234,   204,   428,     0,   203,
     208,     0,   428,    91,     0,   325,     0,     0,   327,     0,
       0,     0,   428,     0,   253,   428,     0,     0,   271,   270,
     272,     0,     0,     0,     0,     0,   300,   428,   299,     0,
     301,     0,     0,   252,   165,   289,   219,   178,   170,   171,
     177,   179,   180,     0,   231,   181,     0,   225,   226,   224,
     227,   228,   220,   221,   222,   223,     0,   117,     0,     0,
       0,     0,   391,     0,   248,   249,   382,     0,     0,   250,
       0,   384,   106,     0,   428,   136,     0,   134,   137,     0,
     428,     0,   428,     0,    65,    63,     0,   415,     0,   149,
     399,   121,     0,   350,   366,     0,   360,   362,   364,     0,
       0,     0,   428,   368,     0,   335,     0,    20,   337,   428,
     428,   244,     0,     0,   205,   207,   428,     0,   428,    92,
      93,     0,   326,   323,   328,     0,   257,   294,     0,     0,
       0,   285,     0,   276,   267,     0,     0,   275,   428,   428,
     264,   428,   292,   281,   293,   240,   291,   287,     0,   217,
     216,   428,     0,   165,     0,   428,   428,     0,     0,   378,
     377,   104,    22,    24,   135,     0,   107,    15,    34,     0,
      23,     0,     0,     0,   428,     0,     0,     0,     0,     0,
       0,     0,   370,     0,   359,     0,     0,   376,     0,   428,
       0,    19,    17,     0,    12,     0,     0,   202,    60,     0,
     428,     0,   428,   273,     0,     0,   428,   428,     0,     0,
     428,     0,     0,     0,   266,   428,   428,     0,   389,     0,
       0,   395,     0,   383,     0,     0,   118,     0,   428,   428,
      64,    62,     0,    67,     0,   428,     0,   367,     0,   361,
     363,   365,   371,     0,   428,   369,    58,     0,    21,     0,
       0,   235,   210,   206,   209,   428,     0,     0,   237,   428,
     261,   254,   428,   314,     0,   428,     0,   313,   319,     0,
       0,   302,   268,   428,     0,   428,   428,   265,   241,   297,
       0,   298,   290,   390,     0,   387,   388,   396,   386,   428,
     385,   380,     0,    25,   428,   428,     0,     0,   412,     0,
     351,   372,   349,   428,   374,   336,    18,   243,    61,    88,
       0,   428,     0,     0,   341,     0,   286,     0,     0,   318,
     428,     0,   428,   428,   263,     0,   428,   262,   259,   288,
     397,     0,     0,   393,     0,   379,     0,   108,     0,    66,
     128,     0,   375,    89,   238,     0,   340,   342,   338,   339,
     255,   315,     0,   312,   277,   269,   303,   428,   307,   308,
     260,     0,     0,   394,   381,   428,     0,    35,   373,     0,
       0,     0,     0,   305,   309,   311,   194,   392,   110,   109,
     345,   346,     0,   343,   316,   304,     0,     0,     0,   344,
       0,     0,   306,   310,   111,   347,   317
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -796,  -796,  -796,   796,   829,  -796,  -796,  -796,  -796,  -796,
    -796,  -796,  -796,  -796,  -796,    19,    24,  -796,  -796,  -379,
      18,   -10,  -796,  -605,  -796,  -796,  -796,  -255,  -554,  -112,
     490,  -352,   721,  -248,  -341,   739,  -796,   138,   -67,   -61,
    -284,   288,   -11,  -108,   -98,    16,  -457,  -796,   -43,  -144,
     494,  -489,  -796,  -795,  -197,   688,  -796,  -796,  -796,  -796,
    -796,  -796,  -796,  -796,  -796,  -409,  -796,  -796,  -796,  -308,
    -796,  -796,  -796,  -796,  -796,  -796,  -796,  -796,  -796,  -690,
    -796,  -796,  -738,  -796,  -796,  -662,  -283,  -796,   478,   608,
      11,  -437,  -796,  -796,  -796,   126,  -796,  -796,  -796,  -796,
    -796,   -76,  -400,  -796,  -796,  -796,  -796,  -796,   159,  -796,
    -677,  -476,  -796,  -796,  -796,   704,   289,   566,  -796,   358,
    -796,   980,    79,  -132,   691,  -241,   682,   -47,  -119,  -796,
    -796,  -215,   355,  -796,   680,    -2
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     1,     2,     4,    60,   622,   589,   759,   700,   737,
     147,   321,   499,   380,   765,   414,   415,   298,   385,   383,
     416,   134,    64,   677,   876,   898,   211,    65,   672,   343,
     356,   270,   271,   363,   469,   272,   273,   167,   168,   365,
     330,   274,   418,   190,   180,   183,   212,   213,   205,   195,
     508,   509,   706,   763,   764,    66,    67,   623,   520,   821,
     304,   725,    68,   323,   460,   419,   640,   825,   521,   420,
     723,   718,   534,   716,   421,   726,   658,   790,   539,   782,
     882,   896,   834,   870,   776,   777,   302,   392,   393,   394,
     128,   835,   770,   823,   856,   857,   892,    69,   369,   686,
     279,   174,   610,   689,   690,   691,   687,   611,   612,   851,
     696,   579,   735,   844,   667,   580,   798,   571,   842,   730,
     799,   138,   259,   220,   242,   150,   257,   151,   251,   479,
     349,   252,   101,    70,   160,   275
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
       5,   149,    71,   490,   376,   239,   513,   379,   192,   226,
     587,   543,   223,   350,   123,   461,   319,   704,   625,   491,
     282,    92,    63,    61,   201,   135,   374,   277,    62,  -143,
     342,   678,   861,   787,   198,   504,   124,   208,   680,   502,
     209,   728,   247,   227,   467,   518,   269,   837,   838,   381,
     346,   360,   575,  -428,   170,   214,   107,   199,   198,   615,
     172,   482,   585,   617,   278,   701,   456,   522,   468,   198,
       3,   175,   328,   181,   184,   184,   171,   814,   471,   108,
     191,   249,   175,   173,   301,   280,   196,   250,   247,    96,
     247,   616,   206,   185,   865,   758,   206,   476,   132,   284,
     172,   172,   172,   503,   670,   221,   906,   519,   181,   184,
     184,   635,   636,   829,   494,   191,   495,   175,   440,   281,
     443,   444,   375,   238,   173,   173,   576,   224,   225,   347,
     348,   166,   803,   629,   484,   221,   852,   707,   514,   299,
     172,   133,   586,   165,    97,    71,   253,   673,   166,   258,
     260,   260,   260,   260,   816,   681,   240,   474,  -428,   175,
     206,   175,   196,   173,   285,    63,    61,   165,   863,   329,
      72,    62,   166,   577,   373,   184,   184,   578,   536,   344,
      94,    95,   702,   166,   341,   184,   184,   250,   250,   241,
     241,   733,   895,   292,   293,   236,   650,   245,   287,   599,
     303,   156,     5,   294,   295,   157,   902,   364,    93,   351,
     746,   694,    98,   794,   705,   202,   466,   753,   237,   454,
     246,   300,   472,   102,   158,   481,   647,   329,   331,   200,
     159,   714,   261,   262,   263,   455,   247,   260,   544,   795,
     458,   459,   796,   253,   203,   602,   253,   253,   557,   558,
     559,   560,   561,   562,   563,   564,   565,    23,   360,   802,
     230,   527,   501,  -181,   597,   234,   378,   545,   357,  -428,
     103,   889,   366,   797,    26,   769,   156,   106,   370,   661,
     157,   361,   387,   250,   329,   215,   331,   747,   303,   749,
     750,   751,   497,   904,   493,   366,   384,   247,    91,   492,
     301,   649,   423,    71,   439,   159,   248,   288,   203,   216,
     724,   166,   515,   122,   467,   422,   127,   247,   336,    71,
     125,   463,   525,    63,    61,   245,   441,   550,   470,    62,
     547,    71,   582,   583,   422,   129,   148,   148,   468,   388,
     389,   390,   253,   331,   391,   526,   788,   253,   340,   258,
     538,   467,   682,   169,   247,   600,   659,   130,   470,    99,
     366,   551,   366,   100,   247,   340,   175,   362,   874,   388,
     389,   390,   166,   193,   470,   468,   104,   105,   510,   287,
     379,   247,   309,   384,   366,   804,   818,   310,   311,   762,
     312,   313,   314,   641,   131,   175,   136,   382,   507,   871,
     144,   247,   652,   196,   145,   315,   378,   146,   228,  -428,
     638,   247,    86,    87,   594,   540,   860,   595,   423,   316,
     603,   137,   329,   695,   596,   626,   181,   184,   184,   897,
     627,   422,   140,   191,    89,   175,   576,   247,   888,   576,
     301,   176,   854,   177,   178,   548,   549,   179,   626,   141,
     161,   630,   142,   698,   805,   143,   572,   572,   152,   423,
     581,   830,   221,   221,   847,   566,   831,   569,  -428,   153,
     740,   477,   422,   741,   478,   620,   651,   253,   621,   858,
     742,   331,   859,   577,   154,   221,   577,   578,   357,   872,
     578,   366,   866,   155,   175,   317,   613,   510,   618,   318,
     186,   884,   187,   188,   885,   510,   189,   162,   703,  -181,
     384,   886,   656,   324,   325,   657,   709,   507,   423,   423,
     512,   868,   182,   221,   869,   507,   883,   326,   327,   172,
     773,   422,   422,   306,   371,   470,   721,   722,  -428,   194,
     208,  -428,   148,   209,   148,   422,   452,   453,   204,   683,
     458,   459,   197,   458,   459,   537,   217,   309,   450,   451,
     452,   453,   310,   311,   218,   312,   313,   314,   219,   675,
     676,   222,   744,   780,   781,   774,   506,  -169,   581,   229,
     315,   890,   618,   899,   900,  -174,  -175,   757,   175,  -172,
     618,  -176,   417,  -173,   316,   231,   232,   729,   767,    29,
      30,    31,    32,   233,    34,   779,    35,   254,   784,   613,
     697,   417,   235,   243,   255,   256,   276,   618,   264,   265,
     283,   423,   286,   287,   510,   166,   148,   806,   289,   290,
     291,   752,   297,   809,   422,  -200,   247,   296,   423,   306,
     826,   307,   320,   308,   507,    29,    30,    31,    32,   470,
      34,   422,    35,   448,   449,   450,   451,   452,   453,   303,
     322,   303,  -178,   731,   731,   581,  -170,  -171,  -177,   644,
     317,   646,  -179,  -180,   318,   332,  -181,   329,   333,   334,
     655,   335,   891,   337,   581,   613,    91,   613,   613,   613,
     338,   581,   846,   813,   339,   807,   352,   531,   533,   353,
     354,   367,   355,   905,   368,   377,   662,   372,   417,   382,
     618,   395,   386,   425,   778,   446,   447,   448,   449,   450,
     451,   452,   453,   384,   791,   442,   552,   464,   426,   679,
     556,   465,   455,   581,   775,   473,   331,   447,   448,   449,
     450,   451,   452,   453,   568,   480,   340,   692,   485,   417,
     487,   488,   697,   496,   498,   505,   500,   511,   528,   591,
     517,   523,   535,   384,   541,   524,   529,   824,   530,   542,
     221,   546,   867,   778,   555,   553,   567,   570,   574,   584,
     588,   618,   592,   618,   618,   593,   609,   598,   619,   624,
     628,   632,   631,   775,   634,   639,   727,   843,   642,   643,
     645,   648,   654,   470,   653,   660,   554,   663,   417,   417,
     665,   697,   666,   738,   669,   668,   674,   671,   693,   384,
     684,   695,   417,   423,   708,   685,   688,   699,   778,   710,
     618,   470,   711,   754,   618,   712,   422,   713,   715,   301,
     717,   719,   581,   720,   734,   309,   748,   375,   775,   768,
     310,   311,   736,   312,   313,   314,   739,   743,   664,   745,
     755,   756,   483,   760,   789,   470,   766,   761,   315,   772,
     771,   783,   785,   618,   786,   792,   793,   801,   808,   811,
     810,   148,   316,   812,   148,   345,   815,   817,    73,   445,
     446,   447,   448,   449,   450,   451,   452,   453,   819,   609,
      74,    75,    76,    77,    78,    79,    80,    81,    82,    83,
      84,   417,   827,   820,   828,   841,   822,   832,   833,   836,
     266,    85,    86,    87,   839,   840,   845,   848,   417,   445,
     446,   447,   448,   449,   450,   451,   452,   453,   849,   267,
     268,   121,   850,   853,    89,   445,   446,   447,   448,   449,
     450,   451,   452,   453,   855,   862,   864,   873,   317,   875,
     877,   879,   318,   894,   880,   881,   887,    -3,     6,   901,
    -428,     7,     8,     9,   903,   609,   244,   609,   609,   609,
     601,    10,  -428,  -428,  -428,  -428,  -428,  -428,  -428,  -428,
    -428,  -428,  -428,   614,   358,   633,    11,    12,    13,   516,
     305,    14,   166,  -428,  -428,  -428,   893,    90,    15,   457,
     878,    16,   359,    17,    18,    19,    20,    21,    22,    23,
      24,   800,   139,  -428,   732,   573,  -428,   462,   475,     0,
     148,    25,     0,   486,   489,     0,    26,    27,    28,    29,
      30,    31,    32,    33,    34,     0,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    47,    48,
      49,    50,    51,    52,    53,    54,     0,     0,    55,    56,
       0,     0,     0,     0,    57,    58,    59,     0,     0,  -428,
       0,     0,     0,     0,  -428,     0,     0,     0,     0,  -428,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     6,     0,  -428,     7,     8,     9,     0,     0,     0,
       0,     0,     0,   417,    10,  -428,  -428,  -428,  -428,  -428,
    -428,  -428,  -428,  -428,  -428,  -428,     0,     0,     0,    11,
      12,    13,     0,   424,    14,     0,  -428,  -428,  -428,   609,
       0,    15,     0,     0,    16,     0,    17,    18,    19,    20,
      21,    22,    23,    24,     0,     0,  -428,     0,     0,  -428,
       0,     0,     0,     0,    25,     0,     0,     0,     0,    26,
      27,    28,    29,    30,    31,    32,    33,    34,     0,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    44,    45,
      46,    47,    48,    49,    50,    51,    52,    53,    54,     0,
       0,    55,    56,     0,     0,     0,     0,    57,    58,    59,
       0,     6,  -428,  -428,     7,     8,     9,  -428,     0,     0,
       0,     0,  -428,     0,    10,  -428,  -428,  -428,  -428,  -428,
    -428,  -428,  -428,  -428,  -428,  -428,     0,     0,     0,    11,
      12,    13,     0,     0,    14,     0,  -428,  -428,  -428,     0,
       0,    15,     0,     0,    16,     0,    17,    18,    19,    20,
      21,    22,    23,    24,     0,     0,  -428,     0,     0,  -428,
       0,     0,     0,     0,    25,     0,     0,     0,     0,    26,
      27,    28,    29,    30,    31,    32,    33,    34,     0,    35,
      36,    37,    38,    39,    40,    41,    42,    43,    44,    45,
      46,    47,    48,    49,    50,    51,    52,    53,    54,     0,
       0,    55,    56,     0,     0,     0,     0,    57,    58,    59,
       0,   396,  -428,   397,     0,     0,     0,  -428,     0,     0,
       0,     0,  -428,     0,   398,   109,   110,   111,   112,   113,
     114,   115,   116,   117,   118,   119,     0,     0,     0,   399,
       0,     0,     0,  -428,     0,     0,   120,    86,    87,     0,
       0,     0,     0,     0,     0,     0,   400,   401,   402,     0,
       0,     0,   403,   404,     0,     0,   405,     0,     0,    89,
     406,   407,   408,     0,   409,   410,   411,     0,     0,     0,
       0,     0,    29,    30,    31,    32,     0,    34,   604,    35,
      73,     0,     0,    39,    40,     0,     0,     0,     0,     0,
       0,   412,    74,    75,    76,    77,    78,    79,    80,    81,
      82,    83,    84,     0,     0,     0,     0,     0,     0,     0,
    -428,     0,     0,    85,    86,    87,     0,     0,     0,     0,
     413,     0,    90,     0,     0,   605,     0,     0,     0,     0,
       0,     0,     0,   121,   397,     0,    89,     0,     0,     0,
       0,     0,     0,     0,     0,   398,   109,   110,   111,   112,
     113,   114,   115,   116,   117,   118,   119,     0,     0,     0,
     399,     0,     0,     0,     0,     0,     0,   120,    86,    87,
       0,     0,     0,     0,     0,     0,     0,   400,   401,   402,
       0,   606,   607,   608,   404,     0,     0,   405,     0,     0,
      89,   406,   407,   408,     0,   409,   410,   411,     0,    90,
       0,     0,     0,    29,    30,    31,    32,     0,    34,     0,
      35,     0,     0,     0,    39,    40,     0,     0,     0,     0,
       0,     0,   412,   397,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,   398,   109,   110,   111,   112,   113,
     114,   115,   116,   117,   118,   119,   458,   459,     0,   399,
       0,   413,     0,    90,     0,     0,   120,    86,    87,     0,
       0,     0,     0,     0,     0,     0,   400,   401,   402,     0,
       0,     0,     0,   404,     0,     0,   405,     0,     0,    89,
     406,   407,   408,     0,   409,   410,   411,     0,     0,     0,
       0,     0,    29,    30,    31,    32,     0,    34,     0,    35,
      73,     0,     0,    39,    40,     0,     0,     0,     0,     0,
       0,   412,    74,    75,    76,    77,    78,    79,    80,    81,
      82,    83,    84,     0,     0,     0,     0,     0,     0,     0,
       0,     0,   266,    85,    86,    87,     0,     0,     0,     0,
     413,     0,    90,     0,     0,    73,     0,     0,     0,     0,
       0,   267,   268,   121,     0,     0,    89,    74,    75,    76,
      77,    78,    79,    80,    81,    82,    83,    84,     0,   163,
       0,     0,     0,     0,     0,     0,     0,   266,    85,    86,
      87,   109,   110,   111,   112,   113,   114,   115,   116,   117,
     118,   119,     0,     0,     0,     0,   267,   268,   121,     0,
       0,    89,   120,    86,    87,     0,     0,     0,     0,     0,
       0,     0,     0,     0,   637,    73,   126,     0,     0,    90,
       0,     0,   164,     0,     0,    89,     0,    74,    75,    76,
      77,    78,    79,    80,    81,    82,    83,    84,     0,    73,
       0,     0,     0,     0,     0,     0,     0,     0,    85,    86,
      87,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,     0,     0,    90,     0,     0,     0,   121,     0,
       0,    89,    85,    86,    87,     0,     0,     0,   165,     0,
       0,     0,     0,   166,    73,     0,     0,     0,    90,     0,
       0,     0,   121,     0,     0,    89,    74,    75,    76,    77,
      78,    79,    80,    81,    82,    83,    84,     0,     0,     0,
       0,     0,     0,     0,     0,     0,   309,    85,    86,    87,
       0,   310,   311,     0,   312,   313,   314,     0,     0,   605,
      73,     0,     0,     0,    90,     0,     0,   121,     0,   315,
      89,     0,    74,    75,    76,    77,    78,    79,    80,    81,
      82,    83,    84,   316,    73,     0,   532,     0,    90,     0,
       0,     0,     0,    85,    86,    87,   109,   110,   111,   112,
     113,   114,   115,   116,   117,   118,   119,     0,    73,     0,
       0,     0,     0,    88,     0,     0,    89,   120,    86,    87,
      74,    75,    76,    77,    78,    79,    80,    81,    82,    83,
      84,     0,   590,    90,     0,     0,     0,   121,     0,     0,
      89,    85,    86,    87,    74,    75,    76,    77,    78,    79,
      80,    81,    82,    83,    84,     0,     0,     0,     0,   317,
       0,   121,     0,   318,    89,    85,    86,    87,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,    90,
       0,     0,     0,     0,   207,   121,  -194,     0,    89,     0,
     208,  -194,  -194,   209,  -194,  -194,  -194,     0,     0,     0,
       0,     0,     0,    90,     0,     0,     0,     0,     0,  -194,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,  -194,     0,     0,     0,    90,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     210,     0,     0,     0,   309,     0,     0,     0,     0,   310,
     311,    90,   312,   313,   314,     0,   427,   428,   429,   430,
     431,   432,   433,   434,   435,   436,   437,   315,     0,     0,
       0,     0,     0,     0,     0,     0,     0,   438,    86,    87,
       0,   316,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,  -194,
      89,     0,     0,  -194,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,   317,     0,     0,
       0,   318
};

static const yytype_int16 yycheck[] =
{
       2,    48,     4,   355,   288,   137,   385,   290,    84,   117,
     467,   420,   110,   254,    25,   323,   213,   622,   507,   360,
     164,    10,     4,     4,    91,    35,    26,    26,     4,    26,
     245,    29,   827,   723,     3,   376,    25,     7,   592,     3,
      10,    27,    42,   119,    39,     3,   158,   785,   786,   297,
     247,     3,   461,    32,    65,    98,     3,    26,     3,    36,
      99,   345,    32,   500,    63,   619,   321,    26,    63,     3,
       0,    73,    26,    75,    76,    77,    65,   754,   333,    26,
      82,   148,    84,   122,    63,   161,    88,   148,    42,     3,
      42,    68,    94,    77,   832,   700,    98,   338,    78,   166,
      99,    99,    99,    67,   580,   107,   901,    65,   110,   111,
     112,   520,   521,   775,   362,   117,   364,   119,   315,   162,
     317,   318,   122,   133,   122,   122,     1,   111,   112,   248,
     249,   117,   737,   512,   349,   137,   813,   626,   386,   200,
      99,   121,   112,   112,    58,   147,   148,   584,   117,   151,
     152,   153,   154,   155,   759,   592,     3,     3,    33,   161,
     162,   163,   164,   122,   166,   147,   147,   112,   830,   230,
       4,   147,   117,    48,   286,   177,   178,    52,   112,   246,
       3,     4,   619,   117,   245,   187,   188,   248,   249,    36,
      36,   667,   882,   177,   178,     3,   537,     3,     3,   483,
     202,     3,   204,   187,   188,     7,   896,   274,     7,   256,
     686,   611,     3,     3,   623,     3,   328,   693,    26,    14,
      26,    26,   334,    26,    26,   344,   534,   288,   230,    91,
      32,   640,   153,   154,   155,    30,    42,   239,     3,    29,
     115,   116,    32,   245,    32,   493,   248,   249,   445,   446,
     447,   448,   449,   450,   451,   452,   453,    52,     3,   735,
     122,   405,   374,    26,   479,   127,    29,    32,   270,    32,
       3,   876,   274,    63,    69,   712,     3,     3,   280,     3,
       7,    26,     3,   344,   345,     3,   288,   687,   290,   689,
     690,   691,   368,   898,   361,   297,   298,    42,    10,   360,
      63,    26,   304,   305,   315,    32,   112,   169,    32,    27,
     651,   117,     3,    25,    39,   304,    28,    42,   239,   321,
      26,   323,     3,   305,   305,     3,   315,   435,   330,   305,
     428,   333,   464,   465,   323,     3,    48,    49,    63,    60,
      61,    62,   344,   345,    65,    26,   725,   349,    26,   351,
     417,    39,   593,    65,    42,   487,   553,     3,   360,     3,
     362,   437,   364,     7,    42,    26,   368,   112,   844,    60,
      61,    62,   117,    85,   376,    63,    21,    22,   380,     3,
     663,    42,     3,   385,   386,    26,   765,     8,     9,    10,
      11,    12,    13,   525,     3,   397,     4,    28,   380,   836,
      45,    42,    26,   405,     4,    26,    29,     7,   120,    32,
     522,    42,    37,    38,    29,   417,   825,    32,   420,    40,
     496,     3,   483,    28,    39,    28,   428,   429,   430,   886,
      33,   420,    26,   435,    59,   437,     1,    42,   875,     1,
      63,    15,   821,    17,    18,   429,   430,    21,    28,    26,
       3,   512,    29,    33,   738,    32,   458,   459,     7,   461,
     462,    28,   464,   465,   805,   454,    33,   456,    33,     7,
      29,    29,   461,    32,    32,    26,   537,   479,    29,    29,
      39,   483,    32,    48,     7,   487,    48,    52,   490,   841,
      52,   493,   833,     7,   496,   116,   498,   499,   500,   120,
      15,    29,    17,    18,    32,   507,    21,     3,   620,    26,
     512,    39,    29,     7,     8,    32,   628,   499,   520,   521,
     382,    29,    15,   525,    32,   507,   867,    27,    28,    99,
       3,   520,   521,    28,    29,   537,   648,   649,   103,     3,
       7,   103,   254,    10,   256,   534,   117,   118,    32,   596,
     115,   116,     3,   115,   116,   417,     3,     3,   115,   116,
     117,   118,     8,     9,    32,    11,    12,    13,    39,    28,
      29,     3,   684,    28,    29,    48,     3,    26,   580,     3,
      26,    27,   584,    27,    28,    26,    26,   699,   590,    26,
     592,    26,   304,    26,    40,    26,     3,   664,   710,    72,
      73,    74,    75,     3,    77,   717,    79,    32,   720,   611,
     612,   323,     3,     3,    29,    28,    33,   619,    29,    29,
       3,   623,    26,     3,   626,   117,   338,   739,    26,     3,
       3,   692,   117,   745,   623,    32,    42,    32,   640,    28,
     772,    57,    27,    57,   626,    72,    73,    74,    75,   651,
      77,   640,    79,   113,   114,   115,   116,   117,   118,   661,
      29,   663,    26,   665,   666,   667,    26,    26,    26,   531,
     116,   533,    26,    26,   120,   117,    26,   738,    27,    26,
     542,     3,   879,    28,   686,   687,   398,   689,   690,   691,
      27,   693,   804,   754,    27,   742,    28,   409,   410,    35,
      27,     3,    28,   900,     3,   117,   568,    32,   420,    28,
     712,    32,   117,     3,   716,   111,   112,   113,   114,   115,
     116,   117,   118,   725,   726,    26,   438,     3,   122,   591,
     442,     3,    30,   735,   716,    27,   738,   112,   113,   114,
     115,   116,   117,   118,   456,    27,    26,   609,    33,   461,
       3,    35,   754,    27,    32,    32,    27,    27,    63,   471,
      28,    26,     3,   765,    26,    32,    63,   769,    63,    33,
     772,     3,   833,   775,     3,    27,     7,    26,    33,    27,
       8,   783,    27,   785,   786,    27,   498,    27,    27,    39,
      26,     3,    27,   775,     3,     3,   658,   799,     3,    32,
       3,    26,   117,   805,    67,    27,    27,     3,   520,   521,
       3,   813,     3,   675,    32,    26,     3,    27,    33,   821,
      26,    28,   534,   825,     3,    27,    26,    26,   830,    26,
     832,   833,    33,   695,   836,    27,   825,    27,    27,    63,
      26,    26,   844,    26,     3,     3,     3,   122,   830,   711,
       8,     9,    32,    11,    12,    13,    26,    29,   570,    26,
      29,    29,    43,    27,   726,   867,    27,    33,    26,     3,
      33,    27,    27,   875,    27,    29,    27,    27,    27,    27,
     103,   593,    40,   103,   596,    43,    27,    29,     3,   110,
     111,   112,   113,   114,   115,   116,   117,   118,    29,   611,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,   623,    39,    27,    26,    26,    63,    27,   780,    27,
      35,    36,    37,    38,    29,    63,    33,    27,   640,   110,
     111,   112,   113,   114,   115,   116,   117,   118,    29,    54,
      55,    56,    27,    29,    59,   110,   111,   112,   113,   114,
     115,   116,   117,   118,     3,     3,    29,     3,   116,    27,
      29,    26,   120,     3,    28,    27,    27,     0,     1,    39,
       3,     4,     5,     6,    29,   687,   147,   689,   690,   691,
     490,    14,    15,    16,    17,    18,    19,    20,    21,    22,
      23,    24,    25,   499,   273,   517,    29,    30,    31,   391,
     204,    34,   117,    36,    37,    38,   880,   122,    41,   321,
     851,    44,   273,    46,    47,    48,    49,    50,    51,    52,
      53,   732,    42,    56,   666,   459,    59,   323,   337,    -1,
     742,    64,    -1,   351,   354,    -1,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    -1,    79,    80,    81,    82,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      93,    94,    95,    96,    97,    98,    -1,    -1,   101,   102,
      -1,    -1,    -1,    -1,   107,   108,   109,    -1,    -1,   112,
      -1,    -1,    -1,    -1,   117,    -1,    -1,    -1,    -1,   122,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,     1,    -1,     3,     4,     5,     6,    -1,    -1,    -1,
      -1,    -1,    -1,   825,    14,    15,    16,    17,    18,    19,
      20,    21,    22,    23,    24,    25,    -1,    -1,    -1,    29,
      30,    31,    -1,    33,    34,    -1,    36,    37,    38,   851,
      -1,    41,    -1,    -1,    44,    -1,    46,    47,    48,    49,
      50,    51,    52,    53,    -1,    -1,    56,    -1,    -1,    59,
      -1,    -1,    -1,    -1,    64,    -1,    -1,    -1,    -1,    69,
      70,    71,    72,    73,    74,    75,    76,    77,    -1,    79,
      80,    81,    82,    83,    84,    85,    86,    87,    88,    89,
      90,    91,    92,    93,    94,    95,    96,    97,    98,    -1,
      -1,   101,   102,    -1,    -1,    -1,    -1,   107,   108,   109,
      -1,     1,   112,     3,     4,     5,     6,   117,    -1,    -1,
      -1,    -1,   122,    -1,    14,    15,    16,    17,    18,    19,
      20,    21,    22,    23,    24,    25,    -1,    -1,    -1,    29,
      30,    31,    -1,    -1,    34,    -1,    36,    37,    38,    -1,
      -1,    41,    -1,    -1,    44,    -1,    46,    47,    48,    49,
      50,    51,    52,    53,    -1,    -1,    56,    -1,    -1,    59,
      -1,    -1,    -1,    -1,    64,    -1,    -1,    -1,    -1,    69,
      70,    71,    72,    73,    74,    75,    76,    77,    -1,    79,
      80,    81,    82,    83,    84,    85,    86,    87,    88,    89,
      90,    91,    92,    93,    94,    95,    96,    97,    98,    -1,
      -1,   101,   102,    -1,    -1,    -1,    -1,   107,   108,   109,
      -1,     1,   112,     3,    -1,    -1,    -1,   117,    -1,    -1,
      -1,    -1,   122,    -1,    14,    15,    16,    17,    18,    19,
      20,    21,    22,    23,    24,    25,    -1,    -1,    -1,    29,
      -1,    -1,    -1,    33,    -1,    -1,    36,    37,    38,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    46,    47,    48,    -1,
      -1,    -1,    52,    53,    -1,    -1,    56,    -1,    -1,    59,
      60,    61,    62,    -1,    64,    65,    66,    -1,    -1,    -1,
      -1,    -1,    72,    73,    74,    75,    -1,    77,     1,    79,
       3,    -1,    -1,    83,    84,    -1,    -1,    -1,    -1,    -1,
      -1,    91,    15,    16,    17,    18,    19,    20,    21,    22,
      23,    24,    25,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      33,    -1,    -1,    36,    37,    38,    -1,    -1,    -1,    -1,
     120,    -1,   122,    -1,    -1,    48,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    56,     3,    -1,    59,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    14,    15,    16,    17,    18,
      19,    20,    21,    22,    23,    24,    25,    -1,    -1,    -1,
      29,    -1,    -1,    -1,    -1,    -1,    -1,    36,    37,    38,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    46,    47,    48,
      -1,   104,   105,   106,    53,    -1,    -1,    56,    -1,    -1,
      59,    60,    61,    62,    -1,    64,    65,    66,    -1,   122,
      -1,    -1,    -1,    72,    73,    74,    75,    -1,    77,    -1,
      79,    -1,    -1,    -1,    83,    84,    -1,    -1,    -1,    -1,
      -1,    -1,    91,     3,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    14,    15,    16,    17,    18,    19,
      20,    21,    22,    23,    24,    25,   115,   116,    -1,    29,
      -1,   120,    -1,   122,    -1,    -1,    36,    37,    38,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    46,    47,    48,    -1,
      -1,    -1,    -1,    53,    -1,    -1,    56,    -1,    -1,    59,
      60,    61,    62,    -1,    64,    65,    66,    -1,    -1,    -1,
      -1,    -1,    72,    73,    74,    75,    -1,    77,    -1,    79,
       3,    -1,    -1,    83,    84,    -1,    -1,    -1,    -1,    -1,
      -1,    91,    15,    16,    17,    18,    19,    20,    21,    22,
      23,    24,    25,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    35,    36,    37,    38,    -1,    -1,    -1,    -1,
     120,    -1,   122,    -1,    -1,     3,    -1,    -1,    -1,    -1,
      -1,    54,    55,    56,    -1,    -1,    59,    15,    16,    17,
      18,    19,    20,    21,    22,    23,    24,    25,    -1,     3,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    35,    36,    37,
      38,    15,    16,    17,    18,    19,    20,    21,    22,    23,
      24,    25,    -1,    -1,    -1,    -1,    54,    55,    56,    -1,
      -1,    59,    36,    37,    38,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,   117,     3,     4,    -1,    -1,   122,
      -1,    -1,    56,    -1,    -1,    59,    -1,    15,    16,    17,
      18,    19,    20,    21,    22,    23,    24,    25,    -1,     3,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    36,    37,
      38,    15,    16,    17,    18,    19,    20,    21,    22,    23,
      24,    25,    -1,    -1,   122,    -1,    -1,    -1,    56,    -1,
      -1,    59,    36,    37,    38,    -1,    -1,    -1,   112,    -1,
      -1,    -1,    -1,   117,     3,    -1,    -1,    -1,   122,    -1,
      -1,    -1,    56,    -1,    -1,    59,    15,    16,    17,    18,
      19,    20,    21,    22,    23,    24,    25,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,     3,    36,    37,    38,
      -1,     8,     9,    -1,    11,    12,    13,    -1,    -1,    48,
       3,    -1,    -1,    -1,   122,    -1,    -1,    56,    -1,    26,
      59,    -1,    15,    16,    17,    18,    19,    20,    21,    22,
      23,    24,    25,    40,     3,    -1,   120,    -1,   122,    -1,
      -1,    -1,    -1,    36,    37,    38,    15,    16,    17,    18,
      19,    20,    21,    22,    23,    24,    25,    -1,     3,    -1,
      -1,    -1,    -1,    56,    -1,    -1,    59,    36,    37,    38,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    -1,     3,   122,    -1,    -1,    -1,    56,    -1,    -1,
      59,    36,    37,    38,    15,    16,    17,    18,    19,    20,
      21,    22,    23,    24,    25,    -1,    -1,    -1,    -1,   116,
      -1,    56,    -1,   120,    59,    36,    37,    38,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   122,
      -1,    -1,    -1,    -1,     1,    56,     3,    -1,    59,    -1,
       7,     8,     9,    10,    11,    12,    13,    -1,    -1,    -1,
      -1,    -1,    -1,   122,    -1,    -1,    -1,    -1,    -1,    26,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    40,    -1,    -1,    -1,   122,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      57,    -1,    -1,    -1,     3,    -1,    -1,    -1,    -1,     8,
       9,   122,    11,    12,    13,    -1,    15,    16,    17,    18,
      19,    20,    21,    22,    23,    24,    25,    26,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    36,    37,    38,
      -1,    40,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   116,
      59,    -1,    -1,   120,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,   116,    -1,    -1,
      -1,   120
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint16 yystos[] =
{
       0,   124,   125,     0,   126,   258,     1,     4,     5,     6,
      14,    29,    30,    31,    34,    41,    44,    46,    47,    48,
      49,    50,    51,    52,    53,    64,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    79,    80,    81,    82,    83,
      84,    85,    86,    87,    88,    89,    90,    91,    92,    93,
      94,    95,    96,    97,    98,   101,   102,   107,   108,   109,
     127,   138,   139,   143,   145,   150,   178,   179,   185,   220,
     256,   258,     4,     3,    15,    16,    17,    18,    19,    20,
      21,    22,    23,    24,    25,    36,    37,    38,    56,    59,
     122,   164,   213,     7,     3,     4,     3,    58,     3,     3,
       7,   255,    26,     3,   255,   255,     3,     3,    26,    15,
      16,    17,    18,    19,    20,    21,    22,    23,    24,    25,
      36,    56,   164,   165,   213,    26,     4,   164,   213,     3,
       3,     3,    78,   121,   144,   144,     4,     3,   244,   244,
      26,    26,    29,    32,   255,     4,     7,   133,   164,   250,
     248,   250,     7,     7,     7,     7,     3,     7,    26,    32,
     257,     3,     3,     3,    56,   112,   117,   160,   161,   164,
     165,   213,    99,   122,   224,   258,    15,    17,    18,    21,
     167,   258,    15,   168,   258,   168,    15,    17,    18,    21,
     166,   258,   224,   164,     3,   172,   258,     3,     3,    26,
     160,   161,     3,    32,    32,   171,   258,     1,     7,    10,
      57,   149,   169,   170,   171,     3,    27,     3,    32,    39,
     246,   258,     3,   167,   168,   168,   166,   224,   164,     3,
     160,    26,     3,     3,   160,     3,     3,    26,   144,   246,
       3,    36,   247,     3,   127,     3,    26,    42,   112,   161,
     162,   251,   254,   258,    32,    29,    28,   249,   258,   245,
     258,   245,   245,   245,    29,    29,    35,    54,    55,   152,
     154,   155,   158,   159,   164,   258,    33,    26,    63,   223,
     224,   171,   172,     3,   161,   258,    26,     3,   160,    26,
       3,     3,   168,   168,   168,   168,    32,   117,   140,   162,
      26,    63,   209,   258,   183,   126,    28,    57,    57,     3,
       8,     9,    11,    12,    13,    26,    40,   116,   120,   177,
      27,   134,    29,   186,     7,     8,    27,    28,    26,   162,
     163,   258,   117,    27,    26,     3,   245,    28,    27,    27,
      26,   162,   254,   152,   161,    43,   177,   251,   251,   253,
     248,   250,    28,    35,    27,    28,   153,   258,   155,   158,
       3,    26,   112,   156,   161,   162,   258,     3,     3,   221,
     258,    29,    32,   152,    26,   122,   163,   117,    29,   209,
     136,   156,    28,   142,   258,   141,   117,     3,    60,    61,
      62,    65,   210,   211,   212,    32,     1,     3,    14,    29,
      46,    47,    48,    52,    53,    56,    60,    61,    62,    64,
      65,    66,    91,   120,   138,   139,   143,   164,   165,   188,
     192,   197,   213,   258,    33,     3,   122,    15,    16,    17,
      18,    19,    20,    21,    22,    23,    24,    25,    36,   165,
     177,   213,    26,   177,   177,   110,   111,   112,   113,   114,
     115,   116,   117,   118,    14,    30,   150,   178,   115,   116,
     187,   192,   238,   258,     3,     3,   152,    39,    63,   157,
     258,   150,   152,    27,     3,   247,   248,    29,    32,   252,
      27,   251,   163,    43,   254,    33,   249,     3,    35,   257,
     154,   157,   162,   161,   156,   156,    27,   224,    32,   135,
      27,   152,     3,    67,   157,    32,     3,   143,   173,   174,
     258,    27,   160,   142,   156,     3,   212,    28,     3,    65,
     181,   191,    26,    26,    32,     3,    26,   172,    63,    63,
      63,   164,   120,   164,   195,     3,   112,   160,   161,   201,
     258,    26,    33,   188,     3,    32,     3,   167,   168,   168,
     166,   224,   164,    27,    27,     3,   164,   177,   177,   177,
     177,   177,   177,   177,   177,   177,   213,     7,   164,   213,
      26,   240,   258,   240,    33,   188,     1,    48,    52,   234,
     238,   258,   246,   246,    27,    32,   112,   169,     8,   129,
       3,   164,    27,    27,    29,    32,    39,   254,    27,   163,
     246,   153,   156,   224,     1,    48,   104,   105,   106,   164,
     225,   230,   231,   258,   173,    36,    68,   214,   258,    27,
      26,    29,   128,   180,    39,   174,    28,    33,    26,   142,
     162,    27,     3,   211,     3,   188,   188,   117,   152,     3,
     189,   246,     3,    32,   160,     3,   160,   192,    26,    26,
     157,   162,    26,    67,   117,   160,    29,    32,   199,   177,
      27,     3,   160,     3,   164,     3,     3,   237,    26,    32,
     234,    27,   151,   214,     3,    28,    29,   146,    29,   160,
     151,   214,   248,   250,    26,    27,   222,   229,    26,   226,
     227,   228,   160,    33,   225,    28,   233,   258,    33,    26,
     131,   151,   214,   152,   146,   188,   175,   174,     3,   152,
      26,    33,    27,    27,   188,    27,   196,    26,   194,    26,
      26,   152,   152,   193,   157,   184,   198,   160,    27,   161,
     242,   258,   242,   234,     3,   235,    32,   132,   160,    26,
      29,    32,    39,    29,   152,    26,   234,   225,     3,   225,
     225,   225,   162,   234,   160,    29,    29,   152,   146,   130,
      27,    33,    10,   176,   177,   137,    27,   152,   160,   214,
     215,    33,     3,     3,    48,   143,   207,   208,   258,   152,
      28,    29,   202,    27,   152,    27,    27,   202,   142,   160,
     200,   258,    29,    27,     3,    29,    32,    63,   239,   243,
     239,    27,   234,   146,    26,   163,   152,   250,    27,   152,
     103,    27,   103,   162,   233,    27,   146,    29,   142,    29,
      27,   182,    63,   216,   258,   190,   246,    39,    26,   208,
      28,    33,    27,   160,   205,   214,    27,   205,   205,    29,
      63,    26,   241,   258,   236,    33,   152,   157,    27,    29,
      27,   232,   233,    29,   142,     3,   217,   218,    29,    32,
     188,   176,     3,   208,    29,   205,   157,   162,    29,    32,
     206,   214,   154,     3,   234,    27,   147,    29,   231,    26,
      28,    27,   203,   157,    29,    32,    39,    27,   214,   146,
      27,   177,   219,   218,     3,   202,   204,   169,   148,    27,
      28,    39,   202,    29,   146,   177,   176
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint16 yyr1[] =
{
       0,   123,   125,   124,   126,   126,   127,   127,   127,   127,
     127,   128,   127,   127,   129,   127,   127,   130,   127,   127,
     131,   127,   127,   127,   132,   127,   127,   127,   127,   127,
     133,   127,   134,   127,   127,   127,   127,   127,   127,   127,
     127,   127,   127,   127,   127,   127,   127,   127,   127,   127,
     127,   127,   127,   127,   127,   127,   127,   135,   127,   136,
     137,   127,   127,   127,   127,   127,   127,   127,   127,   127,
     127,   127,   127,   127,   127,   127,   127,   127,   127,   127,
     127,   127,   127,   127,   138,   138,   140,   139,   139,   139,
     141,   139,   142,   142,   142,   143,   143,   143,   143,   143,
     143,   144,   144,   144,   145,   145,   145,   146,   147,   146,
     148,   146,   149,   149,   149,   150,   150,   150,   151,   152,
     152,   153,   153,   154,   154,   155,   155,   155,   155,   155,
     156,   156,   156,   156,   157,   157,   157,   157,   157,   158,
     158,   159,   159,   160,   160,   160,   161,   161,   162,   162,
     163,   163,   164,   164,   164,   164,   164,   164,   164,   164,
     164,   164,   164,   164,   164,   164,   164,   164,   164,   165,
     165,   165,   165,   165,   165,   165,   165,   165,   165,   165,
     165,   165,   166,   166,   166,   166,   166,   167,   167,   167,
     167,   167,   168,   168,   170,   169,   169,   169,   171,   171,
     172,   172,   173,   173,   174,   175,   174,   174,   174,   176,
     176,   177,   177,   177,   177,   177,   177,   177,   177,   177,
     177,   177,   177,   177,   177,   177,   177,   177,   177,   177,
     177,   177,   178,   178,   180,   179,   181,   182,   179,   183,
     184,   179,   185,   185,   185,   185,   185,   186,   185,   187,
     187,   187,   188,   189,   190,   188,   191,   188,   188,   192,
     192,   192,   192,   192,   193,   192,   192,   194,   192,   192,
     192,   192,   192,   192,   195,   192,   196,   192,   192,   192,
     192,   192,   192,   192,   192,   197,   197,   198,   197,   199,
     197,   197,   197,   197,   197,   197,   197,   200,   200,   201,
     201,   201,   202,   203,   202,   204,   202,   205,   205,   206,
     206,   206,   207,   207,   208,   208,   208,   208,   208,   208,
     209,   209,   210,   210,   211,   211,   211,   211,   211,   212,
     212,   212,   213,   213,   213,   214,   214,   214,   215,   215,
     216,   216,   217,   217,   218,   218,   219,   219,   221,   220,
     222,   220,   220,   220,   220,   223,   223,   224,   224,   225,
     226,   225,   227,   225,   228,   225,   229,   225,   225,   230,
     231,   231,   232,   231,   233,   233,   233,   234,   235,   234,
     236,   234,   237,   234,   234,   238,   238,   239,   239,   240,
     240,   240,   241,   241,   242,   242,   243,   243,   244,   245,
     245,   246,   246,   246,   247,   247,   248,   249,   249,   250,
     250,   250,   250,   251,   252,   251,   253,   251,   251,   254,
     254,   255,   255,   256,   256,   257,   257,   257,   258
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     0,     2,     2,     1,     2,     2,     2,     2,
       1,     0,     7,     4,     0,     7,     4,     0,     9,     7,
       0,     8,     7,     7,     0,     9,     1,     1,     4,     4,
       0,     3,     0,     5,     7,    11,     3,     3,     3,     3,
       1,     1,     1,     2,     1,     1,     2,     2,     2,     2,
       2,     1,     3,     3,     3,     2,     2,     0,     8,     0,
       0,    10,     8,     6,     8,     6,    10,     8,     5,     3,
       5,     2,     5,     2,     1,     1,     1,     1,     5,     1,
       1,     2,     2,     1,     1,     1,     0,     5,    10,    11,
       0,     6,     3,     3,     1,     2,     2,     1,     1,     2,
       2,     4,     2,     2,     7,     3,     6,     1,     0,     6,
       0,     8,     2,     1,     2,     1,     1,     2,     2,     2,
       1,     3,     1,     1,     2,     2,     3,     3,     8,     3,
       2,     2,     1,     1,     2,     3,     2,     2,     1,     1,
       1,     2,     1,     1,     2,     2,     2,     2,     3,     4,
       1,     1,     1,     2,     2,     1,     1,     1,     1,     1,
       2,     2,     2,     2,     2,     2,     3,     2,     2,     1,
       2,     2,     1,     1,     1,     1,     1,     2,     2,     2,
       2,     2,     1,     1,     2,     2,     1,     1,     1,     2,
       2,     1,     1,     1,     0,     2,     1,     1,     3,     1,
       1,     1,     3,     1,     1,     0,     4,     2,     1,     1,
       1,     1,     1,     1,     1,     1,     4,     4,     1,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     3,     2,
       2,     3,     1,     1,     0,     8,     0,     0,    11,     0,
       0,     9,     4,     9,     6,     5,     1,     0,     6,     2,
       2,     1,     2,     0,     0,     7,     0,     3,     1,     6,
       7,     5,     6,     6,     0,     5,     4,     0,     5,     7,
       2,     2,     2,     4,     0,     3,     0,     7,     1,     1,
       1,     3,     1,     1,     1,     3,     6,     0,     6,     0,
       5,     3,     3,     3,     3,     1,     1,     1,     1,     1,
       1,     1,     1,     0,     5,     0,     6,     2,     2,     2,
       4,     2,     3,     1,     1,     3,     5,     7,     2,     1,
       2,     1,     1,     3,     1,     2,     3,     2,     3,     1,
       1,     1,     1,     1,     1,     1,     4,     1,     3,     3,
       2,     1,     1,     3,     4,     3,     1,     3,     0,     9,
       0,     9,     1,     1,     4,     3,     2,     1,     1,     2,
       0,     3,     0,     3,     0,     3,     0,     3,     1,     3,
       2,     3,     0,     6,     3,     4,     1,     2,     0,     5,
       0,     6,     0,     3,     1,     5,     5,     1,     1,     3,
       4,     1,     3,     1,     4,     1,     1,     2,     3,     4,
       1,     2,     2,     1,     1,     1,     2,     3,     1,     2,
       3,     3,     8,     2,     0,     4,     0,     3,     1,     3,
       1,     1,     1,     5,     2,     2,     2,     2,     0
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                  \
do                                                              \
  if (yychar == YYEMPTY)                                        \
    {                                                           \
      yychar = (Token);                                         \
      yylval = (Value);                                         \
      YYPOPSTACK (yylen);                                       \
      yystate = *yyssp;                                         \
      goto yybackup;                                            \
    }                                                           \
  else                                                          \
    {                                                           \
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256



/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)

/* This macro is provided for backward compatibility. */
#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, int yyrule)
{
  unsigned long int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &(yyvsp[(yyi + 1) - (yynrhs)])
                                              );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            /* Fall through.  */
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (! (yysize <= yysize1
                         && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                    return 2;
                  yysize = yysize1;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
      return 2;
    yysize = yysize1;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
{
  YYUSE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yystacksize);

        yyss = yyss1;
        yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 2:
#line 559 "parser.y" /* yacc.c:1646  */
    { 
                    {
		      int ii;
		      for (ii = 0; ii < 256; ii++) {
			handler_stack[ii] = 0;
		      }
		      handler_stack[0] = comment_handler;
		    }
                    doc_stack[0] = doctitle;
                 }
#line 2851 "y.tab.c" /* yacc.c:1646  */
    break;

  case 3:
#line 568 "parser.y" /* yacc.c:1646  */
    {
		   CommentHandler::cleanup();
                   cplus_cleanup();
		   doc_entry = doctitle;
		   if (lang_init) {
		     lang->close();
		   }
		   if (te_index) {
		     fprintf(stderr,"%s : EOF.  Missing #endif detected.\n", input_file);
		     FatalError();
		   }
               }
#line 2868 "y.tab.c" /* yacc.c:1646  */
    break;

  case 4:
#line 582 "parser.y" /* yacc.c:1646  */
    { 
		     scanner_clear_start();
                     Error = 0;
                }
#line 2877 "y.tab.c" /* yacc.c:1646  */
    break;

  case 5:
#line 586 "parser.y" /* yacc.c:1646  */
    {
	       }
#line 2884 "y.tab.c" /* yacc.c:1646  */
    break;

  case 6:
#line 590 "parser.y" /* yacc.c:1646  */
    {
                  if (allow) {
//		    init_language();
		    doc_entry = 0;
		    // comment_handler->clear();
		    include_file((yyvsp[0].id));
		  }
                }
#line 2897 "y.tab.c" /* yacc.c:1646  */
    break;

  case 7:
#line 601 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   int oldextern = WrapExtern;
//		   init_language();
		   doc_entry = 0;
		   // comment_handler->clear();
		   WrapExtern = 1;
		   if (include_file((yyvsp[0].id)) >= 0) {
		     add_symbol("SWIGEXTERN",0,0);
		   } else {
		     WrapExtern = oldextern;
		   }
		 }
	       }
#line 2916 "y.tab.c" /* yacc.c:1646  */
    break;

  case 8:
#line 618 "parser.y" /* yacc.c:1646  */
    {
		  if (allow) {
		    int oldextern = WrapExtern;
		    init_language();
		    doc_entry = 0;
		    WrapExtern = 1;
		    if (include_file((yyvsp[0].id)) >= 0) {
		      add_symbol("SWIGEXTERN",0,0);
		      lang->import((yyvsp[0].id));
		    } else {
		      WrapExtern = oldextern;
		    }
		  }
                }
#line 2935 "y.tab.c" /* yacc.c:1646  */
    break;

  case 9:
#line 636 "parser.y" /* yacc.c:1646  */
    {
                  if (allow) {
                     if ((checkout_file((yyvsp[0].id),(yyvsp[0].id))) == 0) {
                       fprintf(stderr,"%s checked out from the SWIG library.\n",(yyvsp[0].id));
                      }
                  }
                }
#line 2947 "y.tab.c" /* yacc.c:1646  */
    break;

  case 10:
#line 646 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
                  doc_entry = 0;
		  if (Verbose) {
		    fprintf(stderr,"%s : Line %d.  CPP %s ignored.\n", input_file, line_number,(yyvsp[0].id));
		  }
		 }
		}
#line 2960 "y.tab.c" /* yacc.c:1646  */
    break;

  case 11:
#line 657 "parser.y" /* yacc.c:1646  */
    {
		  if (allow) {
		    init_language();
		    if (Active_type) delete Active_type;
		    Active_type = new DataType((yyvsp[-3].type));
		    Active_extern = (yyvsp[-4].ivalue);
		    (yyvsp[-3].type)->is_pointer += (yyvsp[-2].decl).is_pointer;
		    if ((yyvsp[-1].ivalue) > 0) {
		      (yyvsp[-3].type)->is_pointer++;
		      (yyvsp[-3].type)->status = STAT_READONLY;
                      (yyvsp[-3].type)->arraystr = copy_string(ArrayString);
		    }
		    if ((yyvsp[-2].decl).is_reference) {
		      fprintf(stderr,"%s : Line %d. Error. Linkage to C++ reference not allowed.\n", input_file, line_number);
		      FatalError();
		    } else {
		      if ((yyvsp[-3].type)->qualifier) {
			if ((strcmp((yyvsp[-3].type)->qualifier,"const") == 0)) {
			  if ((yyvsp[0].dtype).type != T_ERROR)
			    create_constant((yyvsp[-2].decl).id, (yyvsp[-3].type), (yyvsp[0].dtype).id);
			} else 
			  create_variable((yyvsp[-4].ivalue),(yyvsp[-2].decl).id,(yyvsp[-3].type));
		      } else
			create_variable((yyvsp[-4].ivalue),(yyvsp[-2].decl).id,(yyvsp[-3].type));
		    }
		  }
		  delete (yyvsp[-3].type);
                }
#line 2993 "y.tab.c" /* yacc.c:1646  */
    break;

  case 12:
#line 684 "parser.y" /* yacc.c:1646  */
    { }
#line 2999 "y.tab.c" /* yacc.c:1646  */
    break;

  case 13:
#line 688 "parser.y" /* yacc.c:1646  */
    { 
                   skip_decl();
		   fprintf(stderr,"%s : Line %d. Function pointers not currently supported.\n",
			   input_file, line_number);
		}
#line 3009 "y.tab.c" /* yacc.c:1646  */
    break;

  case 14:
#line 696 "parser.y" /* yacc.c:1646  */
    {
		  if (Verbose) {
		    fprintf(stderr,"static variable %s ignored.\n",(yyvsp[-2].decl).id);
		  }
		  Active_static = 1;
		  delete (yyvsp[-3].type);
		}
#line 3021 "y.tab.c" /* yacc.c:1646  */
    break;

  case 15:
#line 702 "parser.y" /* yacc.c:1646  */
    {
		  Active_static = 0;
		}
#line 3029 "y.tab.c" /* yacc.c:1646  */
    break;

  case 16:
#line 708 "parser.y" /* yacc.c:1646  */
    { 
                   skip_decl();
		   fprintf(stderr,"%s : Line %d. Function pointers not currently supported.\n",
			   input_file, line_number);
		}
#line 3039 "y.tab.c" /* yacc.c:1646  */
    break;

  case 17:
#line 717 "parser.y" /* yacc.c:1646  */
    {
		  if (allow) {
		    init_language();
		    if (Active_type) delete Active_type;
		    Active_type = new DataType((yyvsp[-5].type));
		    Active_extern = (yyvsp[-6].ivalue);
		    (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		    (yyvsp[-5].type)->is_reference = (yyvsp[-4].decl).is_reference;
		    create_function((yyvsp[-6].ivalue), (yyvsp[-4].decl).id, (yyvsp[-5].type), (yyvsp[-2].pl));
		  }
		  delete (yyvsp[-5].type);
		  delete (yyvsp[-2].pl);
		}
#line 3057 "y.tab.c" /* yacc.c:1646  */
    break;

  case 18:
#line 729 "parser.y" /* yacc.c:1646  */
    { }
#line 3063 "y.tab.c" /* yacc.c:1646  */
    break;

  case 19:
#line 733 "parser.y" /* yacc.c:1646  */
    {
		  if (allow) {
		    init_language();
		    (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		    (yyvsp[-5].type)->is_reference = (yyvsp[-4].decl).is_reference;
		    create_function((yyvsp[-6].ivalue), (yyvsp[-4].decl).id, (yyvsp[-5].type), (yyvsp[-2].pl));
		  }
		  delete (yyvsp[-5].type);
		  delete (yyvsp[-2].pl);
		}
#line 3078 "y.tab.c" /* yacc.c:1646  */
    break;

  case 20:
#line 746 "parser.y" /* yacc.c:1646  */
    { 
		  if (allow) {
                    init_language();
		    DataType *t = new DataType(T_INT);
                    t->is_pointer += (yyvsp[-4].decl).is_pointer;
		    t->is_reference = (yyvsp[-4].decl).is_reference;
		    create_function((yyvsp[-5].ivalue),(yyvsp[-4].decl).id,t,(yyvsp[-2].pl));
		    delete t;
		  }
                }
#line 3093 "y.tab.c" /* yacc.c:1646  */
    break;

  case 21:
#line 755 "parser.y" /* yacc.c:1646  */
    { }
#line 3099 "y.tab.c" /* yacc.c:1646  */
    break;

  case 22:
#line 759 "parser.y" /* yacc.c:1646  */
    {
		  if ((allow) && (Inline)) {
		    if (strlen(CCode.get())) {
		      init_language();
		      (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		      (yyvsp[-5].type)->is_reference = (yyvsp[-4].decl).is_reference;
		      create_function(0, (yyvsp[-4].decl).id, (yyvsp[-5].type), (yyvsp[-2].pl));
		    }
		  }
		  delete (yyvsp[-5].type);
		  delete (yyvsp[-2].pl);
		}
#line 3116 "y.tab.c" /* yacc.c:1646  */
    break;

  case 23:
#line 774 "parser.y" /* yacc.c:1646  */
    {
		  if (allow) {
		    init_language();
		    (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		    (yyvsp[-5].type)->is_reference = (yyvsp[-4].decl).is_reference;
		    if (Inline) {
		      fprintf(stderr,"%s : Line %d. Repeated %%inline directive.\n",input_file,line_number);
		      FatalError();
		    } else {
		      if (strlen(CCode.get())) {
			fprintf(f_header,"static ");
			emit_extern_func((yyvsp[-4].decl).id,(yyvsp[-5].type),(yyvsp[-2].pl),3,f_header);
			fprintf(f_header,"%s\n",CCode.get());
		      }
		      create_function(0, (yyvsp[-4].decl).id, (yyvsp[-5].type), (yyvsp[-2].pl));
		    }
		  }
		  delete (yyvsp[-5].type);
		  delete (yyvsp[-2].pl);
		}
#line 3141 "y.tab.c" /* yacc.c:1646  */
    break;

  case 24:
#line 797 "parser.y" /* yacc.c:1646  */
    {
		  if (allow) {
		    if (Verbose) {
		      fprintf(stderr,"static function %s ignored.\n", (yyvsp[-4].decl).id);
		    }
		  }
		  Active_static = 1;
		  delete (yyvsp[-5].type);
		  delete (yyvsp[-2].pl);
		}
#line 3156 "y.tab.c" /* yacc.c:1646  */
    break;

  case 25:
#line 806 "parser.y" /* yacc.c:1646  */
    {
		  Active_static = 0;
		 }
#line 3164 "y.tab.c" /* yacc.c:1646  */
    break;

  case 26:
#line 812 "parser.y" /* yacc.c:1646  */
    {
		  if (allow)
		    Status = Status | STAT_READONLY;
	       }
#line 3173 "y.tab.c" /* yacc.c:1646  */
    break;

  case 27:
#line 819 "parser.y" /* yacc.c:1646  */
    {
		 if (allow)
		   Status = Status & ~STAT_READONLY;
	       }
#line 3182 "y.tab.c" /* yacc.c:1646  */
    break;

  case 28:
#line 825 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
                     strcpy(yy_rename,(yyvsp[-1].id));
                     Rename_true = 1;
		 }
               }
#line 3193 "y.tab.c" /* yacc.c:1646  */
    break;

  case 29:
#line 833 "parser.y" /* yacc.c:1646  */
    { 
		 if (name_hash.lookup((yyvsp[-2].id))) {
		   name_hash.remove((yyvsp[-2].id));
		 }
		 name_hash.add((yyvsp[-2].id),copy_string((yyvsp[-1].id)));
	       }
#line 3204 "y.tab.c" /* yacc.c:1646  */
    break;

  case 30:
#line 842 "parser.y" /* yacc.c:1646  */
    {
                     NewObject = 1;
                }
#line 3212 "y.tab.c" /* yacc.c:1646  */
    break;

  case 31:
#line 844 "parser.y" /* yacc.c:1646  */
    {
                     NewObject = 0;
               }
#line 3220 "y.tab.c" /* yacc.c:1646  */
    break;

  case 32:
#line 850 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   fprintf(stderr,"%s : Lind %d. Empty %%name() is no longer supported.\n",
			   input_file, line_number);
		   FatalError();
		 }
	       }
#line 3232 "y.tab.c" /* yacc.c:1646  */
    break;

  case 33:
#line 856 "parser.y" /* yacc.c:1646  */
    {
		 Rename_true = 0;
	       }
#line 3240 "y.tab.c" /* yacc.c:1646  */
    break;

  case 34:
#line 862 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   init_language();
		   if (add_symbol((yyvsp[-4].id),(DataType *) 0, (char *) 0)) {
		     fprintf(stderr,"%s : Line %d. Name of native function %s conflicts with previous declaration (ignored)\n",
			     input_file, line_number, (yyvsp[-4].id));
		   } else {
		     doc_entry = new DocDecl((yyvsp[-4].id),doc_stack[doc_stack_top]);
		     lang->add_native((yyvsp[-4].id),(yyvsp[-1].id));
		   }
		 }
	       }
#line 3257 "y.tab.c" /* yacc.c:1646  */
    break;

  case 35:
#line 874 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   init_language();
		   (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		   if (add_symbol((yyvsp[-8].id),(DataType *) 0, (char *) 0)) {
		     fprintf(stderr,"%s : Line %d. Name of native function %s conflicts with previous declaration (ignored)\n",
			     input_file, line_number, (yyvsp[-8].id));
		   } else {
		     if ((yyvsp[-6].ivalue)) {
		       emit_extern_func((yyvsp[-4].decl).id, (yyvsp[-5].type), (yyvsp[-2].pl), (yyvsp[-6].ivalue), f_header);
		     }
		     doc_entry = new DocDecl((yyvsp[-8].id),doc_stack[doc_stack_top]);
		     lang->add_native((yyvsp[-8].id),(yyvsp[-4].decl).id);
		   }
		 }
		 delete (yyvsp[-5].type);
		 delete (yyvsp[-2].pl);
	       }
#line 3280 "y.tab.c" /* yacc.c:1646  */
    break;

  case 36:
#line 895 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   if (!title_init) {
		     title_init = 1;
		     doc_init = 1;
		     if (!comment_handler) {
		       comment_handler = new CommentHandler();
		     }
		     { 
		       int ii;
		       for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
			 comment_handler->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		       }
		     }
		     // Create a new title for documentation 
		     {
		       int temp = line_number;
		       line_number = (yyvsp[-2].ivalue);
		       if (!doctitle)
			 doctitle = new DocTitle((yyvsp[-1].id),0);
		       else {
			 doctitle->name = copy_string(title);
			 doctitle->line_number = (yyvsp[-2].ivalue);
			 doctitle->end_line = (yyvsp[-2].ivalue);
		       }
		       line_number = temp;
		     }
		     doctitle->usage = (yyvsp[-1].id);
		     doc_entry = doctitle;
		     doc_stack[0] = doc_entry;
		     doc_stack_top = 0;
		     handler_stack[0] = comment_handler;
		     { 
		       int ii;
		       for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
			 doc_stack[doc_stack_top]->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		       }
		     }

		   } else {
		     // Ignore it
		   }
		 }
	       }
#line 3329 "y.tab.c" /* yacc.c:1646  */
    break;

  case 37:
#line 943 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern) && (!IgnoreDoc)) {
		   // Copy old comment handler
		   // if (handler_stack[1]) delete handler_stack[1];
		   handler_stack[1] = new CommentHandler(handler_stack[0]);  
		   comment_handler = handler_stack[1];
		   { 
		     int ii;
		     for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
		       comment_handler->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		     }
		   }
		   {
		     int temp = line_number;
		     line_number = (yyvsp[-2].ivalue);
		     doc_entry = new DocSection((yyvsp[-1].id),doc_stack[0]);
		     line_number = temp;
		   }
		   doc_stack_top = 1;
		   doc_stack[1] = doc_entry;
		   { 
		     int ii;
		     for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
		       doc_stack[doc_stack_top]->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		     }
		   }
		 }
	       }
#line 3362 "y.tab.c" /* yacc.c:1646  */
    break;

  case 38:
#line 973 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern) && (!IgnoreDoc)) {
		   if (doc_stack_top < 1) {
		     fprintf(stderr,"%s : Line %d. Can't apply %%subsection here.\n", input_file,line_number);
		     FatalError();
		   } else {

		     // Copy old comment handler
		     // if (handler_stack[2]) delete handler_stack[2];
		     handler_stack[2] = new CommentHandler(handler_stack[1]);
		     comment_handler = handler_stack[2];
		     { 
		       int ii;
		       for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
			 comment_handler->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		       }
		     }
		     {
		       int temp = line_number;
		       line_number = (yyvsp[-2].ivalue);
		       doc_entry = new DocSection((yyvsp[-1].id),doc_stack[1]);
		       line_number = temp;
		     }
		     doc_stack_top = 2;
		     doc_stack[2] = doc_entry;
		     { 
		       int ii;
		       for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
			 doc_stack[doc_stack_top]->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		       }
		     }
		   }
		 }
	       }
#line 3401 "y.tab.c" /* yacc.c:1646  */
    break;

  case 39:
#line 1009 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern) && (!IgnoreDoc)) {
		   if (doc_stack_top < 2) {
		     fprintf(stderr,"%s : Line %d. Can't apply %%subsubsection here.\n", input_file,line_number);
		     FatalError();
		   } else {

		     // Copy old comment handler

		     // if (handler_stack[3]) delete handler_stack[3];
		     handler_stack[3] = new CommentHandler(handler_stack[2]);
		     comment_handler = handler_stack[3];
		     { 
		       int ii;
		       for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
			 comment_handler->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		       }
		     }
		     {
		       int temp = line_number;
		       line_number = (yyvsp[-2].ivalue);
		       doc_entry = new DocSection((yyvsp[-1].id),doc_stack[2]);
		       line_number = temp;
		     }
		     doc_stack_top = 3;
		     doc_stack[3] = doc_entry;
		     { 
		       int ii;
		       for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
			 doc_stack[doc_stack_top]->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		       }
		     }
		   }
		 }
	       }
#line 3441 "y.tab.c" /* yacc.c:1646  */
    break;

  case 40:
#line 1046 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   fprintf(stderr,"%%alpha directive is obsolete.  Use '%%style sort' instead.\n");
		   handler_stack[0]->style("sort",0);
		   doc_stack[0]->style("sort",0);
		 }
	       }
#line 3453 "y.tab.c" /* yacc.c:1646  */
    break;

  case 41:
#line 1054 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   fprintf(stderr,"%%raw directive is obsolete. Use '%%style nosort' instead.\n");
		   handler_stack[0]->style("nosort",0);
		   doc_stack[0]->style("nosort",0);
		 }
	       }
#line 3465 "y.tab.c" /* yacc.c:1646  */
    break;

  case 42:
#line 1062 "parser.y" /* yacc.c:1646  */
    { }
#line 3471 "y.tab.c" /* yacc.c:1646  */
    break;

  case 43:
#line 1066 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   (yyvsp[0].id)[strlen((yyvsp[0].id)) - 1] = 0;
		   doc_entry = new DocText((yyvsp[0].id),doc_stack[doc_stack_top]);
		   doc_entry = 0;
		 }
	       }
#line 3483 "y.tab.c" /* yacc.c:1646  */
    break;

  case 44:
#line 1075 "parser.y" /* yacc.c:1646  */
    { }
#line 3489 "y.tab.c" /* yacc.c:1646  */
    break;

  case 45:
#line 1079 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   init_language();
		   (yyvsp[0].id)[strlen((yyvsp[0].id)) - 1] = 0;
//		   fprintf(f_header,"#line %d \"%s\"\n", start_line, input_file);
		   fprintf(f_header, "%s\n", (yyvsp[0].id));
		 }
	       }
#line 3502 "y.tab.c" /* yacc.c:1646  */
    break;

  case 46:
#line 1090 "parser.y" /* yacc.c:1646  */
    {
                 if (allow && (!WrapExtern)) {
		   init_language();
		   (yyvsp[0].id)[strlen((yyvsp[0].id)) - 1] = 0;
		   fprintf(f_wrappers,"%s\n",(yyvsp[0].id));
		 }
	       }
#line 3514 "y.tab.c" /* yacc.c:1646  */
    break;

  case 47:
#line 1100 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   init_language();
		   (yyvsp[0].id)[strlen((yyvsp[0].id)) -1] = 0;
		   fprintf(f_init,"%s\n", (yyvsp[0].id));
		 }
	       }
#line 3526 "y.tab.c" /* yacc.c:1646  */
    break;

  case 48:
#line 1109 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   init_language();
		   (yyvsp[0].id)[strlen((yyvsp[0].id)) - 1] = 0;
		   fprintf(f_header, "%s\n", (yyvsp[0].id));
		   start_inline((yyvsp[0].id),start_line);
		 }
	       }
#line 3539 "y.tab.c" /* yacc.c:1646  */
    break;

  case 49:
#line 1119 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern)) {
		   fprintf(stderr,"%s\n", (yyvsp[0].id));
		 }
	       }
#line 3549 "y.tab.c" /* yacc.c:1646  */
    break;

  case 50:
#line 1125 "parser.y" /* yacc.c:1646  */
    {
                 if (allow && (!WrapExtern)) {
                   fprintf(stderr,"%s\n", (yyvsp[0].id));
                 }
               }
#line 3559 "y.tab.c" /* yacc.c:1646  */
    break;

  case 51:
#line 1132 "parser.y" /* yacc.c:1646  */
    {
                   DocOnly = 1;
               }
#line 3567 "y.tab.c" /* yacc.c:1646  */
    break;

  case 52:
#line 1138 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   if (!module_init) {
		     lang->set_init((yyvsp[-1].id));
		     module_init = 1;
		     init_language();
		   } else {
		     if (Verbose)
		       fprintf(stderr,"%s : Line %d. %%init %s ignored.\n",
			       input_file, line_number, (yyvsp[-1].id));
		   }
		   if ((yyvsp[0].ilist).count > 0) {
		     fprintf(stderr,"%s : Line %d. Warning. Init list no longer supported.\n",
			     input_file,line_number);
		   }
		 }
		 for (i = 0; i < (yyvsp[0].ilist).count; i++)
		   if ((yyvsp[0].ilist).names[i]) delete [] (yyvsp[0].ilist).names[i];
		 delete [] (yyvsp[0].ilist).names;
	       }
#line 3592 "y.tab.c" /* yacc.c:1646  */
    break;

  case 53:
#line 1160 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   if ((yyvsp[0].ilist).count)
		     lang->set_module((yyvsp[-1].id),(yyvsp[0].ilist).names);
		   else
		     lang->set_module((yyvsp[-1].id),0);
		   module_init = 1;
		   init_language();
		 }
		 for (i = 0; i < (yyvsp[0].ilist).count; i++)
		   if ((yyvsp[0].ilist).names[i]) delete [] (yyvsp[0].ilist).names[i];
		 delete [] (yyvsp[0].ilist).names;
	       }
#line 3610 "y.tab.c" /* yacc.c:1646  */
    break;

  case 54:
#line 1176 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   if (((yyvsp[0].dtype).type != T_ERROR) && ((yyvsp[0].dtype).type != T_SYMBOL)) {
		     init_language();
		     temp_typeptr = new DataType((yyvsp[0].dtype).type);
		     create_constant((yyvsp[-1].id), temp_typeptr, (yyvsp[0].dtype).id);
		     delete temp_typeptr;
		   } else if ((yyvsp[0].dtype).type == T_SYMBOL) {
		     // Add a symbol to the SWIG symbol table
		     if (add_symbol((yyvsp[-1].id),(DataType *) 0, (char *) 0)) {
		       fprintf(stderr,"%s : Line %d. Warning. Symbol %s already defined.\n", 
			       input_file,line_number, (yyvsp[-1].id));
		     }
		   }
		 }
	       }
#line 3631 "y.tab.c" /* yacc.c:1646  */
    break;

  case 55:
#line 1195 "parser.y" /* yacc.c:1646  */
    {
		 if (Verbose) {
		   fprintf(stderr,"%s : Line %d.  CPP Macro ignored.\n", input_file, line_number);
		 }
	       }
#line 3641 "y.tab.c" /* yacc.c:1646  */
    break;

  case 56:
#line 1202 "parser.y" /* yacc.c:1646  */
    {
		 remove_symbol((yyvsp[0].id));
	       }
#line 3649 "y.tab.c" /* yacc.c:1646  */
    break;

  case 57:
#line 1208 "parser.y" /* yacc.c:1646  */
    { scanner_clear_start(); }
#line 3655 "y.tab.c" /* yacc.c:1646  */
    break;

  case 58:
#line 1208 "parser.y" /* yacc.c:1646  */
    { 
		 if (allow) {
		   init_language();
		   if ((yyvsp[-5].id)) {
		     temp_type.type = T_INT;
		     temp_type.is_pointer = 0;
		     temp_type.implicit_ptr = 0;
		     sprintf(temp_type.name,"int");
		     temp_type.typedef_add((yyvsp[-5].id),1);
		   }
		 }
	       }
#line 3672 "y.tab.c" /* yacc.c:1646  */
    break;

  case 59:
#line 1223 "parser.y" /* yacc.c:1646  */
    { scanner_clear_start(); }
#line 3678 "y.tab.c" /* yacc.c:1646  */
    break;

  case 60:
#line 1223 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   init_language();
		   temp_type.type = T_INT;
		   temp_type.is_pointer = 0;
		   temp_type.implicit_ptr = 0;
		   sprintf(temp_type.name,"int");
		   Active_typedef = new DataType(&temp_type);
		   temp_type.typedef_add((yyvsp[0].id),1);
		 }
	       }
#line 3694 "y.tab.c" /* yacc.c:1646  */
    break;

  case 61:
#line 1233 "parser.y" /* yacc.c:1646  */
    { }
#line 3700 "y.tab.c" /* yacc.c:1646  */
    break;

  case 62:
#line 1243 "parser.y" /* yacc.c:1646  */
    {
		   TMParm *p;
                   skip_brace();
		   p = (yyvsp[-1].tmparm);
		   while (p) {
		     typemap_register((yyvsp[-3].id),(yyvsp[-5].id),p->p->t,p->p->name,CCode,p->args);
		     p = p->next;
                   }
		   delete (yyvsp[-5].id);
		   delete (yyvsp[-3].id);
	       }
#line 3716 "y.tab.c" /* yacc.c:1646  */
    break;

  case 63:
#line 1256 "parser.y" /* yacc.c:1646  */
    {
		 if (!typemap_lang) {
		   fprintf(stderr,"SWIG internal error. No typemap_lang specified.\n");
		   fprintf(stderr,"typemap on %s : Line %d. will be ignored.\n",input_file,line_number);
		   FatalError();
		 } else {
		   TMParm *p;
		   skip_brace();
		   p = (yyvsp[-1].tmparm);
		   while (p) {
		     typemap_register((yyvsp[-3].id),typemap_lang,p->p->t,p->p->name,CCode,p->args);
		     p = p->next;
		   }
		 }
		 delete (yyvsp[-3].id);
	       }
#line 3737 "y.tab.c" /* yacc.c:1646  */
    break;

  case 64:
#line 1275 "parser.y" /* yacc.c:1646  */
    {
		 TMParm *p;
		 p = (yyvsp[-1].tmparm);
		 while (p) {
                   typemap_clear((yyvsp[-3].id),(yyvsp[-5].id),p->p->t,p->p->name);
		   p = p->next;
		 }
		 delete (yyvsp[-5].id);
		 delete (yyvsp[-3].id);
	       }
#line 3752 "y.tab.c" /* yacc.c:1646  */
    break;

  case 65:
#line 1287 "parser.y" /* yacc.c:1646  */
    {
		 if (!typemap_lang) {
		   fprintf(stderr,"SWIG internal error. No typemap_lang specified.\n");
		   fprintf(stderr,"typemap on %s : Line %d. will be ignored.\n",input_file,line_number);
		   FatalError();
		 } else {
		   TMParm *p;
		   p = (yyvsp[-1].tmparm);
		   while (p) {
		     typemap_clear((yyvsp[-3].id),typemap_lang,p->p->t,p->p->name);
		     p = p->next;
		   }
		 }
		 delete (yyvsp[-3].id);
	       }
#line 3772 "y.tab.c" /* yacc.c:1646  */
    break;

  case 66:
#line 1305 "parser.y" /* yacc.c:1646  */
    {
                   TMParm *p;
		   p = (yyvsp[-3].tmparm);
		   while (p) {
		     typemap_copy((yyvsp[-5].id),(yyvsp[-7].id),(yyvsp[-1].tmparm)->p->t,(yyvsp[-1].tmparm)->p->name,p->p->t,p->p->name);
		     p = p->next;
		   }
		   delete (yyvsp[-7].id);
		   delete (yyvsp[-5].id);
		   delete (yyvsp[-1].tmparm)->p;
		   delete (yyvsp[-1].tmparm);
	       }
#line 3789 "y.tab.c" /* yacc.c:1646  */
    break;

  case 67:
#line 1320 "parser.y" /* yacc.c:1646  */
    {
		 if (!typemap_lang) {
		   fprintf(stderr,"SWIG internal error. No typemap_lang specified.\n");
		   fprintf(stderr,"typemap on %s : Line %d. will be ignored.\n",input_file,line_number);
		   FatalError();
		 } else {
                   TMParm *p;
		   p = (yyvsp[-3].tmparm);
		   while (p) {
		     typemap_copy((yyvsp[-5].id),typemap_lang,(yyvsp[-1].tmparm)->p->t,(yyvsp[-1].tmparm)->p->name,p->p->t,p->p->name);
		     p = p->next;
		   }
		 }
		 delete (yyvsp[-5].id);
		 delete (yyvsp[-1].tmparm)->p;
		 delete (yyvsp[-1].tmparm);
	       }
#line 3811 "y.tab.c" /* yacc.c:1646  */
    break;

  case 68:
#line 1341 "parser.y" /* yacc.c:1646  */
    {
		 TMParm *p;
		 p = (yyvsp[-1].tmparm);
		 while(p) {
		   typemap_apply((yyvsp[-3].tmparm)->p->t,(yyvsp[-3].tmparm)->p->name,p->p->t,p->p->name);
		   p = p->next;
		 }
		 delete (yyvsp[-1].tmparm);
		 delete (yyvsp[-3].tmparm)->args;
		 delete (yyvsp[-3].tmparm);
               }
#line 3827 "y.tab.c" /* yacc.c:1646  */
    break;

  case 69:
#line 1352 "parser.y" /* yacc.c:1646  */
    {
		 TMParm *p;
		 p = (yyvsp[-1].tmparm);
		 while (p) {
		   typemap_clear_apply(p->p->t, p->p->name);
		   p = p->next;
		 }
               }
#line 3840 "y.tab.c" /* yacc.c:1646  */
    break;

  case 70:
#line 1369 "parser.y" /* yacc.c:1646  */
    {
                    skip_brace();
                    fragment_register("except",(yyvsp[-2].id), CCode);
		    delete (yyvsp[-2].id);
	       }
#line 3850 "y.tab.c" /* yacc.c:1646  */
    break;

  case 71:
#line 1376 "parser.y" /* yacc.c:1646  */
    {
                    skip_brace();
                    fragment_register("except",typemap_lang, CCode);
               }
#line 3859 "y.tab.c" /* yacc.c:1646  */
    break;

  case 72:
#line 1383 "parser.y" /* yacc.c:1646  */
    {
                     fragment_clear("except",(yyvsp[-2].id));
               }
#line 3867 "y.tab.c" /* yacc.c:1646  */
    break;

  case 73:
#line 1388 "parser.y" /* yacc.c:1646  */
    {
                     fragment_clear("except",typemap_lang);
	       }
#line 3875 "y.tab.c" /* yacc.c:1646  */
    break;

  case 74:
#line 1394 "parser.y" /* yacc.c:1646  */
    { }
#line 3881 "y.tab.c" /* yacc.c:1646  */
    break;

  case 75:
#line 1395 "parser.y" /* yacc.c:1646  */
    { }
#line 3887 "y.tab.c" /* yacc.c:1646  */
    break;

  case 76:
#line 1396 "parser.y" /* yacc.c:1646  */
    { }
#line 3893 "y.tab.c" /* yacc.c:1646  */
    break;

  case 77:
#line 1397 "parser.y" /* yacc.c:1646  */
    {
		 if (!Error) {
		   {
		     static int last_error_line = -1;
		     if (last_error_line != line_number) {
		       fprintf(stderr,"%s : Line %d. Syntax error in input.\n", input_file, line_number);
		       FatalError();
		       last_error_line = line_number;
                       // Try to make some kind of recovery.
		       skip_decl();
		     }
		     Error = 1;
		   }
		 }
	       }
#line 3913 "y.tab.c" /* yacc.c:1646  */
    break;

  case 78:
#line 1415 "parser.y" /* yacc.c:1646  */
    { }
#line 3919 "y.tab.c" /* yacc.c:1646  */
    break;

  case 79:
#line 1416 "parser.y" /* yacc.c:1646  */
    { }
#line 3925 "y.tab.c" /* yacc.c:1646  */
    break;

  case 80:
#line 1420 "parser.y" /* yacc.c:1646  */
    { }
#line 3931 "y.tab.c" /* yacc.c:1646  */
    break;

  case 81:
#line 1424 "parser.y" /* yacc.c:1646  */
    {
		 { 
		   int ii,jj;
		   for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
		     comment_handler->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		     for (jj = 0; jj < doc_stack_top; jj++) 
		       doc_stack[jj]->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		     if (doctitle)
		       doctitle->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		     doc->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		   }
		 }
	       }
#line 3949 "y.tab.c" /* yacc.c:1646  */
    break;

  case 82:
#line 1440 "parser.y" /* yacc.c:1646  */
    {
		 { 
		   int ii;
		   for (ii = 0; ii < (yyvsp[0].dlist).count; ii++) {
		     comment_handler = new CommentHandler(comment_handler);
		     handler_stack[doc_stack_top] = comment_handler;
		     comment_handler->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		     doc_stack[doc_stack_top]->style((yyvsp[0].dlist).names[ii],(yyvsp[0].dlist).values[ii]);
		   }
		 }
	       }
#line 3965 "y.tab.c" /* yacc.c:1646  */
    break;

  case 83:
#line 1453 "parser.y" /* yacc.c:1646  */
    { }
#line 3971 "y.tab.c" /* yacc.c:1646  */
    break;

  case 84:
#line 1459 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   if (IgnoreDoc) {
		     /* Already in a disabled documentation */
		     doc_scope++;
		   } else {
		     if (Verbose)
		       fprintf(stderr,"%s : Line %d. Documentation disabled.\n", input_file, line_number);
		     IgnoreDoc = 1;
		     doc_scope = 1;
		   }
		 }
	       }
#line 3989 "y.tab.c" /* yacc.c:1646  */
    break;

  case 85:
#line 1473 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   if (IgnoreDoc) {
		     if (doc_scope > 1) {
		       doc_scope--;
		     } else {
		       if (Verbose)
			 fprintf(stderr,"%s : Line %d. Documentation enabled.\n", input_file, line_number);
		       IgnoreDoc = 0;
		       doc_scope = 0;
		     }
		   }
		 }
	       }
#line 4008 "y.tab.c" /* yacc.c:1646  */
    break;

  case 86:
#line 1492 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   init_language();
		   /* Add a new typedef */
		   Active_typedef = new DataType((yyvsp[-1].type));
		   (yyvsp[-1].type)->is_pointer += (yyvsp[0].decl).is_pointer;
		   (yyvsp[-1].type)->typedef_add((yyvsp[0].decl).id);
		   /* If this is %typedef, add it to the header */
		   if ((yyvsp[-2].ivalue)) 
		     fprintf(f_header,"typedef %s %s;\n", (yyvsp[-1].type)->print_full(), (yyvsp[0].decl).id);
		   cplus_register_type((yyvsp[0].decl).id);
		 }
	       }
#line 4026 "y.tab.c" /* yacc.c:1646  */
    break;

  case 87:
#line 1504 "parser.y" /* yacc.c:1646  */
    { }
#line 4032 "y.tab.c" /* yacc.c:1646  */
    break;

  case 88:
#line 1508 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   init_language();
		   /* Typedef'd pointer */
		   if ((yyvsp[-9].ivalue)) {
		     sprintf(temp_name,"(*%s)",(yyvsp[-5].id));
		     fprintf(f_header,"typedef ");
		     emit_extern_func(temp_name, (yyvsp[-8].type),(yyvsp[-2].pl),0,f_header);
		   }
		   strcpy((yyvsp[-8].type)->name,"<function ptr>");
		   (yyvsp[-8].type)->type = T_USER;
		   (yyvsp[-8].type)->is_pointer = 1;
		   (yyvsp[-8].type)->typedef_add((yyvsp[-5].id),1);
		   cplus_register_type((yyvsp[-5].id));
		 }
		 delete (yyvsp[-8].type);
		 delete (yyvsp[-5].id);
		 delete (yyvsp[-2].pl);
	       }
#line 4056 "y.tab.c" /* yacc.c:1646  */
    break;

  case 89:
#line 1530 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   init_language();
		   if ((yyvsp[-10].ivalue)) {
		     (yyvsp[-9].type)->is_pointer += (yyvsp[-8].ivalue);
		     sprintf(temp_name,"(*%s)",(yyvsp[-5].id));
		     fprintf(f_header,"typedef ");
		     emit_extern_func(temp_name, (yyvsp[-9].type),(yyvsp[-2].pl),0,f_header);
		   }

		   /* Typedef'd pointer */
		   strcpy((yyvsp[-9].type)->name,"<function ptr>");
		   (yyvsp[-9].type)->type = T_USER;
		   (yyvsp[-9].type)->is_pointer = 1;
		   (yyvsp[-9].type)->typedef_add((yyvsp[-5].id),1);
		   cplus_register_type((yyvsp[-5].id));
		 }
		 delete (yyvsp[-9].type);
		 delete (yyvsp[-5].id);
		 delete (yyvsp[-2].pl);
	       }
#line 4082 "y.tab.c" /* yacc.c:1646  */
    break;

  case 90:
#line 1554 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   init_language();
		   Active_typedef = new DataType((yyvsp[-2].type));
		   // This datatype is going to be readonly
			
		   (yyvsp[-2].type)->status = STAT_READONLY | STAT_REPLACETYPE;
		   (yyvsp[-2].type)->is_pointer += (yyvsp[-1].decl).is_pointer;
		   // Turn this into a "pointer" corresponding to the array
		   (yyvsp[-2].type)->is_pointer++;
		   (yyvsp[-2].type)->arraystr = copy_string(ArrayString);
		   (yyvsp[-2].type)->typedef_add((yyvsp[-1].decl).id);
		   fprintf(stderr,"%s : Line %d. Warning. Array type %s will be read-only without a typemap\n",input_file,line_number, (yyvsp[-1].decl).id);
		   cplus_register_type((yyvsp[-1].decl).id);

		 }
	       }
#line 4104 "y.tab.c" /* yacc.c:1646  */
    break;

  case 91:
#line 1570 "parser.y" /* yacc.c:1646  */
    { }
#line 4110 "y.tab.c" /* yacc.c:1646  */
    break;

  case 92:
#line 1583 "parser.y" /* yacc.c:1646  */
    {
                if (allow) {
		  if (Active_typedef) {
		    DataType *t;
		    t = new DataType(Active_typedef);
		    t->is_pointer += (yyvsp[-1].decl).is_pointer;
		    t->typedef_add((yyvsp[-1].decl).id);
		    cplus_register_type((yyvsp[-1].decl).id);
		    delete t;
		  }
		}
              }
#line 4127 "y.tab.c" /* yacc.c:1646  */
    break;

  case 93:
#line 1595 "parser.y" /* yacc.c:1646  */
    {
		    DataType *t;
		    t = new DataType(Active_typedef);
		    t->status = STAT_READONLY | STAT_REPLACETYPE;
		    t->is_pointer += (yyvsp[-1].decl).is_pointer + 1;
		    t->arraystr = copy_string(ArrayString);
		    t->typedef_add((yyvsp[-1].decl).id);
		    cplus_register_type((yyvsp[-1].decl).id);
		    delete t;
    		    fprintf(stderr,"%s : Line %d. Warning. Array type %s will be read-only without a typemap.\n",input_file,line_number, (yyvsp[-1].decl).id);
	      }
#line 4143 "y.tab.c" /* yacc.c:1646  */
    break;

  case 94:
#line 1606 "parser.y" /* yacc.c:1646  */
    { }
#line 4149 "y.tab.c" /* yacc.c:1646  */
    break;

  case 95:
#line 1626 "parser.y" /* yacc.c:1646  */
    {
		 /* Push old if-then-else status */
		 if_push();
		 /* Look a symbol up in the symbol table */
		 if (lookup_symbol((yyvsp[0].id))) {
		   in_then = 1;
		   in_else = 0;
		   allow = 1 & prev_allow;
		 } else {
		   /* Condition is false.   Skip over whatever is in this block */
		   in_else = skip_cond(1);
		   if (in_else == -1) {
		     /* Unrecoverable error */
		     SWIG_exit(1);
		   }
		   if (!in_else) {
		     if_pop();        // Pop out. Reached end of block
		   } else {
		     allow = prev_allow;
		     in_then = 0;
		   }
		 }
                }
#line 4177 "y.tab.c" /* yacc.c:1646  */
    break;

  case 96:
#line 1652 "parser.y" /* yacc.c:1646  */
    {
		 if_push();
		 if (lookup_symbol((yyvsp[0].id))) {
		   /* Condition is false.   Skip over whatever is in this block */
		   in_else = skip_cond(1);
		   if (in_else == -1) {
		     /* Unrecoverable error */
		     SWIG_exit(1);
		   }
		   if (!in_else) {
		     if_pop();        // Pop out. Reached end of block
		   } else {
		     allow = prev_allow;
		     in_then = 0;
		   }
		 } else {
		   in_then = 1;
		   in_else = 0;		   
		   allow = 1 & prev_allow;
		 }
	       }
#line 4203 "y.tab.c" /* yacc.c:1646  */
    break;

  case 97:
#line 1675 "parser.y" /* yacc.c:1646  */
    {
		 if ((!in_then) || (in_else)) {
		   fprintf(stderr,"%s : Line %d. Misplaced else\n", input_file, line_number);
		   FatalError();
		 } else {
		   in_then = 0;
		   in_else = 1;
		   if (allow) {
		     allow = 0;
		     /* Skip over rest of the conditional */
		     skip_cond(0);
		     if_pop();
		   } else {
		     allow = 1;
		   }
		   allow = allow & prev_allow;
		 }
	       }
#line 4226 "y.tab.c" /* yacc.c:1646  */
    break;

  case 98:
#line 1694 "parser.y" /* yacc.c:1646  */
    {
		 if ((!in_then) && (!in_else)) {
		   fprintf(stderr,"%s : Line %d. Misplaced endif\n", input_file, line_number);
		   FatalError();
		 } else {
		   if_pop();
		 }
	       }
#line 4239 "y.tab.c" /* yacc.c:1646  */
    break;

  case 99:
#line 1704 "parser.y" /* yacc.c:1646  */
    {
		 /* Push old if-then-else status */
		 if_push();
		 if ((yyvsp[0].ivalue)) {
		   in_then = 1;
		   in_else = 0;
		   allow = 1 & prev_allow;
		 } else {
		   /* Condition is false.   Skip over whatever is in this block */
		   in_else = skip_cond(1);
		   if (in_else == -1) {
		     /* Unrecoverable error */
		     SWIG_exit(1);
		   }
		   if (!in_else) {
		     if_pop();        // Pop out. Reached end of block
		   } else {
		     allow = prev_allow;
		     in_then = 0;
		   }
		 }
	       }
#line 4266 "y.tab.c" /* yacc.c:1646  */
    break;

  case 100:
#line 1730 "parser.y" /* yacc.c:1646  */
    {
		 /* have to pop old if clause off */
		 if_pop();

		 /* Push old if-then-else status */
		 if_push();
		 if ((yyvsp[0].ivalue)) {
		   in_then = 1;
		   in_else = 0;
		   allow = 1 & prev_allow;
		 } else {
		   /* Condition is false.   Skip over whatever is in this block */
		   in_else = skip_cond(1);
		   if (in_else == -1) {
		     /* Unrecoverable error */
		     SWIG_exit(1);
		   }
		   if (!in_else) {
		     if_pop();        // Pop out. Reached end of block
		   } else {
		     allow = prev_allow;
		     in_then = 0;
		   }
		 }
	       }
#line 4296 "y.tab.c" /* yacc.c:1646  */
    break;

  case 101:
#line 1759 "parser.y" /* yacc.c:1646  */
    {

                 /* Look ID up in the symbol table */
                    if (lookup_symbol((yyvsp[-1].id))) {
		      (yyval.ivalue) = 1;
		    } else {
		      (yyval.ivalue) = 0;
		    }
               }
#line 4310 "y.tab.c" /* yacc.c:1646  */
    break;

  case 102:
#line 1768 "parser.y" /* yacc.c:1646  */
    {
		 if (lookup_symbol((yyvsp[0].id))) {
		   (yyval.ivalue) = 1;
		 } else {
		   (yyval.ivalue) = 0;
		 }
	       }
#line 4322 "y.tab.c" /* yacc.c:1646  */
    break;

  case 103:
#line 1775 "parser.y" /* yacc.c:1646  */
    {
                      if ((yyvsp[0].ivalue)) (yyval.ivalue) = 0;
		      else (yyval.ivalue) = 1;
	       }
#line 4331 "y.tab.c" /* yacc.c:1646  */
    break;

  case 104:
#line 1781 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern))
		   lang->pragma((yyvsp[-4].id),(yyvsp[-2].id),(yyvsp[-1].id));
		   fprintf(stderr,"%s : Line %d. Warning. '%%pragma(lang,opt=value)' syntax is obsolete.\n",
			   input_file,line_number);
		   fprintf(stderr,"        Use '%%pragma(lang) opt=value' instead.\n");
	       }
#line 4343 "y.tab.c" /* yacc.c:1646  */
    break;

  case 105:
#line 1789 "parser.y" /* yacc.c:1646  */
    {
                 if (allow && (!WrapExtern)) 
		   swig_pragma((yyvsp[-1].id),(yyvsp[0].id));
    	       }
#line 4352 "y.tab.c" /* yacc.c:1646  */
    break;

  case 106:
#line 1793 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern))
		   lang->pragma((yyvsp[-3].id),(yyvsp[-1].id),(yyvsp[0].id));
	       }
#line 4361 "y.tab.c" /* yacc.c:1646  */
    break;

  case 107:
#line 1801 "parser.y" /* yacc.c:1646  */
    { }
#line 4367 "y.tab.c" /* yacc.c:1646  */
    break;

  case 108:
#line 1802 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   init_language();
		   temp_typeptr = new DataType(Active_type);
		   temp_typeptr->is_pointer += (yyvsp[-2].decl).is_pointer;
		   if ((yyvsp[-1].ivalue) > 0) {
		     temp_typeptr->is_pointer++;
		     temp_typeptr->status = STAT_READONLY;
		     temp_typeptr->arraystr = copy_string(ArrayString);
		   }
		   if ((yyvsp[-2].decl).is_reference) {
		     fprintf(stderr,"%s : Line %d. Error. Linkage to C++ reference not allowed.\n", input_file, line_number);
		     FatalError();
		   } else {
		     if (temp_typeptr->qualifier) {
		       if ((strcmp(temp_typeptr->qualifier,"const") == 0)) {
			 /* Okay.  This is really some sort of C++ constant here. */
			 if ((yyvsp[0].dtype).type != T_ERROR)
			   create_constant((yyvsp[-2].decl).id, temp_typeptr, (yyvsp[0].dtype).id);
		       } else 
			 create_variable(Active_extern,(yyvsp[-2].decl).id, temp_typeptr);
		     } else
		       create_variable(Active_extern, (yyvsp[-2].decl).id, temp_typeptr);
		   }
		   delete temp_typeptr;
		 }
	       }
#line 4399 "y.tab.c" /* yacc.c:1646  */
    break;

  case 109:
#line 1828 "parser.y" /* yacc.c:1646  */
    { }
#line 4405 "y.tab.c" /* yacc.c:1646  */
    break;

  case 110:
#line 1829 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   init_language();
		   temp_typeptr = new DataType(Active_type);
		   temp_typeptr->is_pointer += (yyvsp[-4].decl).is_pointer;
		   temp_typeptr->is_reference = (yyvsp[-4].decl).is_reference;
		   create_function(Active_extern, (yyvsp[-4].decl).id, temp_typeptr, (yyvsp[-2].pl));
		   delete temp_typeptr;
		 }
		 delete (yyvsp[-2].pl);
	       }
#line 4421 "y.tab.c" /* yacc.c:1646  */
    break;

  case 111:
#line 1839 "parser.y" /* yacc.c:1646  */
    { }
#line 4427 "y.tab.c" /* yacc.c:1646  */
    break;

  case 112:
#line 1842 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.dtype) = (yyvsp[-1].dtype);
                 }
#line 4435 "y.tab.c" /* yacc.c:1646  */
    break;

  case 113:
#line 1845 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.dtype).type = T_SYMBOL;
	       }
#line 4443 "y.tab.c" /* yacc.c:1646  */
    break;

  case 114:
#line 1848 "parser.y" /* yacc.c:1646  */
    {
		 if (Verbose) 
		   fprintf(stderr,"%s : Line %d.  Warning. Unable to parse #define (ignored)\n", input_file, line_number);
		 (yyval.dtype).type = T_ERROR;
	       }
#line 4453 "y.tab.c" /* yacc.c:1646  */
    break;

  case 115:
#line 1856 "parser.y" /* yacc.c:1646  */
    { (yyval.ivalue) = 1; }
#line 4459 "y.tab.c" /* yacc.c:1646  */
    break;

  case 116:
#line 1857 "parser.y" /* yacc.c:1646  */
    {(yyval.ivalue) = 0; }
#line 4465 "y.tab.c" /* yacc.c:1646  */
    break;

  case 117:
#line 1858 "parser.y" /* yacc.c:1646  */
    {
		 if (strcmp((yyvsp[0].id),"C") == 0) {
		   (yyval.ivalue) = 2;
		 } else {
		   fprintf(stderr,"%s : Line %d.  Unrecognized extern type \"%s\" (ignored).\n", input_file, line_number, (yyvsp[0].id));
		   FatalError();
		 }
	       }
#line 4478 "y.tab.c" /* yacc.c:1646  */
    break;

  case 118:
#line 1870 "parser.y" /* yacc.c:1646  */
    { skip_brace(); }
#line 4484 "y.tab.c" /* yacc.c:1646  */
    break;

  case 119:
#line 1879 "parser.y" /* yacc.c:1646  */
    {
                 if (((yyvsp[-1].p)->t->type != T_VOID) || ((yyvsp[-1].p)->t->is_pointer))
		   (yyvsp[0].pl)->insert((yyvsp[-1].p),0);
		 (yyval.pl) = (yyvsp[0].pl);
		 delete (yyvsp[-1].p);
		}
#line 4495 "y.tab.c" /* yacc.c:1646  */
    break;

  case 120:
#line 1885 "parser.y" /* yacc.c:1646  */
    { (yyval.pl) = new ParmList;}
#line 4501 "y.tab.c" /* yacc.c:1646  */
    break;

  case 121:
#line 1888 "parser.y" /* yacc.c:1646  */
    {
		 (yyvsp[0].pl)->insert((yyvsp[-1].p),0);
		 (yyval.pl) = (yyvsp[0].pl);
		 delete (yyvsp[-1].p);
                }
#line 4511 "y.tab.c" /* yacc.c:1646  */
    break;

  case 122:
#line 1893 "parser.y" /* yacc.c:1646  */
    { (yyval.pl) = new ParmList;}
#line 4517 "y.tab.c" /* yacc.c:1646  */
    break;

  case 123:
#line 1896 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.p) = (yyvsp[0].p);
		  if (typemap_check("ignore",typemap_lang,(yyval.p)->t,(yyval.p)->name))
		    (yyval.p)->ignore = 1;
               }
#line 4527 "y.tab.c" /* yacc.c:1646  */
    break;

  case 124:
#line 1901 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.p) = (yyvsp[0].p);
                  (yyval.p)->call_type = (yyval.p)->call_type | (yyvsp[-1].ivalue);
		  if (InArray && ((yyval.p)->call_type & CALL_VALUE)) {
		     fprintf(stderr,"%s : Line %d. Error. Can't use %%val with an array.\n", input_file, line_number);
		     FatalError();
		  }
		  if (!(yyval.p)->t->is_pointer) {
		     fprintf(stderr,"%s : Line %d. Error. Can't use %%val or %%out with a non-pointer argument.\n", input_file, line_number);
		     FatalError();
		  } else {
		    (yyval.p)->t->is_pointer--;
		  }
		}
#line 4546 "y.tab.c" /* yacc.c:1646  */
    break;

  case 125:
#line 1916 "parser.y" /* yacc.c:1646  */
    {
		    if (InArray) {
		      (yyvsp[-1].type)->is_pointer++;
		      if (Verbose) {
			fprintf(stderr,"%s : Line %d. Warning. Array %s", input_file, line_number, (yyvsp[-1].type)->print_type());
			print_array();
			fprintf(stderr," has been converted to %s.\n", (yyvsp[-1].type)->print_type());
		      }
		      // Add array string to the type
		      (yyvsp[-1].type)->arraystr = copy_string(ArrayString.get());
		    } 
		    (yyval.p) = new Parm((yyvsp[-1].type),(yyvsp[0].id));
		    (yyval.p)->call_type = 0;
		    (yyval.p)->defvalue = DefArg;
		    if (((yyvsp[-1].type)->type == T_USER) && !((yyvsp[-1].type)->is_pointer)) {
		      if (Verbose)
			fprintf(stderr,"%s : Line %d. Warning : Parameter of type '%s'\nhas been remapped to '%s *' and will be called using *((%s *) ptr).\n",
				input_file, line_number, (yyvsp[-1].type)->name, (yyvsp[-1].type)->name, (yyvsp[-1].type)->name);

		      (yyval.p)->call_type = CALL_REFERENCE;
		      (yyval.p)->t->is_pointer++;
		    }
		    delete (yyvsp[-1].type);
		    delete (yyvsp[0].id);
                 }
#line 4576 "y.tab.c" /* yacc.c:1646  */
    break;

  case 126:
#line 1942 "parser.y" /* yacc.c:1646  */
    {
		   (yyval.p) = new Parm((yyvsp[-2].type),(yyvsp[0].id));
		   (yyval.p)->t->is_pointer += (yyvsp[-1].ivalue);
		   (yyval.p)->call_type = 0;
		   (yyval.p)->defvalue = DefArg;
		   if (InArray) {
		     (yyval.p)->t->is_pointer++;
		     if (Verbose) {
		       fprintf(stderr,"%s : Line %d. Warning. Array %s", input_file, line_number, (yyval.p)->t->print_type());
		       print_array();
		       fprintf(stderr," has been converted to %s.\n", (yyval.p)->t->print_type());
		     }
		     // Add array string to the type
		     (yyval.p)->t->arraystr = copy_string(ArrayString.get());
		    }
		   delete (yyvsp[-2].type);
		   delete (yyvsp[0].id);
		}
#line 4599 "y.tab.c" /* yacc.c:1646  */
    break;

  case 127:
#line 1961 "parser.y" /* yacc.c:1646  */
    {
		  (yyval.p) = new Parm((yyvsp[-2].type),(yyvsp[0].id));
		  (yyval.p)->t->is_reference = 1;
		  (yyval.p)->call_type = 0;
		  (yyval.p)->t->is_pointer++;
		  (yyval.p)->defvalue = DefArg;
		  if (!CPlusPlus) {
			fprintf(stderr,"%s : Line %d. Warning.  Use of C++ Reference detected.  Use the -c++ option.\n", input_file, line_number);
		  }
		  delete (yyvsp[-2].type);
		  delete (yyvsp[0].id);
		}
#line 4616 "y.tab.c" /* yacc.c:1646  */
    break;

  case 128:
#line 1973 "parser.y" /* yacc.c:1646  */
    {
                  fprintf(stderr,"%s : Line %d. Error. Function pointer not allowed (remap with typedef).\n", input_file, line_number);
		  FatalError();
		  (yyval.p) = new Parm((yyvsp[-7].type),(yyvsp[-4].id));
		  (yyval.p)->t->type = T_ERROR;
		  (yyval.p)->name = copy_string((yyvsp[-4].id));
		  strcpy((yyval.p)->t->name,"<function ptr>");
		  delete (yyvsp[-7].type);
		  delete (yyvsp[-4].id);
		  delete (yyvsp[-1].pl);
		}
#line 4632 "y.tab.c" /* yacc.c:1646  */
    break;

  case 129:
#line 1984 "parser.y" /* yacc.c:1646  */
    {
                  fprintf(stderr,"%s : Line %d. Variable length arguments not supported (ignored).\n", input_file, line_number);
		  (yyval.p) = new Parm(new DataType(T_INT),(char*)"varargs");
		  (yyval.p)->t->type = T_ERROR;
		  (yyval.p)->name = copy_string("varargs");
		  strcpy((yyval.p)->t->name,"<varargs>");
		  FatalError();
		}
#line 4645 "y.tab.c" /* yacc.c:1646  */
    break;

  case 130:
#line 1994 "parser.y" /* yacc.c:1646  */
    {
                    (yyval.id) = (yyvsp[-1].id); 
                    InArray = 0;
		    if ((yyvsp[0].dtype).type == T_CHAR)
		      DefArg = copy_string(ConstChar);
		    else
		      DefArg = copy_string((yyvsp[0].dtype).id);
                    if ((yyvsp[0].dtype).id) delete (yyvsp[0].dtype).id;
                }
#line 4659 "y.tab.c" /* yacc.c:1646  */
    break;

  case 131:
#line 2003 "parser.y" /* yacc.c:1646  */
    {
                    (yyval.id) = (yyvsp[-1].id); 
                    InArray = (yyvsp[0].ivalue); 
                    DefArg = 0;
               }
#line 4669 "y.tab.c" /* yacc.c:1646  */
    break;

  case 132:
#line 2008 "parser.y" /* yacc.c:1646  */
    {
                         (yyval.id) = new char[1];
                         (yyval.id)[0] = 0;
                         InArray = (yyvsp[0].ivalue);
                         DefArg = 0;
               }
#line 4680 "y.tab.c" /* yacc.c:1646  */
    break;

  case 133:
#line 2014 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = new char[1];
	                 (yyval.id)[0] = 0;
                         InArray = 0;
                         DefArg = 0;
               }
#line 4690 "y.tab.c" /* yacc.c:1646  */
    break;

  case 134:
#line 2021 "parser.y" /* yacc.c:1646  */
    { (yyval.dtype) = (yyvsp[0].dtype); }
#line 4696 "y.tab.c" /* yacc.c:1646  */
    break;

  case 135:
#line 2022 "parser.y" /* yacc.c:1646  */
    {
		 (yyval.dtype).id = new char[strlen((yyvsp[0].id))+2];
		 (yyval.dtype).id[0] = '&';
		 strcpy(&(yyval.dtype).id[1], (yyvsp[0].id));
		 (yyval.dtype).type = T_USER;
	       }
#line 4707 "y.tab.c" /* yacc.c:1646  */
    break;

  case 136:
#line 2028 "parser.y" /* yacc.c:1646  */
    {
		 skip_brace();
		 (yyval.dtype).id = 0; (yyval.dtype).type = T_INT;
	       }
#line 4716 "y.tab.c" /* yacc.c:1646  */
    break;

  case 137:
#line 2032 "parser.y" /* yacc.c:1646  */
    {
               }
#line 4723 "y.tab.c" /* yacc.c:1646  */
    break;

  case 138:
#line 2034 "parser.y" /* yacc.c:1646  */
    {(yyval.dtype).id = 0; (yyval.dtype).type = T_INT;}
#line 4729 "y.tab.c" /* yacc.c:1646  */
    break;

  case 139:
#line 2037 "parser.y" /* yacc.c:1646  */
    { (yyval.ivalue) = CALL_VALUE; }
#line 4735 "y.tab.c" /* yacc.c:1646  */
    break;

  case 140:
#line 2038 "parser.y" /* yacc.c:1646  */
    { (yyval.ivalue) = CALL_OUTPUT; }
#line 4741 "y.tab.c" /* yacc.c:1646  */
    break;

  case 141:
#line 2041 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.ivalue) = (yyvsp[-1].ivalue) | (yyvsp[0].ivalue);
               }
#line 4749 "y.tab.c" /* yacc.c:1646  */
    break;

  case 142:
#line 2044 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.ivalue) = (yyvsp[0].ivalue);
	       }
#line 4757 "y.tab.c" /* yacc.c:1646  */
    break;

  case 143:
#line 2051 "parser.y" /* yacc.c:1646  */
    { (yyval.decl).id = (yyvsp[0].id);
                      (yyval.decl).is_pointer = 0;
		      (yyval.decl).is_reference = 0;
                }
#line 4766 "y.tab.c" /* yacc.c:1646  */
    break;

  case 144:
#line 2055 "parser.y" /* yacc.c:1646  */
    {
                      (yyval.decl).id = (yyvsp[0].id);
		      (yyval.decl).is_pointer = (yyvsp[-1].ivalue);
		      (yyval.decl).is_reference = 0;
	       }
#line 4776 "y.tab.c" /* yacc.c:1646  */
    break;

  case 145:
#line 2060 "parser.y" /* yacc.c:1646  */
    {
		      (yyval.decl).id = (yyvsp[0].id);
		      (yyval.decl).is_pointer = 1;
		      (yyval.decl).is_reference = 1;
		      if (!CPlusPlus) {
			fprintf(stderr,"%s : Line %d. Warning.  Use of C++ Reference detected.  Use the -c++ option.\n", input_file, line_number);
		      }
	       }
#line 4789 "y.tab.c" /* yacc.c:1646  */
    break;

  case 146:
#line 2070 "parser.y" /* yacc.c:1646  */
    { (yyval.ivalue) = 1; }
#line 4795 "y.tab.c" /* yacc.c:1646  */
    break;

  case 147:
#line 2071 "parser.y" /* yacc.c:1646  */
    { (yyval.ivalue) = (yyvsp[0].ivalue) + 1;}
#line 4801 "y.tab.c" /* yacc.c:1646  */
    break;

  case 148:
#line 2075 "parser.y" /* yacc.c:1646  */
    {
		 (yyval.ivalue) = (yyvsp[0].ivalue) + 1;
		 "[]" >> ArrayString;
              }
#line 4810 "y.tab.c" /* yacc.c:1646  */
    break;

  case 149:
#line 2079 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.ivalue) = (yyvsp[0].ivalue) + 1;
		 "]" >> ArrayString;
		 (yyvsp[-2].dtype).id >> ArrayString;
		 "[" >> ArrayString;
              }
#line 4821 "y.tab.c" /* yacc.c:1646  */
    break;

  case 150:
#line 2086 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.ivalue) = (yyvsp[0].ivalue);
              }
#line 4829 "y.tab.c" /* yacc.c:1646  */
    break;

  case 151:
#line 2089 "parser.y" /* yacc.c:1646  */
    { (yyval.ivalue) = 0;
                        ArrayString = "";
              }
#line 4837 "y.tab.c" /* yacc.c:1646  */
    break;

  case 152:
#line 2097 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
               }
#line 4845 "y.tab.c" /* yacc.c:1646  */
    break;

  case 153:
#line 2100 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
	       }
#line 4853 "y.tab.c" /* yacc.c:1646  */
    break;

  case 154:
#line 2103 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
	       }
#line 4861 "y.tab.c" /* yacc.c:1646  */
    break;

  case 155:
#line 2106 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 4869 "y.tab.c" /* yacc.c:1646  */
    break;

  case 156:
#line 2109 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 4877 "y.tab.c" /* yacc.c:1646  */
    break;

  case 157:
#line 2112 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 4885 "y.tab.c" /* yacc.c:1646  */
    break;

  case 158:
#line 2115 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 4893 "y.tab.c" /* yacc.c:1646  */
    break;

  case 159:
#line 2118 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 4901 "y.tab.c" /* yacc.c:1646  */
    break;

  case 160:
#line 2121 "parser.y" /* yacc.c:1646  */
    {
                   if ((yyvsp[0].type)) (yyval.type) = (yyvsp[0].type);
		   else (yyval.type) = (yyvsp[-1].type);
	       }
#line 4910 "y.tab.c" /* yacc.c:1646  */
    break;

  case 161:
#line 2125 "parser.y" /* yacc.c:1646  */
    {
                   if ((yyvsp[0].type)) (yyval.type) = (yyvsp[0].type);
		   else (yyval.type) = (yyvsp[-1].type);
	       }
#line 4919 "y.tab.c" /* yacc.c:1646  */
    break;

  case 162:
#line 2129 "parser.y" /* yacc.c:1646  */
    {
		 (yyval.type) = (yyvsp[-1].type);
		 if (strlen((yyvsp[0].id)) > 0) {
		    if ((strlen((yyvsp[0].id)) + strlen((yyval.type)->name)) >= MAX_NAME) {
		      fprintf(stderr,"%s : Line %d. Fatal error. Type-name is too long!\n", 
			      input_file, line_number);
		    } else {
		      strcat((yyval.type)->name,(yyvsp[0].id));
		    }
		  }
	       }
#line 4935 "y.tab.c" /* yacc.c:1646  */
    break;

  case 163:
#line 2140 "parser.y" /* yacc.c:1646  */
    {
		  (yyval.type) = new DataType;
		  strcpy((yyval.type)->name,(yyvsp[-1].id));
		  (yyval.type)->type = T_USER;
		  /* Do a typedef lookup */
		  (yyval.type)->typedef_resolve();
		  if (strlen((yyvsp[0].id)) > 0) {
		    if ((strlen((yyvsp[0].id)) + strlen((yyval.type)->name)) >= MAX_NAME) {
		      fprintf(stderr,"%s : Line %d. Fatal error. Type-name is too long!\n", 
			      input_file, line_number);
		    } else {
		      strcat((yyval.type)->name,(yyvsp[0].id));
		    }
		  }
	       }
#line 4955 "y.tab.c" /* yacc.c:1646  */
    break;

  case 164:
#line 2155 "parser.y" /* yacc.c:1646  */
    {
		  (yyval.type) = (yyvsp[0].type);
                  (yyval.type)->qualifier = new char[6];
		  strcpy((yyval.type)->qualifier,"const");
     	       }
#line 4965 "y.tab.c" /* yacc.c:1646  */
    break;

  case 165:
#line 2160 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.type) = new DataType;
		  sprintf((yyval.type)->name,"%s %s",(yyvsp[-1].id), (yyvsp[0].id));
		  (yyval.type)->type = T_USER;
	       }
#line 4975 "y.tab.c" /* yacc.c:1646  */
    break;

  case 166:
#line 2165 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.type) = new DataType;
                  sprintf((yyval.type)->name,"%s::%s",(yyvsp[-2].id),(yyvsp[0].id));
                  (yyval.type)->type = T_USER;
		  (yyval.type)->typedef_resolve();
               }
#line 4986 "y.tab.c" /* yacc.c:1646  */
    break;

  case 167:
#line 2174 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.type) = new DataType;
                  sprintf((yyval.type)->name,"%s", (yyvsp[0].id));
                  (yyval.type)->type = T_USER;
                  (yyval.type)->typedef_resolve(1);
               }
#line 4997 "y.tab.c" /* yacc.c:1646  */
    break;

  case 168:
#line 2180 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.type) = new DataType;
                  sprintf((yyval.type)->name,"enum %s", (yyvsp[0].id));
                  (yyval.type)->type = T_INT;
                  (yyval.type)->typedef_resolve(1);
               }
#line 5008 "y.tab.c" /* yacc.c:1646  */
    break;

  case 169:
#line 2190 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
               }
#line 5016 "y.tab.c" /* yacc.c:1646  */
    break;

  case 170:
#line 2193 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
	       }
#line 5024 "y.tab.c" /* yacc.c:1646  */
    break;

  case 171:
#line 2196 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
	       }
#line 5032 "y.tab.c" /* yacc.c:1646  */
    break;

  case 172:
#line 2199 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 5040 "y.tab.c" /* yacc.c:1646  */
    break;

  case 173:
#line 2202 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 5048 "y.tab.c" /* yacc.c:1646  */
    break;

  case 174:
#line 2205 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 5056 "y.tab.c" /* yacc.c:1646  */
    break;

  case 175:
#line 2208 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 5064 "y.tab.c" /* yacc.c:1646  */
    break;

  case 176:
#line 2211 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
	       }
#line 5072 "y.tab.c" /* yacc.c:1646  */
    break;

  case 177:
#line 2214 "parser.y" /* yacc.c:1646  */
    {
                   if ((yyvsp[0].type)) (yyval.type) = (yyvsp[0].type);
		   else (yyval.type) = (yyvsp[-1].type);
	       }
#line 5081 "y.tab.c" /* yacc.c:1646  */
    break;

  case 178:
#line 2218 "parser.y" /* yacc.c:1646  */
    {
                   if ((yyvsp[0].type)) (yyval.type) = (yyvsp[0].type);
		   else (yyval.type) = (yyvsp[-1].type);
	       }
#line 5090 "y.tab.c" /* yacc.c:1646  */
    break;

  case 179:
#line 2222 "parser.y" /* yacc.c:1646  */
    {
		   (yyval.type) = (yyvsp[-1].type);
		   strcat((yyval.type)->name,(yyvsp[0].id));
	       }
#line 5099 "y.tab.c" /* yacc.c:1646  */
    break;

  case 180:
#line 2226 "parser.y" /* yacc.c:1646  */
    {
		  (yyval.type) = (yyvsp[0].type);
                  (yyval.type)->qualifier = new char[6];
		  strcpy((yyval.type)->qualifier,"const");
     	       }
#line 5109 "y.tab.c" /* yacc.c:1646  */
    break;

  case 181:
#line 2231 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.type) = new DataType;
		  sprintf((yyval.type)->name,"%s %s",(yyvsp[-1].id), (yyvsp[0].id));
		  (yyval.type)->type = T_USER;
	       }
#line 5119 "y.tab.c" /* yacc.c:1646  */
    break;

  case 182:
#line 2240 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (DataType *) 0;
               }
#line 5127 "y.tab.c" /* yacc.c:1646  */
    break;

  case 183:
#line 2243 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
		   (yyval.type)->type = T_INT;
		   sprintf(temp_name,"signed %s",(yyvsp[0].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5138 "y.tab.c" /* yacc.c:1646  */
    break;

  case 184:
#line 2249 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
		   (yyval.type)->type = T_SHORT;
		   sprintf(temp_name,"signed %s",(yyvsp[-1].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5149 "y.tab.c" /* yacc.c:1646  */
    break;

  case 185:
#line 2255 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
		   (yyval.type)->type = T_LONG;
		   sprintf(temp_name,"signed %s",(yyvsp[-1].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5160 "y.tab.c" /* yacc.c:1646  */
    break;

  case 186:
#line 2261 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
		   (yyval.type)->type = T_SCHAR;
		   sprintf(temp_name,"signed %s",(yyvsp[0].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5171 "y.tab.c" /* yacc.c:1646  */
    break;

  case 187:
#line 2271 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (DataType *) 0;
               }
#line 5179 "y.tab.c" /* yacc.c:1646  */
    break;

  case 188:
#line 2274 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
		   (yyval.type)->type = T_UINT;
		   sprintf(temp_name,"unsigned %s",(yyvsp[0].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5190 "y.tab.c" /* yacc.c:1646  */
    break;

  case 189:
#line 2280 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
		   (yyval.type)->type = T_USHORT;
		   sprintf(temp_name,"unsigned %s",(yyvsp[-1].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5201 "y.tab.c" /* yacc.c:1646  */
    break;

  case 190:
#line 2286 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[-1].type);
		   (yyval.type)->type = T_ULONG;
		   sprintf(temp_name,"unsigned %s",(yyvsp[-1].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5212 "y.tab.c" /* yacc.c:1646  */
    break;

  case 191:
#line 2292 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.type) = (yyvsp[0].type);
		   (yyval.type)->type = T_UCHAR;
		   sprintf(temp_name,"unsigned %s",(yyvsp[0].type)->name);
		   strcpy((yyval.type)->name,temp_name);
	       }
#line 5223 "y.tab.c" /* yacc.c:1646  */
    break;

  case 192:
#line 2300 "parser.y" /* yacc.c:1646  */
    { }
#line 5229 "y.tab.c" /* yacc.c:1646  */
    break;

  case 193:
#line 2301 "parser.y" /* yacc.c:1646  */
    { }
#line 5235 "y.tab.c" /* yacc.c:1646  */
    break;

  case 194:
#line 2304 "parser.y" /* yacc.c:1646  */
    { scanner_check_typedef(); }
#line 5241 "y.tab.c" /* yacc.c:1646  */
    break;

  case 195:
#line 2304 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.dtype) = (yyvsp[0].dtype);
		   scanner_ignore_typedef();
		   if (ConstChar) delete ConstChar;
		   ConstChar = 0;
                }
#line 5252 "y.tab.c" /* yacc.c:1646  */
    break;

  case 196:
#line 2310 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.dtype).id = (yyvsp[0].id);
                   (yyval.dtype).type = T_CHAR;
		   if (ConstChar) delete ConstChar;
		   ConstChar = new char[strlen((yyvsp[0].id))+3];
		   sprintf(ConstChar,"\"%s\"",(yyvsp[0].id));
		}
#line 5264 "y.tab.c" /* yacc.c:1646  */
    break;

  case 197:
#line 2317 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.dtype).id = (yyvsp[0].id);
		   (yyval.dtype).type = T_CHAR;
		   if (ConstChar) delete ConstChar;
		   ConstChar = new char[strlen((yyvsp[0].id))+3];
		   sprintf(ConstChar,"'%s'",(yyvsp[0].id));
		 }
#line 5276 "y.tab.c" /* yacc.c:1646  */
    break;

  case 198:
#line 2329 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.ilist) = (yyvsp[-2].ilist);
		 (yyval.ilist).names[(yyval.ilist).count] = copy_string((yyvsp[0].id));
		 (yyval.ilist).count++;
		 (yyval.ilist).names[(yyval.ilist).count] = (char *) 0;
                }
#line 5287 "y.tab.c" /* yacc.c:1646  */
    break;

  case 199:
#line 2335 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.ilist).names = new char *[NI_NAMES];
		 (yyval.ilist).count = 0;
		 for (i = 0; i < NI_NAMES; i++) 
		   (yyval.ilist).names[i] = (char *) 0;
	       }
#line 5298 "y.tab.c" /* yacc.c:1646  */
    break;

  case 200:
#line 2345 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (yyvsp[0].id); }
#line 5304 "y.tab.c" /* yacc.c:1646  */
    break;

  case 201:
#line 2346 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (char *) 0;}
#line 5310 "y.tab.c" /* yacc.c:1646  */
    break;

  case 202:
#line 2352 "parser.y" /* yacc.c:1646  */
    {}
#line 5316 "y.tab.c" /* yacc.c:1646  */
    break;

  case 203:
#line 2353 "parser.y" /* yacc.c:1646  */
    {}
#line 5322 "y.tab.c" /* yacc.c:1646  */
    break;

  case 204:
#line 2357 "parser.y" /* yacc.c:1646  */
    {
		   temp_typeptr = new DataType(T_INT);
		   create_constant((yyvsp[0].id), temp_typeptr, (yyvsp[0].id));
		   delete temp_typeptr;
		 }
#line 5332 "y.tab.c" /* yacc.c:1646  */
    break;

  case 205:
#line 2362 "parser.y" /* yacc.c:1646  */
    { scanner_check_typedef();}
#line 5338 "y.tab.c" /* yacc.c:1646  */
    break;

  case 206:
#line 2362 "parser.y" /* yacc.c:1646  */
    {
		   temp_typeptr = new DataType((yyvsp[0].dtype).type);
// Use enum name instead of value
// OLD		   create_constant($1, temp_typeptr, $4.id);
                   create_constant((yyvsp[-3].id), temp_typeptr, (yyvsp[-3].id));
		   delete temp_typeptr;
                 }
#line 5350 "y.tab.c" /* yacc.c:1646  */
    break;

  case 207:
#line 2369 "parser.y" /* yacc.c:1646  */
    { }
#line 5356 "y.tab.c" /* yacc.c:1646  */
    break;

  case 208:
#line 2370 "parser.y" /* yacc.c:1646  */
    { }
#line 5362 "y.tab.c" /* yacc.c:1646  */
    break;

  case 209:
#line 2373 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.dtype) = (yyvsp[0].dtype);
		   if (((yyval.dtype).type != T_INT) && ((yyval.dtype).type != T_UINT) &&
		       ((yyval.dtype).type != T_LONG) && ((yyval.dtype).type != T_ULONG) &&
		       ((yyval.dtype).type != T_SHORT) && ((yyval.dtype).type != T_USHORT) && 
		       ((yyval.dtype).type != T_SCHAR) && ((yyval.dtype).type != T_UCHAR)) {
		     fprintf(stderr,"%s : Lind %d. Type error. Expecting an int\n",
			     input_file, line_number);
		     FatalError();
		   }

                }
#line 5379 "y.tab.c" /* yacc.c:1646  */
    break;

  case 210:
#line 2385 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.dtype).id = (yyvsp[0].id);
		   (yyval.dtype).type = T_CHAR;
		 }
#line 5388 "y.tab.c" /* yacc.c:1646  */
    break;

  case 211:
#line 2396 "parser.y" /* yacc.c:1646  */
    { 
                  (yyval.dtype).id = (yyvsp[0].id);
                  (yyval.dtype).type = T_INT;
                 }
#line 5397 "y.tab.c" /* yacc.c:1646  */
    break;

  case 212:
#line 2400 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.dtype).id = (yyvsp[0].id);
                  (yyval.dtype).type = T_DOUBLE;
               }
#line 5406 "y.tab.c" /* yacc.c:1646  */
    break;

  case 213:
#line 2404 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.dtype).id = (yyvsp[0].id);
		  (yyval.dtype).type = T_UINT;
	       }
#line 5415 "y.tab.c" /* yacc.c:1646  */
    break;

  case 214:
#line 2408 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.dtype).id = (yyvsp[0].id);
		  (yyval.dtype).type = T_LONG;
	       }
#line 5424 "y.tab.c" /* yacc.c:1646  */
    break;

  case 215:
#line 2412 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.dtype).id = (yyvsp[0].id);
		  (yyval.dtype).type = T_ULONG;
	       }
#line 5433 "y.tab.c" /* yacc.c:1646  */
    break;

  case 216:
#line 2416 "parser.y" /* yacc.c:1646  */
    {
	          (yyval.dtype).id = new char[strlen((yyvsp[-1].type)->name)+9];
		  sprintf((yyval.dtype).id,"sizeof(%s)", (yyvsp[-1].type)->name);
		  (yyval.dtype).type = T_INT;
	       }
#line 5443 "y.tab.c" /* yacc.c:1646  */
    break;

  case 217:
#line 2421 "parser.y" /* yacc.c:1646  */
    {
		  (yyval.dtype).id = new char[strlen((yyvsp[0].dtype).id)+strlen((yyvsp[-2].type)->name)+3];
		  sprintf((yyval.dtype).id,"(%s)%s",(yyvsp[-2].type)->name,(yyvsp[0].dtype).id);
		  (yyval.dtype).type = (yyvsp[-2].type)->type;
	       }
#line 5453 "y.tab.c" /* yacc.c:1646  */
    break;

  case 218:
#line 2426 "parser.y" /* yacc.c:1646  */
    {
		 (yyval.dtype).id = lookup_symvalue((yyvsp[0].id));
		 if ((yyval.dtype).id == (char *) 0)
		   (yyval.dtype).id = (yyvsp[0].id);
		 else {
		   (yyval.dtype).id = new char[strlen((yyval.dtype).id)+3];
		   sprintf((yyval.dtype).id,"(%s)",lookup_symvalue((yyvsp[0].id)));
		 }
		 temp_typeptr = lookup_symtype((yyvsp[0].id));
		 if (temp_typeptr) (yyval.dtype).type = temp_typeptr->type;
		 else (yyval.dtype).type = T_INT;
               }
#line 5470 "y.tab.c" /* yacc.c:1646  */
    break;

  case 219:
#line 2438 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.dtype).id = new char[strlen((yyvsp[-2].id))+strlen((yyvsp[0].id))+3];
		  sprintf((yyval.dtype).id,"%s::%s",(yyvsp[-2].id),(yyvsp[0].id));
                  (yyval.dtype).type = T_INT;
		  delete (yyvsp[-2].id);
		  delete (yyvsp[0].id);
               }
#line 5482 "y.tab.c" /* yacc.c:1646  */
    break;

  case 220:
#line 2445 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"+");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;
	       }
#line 5493 "y.tab.c" /* yacc.c:1646  */
    break;

  case 221:
#line 2451 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"-");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;
	       }
#line 5504 "y.tab.c" /* yacc.c:1646  */
    break;

  case 222:
#line 2457 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"*");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5516 "y.tab.c" /* yacc.c:1646  */
    break;

  case 223:
#line 2464 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"/");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5528 "y.tab.c" /* yacc.c:1646  */
    break;

  case 224:
#line 2471 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"&");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 if (((yyvsp[-2].dtype).type == T_DOUBLE) || ((yyvsp[0].dtype).type == T_DOUBLE)) {
		   fprintf(stderr,"%s : Line %d. Type error in constant expression (expecting integers).\n", input_file, line_number);
		   FatalError();
		 }
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5544 "y.tab.c" /* yacc.c:1646  */
    break;

  case 225:
#line 2482 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"|");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 if (((yyvsp[-2].dtype).type == T_DOUBLE) || ((yyvsp[0].dtype).type == T_DOUBLE)) {
		   fprintf(stderr,"%s : Line %d. Type error in constant expression (expecting integers).\n", input_file, line_number);
		   FatalError();
		 }
		 (yyval.dtype).type = T_INT;
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5561 "y.tab.c" /* yacc.c:1646  */
    break;

  case 226:
#line 2494 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"^");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 if (((yyvsp[-2].dtype).type == T_DOUBLE) || ((yyvsp[0].dtype).type == T_DOUBLE)) {
		   fprintf(stderr,"%s : Line %d. Type error in constant expression (expecting integers).\n", input_file, line_number);
		   FatalError();
		 }
		 (yyval.dtype).type = T_INT;
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5578 "y.tab.c" /* yacc.c:1646  */
    break;

  case 227:
#line 2506 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,"<<");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 if (((yyvsp[-2].dtype).type == T_DOUBLE) || ((yyvsp[0].dtype).type == T_DOUBLE)) {
		   fprintf(stderr,"%s : Line %d. Type error in constant expression (expecting integers).\n", input_file, line_number);
		   FatalError();
		 }
		 (yyval.dtype).type = T_INT;
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5595 "y.tab.c" /* yacc.c:1646  */
    break;

  case 228:
#line 2518 "parser.y" /* yacc.c:1646  */
    {
	         E_BINARY((yyval.dtype).id,(yyvsp[-2].dtype).id,(yyvsp[0].dtype).id,">>");
		 (yyval.dtype).type = promote((yyvsp[-2].dtype).type,(yyvsp[0].dtype).type);
		 if (((yyvsp[-2].dtype).type == T_DOUBLE) || ((yyvsp[0].dtype).type == T_DOUBLE)) {
		   fprintf(stderr,"%s : Line %d. Type error in constant expression (expecting integers).\n", input_file, line_number);
		   FatalError();
		 }
		 (yyval.dtype).type = T_INT;
		 delete (yyvsp[-2].dtype).id;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5612 "y.tab.c" /* yacc.c:1646  */
    break;

  case 229:
#line 2530 "parser.y" /* yacc.c:1646  */
    {
	          (yyval.dtype).id = new char[strlen((yyvsp[0].dtype).id)+2];
		  sprintf((yyval.dtype).id,"-%s",(yyvsp[0].dtype).id);
		  (yyval.dtype).type = (yyvsp[0].dtype).type;
		 delete (yyvsp[0].dtype).id;

	       }
#line 5624 "y.tab.c" /* yacc.c:1646  */
    break;

  case 230:
#line 2537 "parser.y" /* yacc.c:1646  */
    {
	          (yyval.dtype).id = new char[strlen((yyvsp[0].dtype).id)+2];
		  sprintf((yyval.dtype).id,"~%s",(yyvsp[0].dtype).id);
		  if ((yyvsp[0].dtype).type == T_DOUBLE) {
		   fprintf(stderr,"%s : Line %d. Type error in constant expression (expecting integers).\n", input_file, line_number);
		   FatalError();
		  }
		  (yyval.dtype).type = (yyvsp[0].dtype).type;
		  delete (yyvsp[0].dtype).id;
	       }
#line 5639 "y.tab.c" /* yacc.c:1646  */
    break;

  case 231:
#line 2547 "parser.y" /* yacc.c:1646  */
    {
	          (yyval.dtype).id = new char[strlen((yyvsp[-1].dtype).id)+3];
	          sprintf((yyval.dtype).id,"(%s)", (yyvsp[-1].dtype).id);
		  (yyval.dtype).type = (yyvsp[-1].dtype).type;
		  delete (yyvsp[-1].dtype).id;
	       }
#line 5650 "y.tab.c" /* yacc.c:1646  */
    break;

  case 232:
#line 2558 "parser.y" /* yacc.c:1646  */
    { }
#line 5656 "y.tab.c" /* yacc.c:1646  */
    break;

  case 233:
#line 2559 "parser.y" /* yacc.c:1646  */
    {}
#line 5662 "y.tab.c" /* yacc.c:1646  */
    break;

  case 234:
#line 2565 "parser.y" /* yacc.c:1646  */
    {
	       char *iname;
	       if (allow) {
		 init_language();
		 DataType::new_scope();

		 sprintf(temp_name,"CPP_CLASS:%s\n",(yyvsp[-2].id));
		 if (add_symbol(temp_name, (DataType *) 0, (char *) 0)) {
		   fprintf(stderr,"%s : Line %d. Error. %s %s is multiply defined.\n", input_file, line_number, (yyvsp[-3].id), (yyvsp[-2].id));
		   FatalError();
		 }
		 if ((!CPlusPlus) && (strcmp((yyvsp[-3].id),"class") == 0))
		   fprintf(stderr,"%s : Line %d. *** WARNING ***. C++ mode is disabled (enable using -c++)\n", input_file, line_number);

		 iname = make_name((yyvsp[-2].id));
		 doc_entry = new DocClass(iname, doc_parent());
		 if (iname == (yyvsp[-2].id)) 
		   cplus_open_class((yyvsp[-2].id), 0, (yyvsp[-3].id));
		 else
		   cplus_open_class((yyvsp[-2].id), iname, (yyvsp[-3].id));
		 if (strcmp((yyvsp[-3].id),"class") == 0)
		   cplus_mode = CPLUS_PRIVATE;
		 else
		   cplus_mode = CPLUS_PUBLIC;
		 doc_stack_top++;
		 doc_stack[doc_stack_top] = doc_entry;
		 scanner_clear_start();
		 nested_list = 0;
		 // Merge in scope from base classes
		 cplus_inherit_scope((yyvsp[-1].ilist).count,(yyvsp[-1].ilist).names);
	       }
              }
#line 5699 "y.tab.c" /* yacc.c:1646  */
    break;

  case 235:
#line 2596 "parser.y" /* yacc.c:1646  */
    {
		if (allow) {
		  if ((yyvsp[-4].ilist).names) {
		    if (strcmp((yyvsp[-6].id),"union") != 0)
		      cplus_inherit((yyvsp[-4].ilist).count, (yyvsp[-4].ilist).names);
		    else {
		      fprintf(stderr,"%s : Line %d.  Inheritance not allowed for unions.\n",input_file, line_number);
		      FatalError();
		    }
		  }
		  // Clean up the inheritance list
		  if ((yyvsp[-4].ilist).names) {
		    int j;
		    for (j = 0; j < (yyvsp[-4].ilist).count; j++) {
		      if ((yyvsp[-4].ilist).names[j]) delete [] (yyvsp[-4].ilist).names[j];
		    }
		    delete [] (yyvsp[-4].ilist).names;
		  }

		  // Dumped nested declarations (if applicable)
		  dump_nested((yyvsp[-5].id));

		  // Save and collapse current scope
		  cplus_register_scope(DataType::collapse_scope((yyvsp[-5].id)));

		  // Restore the original doc entry for this class
		  doc_entry = doc_stack[doc_stack_top];
		  cplus_class_close((char *) 0); 
		  doc_entry = 0;
		  // Bump the documentation stack back down
		  doc_stack_top--;
		  cplus_mode = CPLUS_PUBLIC;
		}
	      }
#line 5738 "y.tab.c" /* yacc.c:1646  */
    break;

  case 236:
#line 2633 "parser.y" /* yacc.c:1646  */
    {
	       if (allow) {
		 char *iname;
		 init_language();
		 DataType::new_scope();

		 sprintf(temp_name,"CPP_CLASS:%s\n",(yyvsp[-2].id));
		 if (add_symbol(temp_name, (DataType *) 0, (char *) 0)) {
		   fprintf(stderr,"%s : Line %d. Error. %s %s is multiply defined.\n", input_file, line_number, (yyvsp[-3].id), (yyvsp[-2].id));
		   FatalError();
		 }
		 if ((!CPlusPlus) && (strcmp((yyvsp[-3].id),"class") == 0))
		   fprintf(stderr,"%s : Line %d. *** WARNING ***. C++ mode is disabled (enable using -c++)\n", input_file, line_number);
		 
		 iname = make_name((yyvsp[-2].id));
		 doc_entry = new DocClass(iname, doc_parent());
		 if ((yyvsp[-2].id) == iname) 
		   cplus_open_class((yyvsp[-2].id), 0, (yyvsp[-3].id));
		 else
		   cplus_open_class((yyvsp[-2].id), iname, (yyvsp[-3].id));
		 if (strcmp((yyvsp[-3].id),"class") == 0)
		   cplus_mode = CPLUS_PRIVATE;
		 else
		   cplus_mode = CPLUS_PUBLIC;
		 // Create a documentation entry for the class
		 doc_stack_top++;
		 doc_stack[doc_stack_top] = doc_entry;
		 scanner_clear_start();
		 nested_list = 0;

		 // Merge in scope from base classes
		 cplus_inherit_scope((yyvsp[-1].ilist).count,(yyvsp[-1].ilist).names);

	       }
              }
#line 5778 "y.tab.c" /* yacc.c:1646  */
    break;

  case 237:
#line 2667 "parser.y" /* yacc.c:1646  */
    {
		if (allow) {
		  if ((yyvsp[-5].ilist).names) {
		    if (strcmp((yyvsp[-7].id),"union") != 0)
		      cplus_inherit((yyvsp[-5].ilist).count, (yyvsp[-5].ilist).names);
		    else {
		      fprintf(stderr,"%s : Line %d.  Inheritance not allowed for unions.\n",input_file, line_number);
		      FatalError();
		    }
		  }
		  // Create a datatype for correctly processing the typedef
		  Active_typedef = new DataType();
		  Active_typedef->type = T_USER;
		  sprintf(Active_typedef->name,"%s %s", (yyvsp[-7].id),(yyvsp[-6].id));
		  Active_typedef->is_pointer = 0;
		  Active_typedef->implicit_ptr = 0;

		  // Clean up the inheritance list
		  if ((yyvsp[-5].ilist).names) {
		    int j;
		    for (j = 0; j < (yyvsp[-5].ilist).count; j++) {
		      if ((yyvsp[-5].ilist).names[j]) delete [] (yyvsp[-5].ilist).names[j];
		    }
		    delete [] (yyvsp[-5].ilist).names;
		  }

		  if ((yyvsp[0].decl).is_pointer > 0) {
		    fprintf(stderr,"%s : Line %d.  typedef struct { } *id not supported properly. Winging it...\n", input_file, line_number);

		  }
		  // Create dump nested class code
		  if ((yyvsp[0].decl).is_pointer > 0) {
		    dump_nested((yyvsp[-6].id));
		  } else {
		    dump_nested((yyvsp[0].decl).id);
		  }
		    
		  // Collapse any datatypes created in the the class

		  cplus_register_scope(DataType::collapse_scope((yyvsp[-6].id)));

		  doc_entry = doc_stack[doc_stack_top];
		  if ((yyvsp[0].decl).is_pointer > 0) {
		    cplus_class_close((yyvsp[-6].id));
		  } else {
		    cplus_class_close((yyvsp[0].decl).id); 
		  }
		  doc_stack_top--;
		  doc_entry = 0;

		  // Create a typedef in global scope

		  if ((yyvsp[0].decl).is_pointer == 0)
		    Active_typedef->typedef_add((yyvsp[0].decl).id);
		  else {
		    DataType *t = new DataType(Active_typedef);
		    t->is_pointer += (yyvsp[0].decl).is_pointer;
		    t->typedef_add((yyvsp[0].decl).id);
		    cplus_register_type((yyvsp[0].decl).id);
		    delete t;
		  }
		  cplus_mode = CPLUS_PUBLIC;
		}
	      }
#line 5847 "y.tab.c" /* yacc.c:1646  */
    break;

  case 238:
#line 2730 "parser.y" /* yacc.c:1646  */
    { }
#line 5853 "y.tab.c" /* yacc.c:1646  */
    break;

  case 239:
#line 2734 "parser.y" /* yacc.c:1646  */
    {
	       char *iname;
	       if (allow) {
		 init_language();
		 DataType::new_scope();
		 if ((!CPlusPlus) && (strcmp((yyvsp[-1].id),"class") == 0))
		   fprintf(stderr,"%s : Line %d. *** WARNING ***. C++ mode is disabled (enable using -c++)\n", input_file, line_number);
		 
		 iname = make_name((char*)"");
		 doc_entry = new DocClass(iname,doc_parent());
		 if (strlen(iname))
		   cplus_open_class("", iname, (yyvsp[-1].id));
		 else
		   cplus_open_class("",0,(yyvsp[-1].id));
		 if (strcmp((yyvsp[-1].id),"class") == 0)
		   cplus_mode = CPLUS_PRIVATE;
		 else
		   cplus_mode = CPLUS_PUBLIC;
		 doc_stack_top++;
		 doc_stack[doc_stack_top] = doc_entry;
		 scanner_clear_start();
		 nested_list = 0;
	       }
              }
#line 5882 "y.tab.c" /* yacc.c:1646  */
    break;

  case 240:
#line 2757 "parser.y" /* yacc.c:1646  */
    {
		if (allow) {
		  if ((yyvsp[0].decl).is_pointer > 0) {
		    fprintf(stderr,"%s : Line %d. typedef %s {} *%s not supported correctly. Will be ignored.\n", input_file, line_number, (yyvsp[-5].id), (yyvsp[0].decl).id);
		    cplus_abort();
		  } else {
		    sprintf(temp_name,"CPP_CLASS:%s\n",(yyvsp[0].decl).id);
		    if (add_symbol(temp_name, (DataType *) 0, (char *) 0)) {
		      fprintf(stderr,"%s : Line %d. Error. %s %s is multiply defined.\n", input_file, line_number, (yyvsp[-5].id), (yyvsp[0].decl).id);
		      FatalError();
		    }
		  }
		  // Create a datatype for correctly processing the typedef
		  Active_typedef = new DataType();
		  Active_typedef->type = T_USER;
		  sprintf(Active_typedef->name,"%s",(yyvsp[0].decl).id);
		  Active_typedef->is_pointer = 0;
		  Active_typedef->implicit_ptr = 0;
		  
		  // Dump nested classes
		  if ((yyvsp[0].decl).is_pointer == 0)  
		    dump_nested((yyvsp[0].decl).id);

		  // Go back to previous scope

		  cplus_register_scope(DataType::collapse_scope((char *) 0));
		  
		  doc_entry = doc_stack[doc_stack_top];
		  // Change name of doc_entry
		  doc_entry->name = copy_string((yyvsp[0].decl).id);
		  if ((yyvsp[0].decl).is_pointer == 0) 
		    cplus_class_close((yyvsp[0].decl).id); 
		  doc_entry = 0;
		  doc_stack_top--;
		  cplus_mode = CPLUS_PUBLIC;
		}
	      }
#line 5924 "y.tab.c" /* yacc.c:1646  */
    break;

  case 241:
#line 2793 "parser.y" /* yacc.c:1646  */
    { }
#line 5930 "y.tab.c" /* yacc.c:1646  */
    break;

  case 242:
#line 2798 "parser.y" /* yacc.c:1646  */
    {
	       char *iname;
		 if (allow) {
		   init_language();
		   iname = make_name((yyvsp[-1].id));
		   lang->cpp_class_decl((yyvsp[-1].id),iname,(yyvsp[-2].id));
		 }
	     }
#line 5943 "y.tab.c" /* yacc.c:1646  */
    break;

  case 243:
#line 2809 "parser.y" /* yacc.c:1646  */
    {
	       if (allow) {
		 init_language();
		 if (!CPlusPlus) 
		   fprintf(stderr,"%s : Line %d. *** WARNING ***. C++ mode is disabled (enable using -c++)\n", input_file, line_number);
		 
		 (yyvsp[-7].type)->is_pointer += (yyvsp[-6].decl).is_pointer;
		 (yyvsp[-7].type)->is_reference = (yyvsp[-6].decl).is_reference;
		 // Fix up the function name
		 sprintf(temp_name,"%s::%s",(yyvsp[-6].decl).id,(yyvsp[-4].id));
		 if (!Rename_true) {
		   Rename_true = 1;
		   sprintf(yy_rename,"%s_%s",(yyvsp[-6].decl).id,(yyvsp[-4].id));
		 }
		 create_function((yyvsp[-8].ivalue), temp_name, (yyvsp[-7].type), (yyvsp[-2].pl));
	       }
	       delete (yyvsp[-7].type);
	       delete (yyvsp[-2].pl);
	      }
#line 5967 "y.tab.c" /* yacc.c:1646  */
    break;

  case 244:
#line 2830 "parser.y" /* yacc.c:1646  */
    {
	       if (allow) {
		 init_language();
		 if (!CPlusPlus) 
		   fprintf(stderr,"%s : Line %d. *** WARNING ***. C++ mode is disabled (enable using -c++)\n", input_file, line_number);

		 (yyvsp[-4].type)->is_pointer += (yyvsp[-3].decl).is_pointer;
		 // Fix up the function name
		 sprintf(temp_name,"%s::%s",(yyvsp[-3].decl).id,(yyvsp[-1].id));
		 if (!Rename_true) {
		   Rename_true = 1;
		   sprintf(yy_rename,"%s_%s",(yyvsp[-3].decl).id,(yyvsp[-1].id));
		 }
		 create_variable((yyvsp[-5].ivalue),temp_name, (yyvsp[-4].type));
	       }
	       delete (yyvsp[-4].type);
	     }
#line 5989 "y.tab.c" /* yacc.c:1646  */
    break;

  case 245:
#line 2850 "parser.y" /* yacc.c:1646  */
    {
	       fprintf(stderr,"%s : Line %d. Operator overloading not supported (ignored).\n", input_file, line_number);
		skip_decl();
		delete (yyvsp[-3].type);
	     }
#line 5999 "y.tab.c" /* yacc.c:1646  */
    break;

  case 246:
#line 2858 "parser.y" /* yacc.c:1646  */
    {
	       fprintf(stderr,"%s : Line %d. Templates not currently supported (ignored).\n",
		       input_file, line_number);
	       skip_decl();
	     }
#line 6009 "y.tab.c" /* yacc.c:1646  */
    break;

  case 247:
#line 2866 "parser.y" /* yacc.c:1646  */
    {
	       cplus_mode = CPLUS_PUBLIC;
               doc_entry = cplus_set_class((yyvsp[-1].id));
	       if (!doc_entry) {
		 doc_entry = new DocClass((yyvsp[-1].id),doc_parent());
	       };
	       doc_stack_top++;
	       doc_stack[doc_stack_top] = doc_entry;
	       scanner_clear_start();
	       AddMethods = 1;
	     }
#line 6025 "y.tab.c" /* yacc.c:1646  */
    break;

  case 248:
#line 2876 "parser.y" /* yacc.c:1646  */
    {
	       cplus_unset_class();
	       doc_entry = 0;
	       doc_stack_top--;
	       AddMethods = 0;
	     }
#line 6036 "y.tab.c" /* yacc.c:1646  */
    break;

  case 249:
#line 2884 "parser.y" /* yacc.c:1646  */
    { }
#line 6042 "y.tab.c" /* yacc.c:1646  */
    break;

  case 250:
#line 2885 "parser.y" /* yacc.c:1646  */
    { }
#line 6048 "y.tab.c" /* yacc.c:1646  */
    break;

  case 251:
#line 2886 "parser.y" /* yacc.c:1646  */
    { }
#line 6054 "y.tab.c" /* yacc.c:1646  */
    break;

  case 252:
#line 2889 "parser.y" /* yacc.c:1646  */
    {}
#line 6060 "y.tab.c" /* yacc.c:1646  */
    break;

  case 253:
#line 2890 "parser.y" /* yacc.c:1646  */
    {
	           AddMethods = 1;
	     }
#line 6068 "y.tab.c" /* yacc.c:1646  */
    break;

  case 254:
#line 2892 "parser.y" /* yacc.c:1646  */
    {
	           AddMethods = 0;
	     }
#line 6076 "y.tab.c" /* yacc.c:1646  */
    break;

  case 255:
#line 2894 "parser.y" /* yacc.c:1646  */
    { }
#line 6082 "y.tab.c" /* yacc.c:1646  */
    break;

  case 256:
#line 2895 "parser.y" /* yacc.c:1646  */
    {
	       skip_decl();
		   {
		     static int last_error_line = -1;
		     if (last_error_line != line_number) {
		       fprintf(stderr,"%s : Line %d. Syntax error in input.\n", input_file, line_number);
		       FatalError();
		       last_error_line = line_number;
		     }
		   }
	     }
#line 6098 "y.tab.c" /* yacc.c:1646  */
    break;

  case 257:
#line 2905 "parser.y" /* yacc.c:1646  */
    { }
#line 6104 "y.tab.c" /* yacc.c:1646  */
    break;

  case 258:
#line 2906 "parser.y" /* yacc.c:1646  */
    { }
#line 6110 "y.tab.c" /* yacc.c:1646  */
    break;

  case 259:
#line 2909 "parser.y" /* yacc.c:1646  */
    {
                char *iname;
                if (allow) {
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		    Stat_func++;
		    (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		    (yyvsp[-5].type)->is_reference = (yyvsp[-4].decl).is_reference;
		    if (Verbose) {
		      fprintf(stderr,"Wrapping member function : %s\n",(yyvsp[-4].decl).id);
		    }
		    iname = make_name((yyvsp[-4].decl).id);
		    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		    if (iname == (yyvsp[-4].decl).id) iname = 0;
		    cplus_member_func((yyvsp[-4].decl).id, iname, (yyvsp[-5].type),(yyvsp[-2].pl),0);
		  }
		  scanner_clear_start();
		}
		delete (yyvsp[-5].type);
		delete (yyvsp[-2].pl);
              }
#line 6136 "y.tab.c" /* yacc.c:1646  */
    break;

  case 260:
#line 2933 "parser.y" /* yacc.c:1646  */
    {
	       char *iname;
	       if (allow) {
		 init_language();
		 if (cplus_mode == CPLUS_PUBLIC) {
		   Stat_func++;
		   (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		   (yyvsp[-5].type)->is_reference = (yyvsp[-4].decl).is_reference;
		   if (Verbose) {
		     fprintf(stderr,"Wrapping virtual member function : %s\n",(yyvsp[-4].decl).id);
		   }
		   iname = make_name((yyvsp[-4].decl).id);
		   doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		   if (iname == (yyvsp[-4].decl).id) iname = 0;
		   cplus_member_func((yyvsp[-4].decl).id,iname,(yyvsp[-5].type),(yyvsp[-2].pl),1);
		 }
		 scanner_clear_start();
	       }
	       delete (yyvsp[-5].type);
	       delete (yyvsp[-2].pl);
	     }
#line 6162 "y.tab.c" /* yacc.c:1646  */
    break;

  case 261:
#line 2956 "parser.y" /* yacc.c:1646  */
    {
		char *iname;
		if (allow) {
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		    Stat_func++;
		    if (Verbose) {
		      fprintf(stderr,"Wrapping C++ constructor %s\n", (yyvsp[-4].id));
		    }
		    iname = make_name((yyvsp[-4].id));
		    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		    if (iname == (yyvsp[-4].id)) iname = 0;
		    cplus_constructor((yyvsp[-4].id),iname, (yyvsp[-2].pl));
		  }
		  scanner_clear_start();
		}
		delete (yyvsp[-2].pl);
	      }
#line 6185 "y.tab.c" /* yacc.c:1646  */
    break;

  case 262:
#line 2977 "parser.y" /* yacc.c:1646  */
    {
		char *iname;
		if (allow) {
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		    Stat_func++;
		    if (Verbose) {
		      fprintf(stderr,"Wrapping C++ destructor %s\n", (yyvsp[-4].id));
		    }
		    iname = make_name((yyvsp[-4].id));
		    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		    if (iname == (yyvsp[-4].id)) iname = 0;
		    cplus_destructor((yyvsp[-4].id),iname);
		  }
		}
		scanner_clear_start();
	      }
#line 6207 "y.tab.c" /* yacc.c:1646  */
    break;

  case 263:
#line 2997 "parser.y" /* yacc.c:1646  */
    {
 	        char *iname;
		if (allow) {
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		    Stat_func++;
		    if (Verbose) {
		      fprintf(stderr,"Wrapping C++ destructor %s\n", (yyvsp[-3].id));
		    }
		    iname = make_name((yyvsp[-3].id));
		    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		    if (iname == (yyvsp[-3].id)) iname = 0;
		    cplus_destructor((yyvsp[-3].id),iname);
		  }
		}
		scanner_clear_start();
	      }
#line 6229 "y.tab.c" /* yacc.c:1646  */
    break;

  case 264:
#line 3017 "parser.y" /* yacc.c:1646  */
    {
		if (allow) {
		  char *iname;
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		    if (Active_type) delete Active_type;
		    Active_type = new DataType((yyvsp[-2].type));
		    (yyvsp[-2].type)->is_pointer += (yyvsp[-1].decl).is_pointer;
		    (yyvsp[-2].type)->is_reference = (yyvsp[-1].decl).is_reference;
		    if ((yyvsp[-2].type)->qualifier) {
		      if ((strcmp((yyvsp[-2].type)->qualifier,"const") == 0) && ((yyvsp[-2].type)->is_pointer == 0)) {
			// Okay.  This is really some sort of C++ constant here.
	  	          if ((yyvsp[0].dtype).type != T_ERROR) {
			    iname = make_name((yyvsp[-1].decl).id);
			    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
			    if (iname == (yyvsp[-1].decl).id) iname = 0;
			    cplus_declare_const((yyvsp[-1].decl).id,iname, (yyvsp[-2].type), (yyvsp[0].dtype).id);
			  }
		      } else {
			int oldstatus = Status;
			char *tm;
			if ((yyvsp[-2].type)->status & STAT_READONLY) {
			  if (!(tm = typemap_lookup("memberin",typemap_lang,(yyvsp[-2].type),(yyvsp[-1].decl).id,"",""))) 
			    Status = Status | STAT_READONLY;
			}
			iname = make_name((yyvsp[-1].decl).id);
			doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
			if (iname == (yyvsp[-1].decl).id) iname = 0;
			cplus_variable((yyvsp[-1].decl).id,iname,(yyvsp[-2].type));
			Status = oldstatus;
		      }
		    } else {
		      char *tm = 0;
		      int oldstatus = Status;
		      if ((yyvsp[-2].type)->status & STAT_READONLY) {
			if (!(tm = typemap_lookup("memberin",typemap_lang,(yyvsp[-2].type),(yyvsp[-1].decl).id,"",""))) 
			  Status = Status | STAT_READONLY;
		      }
		      iname = make_name((yyvsp[-1].decl).id);
		      doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		      if (iname == (yyvsp[-1].decl).id) iname = 0;
		      cplus_variable((yyvsp[-1].decl).id,iname,(yyvsp[-2].type));
		      Status = oldstatus;
		      if (Verbose) {
			fprintf(stderr,"Wrapping member data %s\n", (yyvsp[-1].decl).id);
		      }
		    }
		  }
		  scanner_clear_start();
		}
		delete (yyvsp[-2].type);
	      }
#line 6286 "y.tab.c" /* yacc.c:1646  */
    break;

  case 265:
#line 3068 "parser.y" /* yacc.c:1646  */
    { }
#line 6292 "y.tab.c" /* yacc.c:1646  */
    break;

  case 266:
#line 3070 "parser.y" /* yacc.c:1646  */
    {
		char *iname;
		if (allow) {
		  int oldstatus = Status;
		  char *tm = 0;
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		    if (Active_type) delete Active_type;
		    Active_type = new DataType((yyvsp[-3].type));
		    (yyvsp[-3].type)->is_pointer += (yyvsp[-2].decl).is_pointer + 1;
		    (yyvsp[-3].type)->is_reference = (yyvsp[-2].decl).is_reference;
		    (yyvsp[-3].type)->arraystr = copy_string(ArrayString);
		    if (!(tm = typemap_lookup("memberin",typemap_lang,(yyvsp[-3].type),(yyvsp[-2].decl).id,"",""))) 
		      Status = STAT_READONLY;

		    iname = make_name((yyvsp[-2].decl).id);
		    doc_entry = new DocDecl(iname, doc_stack[doc_stack_top]);
		    if (iname == (yyvsp[-2].decl).id) iname = 0;
		    cplus_variable((yyvsp[-2].decl).id,iname,(yyvsp[-3].type));
		    Status = oldstatus;
		    if (!tm)
		      fprintf(stderr,"%s : Line %d. Warning. Array member will be read-only.\n",input_file,line_number);
		  }
		scanner_clear_start();
		}
		delete (yyvsp[-3].type);
	      }
#line 6324 "y.tab.c" /* yacc.c:1646  */
    break;

  case 267:
#line 3101 "parser.y" /* yacc.c:1646  */
    {
		char *iname;
		if (allow) {
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		    (yyvsp[-1].type)->is_pointer += (yyvsp[0].decl).is_pointer;
		    iname = make_name((yyvsp[0].decl).id);
		    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		    if (iname == (yyvsp[0].decl).id) iname = 0;
		    cplus_static_var((yyvsp[0].decl).id,iname,(yyvsp[-1].type));
		    if (Active_type) delete Active_type;
		    Active_type = new DataType((yyvsp[-1].type));
		    if (Verbose) {
		      fprintf(stderr,"Wrapping static member data %s\n", (yyvsp[0].decl).id);
		    }
		  }
		  scanner_clear_start();
		}
		delete (yyvsp[-1].type);
	      }
#line 6349 "y.tab.c" /* yacc.c:1646  */
    break;

  case 268:
#line 3120 "parser.y" /* yacc.c:1646  */
    { }
#line 6355 "y.tab.c" /* yacc.c:1646  */
    break;

  case 269:
#line 3124 "parser.y" /* yacc.c:1646  */
    {
		char *iname;
		if (allow) {
		  (yyvsp[-5].type)->is_pointer += (yyvsp[-4].decl).is_pointer;
		  (yyvsp[-5].type)->is_reference = (yyvsp[-4].decl).is_reference;
		  if (cplus_mode == CPLUS_PUBLIC) {
		    iname = make_name((yyvsp[-4].decl).id);
		    doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		    if (iname == (yyvsp[-4].decl).id) iname = 0;
		    cplus_static_func((yyvsp[-4].decl).id, iname, (yyvsp[-5].type), (yyvsp[-2].pl));
		    if (Verbose)
		      fprintf(stderr,"Wrapping static member function %s\n",(yyvsp[-4].decl).id);
		  }
		  scanner_clear_start();
		}
		delete (yyvsp[-5].type);
		delete (yyvsp[-2].pl);
	      }
#line 6378 "y.tab.c" /* yacc.c:1646  */
    break;

  case 270:
#line 3144 "parser.y" /* yacc.c:1646  */
    {
		if (allow) {
		  cplus_mode = CPLUS_PUBLIC;
		  if (Verbose)
		    fprintf(stderr,"Public mode\n");
		  scanner_clear_start();
		}
	      }
#line 6391 "y.tab.c" /* yacc.c:1646  */
    break;

  case 271:
#line 3155 "parser.y" /* yacc.c:1646  */
    {
		if (allow) {
		  cplus_mode = CPLUS_PRIVATE;
		  if (Verbose)
		    fprintf(stderr,"Private mode\n");
		  scanner_clear_start();
		}
	      }
#line 6404 "y.tab.c" /* yacc.c:1646  */
    break;

  case 272:
#line 3166 "parser.y" /* yacc.c:1646  */
    {
		if (allow) {
		  cplus_mode = CPLUS_PROTECTED;
		  if (Verbose)
		    fprintf(stderr,"Protected mode\n");
		  scanner_clear_start();
		}
	      }
#line 6417 "y.tab.c" /* yacc.c:1646  */
    break;

  case 273:
#line 3177 "parser.y" /* yacc.c:1646  */
    {
	       if (allow) {
		 strcpy(yy_rename,(yyvsp[-1].id));
		 Rename_true = 1;
	       }
	     }
#line 6428 "y.tab.c" /* yacc.c:1646  */
    break;

  case 274:
#line 3185 "parser.y" /* yacc.c:1646  */
    {
                 NewObject = 1;
             }
#line 6436 "y.tab.c" /* yacc.c:1646  */
    break;

  case 275:
#line 3187 "parser.y" /* yacc.c:1646  */
    {
                 NewObject = 0;
             }
#line 6444 "y.tab.c" /* yacc.c:1646  */
    break;

  case 276:
#line 3192 "parser.y" /* yacc.c:1646  */
    {scanner_clear_start();}
#line 6450 "y.tab.c" /* yacc.c:1646  */
    break;

  case 277:
#line 3192 "parser.y" /* yacc.c:1646  */
    {

		 // if ename was supplied.  Install it as a new integer datatype.

		if (allow) {
		  init_language();
		  if (cplus_mode == CPLUS_PUBLIC) {
		   if ((yyvsp[-5].id)) {
		     cplus_register_type((yyvsp[-5].id));
		     temp_type.type = T_INT;
		     temp_type.is_pointer = 0;
		     temp_type.implicit_ptr = 0;
		     sprintf(temp_type.name,"int");
		     temp_type.typedef_add((yyvsp[-5].id),1); 
		   }
		 }
	       }
	      }
#line 6473 "y.tab.c" /* yacc.c:1646  */
    break;

  case 278:
#line 3210 "parser.y" /* yacc.c:1646  */
    {
		if (allow)
		  Status = Status | STAT_READONLY;
		scanner_clear_start();
              }
#line 6483 "y.tab.c" /* yacc.c:1646  */
    break;

  case 279:
#line 3215 "parser.y" /* yacc.c:1646  */
    {
		if (allow) 
		  Status = Status & ~(STAT_READONLY);
		scanner_clear_start();
	      }
#line 6493 "y.tab.c" /* yacc.c:1646  */
    break;

  case 280:
#line 3221 "parser.y" /* yacc.c:1646  */
    {
		if (allow)
		  fprintf(stderr,"%s : Line %d. Friends are not allowed--members only! (ignored)\n", input_file, line_number);
		skip_decl();
		scanner_clear_start();
	      }
#line 6504 "y.tab.c" /* yacc.c:1646  */
    break;

  case 281:
#line 3229 "parser.y" /* yacc.c:1646  */
    {
		if (allow)
		  fprintf(stderr,"%s : Line %d. Operator overloading not supported (ignored).\n", input_file, line_number);
		skip_decl();
		scanner_clear_start();
	      }
#line 6515 "y.tab.c" /* yacc.c:1646  */
    break;

  case 282:
#line 3235 "parser.y" /* yacc.c:1646  */
    { 
		scanner_clear_start();
	      }
#line 6523 "y.tab.c" /* yacc.c:1646  */
    break;

  case 283:
#line 3240 "parser.y" /* yacc.c:1646  */
    { }
#line 6529 "y.tab.c" /* yacc.c:1646  */
    break;

  case 284:
#line 3244 "parser.y" /* yacc.c:1646  */
    {
	      		scanner_clear_start();
	      }
#line 6537 "y.tab.c" /* yacc.c:1646  */
    break;

  case 285:
#line 3249 "parser.y" /* yacc.c:1646  */
    {
                 if (allow && (!WrapExtern)) { }
    	       }
#line 6545 "y.tab.c" /* yacc.c:1646  */
    break;

  case 286:
#line 3252 "parser.y" /* yacc.c:1646  */
    {
		 if (allow && (!WrapExtern))
                   cplus_add_pragma((yyvsp[-3].id),(yyvsp[-1].id),(yyvsp[0].id));
	       }
#line 6554 "y.tab.c" /* yacc.c:1646  */
    break;

  case 287:
#line 3275 "parser.y" /* yacc.c:1646  */
    { start_line = line_number; skip_brace(); 
	      }
#line 6561 "y.tab.c" /* yacc.c:1646  */
    break;

  case 288:
#line 3276 "parser.y" /* yacc.c:1646  */
    { 

		if (cplus_mode == CPLUS_PUBLIC) {
		  cplus_register_type((yyvsp[-4].id));
		  if ((yyvsp[-1].decl).id) {
		    if (strcmp((yyvsp[-5].id),"class") == 0) {
		      fprintf(stderr,"%s : Line %d.  Warning. Nested classes not currently supported (ignored).\n", input_file, line_number);
		      /* Generate some code for a new class */
		    } else {
		      Nested *n = new Nested;
		      n->code << "typedef " << (yyvsp[-5].id) << " " 
			      << CCode.get() << " $classname_" << (yyvsp[-1].decl).id << ";\n";
		      n->name = copy_string((yyvsp[-1].decl).id);
		      n->line = start_line;
		      n->type = new DataType;
		      n->type->type = T_USER;
		      n->type->is_pointer = (yyvsp[-1].decl).is_pointer;
		      n->type->is_reference = (yyvsp[-1].decl).is_reference;
		      n->next = 0;
		      add_nested(n);
		    }
		  }
		}
	      }
#line 6590 "y.tab.c" /* yacc.c:1646  */
    break;

  case 289:
#line 3301 "parser.y" /* yacc.c:1646  */
    { start_line = line_number; skip_brace();
              }
#line 6597 "y.tab.c" /* yacc.c:1646  */
    break;

  case 290:
#line 3302 "parser.y" /* yacc.c:1646  */
    { 
		if (cplus_mode == CPLUS_PUBLIC) {
		  if (strcmp((yyvsp[-4].id),"class") == 0) {
		    fprintf(stderr,"%s : Line %d.  Warning. Nested classes not currently supported (ignored)\n", input_file, line_number);
		    /* Generate some code for a new class */
		  } else {
		    /* Generate some code for a new class */

		    Nested *n = new Nested;
		    n->code << "typedef " << (yyvsp[-4].id) << " " 
			    << CCode.get() << " $classname_" << (yyvsp[-1].decl).id << ";\n";
		    n->name = copy_string((yyvsp[-1].decl).id);
		    n->line = start_line;
		    n->type = new DataType;
		    n->type->type = T_USER;
		    n->type->is_pointer = (yyvsp[-1].decl).is_pointer;
		    n->type->is_reference = (yyvsp[-1].decl).is_reference;
		    n->next = 0;
		    add_nested(n);

		  }
		}
	      }
#line 6625 "y.tab.c" /* yacc.c:1646  */
    break;

  case 291:
#line 3326 "parser.y" /* yacc.c:1646  */
    {
  		    if (cplus_mode == CPLUS_PUBLIC) {
                       cplus_register_type((yyvsp[-1].id));
                    }
              }
#line 6635 "y.tab.c" /* yacc.c:1646  */
    break;

  case 292:
#line 3333 "parser.y" /* yacc.c:1646  */
    { 
                     skip_decl();
                     fprintf(stderr,"%s : Line %d. Function pointers not currently supported (ignored).\n", input_file, line_number);
		     
	      }
#line 6645 "y.tab.c" /* yacc.c:1646  */
    break;

  case 293:
#line 3338 "parser.y" /* yacc.c:1646  */
    {
                     skip_decl();
                     fprintf(stderr,"%s : Line %d. Function pointers not currently supported (ignored).\n", input_file, line_number);
		     
	      }
#line 6655 "y.tab.c" /* yacc.c:1646  */
    break;

  case 294:
#line 3343 "parser.y" /* yacc.c:1646  */
    { 
                     skip_decl();
                     fprintf(stderr,"%s : Line %d. Function pointers not currently supported (ignored).\n", input_file, line_number);
		     
	      }
#line 6665 "y.tab.c" /* yacc.c:1646  */
    break;

  case 295:
#line 3348 "parser.y" /* yacc.c:1646  */
    { }
#line 6671 "y.tab.c" /* yacc.c:1646  */
    break;

  case 296:
#line 3349 "parser.y" /* yacc.c:1646  */
    { }
#line 6677 "y.tab.c" /* yacc.c:1646  */
    break;

  case 297:
#line 3352 "parser.y" /* yacc.c:1646  */
    { (yyval.decl) = (yyvsp[0].decl);}
#line 6683 "y.tab.c" /* yacc.c:1646  */
    break;

  case 298:
#line 3353 "parser.y" /* yacc.c:1646  */
    { (yyval.decl).id = 0; }
#line 6689 "y.tab.c" /* yacc.c:1646  */
    break;

  case 299:
#line 3356 "parser.y" /* yacc.c:1646  */
    {}
#line 6695 "y.tab.c" /* yacc.c:1646  */
    break;

  case 300:
#line 3357 "parser.y" /* yacc.c:1646  */
    {}
#line 6701 "y.tab.c" /* yacc.c:1646  */
    break;

  case 301:
#line 3358 "parser.y" /* yacc.c:1646  */
    {}
#line 6707 "y.tab.c" /* yacc.c:1646  */
    break;

  case 302:
#line 3361 "parser.y" /* yacc.c:1646  */
    { }
#line 6713 "y.tab.c" /* yacc.c:1646  */
    break;

  case 303:
#line 3362 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   int oldstatus = Status;
		   char *tm;

		   init_language();
		   if (cplus_mode == CPLUS_PUBLIC) {
		     temp_typeptr = new DataType(Active_type);
		     temp_typeptr->is_pointer += (yyvsp[-1].decl).is_pointer;
		     if (Verbose) {
		       fprintf(stderr,"Wrapping member variable : %s\n",(yyvsp[-1].decl).id);
		     }
		     Stat_var++;
		     doc_entry = new DocDecl((yyvsp[-1].decl).id,doc_stack[doc_stack_top]);
		     if (temp_typeptr->status & STAT_READONLY) {
		       if (!(tm = typemap_lookup("memberin",typemap_lang,temp_typeptr,(yyvsp[-1].decl).id,"",""))) 
			 Status = Status | STAT_READONLY;
		     }
		     cplus_variable((yyvsp[-1].decl).id,(char *) 0,temp_typeptr);		
		     Status = oldstatus;
		     delete temp_typeptr;
		   }
		   scanner_clear_start();
		 }
	       }
#line 6743 "y.tab.c" /* yacc.c:1646  */
    break;

  case 304:
#line 3386 "parser.y" /* yacc.c:1646  */
    { }
#line 6749 "y.tab.c" /* yacc.c:1646  */
    break;

  case 305:
#line 3387 "parser.y" /* yacc.c:1646  */
    {
		 if (allow) {
		   int oldstatus = Status;
		   char *tm;

		   init_language();
		   if (cplus_mode == CPLUS_PUBLIC) {
		     temp_typeptr = new DataType(Active_type);
		     temp_typeptr->is_pointer += (yyvsp[-2].decl).is_pointer;
		     if (Verbose) {
		       fprintf(stderr,"Wrapping member variable : %s\n",(yyvsp[-2].decl).id);
		     }
		     Stat_var++;
		     if (!(tm = typemap_lookup("memberin",typemap_lang,temp_typeptr,(yyvsp[-2].decl).id,"",""))) 
		       Status = Status | STAT_READONLY;
		     doc_entry = new DocDecl((yyvsp[-2].decl).id,doc_stack[doc_stack_top]);
		     if (temp_typeptr->status & STAT_READONLY) Status = Status | STAT_READONLY;
		     cplus_variable((yyvsp[-2].decl).id,(char *) 0,temp_typeptr);		
		     Status = oldstatus;
		     if (!tm)
		       fprintf(stderr,"%s : Line %d. Warning. Array member will be read-only.\n",input_file,line_number);
		     delete temp_typeptr;
		   }
		   scanner_clear_start();
		 }
	       }
#line 6780 "y.tab.c" /* yacc.c:1646  */
    break;

  case 306:
#line 3412 "parser.y" /* yacc.c:1646  */
    { }
#line 6786 "y.tab.c" /* yacc.c:1646  */
    break;

  case 307:
#line 3415 "parser.y" /* yacc.c:1646  */
    { 
                    CCode = "";
               }
#line 6794 "y.tab.c" /* yacc.c:1646  */
    break;

  case 308:
#line 3418 "parser.y" /* yacc.c:1646  */
    { skip_brace(); }
#line 6800 "y.tab.c" /* yacc.c:1646  */
    break;

  case 309:
#line 3421 "parser.y" /* yacc.c:1646  */
    { CCode = ""; }
#line 6806 "y.tab.c" /* yacc.c:1646  */
    break;

  case 310:
#line 3422 "parser.y" /* yacc.c:1646  */
    { CCode = ""; }
#line 6812 "y.tab.c" /* yacc.c:1646  */
    break;

  case 311:
#line 3423 "parser.y" /* yacc.c:1646  */
    { skip_brace(); }
#line 6818 "y.tab.c" /* yacc.c:1646  */
    break;

  case 312:
#line 3426 "parser.y" /* yacc.c:1646  */
    {}
#line 6824 "y.tab.c" /* yacc.c:1646  */
    break;

  case 313:
#line 3427 "parser.y" /* yacc.c:1646  */
    {}
#line 6830 "y.tab.c" /* yacc.c:1646  */
    break;

  case 314:
#line 3430 "parser.y" /* yacc.c:1646  */
    {
                    if (allow) {
		      if (cplus_mode == CPLUS_PUBLIC) {
			if (Verbose) {
			  fprintf(stderr,"Creating enum value %s\n", (yyvsp[0].id));
			}
			Stat_const++;
			temp_typeptr = new DataType(T_INT);
			doc_entry = new DocDecl((yyvsp[0].id),doc_stack[doc_stack_top]);
			cplus_declare_const((yyvsp[0].id), (char *) 0, temp_typeptr, (char *) 0);
			delete temp_typeptr;
			scanner_clear_start();
		      }
		    }
                  }
#line 6850 "y.tab.c" /* yacc.c:1646  */
    break;

  case 315:
#line 3445 "parser.y" /* yacc.c:1646  */
    {
		   if (allow) {
		     if (cplus_mode == CPLUS_PUBLIC) {
		       if (Verbose) {
			 fprintf(stderr, "Creating enum value %s = %s\n", (yyvsp[-2].id), (yyvsp[0].dtype).id);
		       }
		       Stat_const++;
		       temp_typeptr = new DataType(T_INT);
		       doc_entry = new DocDecl((yyvsp[-2].id),doc_stack[doc_stack_top]);
		       cplus_declare_const((yyvsp[-2].id),(char *) 0, temp_typeptr,(char *) 0);
// OLD : Bug with value     cplus_declare_const($1,(char *) 0, temp_typeptr,$3.id);
		       delete temp_typeptr;
		       scanner_clear_start();
		     }
		   }
		 }
#line 6871 "y.tab.c" /* yacc.c:1646  */
    break;

  case 316:
#line 3461 "parser.y" /* yacc.c:1646  */
    {
		   if (allow) {
		     if (cplus_mode == CPLUS_PUBLIC) {
		       if (Verbose) {
			 fprintf(stderr,"Creating enum value %s\n", (yyvsp[0].id));
		       }
		       Stat_const++;
		       temp_typeptr = new DataType(T_INT);
		       doc_entry = new DocDecl((yyvsp[-2].id),doc_stack[doc_stack_top]);
		       cplus_declare_const((yyvsp[0].id), (yyvsp[-2].id), temp_typeptr, (char *) 0);
		       delete temp_typeptr;
		       scanner_clear_start();
		     }
		   }
		 }
#line 6891 "y.tab.c" /* yacc.c:1646  */
    break;

  case 317:
#line 3476 "parser.y" /* yacc.c:1646  */
    {
		   if (allow) {
		     if (cplus_mode == CPLUS_PUBLIC) {
		       if (Verbose) {
			 fprintf(stderr, "Creating enum value %s = %s\n", (yyvsp[-2].id), (yyvsp[0].dtype).id);
		       }
		       Stat_const++;
		       temp_typeptr = new DataType(T_INT);
		       doc_entry = new DocDecl((yyvsp[-4].id),doc_stack[doc_stack_top]);
		       cplus_declare_const((yyvsp[-2].id),(yyvsp[-4].id), temp_typeptr, (char *) 0);
// Old : bug with value	       cplus_declare_const($5,$3, temp_typeptr,$7.id);
		       delete temp_typeptr;
		       scanner_clear_start();
		     }
		   }
		 }
#line 6912 "y.tab.c" /* yacc.c:1646  */
    break;

  case 318:
#line 3492 "parser.y" /* yacc.c:1646  */
    { }
#line 6918 "y.tab.c" /* yacc.c:1646  */
    break;

  case 319:
#line 3493 "parser.y" /* yacc.c:1646  */
    { }
#line 6924 "y.tab.c" /* yacc.c:1646  */
    break;

  case 320:
#line 3496 "parser.y" /* yacc.c:1646  */
    {
		   (yyval.ilist) = (yyvsp[0].ilist);
                }
#line 6932 "y.tab.c" /* yacc.c:1646  */
    break;

  case 321:
#line 3499 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.ilist).names = (char **) 0;
		   (yyval.ilist).count = 0;
                }
#line 6941 "y.tab.c" /* yacc.c:1646  */
    break;

  case 322:
#line 3505 "parser.y" /* yacc.c:1646  */
    { 
                   int i;
                   (yyval.ilist).names = new char *[NI_NAMES];
		   (yyval.ilist).count = 0;
		   for (i = 0; i < NI_NAMES; i++){
		     (yyval.ilist).names[i] = (char *) 0;
		   }
                   if ((yyvsp[0].id)) {
                       (yyval.ilist).names[(yyval.ilist).count] = copy_string((yyvsp[0].id));
                       (yyval.ilist).count++;
		   }
               }
#line 6958 "y.tab.c" /* yacc.c:1646  */
    break;

  case 323:
#line 3518 "parser.y" /* yacc.c:1646  */
    { 
                   (yyval.ilist) = (yyvsp[-2].ilist);
                   if ((yyvsp[0].id)) {
		     (yyval.ilist).names[(yyval.ilist).count] = copy_string((yyvsp[0].id));
		     (yyval.ilist).count++;
		   }
               }
#line 6970 "y.tab.c" /* yacc.c:1646  */
    break;

  case 324:
#line 3527 "parser.y" /* yacc.c:1646  */
    {     
                  fprintf(stderr,"%s : Line %d. No access specifier given for base class %s (ignored).\n",
			  input_file,line_number,(yyvsp[0].id));
		  (yyval.id) = (char *) 0;
               }
#line 6980 "y.tab.c" /* yacc.c:1646  */
    break;

  case 325:
#line 3532 "parser.y" /* yacc.c:1646  */
    { 
                  fprintf(stderr,"%s : Line %d. No access specifier given for base class %s (ignored).\n",
			  input_file,line_number,(yyvsp[0].id));
		  (yyval.id) = (char *) 0;
	       }
#line 6990 "y.tab.c" /* yacc.c:1646  */
    break;

  case 326:
#line 3537 "parser.y" /* yacc.c:1646  */
    {
		 if (strcmp((yyvsp[-1].id),"public") == 0) {
		   (yyval.id) = (yyvsp[0].id);
		 } else {
		   fprintf(stderr,"%s : Line %d. %s inheritance not supported (ignored).\n",
			   input_file,line_number,(yyvsp[-1].id));
		   (yyval.id) = (char *) 0;
		 }
               }
#line 7004 "y.tab.c" /* yacc.c:1646  */
    break;

  case 327:
#line 3546 "parser.y" /* yacc.c:1646  */
    {
		 if (strcmp((yyvsp[-1].id),"public") == 0) {
		   (yyval.id) = (yyvsp[0].id);
		 } else {
		   fprintf(stderr,"%s : Line %d. %s inheritance not supported (ignored).\n",
			   input_file,line_number,(yyvsp[-1].id));
		   (yyval.id) = (char *) 0;
		 }
	       }
#line 7018 "y.tab.c" /* yacc.c:1646  */
    break;

  case 328:
#line 3555 "parser.y" /* yacc.c:1646  */
    {
                 if (strcmp((yyvsp[-2].id),"public") == 0) {
		   (yyval.id) = (yyvsp[0].id);
		 } else {
		   fprintf(stderr,"%s : Line %d. %s inheritance not supported (ignored).\n",
			   input_file,line_number,(yyvsp[-2].id));
		   (yyval.id) = (char *) 0;
		 }
               }
#line 7032 "y.tab.c" /* yacc.c:1646  */
    break;

  case 329:
#line 3566 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (char*)"public"; }
#line 7038 "y.tab.c" /* yacc.c:1646  */
    break;

  case 330:
#line 3567 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (char*)"private"; }
#line 7044 "y.tab.c" /* yacc.c:1646  */
    break;

  case 331:
#line 3568 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (char*)"protected"; }
#line 7050 "y.tab.c" /* yacc.c:1646  */
    break;

  case 332:
#line 3572 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (char*)"class"; }
#line 7056 "y.tab.c" /* yacc.c:1646  */
    break;

  case 333:
#line 3573 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (char*)"struct"; }
#line 7062 "y.tab.c" /* yacc.c:1646  */
    break;

  case 334:
#line 3574 "parser.y" /* yacc.c:1646  */
    {(yyval.id) = (char*)"union"; }
#line 7068 "y.tab.c" /* yacc.c:1646  */
    break;

  case 335:
#line 3577 "parser.y" /* yacc.c:1646  */
    {}
#line 7074 "y.tab.c" /* yacc.c:1646  */
    break;

  case 336:
#line 3578 "parser.y" /* yacc.c:1646  */
    { delete (yyvsp[-1].pl);}
#line 7080 "y.tab.c" /* yacc.c:1646  */
    break;

  case 337:
#line 3579 "parser.y" /* yacc.c:1646  */
    {}
#line 7086 "y.tab.c" /* yacc.c:1646  */
    break;

  case 338:
#line 3584 "parser.y" /* yacc.c:1646  */
    { 
                    CCode = "";
               }
#line 7094 "y.tab.c" /* yacc.c:1646  */
    break;

  case 339:
#line 3587 "parser.y" /* yacc.c:1646  */
    { skip_brace(); }
#line 7100 "y.tab.c" /* yacc.c:1646  */
    break;

  case 340:
#line 3590 "parser.y" /* yacc.c:1646  */
    {}
#line 7106 "y.tab.c" /* yacc.c:1646  */
    break;

  case 341:
#line 3591 "parser.y" /* yacc.c:1646  */
    {}
#line 7112 "y.tab.c" /* yacc.c:1646  */
    break;

  case 342:
#line 3594 "parser.y" /* yacc.c:1646  */
    { }
#line 7118 "y.tab.c" /* yacc.c:1646  */
    break;

  case 343:
#line 3595 "parser.y" /* yacc.c:1646  */
    { }
#line 7124 "y.tab.c" /* yacc.c:1646  */
    break;

  case 344:
#line 3598 "parser.y" /* yacc.c:1646  */
    { }
#line 7130 "y.tab.c" /* yacc.c:1646  */
    break;

  case 345:
#line 3599 "parser.y" /* yacc.c:1646  */
    { }
#line 7136 "y.tab.c" /* yacc.c:1646  */
    break;

  case 346:
#line 3602 "parser.y" /* yacc.c:1646  */
    { }
#line 7142 "y.tab.c" /* yacc.c:1646  */
    break;

  case 347:
#line 3603 "parser.y" /* yacc.c:1646  */
    { }
#line 7148 "y.tab.c" /* yacc.c:1646  */
    break;

  case 348:
#line 3611 "parser.y" /* yacc.c:1646  */
    { 
                   ObjCClass = 1;
                   init_language();
		   cplus_mode = CPLUS_PROTECTED;
		   sprintf(temp_name,"CPP_CLASS:%s\n",(yyvsp[-1].id));
		   if (add_symbol(temp_name,(DataType *) 0, (char *) 0)) {
		     fprintf(stderr,"%s : Line %d.  @interface %s is multiple defined.\n",
			     input_file,line_number,(yyvsp[-1].id));
		     FatalError();
		   }
		   // Create a new documentation entry
		   doc_entry = new DocClass((yyvsp[-1].id),doc_parent());
		   doc_stack_top++;
		   doc_stack[doc_stack_top] = doc_entry;
		   scanner_clear_start();
		   cplus_open_class((yyvsp[-1].id), (char *) 0, "");     // Open up a new C++ class
                }
#line 7170 "y.tab.c" /* yacc.c:1646  */
    break;

  case 349:
#line 3627 "parser.y" /* yacc.c:1646  */
    { 
		  if ((yyvsp[-6].id)) {
		      char *inames[1];
		      inames[0] = (yyvsp[-6].id);
		      cplus_inherit(1,inames);
		  }
		  // Restore original doc entry for this class
		  doc_entry = doc_stack[doc_stack_top];
		  cplus_class_close((yyvsp[-7].id));
		  doc_entry = 0;
		  doc_stack_top--;
		  cplus_mode = CPLUS_PUBLIC;
		  ObjCClass = 0;
		  delete (yyvsp[-7].id);
		  delete (yyvsp[-6].id);
                }
#line 7191 "y.tab.c" /* yacc.c:1646  */
    break;

  case 350:
#line 3644 "parser.y" /* yacc.c:1646  */
    {
                 ObjCClass = 1;
		 init_language();
                 cplus_mode = CPLUS_PROTECTED;
                 doc_entry = cplus_set_class((yyvsp[-4].id));
		 if (!doc_entry) {
		   doc_entry = new DocClass((yyvsp[-4].id),doc_parent());
		 }
		 doc_stack_top++;
		 doc_stack[doc_stack_top] = doc_entry;
		 scanner_clear_start();
	       }
#line 7208 "y.tab.c" /* yacc.c:1646  */
    break;

  case 351:
#line 3655 "parser.y" /* yacc.c:1646  */
    {
                 cplus_unset_class();
                 doc_entry = 0;
                 doc_stack_top--;
               }
#line 7218 "y.tab.c" /* yacc.c:1646  */
    break;

  case 352:
#line 3660 "parser.y" /* yacc.c:1646  */
    { skip_to_end(); }
#line 7224 "y.tab.c" /* yacc.c:1646  */
    break;

  case 353:
#line 3661 "parser.y" /* yacc.c:1646  */
    { skip_to_end(); }
#line 7230 "y.tab.c" /* yacc.c:1646  */
    break;

  case 354:
#line 3662 "parser.y" /* yacc.c:1646  */
    {
		 char *iname = make_name((yyvsp[-2].id));
                 init_language();
                 lang->cpp_class_decl((yyvsp[-2].id),iname,"");
		 for (int i = 0; i <(yyvsp[-1].ilist).count; i++) {
		   if ((yyvsp[-1].ilist).names[i]) {
		     iname = make_name((yyvsp[-1].ilist).names[i]);
		     lang->cpp_class_decl((yyvsp[-1].ilist).names[i],iname,"");
		     delete [] (yyvsp[-1].ilist).names[i];
		   }
		 } 
		 delete [] (yyvsp[-1].ilist).names;
	       }
#line 7248 "y.tab.c" /* yacc.c:1646  */
    break;

  case 355:
#line 3677 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (yyvsp[-1].id);}
#line 7254 "y.tab.c" /* yacc.c:1646  */
    break;

  case 356:
#line 3678 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = 0; }
#line 7260 "y.tab.c" /* yacc.c:1646  */
    break;

  case 357:
#line 3682 "parser.y" /* yacc.c:1646  */
    { skip_template(); 
                   CCode.strip();           // Strip whitespace
		   CCode.replace("<","< ");
		   CCode.replace(">"," >");
                   (yyval.id) = CCode.get();
                 }
#line 7271 "y.tab.c" /* yacc.c:1646  */
    break;

  case 358:
#line 3688 "parser.y" /* yacc.c:1646  */
    {
                   (yyval.id) =(char*) "";
               }
#line 7279 "y.tab.c" /* yacc.c:1646  */
    break;

  case 359:
#line 3693 "parser.y" /* yacc.c:1646  */
    { }
#line 7285 "y.tab.c" /* yacc.c:1646  */
    break;

  case 360:
#line 3694 "parser.y" /* yacc.c:1646  */
    { 
                    cplus_mode = CPLUS_PUBLIC;
                 }
#line 7293 "y.tab.c" /* yacc.c:1646  */
    break;

  case 361:
#line 3696 "parser.y" /* yacc.c:1646  */
    { }
#line 7299 "y.tab.c" /* yacc.c:1646  */
    break;

  case 362:
#line 3697 "parser.y" /* yacc.c:1646  */
    {
                    cplus_mode = CPLUS_PRIVATE;
                 }
#line 7307 "y.tab.c" /* yacc.c:1646  */
    break;

  case 363:
#line 3699 "parser.y" /* yacc.c:1646  */
    { }
#line 7313 "y.tab.c" /* yacc.c:1646  */
    break;

  case 364:
#line 3700 "parser.y" /* yacc.c:1646  */
    { 
                    cplus_mode = CPLUS_PROTECTED;
                 }
#line 7321 "y.tab.c" /* yacc.c:1646  */
    break;

  case 365:
#line 3702 "parser.y" /* yacc.c:1646  */
    { }
#line 7327 "y.tab.c" /* yacc.c:1646  */
    break;

  case 366:
#line 3703 "parser.y" /* yacc.c:1646  */
    {
		 if (!Error) {
		   skip_decl();
		   {
		     static int last_error_line = -1;
		     if (last_error_line != line_number) {
		       fprintf(stderr,"%s : Line %d. Syntax error in input.\n", input_file, line_number);
		       FatalError();
		       last_error_line = line_number;
		     }
		     Error = 1;
		   }
		 }
	       }
#line 7346 "y.tab.c" /* yacc.c:1646  */
    break;

  case 367:
#line 3716 "parser.y" /* yacc.c:1646  */
    { }
#line 7352 "y.tab.c" /* yacc.c:1646  */
    break;

  case 368:
#line 3717 "parser.y" /* yacc.c:1646  */
    { }
#line 7358 "y.tab.c" /* yacc.c:1646  */
    break;

  case 369:
#line 3720 "parser.y" /* yacc.c:1646  */
    {
  
                }
#line 7366 "y.tab.c" /* yacc.c:1646  */
    break;

  case 370:
#line 3727 "parser.y" /* yacc.c:1646  */
    { 
                 if (cplus_mode == CPLUS_PUBLIC) {
		   int oldstatus = Status;
		   char *tm;
		   char *iname;
		   if (Active_type) delete Active_type;
		   Active_type = new DataType((yyvsp[-1].type));
		   (yyvsp[-1].type)->is_pointer += (yyvsp[0].decl).is_pointer;
		   (yyvsp[-1].type)->is_reference = (yyvsp[0].decl).is_reference;
		   if ((yyvsp[-1].type)->status & STAT_READONLY) {
		     if (!(tm = typemap_lookup("memberin",typemap_lang,(yyvsp[-1].type),(yyvsp[0].decl).id,"",""))) 
		       Status = Status | STAT_READONLY;
		   }
		   iname = make_name((yyvsp[0].decl).id);
		   doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		   if (iname == (yyvsp[0].decl).id) iname = 0;
		   cplus_variable((yyvsp[0].decl).id,iname,(yyvsp[-1].type));
		   Status = oldstatus; 
		 }
		 scanner_clear_start();
		 delete (yyvsp[-1].type);
               }
#line 7393 "y.tab.c" /* yacc.c:1646  */
    break;

  case 371:
#line 3749 "parser.y" /* yacc.c:1646  */
    { 
		 if (cplus_mode == CPLUS_PUBLIC) {
		   int oldstatus = Status;
		   char *tm, *iname;
		   if (Active_type) delete Active_type;
		   Active_type = new DataType((yyvsp[-2].type));
		   (yyvsp[-2].type)->is_pointer += (yyvsp[-1].decl).is_pointer;
		   (yyvsp[-2].type)->is_reference = (yyvsp[-1].decl).is_reference;
		   (yyvsp[-2].type)->arraystr = copy_string(ArrayString);
		   if ((yyvsp[-2].type)->status & STAT_READONLY) {
		     if (!(tm = typemap_lookup("memberin",typemap_lang,(yyvsp[-2].type),(yyvsp[-1].decl).id,"",""))) 
		       Status = Status | STAT_READONLY;
		   }
		   iname = make_name((yyvsp[-1].decl).id);
		   doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		   if (iname == (yyvsp[-1].decl).id) iname = 0;
		   cplus_variable((yyvsp[-1].decl).id,iname,(yyvsp[-2].type));
		   Status = oldstatus; 
		 }
		 scanner_clear_start();
		 delete (yyvsp[-2].type);
	       }
#line 7420 "y.tab.c" /* yacc.c:1646  */
    break;

  case 372:
#line 3771 "parser.y" /* yacc.c:1646  */
    {
                    strcpy(yy_rename,(yyvsp[-1].id));
                    Rename_true = 1;
	       }
#line 7429 "y.tab.c" /* yacc.c:1646  */
    break;

  case 373:
#line 3774 "parser.y" /* yacc.c:1646  */
    { }
#line 7435 "y.tab.c" /* yacc.c:1646  */
    break;

  case 374:
#line 3776 "parser.y" /* yacc.c:1646  */
    { 
                 if (cplus_mode == CPLUS_PUBLIC) {
		   int oldstatus = Status;
		   char *tm, *iname;
		   DataType *t = new DataType (Active_type);
		   t->is_pointer += (yyvsp[-1].decl).is_pointer;
		   t->is_reference = (yyvsp[-1].decl).is_reference;
		   if (t->status & STAT_READONLY) {
		     if (!(tm = typemap_lookup("memberin",typemap_lang,t,(yyvsp[-1].decl).id,"",""))) 
		       Status = Status | STAT_READONLY;
		   }
		   iname = make_name((yyvsp[-1].decl).id);
		   doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		   if (iname == (yyvsp[-1].decl).id) iname = 0;
		   cplus_variable((yyvsp[-1].decl).id,iname,t);
		   Status = oldstatus; 
		   delete t;
		 }
		 scanner_clear_start();
               }
#line 7460 "y.tab.c" /* yacc.c:1646  */
    break;

  case 375:
#line 3796 "parser.y" /* yacc.c:1646  */
    {
		 char *iname;
                 if (cplus_mode == CPLUS_PUBLIC) {
		   int oldstatus = Status;
		   char *tm;
		   DataType *t = new DataType (Active_type);
		   t->is_pointer += (yyvsp[-2].decl).is_pointer;
		   t->is_reference = (yyvsp[-2].decl).is_reference;
		   t->arraystr = copy_string(ArrayString);
		   if (t->status & STAT_READONLY) {
		     if (!(tm = typemap_lookup("memberin",typemap_lang,t,(yyvsp[-2].decl).id,"",""))) 
		       Status = Status | STAT_READONLY;
		   }
		   iname = make_name((yyvsp[-2].decl).id);
		   doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		   if (iname == (yyvsp[-2].decl).id) iname = 0;
		   cplus_variable((yyvsp[-2].decl).id,iname,t);
		   Status = oldstatus; 
		   delete t;
		 }
		 scanner_clear_start();
               }
#line 7487 "y.tab.c" /* yacc.c:1646  */
    break;

  case 376:
#line 3818 "parser.y" /* yacc.c:1646  */
    { }
#line 7493 "y.tab.c" /* yacc.c:1646  */
    break;

  case 377:
#line 3821 "parser.y" /* yacc.c:1646  */
    { }
#line 7499 "y.tab.c" /* yacc.c:1646  */
    break;

  case 378:
#line 3822 "parser.y" /* yacc.c:1646  */
    {
                   AddMethods = 1;
	       }
#line 7507 "y.tab.c" /* yacc.c:1646  */
    break;

  case 379:
#line 3824 "parser.y" /* yacc.c:1646  */
    {
                   AddMethods = 0;
               }
#line 7515 "y.tab.c" /* yacc.c:1646  */
    break;

  case 380:
#line 3827 "parser.y" /* yacc.c:1646  */
    {
                     strcpy(yy_rename,(yyvsp[-1].id));
                     Rename_true = 1;
	       }
#line 7524 "y.tab.c" /* yacc.c:1646  */
    break;

  case 381:
#line 3830 "parser.y" /* yacc.c:1646  */
    { }
#line 7530 "y.tab.c" /* yacc.c:1646  */
    break;

  case 382:
#line 3831 "parser.y" /* yacc.c:1646  */
    {
                 skip_decl();		                
		 if (!Error) {
		   {
		     static int last_error_line = -1;
		     if (last_error_line != line_number) {
		       fprintf(stderr,"%s : Line %d. Syntax error in input.\n", input_file, line_number);
		       FatalError();
		       last_error_line = line_number;
		     }
		     Error = 1;
		   }
		 }
	       }
#line 7549 "y.tab.c" /* yacc.c:1646  */
    break;

  case 383:
#line 3844 "parser.y" /* yacc.c:1646  */
    { }
#line 7555 "y.tab.c" /* yacc.c:1646  */
    break;

  case 384:
#line 3845 "parser.y" /* yacc.c:1646  */
    { }
#line 7561 "y.tab.c" /* yacc.c:1646  */
    break;

  case 385:
#line 3848 "parser.y" /* yacc.c:1646  */
    {
                 char *iname;
                 // An objective-C instance function
                 // This is like a C++ member function

		 if (strcmp((yyvsp[-2].id),objc_destruct) == 0) {
		   // This is an objective C destructor
                   doc_entry = new DocDecl((yyvsp[-2].id),doc_stack[doc_stack_top]);
                   cplus_destructor((yyvsp[-2].id),(char *) 0);
		 } else {
		   iname = make_name((yyvsp[-2].id));
		   doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		   if (iname == (yyvsp[-2].id)) iname = 0;
		   cplus_member_func((yyvsp[-2].id),iname,(yyvsp[-3].type),(yyvsp[-1].pl),0);
		   scanner_clear_start();
		   delete (yyvsp[-3].type);
		   delete (yyvsp[-2].id);
		   delete (yyvsp[-1].pl);
		 }
               }
#line 7586 "y.tab.c" /* yacc.c:1646  */
    break;

  case 386:
#line 3868 "parser.y" /* yacc.c:1646  */
    { 
                 char *iname;
                 // An objective-C class function
                 // This is like a c++ static member function
                 if (strcmp((yyvsp[-2].id),objc_construct) == 0) {
		   // This is an objective C constructor
		   doc_entry = new DocDecl((yyvsp[-2].id),doc_stack[doc_stack_top]);
                   cplus_constructor((yyvsp[-2].id),0,(yyvsp[-1].pl));
		 } else {
		   iname = make_name((yyvsp[-2].id));
		   doc_entry = new DocDecl(iname,doc_stack[doc_stack_top]);
		   if (iname == (yyvsp[-2].id)) iname = 0;
		   cplus_static_func((yyvsp[-2].id),iname,(yyvsp[-3].type),(yyvsp[-1].pl));
		 }
                 scanner_clear_start();
                 delete (yyvsp[-3].type);
                 delete (yyvsp[-2].id);
                 delete (yyvsp[-1].pl);
               }
#line 7610 "y.tab.c" /* yacc.c:1646  */
    break;

  case 387:
#line 3889 "parser.y" /* yacc.c:1646  */
    { CCode = ""; }
#line 7616 "y.tab.c" /* yacc.c:1646  */
    break;

  case 388:
#line 3890 "parser.y" /* yacc.c:1646  */
    { skip_brace(); }
#line 7622 "y.tab.c" /* yacc.c:1646  */
    break;

  case 389:
#line 3893 "parser.y" /* yacc.c:1646  */
    { 
                  (yyval.type) = (yyvsp[-1].type);
                }
#line 7630 "y.tab.c" /* yacc.c:1646  */
    break;

  case 390:
#line 3896 "parser.y" /* yacc.c:1646  */
    { 
                  (yyval.type) = (yyvsp[-2].type);
                  (yyval.type)->is_pointer += (yyvsp[-1].ivalue);
               }
#line 7639 "y.tab.c" /* yacc.c:1646  */
    break;

  case 391:
#line 3900 "parser.y" /* yacc.c:1646  */
    {       /* Empty type means "id" type */
                  (yyval.type) = new DataType(T_VOID);
		  sprintf((yyval.type)->name,"id");
                  (yyval.type)->is_pointer = 1;
                  (yyval.type)->implicit_ptr = 1;
               }
#line 7650 "y.tab.c" /* yacc.c:1646  */
    break;

  case 392:
#line 3908 "parser.y" /* yacc.c:1646  */
    { 
                  (yyval.type) = new DataType((yyvsp[-1].p)->t);
                  delete (yyvsp[-1].p);
                 }
#line 7659 "y.tab.c" /* yacc.c:1646  */
    break;

  case 393:
#line 3912 "parser.y" /* yacc.c:1646  */
    { 
                  (yyval.type) = new DataType(T_VOID);
		  sprintf((yyval.type)->name,"id");
                  (yyval.type)->is_pointer = 1;
                  (yyval.type)->implicit_ptr = 1;
               }
#line 7670 "y.tab.c" /* yacc.c:1646  */
    break;

  case 394:
#line 3920 "parser.y" /* yacc.c:1646  */
    { 
                   Parm *p= new Parm((yyvsp[-1].type),(yyvsp[0].id));
		   p->objc_separator = (yyvsp[-2].id);
                   (yyval.pl) = (yyvsp[-3].pl);
                   (yyval.pl)->append(p);
               }
#line 7681 "y.tab.c" /* yacc.c:1646  */
    break;

  case 395:
#line 3926 "parser.y" /* yacc.c:1646  */
    { 
                 (yyval.pl) = new ParmList;
               }
#line 7689 "y.tab.c" /* yacc.c:1646  */
    break;

  case 396:
#line 3931 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = copy_string(":"); }
#line 7695 "y.tab.c" /* yacc.c:1646  */
    break;

  case 397:
#line 3932 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = new char[strlen((yyvsp[-1].id))+2]; 
                    strcpy((yyval.id),(yyvsp[-1].id));
		    strcat((yyval.id),":");
		    delete (yyvsp[-1].id);
	        }
#line 7705 "y.tab.c" /* yacc.c:1646  */
    break;

  case 398:
#line 3943 "parser.y" /* yacc.c:1646  */
    {
                    (yyval.dlist) = (yyvsp[0].dlist);
		    (yyval.dlist).names[(yyval.dlist).count] = copy_string((yyvsp[-2].id));
		    (yyval.dlist).values[(yyval.dlist).count] = copy_string((yyvsp[-1].id));
		    format_string((yyval.dlist).values[(yyval.dlist).count]);
		    (yyval.dlist).count++;
                 }
#line 7717 "y.tab.c" /* yacc.c:1646  */
    break;

  case 399:
#line 3953 "parser.y" /* yacc.c:1646  */
    {
                    (yyval.dlist) = (yyvsp[-3].dlist);
		    (yyval.dlist).names[(yyval.dlist).count] = copy_string((yyvsp[-1].id));
		    (yyval.dlist).values[(yyval.dlist).count] = copy_string((yyvsp[0].id));
		    format_string((yyval.dlist).values[(yyval.dlist).count]);
		    (yyval.dlist).count++;
                 }
#line 7729 "y.tab.c" /* yacc.c:1646  */
    break;

  case 400:
#line 3960 "parser.y" /* yacc.c:1646  */
    {
                    (yyval.dlist).names = new char *[NI_NAMES];
		    (yyval.dlist).values = new char *[NI_NAMES];
		    (yyval.dlist).count = 0;
	       }
#line 7739 "y.tab.c" /* yacc.c:1646  */
    break;

  case 401:
#line 3967 "parser.y" /* yacc.c:1646  */
    {
                     (yyval.id) = (yyvsp[0].id);
                 }
#line 7747 "y.tab.c" /* yacc.c:1646  */
    break;

  case 402:
#line 3970 "parser.y" /* yacc.c:1646  */
    {
                     (yyval.id) = (yyvsp[0].id);
	       }
#line 7755 "y.tab.c" /* yacc.c:1646  */
    break;

  case 403:
#line 3973 "parser.y" /* yacc.c:1646  */
    { 
                     (yyval.id) = 0;
                }
#line 7763 "y.tab.c" /* yacc.c:1646  */
    break;

  case 404:
#line 3983 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.id) = (yyvsp[0].id);
               }
#line 7771 "y.tab.c" /* yacc.c:1646  */
    break;

  case 405:
#line 3986 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.id) = copy_string("const");
               }
#line 7779 "y.tab.c" /* yacc.c:1646  */
    break;

  case 406:
#line 3991 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.tmparm) = (yyvsp[-1].tmparm);
                 (yyval.tmparm)->next = (yyvsp[0].tmparm);
		}
#line 7788 "y.tab.c" /* yacc.c:1646  */
    break;

  case 407:
#line 3997 "parser.y" /* yacc.c:1646  */
    {
                 (yyval.tmparm) = (yyvsp[-1].tmparm);
                 (yyval.tmparm)->next = (yyvsp[0].tmparm);
                }
#line 7797 "y.tab.c" /* yacc.c:1646  */
    break;

  case 408:
#line 4001 "parser.y" /* yacc.c:1646  */
    { (yyval.tmparm) = 0;}
#line 7803 "y.tab.c" /* yacc.c:1646  */
    break;

  case 409:
#line 4004 "parser.y" /* yacc.c:1646  */
    {
		    if (InArray) {
		      (yyvsp[-1].type)->is_pointer++;
		      (yyvsp[-1].type)->arraystr = copy_string(ArrayString);
		    }
		    (yyval.tmparm) = new TMParm;
                    (yyval.tmparm)->p = new Parm((yyvsp[-1].type),(yyvsp[0].id));
		    (yyval.tmparm)->p->call_type = 0;
		    (yyval.tmparm)->args = tm_parm;
		    delete (yyvsp[-1].type);
		    delete (yyvsp[0].id);
                 }
#line 7820 "y.tab.c" /* yacc.c:1646  */
    break;

  case 410:
#line 4017 "parser.y" /* yacc.c:1646  */
    {
		  (yyval.tmparm) = new TMParm;
		   (yyval.tmparm)->p = new Parm((yyvsp[-2].type),(yyvsp[0].id));
		   (yyval.tmparm)->p->t->is_pointer += (yyvsp[-1].ivalue);
		   (yyval.tmparm)->p->call_type = 0;
		   if (InArray) {
		     (yyval.tmparm)->p->t->is_pointer++;
		     (yyval.tmparm)->p->t->arraystr = copy_string(ArrayString);
		    }
		   (yyval.tmparm)->args = tm_parm;
		   delete (yyvsp[-2].type);
		   delete (yyvsp[0].id);
		}
#line 7838 "y.tab.c" /* yacc.c:1646  */
    break;

  case 411:
#line 4031 "parser.y" /* yacc.c:1646  */
    {
                  (yyval.tmparm) = new TMParm;
		  (yyval.tmparm)->p = new Parm((yyvsp[-2].type),(yyvsp[0].id));
		  (yyval.tmparm)->p->t->is_reference = 1;
		  (yyval.tmparm)->p->call_type = 0;
		  (yyval.tmparm)->p->t->is_pointer++;
		  if (!CPlusPlus) {
			fprintf(stderr,"%s : Line %d. Warning.  Use of C++ Reference detected.  Use the -c++ option.\n", input_file, line_number);
		  }
		  (yyval.tmparm)->args = tm_parm;
		  delete (yyvsp[-2].type);
		  delete (yyvsp[0].id);
		}
#line 7856 "y.tab.c" /* yacc.c:1646  */
    break;

  case 412:
#line 4044 "parser.y" /* yacc.c:1646  */
    {
                  fprintf(stderr,"%s : Line %d. Error. Function pointer not allowed (remap with typedef).\n", input_file, line_number);
		  FatalError();
                  (yyval.tmparm) = new TMParm;
		  (yyval.tmparm)->p = new Parm((yyvsp[-7].type),(yyvsp[-4].id));
		  (yyval.tmparm)->p->t->type = T_ERROR;
		  (yyval.tmparm)->p->name = copy_string((yyvsp[-4].id));
		  strcpy((yyval.tmparm)->p->t->name,"<function ptr>");
		  (yyval.tmparm)->args = tm_parm;
		  delete (yyvsp[-7].type);
		  delete (yyvsp[-4].id);
		  delete (yyvsp[-1].pl);
		}
#line 7874 "y.tab.c" /* yacc.c:1646  */
    break;

  case 413:
#line 4059 "parser.y" /* yacc.c:1646  */
    {
                    (yyval.id) = (yyvsp[-1].id); 
                    InArray = 0;
                }
#line 7883 "y.tab.c" /* yacc.c:1646  */
    break;

  case 414:
#line 4063 "parser.y" /* yacc.c:1646  */
    { 
                    ArrayBackup = "";
		    ArrayBackup << ArrayString;
                  }
#line 7892 "y.tab.c" /* yacc.c:1646  */
    break;

  case 415:
#line 4066 "parser.y" /* yacc.c:1646  */
    {
                    (yyval.id) = (yyvsp[-3].id);
                    InArray = (yyvsp[-2].ivalue);
                    ArrayString = "";
		    ArrayString << ArrayBackup;
                }
#line 7903 "y.tab.c" /* yacc.c:1646  */
    break;

  case 416:
#line 4072 "parser.y" /* yacc.c:1646  */
    { 
                    ArrayBackup = "";
		    ArrayBackup << ArrayString;
		}
#line 7912 "y.tab.c" /* yacc.c:1646  */
    break;

  case 417:
#line 4075 "parser.y" /* yacc.c:1646  */
    {
		    (yyval.id) = new char[1];
		    (yyval.id)[0] = 0;
		    InArray = (yyvsp[-2].ivalue);
                    ArrayString = "";
                    ArrayString << ArrayBackup;
		}
#line 7924 "y.tab.c" /* yacc.c:1646  */
    break;

  case 418:
#line 4082 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = new char[1];
  	                  (yyval.id)[0] = 0;
                          InArray = 0;
                }
#line 7933 "y.tab.c" /* yacc.c:1646  */
    break;

  case 419:
#line 4088 "parser.y" /* yacc.c:1646  */
    {
                  tm_parm = (yyvsp[-1].pl);
                }
#line 7941 "y.tab.c" /* yacc.c:1646  */
    break;

  case 420:
#line 4091 "parser.y" /* yacc.c:1646  */
    {
                  tm_parm = 0;
                }
#line 7949 "y.tab.c" /* yacc.c:1646  */
    break;

  case 421:
#line 4096 "parser.y" /* yacc.c:1646  */
    {(yyval.id) = (yyvsp[0].id);}
#line 7955 "y.tab.c" /* yacc.c:1646  */
    break;

  case 422:
#line 4097 "parser.y" /* yacc.c:1646  */
    { (yyval.id) = (yyvsp[0].id);}
#line 7961 "y.tab.c" /* yacc.c:1646  */
    break;

  case 423:
#line 4103 "parser.y" /* yacc.c:1646  */
    { }
#line 7967 "y.tab.c" /* yacc.c:1646  */
    break;

  case 424:
#line 4104 "parser.y" /* yacc.c:1646  */
    { }
#line 7973 "y.tab.c" /* yacc.c:1646  */
    break;

  case 425:
#line 4107 "parser.y" /* yacc.c:1646  */
    { }
#line 7979 "y.tab.c" /* yacc.c:1646  */
    break;

  case 426:
#line 4108 "parser.y" /* yacc.c:1646  */
    { }
#line 7985 "y.tab.c" /* yacc.c:1646  */
    break;

  case 427:
#line 4109 "parser.y" /* yacc.c:1646  */
    { }
#line 7991 "y.tab.c" /* yacc.c:1646  */
    break;


#line 7995 "y.tab.c" /* yacc.c:1646  */
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 4143 "parser.y" /* yacc.c:1906  */


void error_recover() {
  int c;
  c = yylex();
  while ((c > 0) && (c != SEMI)) 
    c = yylex();
}

/* Called by the parser (yyparse) when an error is found.*/
void yyerror (const char *) {
  //  Fprintf(stderr,"%s : Line %d. Syntax error.\n", input_file, line_number);
  //  error_recover();
}

