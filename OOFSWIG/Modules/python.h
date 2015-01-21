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

/**************************************************************************
 * $Header: /users/langer/FE/CVSoof/OOF2/OOFSWIG/Modules/python.h,v 1.1.2.2 2014/06/27 20:28:08 langer Exp $
 *
 * python.h
 *
 * Header file for Python module.   Warning ; this is work in progress.
 **************************************************************************/

class PYTHON : public Language {
protected:
  char   *module;               // Module name
  const char   *path;                 // Pathname of where to look for library files
  char   *methods;              // Method table name
  const char   *global_name;          // Name of global variables.
  void    get_pointer(const char *iname,const char *srcname,const char *src,const char *dest, DataType *t, String &f,const char *ret);
  int     shadow;
  int     have_defarg;
  int     docstring;
  int     have_output; 
  int     use_kw;     
  FILE    *f_shadow;
  struct Method {               // Methods list.  Needed to build methods
    char   *name;               // Array at very end.
    char   *function;
    Method *next;
  };
  Method  *head;
  Hash     hash;
  String   classes;
  String   func;
  String   vars;
  String   modinit;
  String   modextern;

  char     *import_file;
  void add_method(const char *name, char *function);
  void print_methods();
  char *usage_var(const char *, DataType *);
  char *usage_func(const char *, DataType *, ParmList *);
  char *usage_const(const char *, DataType *,const char *);
  char *add_docstring(DocEntry *de);

  // Add for Python-COM support
  virtual void initialize_cmodule();
  virtual void close_cmodule();
  virtual void emit_function_header(WrapperFunction &emit_to, char *wname);
  virtual char *convert_self(WrapperFunction &f);
  virtual char *make_funcname_wrapper(const char *fnName);
  void emitAddPragmas(String& output,const char* name,const char* spacing);
public :
  PYTHON() {
    module = (char *) 0;
    path = "python";     // Set this to subdirectory where language
                                  // Dependent library files will be stored
    head = 0;                     // Head of method list
    global_name = "cvar";
    shadow = 0;
    have_defarg = 0;
    import_file = 0;
    use_kw = 0;
  };

  // Don't change any of this
  void parse_args(int, char *argv[]);
  void parse();
  void create_function(char *,const char *, DataType *, ParmList *);
  void link_variable(char *,const char *, DataType *);
  void declare_const(const char *,const char *, DataType *,const char *);
  void initialize(void);
  void headers(void);
  void close(void);
  void set_module(const char *, char **);
  void set_init(const char *);
  void add_native(char *, char *);
  void create_command(const char *,const char *);
  void import(char *);

  // C++ extensions---for creating shadow classes
  
  void cpp_member_func(char *name,const char *iname, DataType *t, ParmList *l);
  void cpp_constructor(char *name,const char *iname, ParmList *l);
  void cpp_destructor(char *name,const char *newname);
  void cpp_open_class(char *classname, const char *rname, char *ctype, int strip);
  void cpp_close_class();
  void cpp_cleanup();
  void cpp_inherit(char **baseclass, int mode = INHERIT_ALL);
  void cpp_variable(char *name,const char *iname, DataType *t);
  void cpp_declare_const(const char *name,const char *iname, DataType *type,const char *value);
  void cpp_class_decl(char *, char *,const char *);
  void pragma(char *, char *, char *);
  void cpp_pragma(Pragma *);
  void add_typedef(DataType *t, char *name);
};

#define PYSHADOW_MEMBER  0x2

