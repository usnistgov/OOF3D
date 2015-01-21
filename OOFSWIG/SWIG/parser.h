/* A Bison parser, made by GNU Bison 3.0.2.  */

/* Bison interface for Yacc-like parsers in C

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
#line 475 "parser.y" /* yacc.c:1909  */
         
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

#line 325 "y.tab.h" /* yacc.c:1909  */
};
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
