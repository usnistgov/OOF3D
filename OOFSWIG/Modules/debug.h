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

class DEBUGLANG : public Language {
private:
  const char *path;
  const char *module;
public:
  DEBUGLANG() {
    path = "debug";
    module = "swig";
  }
  void parse_args(int argc, char *argv[]);
  void parse();
  void create_function(char *,const char *, DataType *, ParmList *); 
  void link_variable(char *,const char *, DataType *) ;
  void declare_const(const char *,const char *, DataType *,const char *);
  void initialize(void);
  void headers(void);
  void close(void);
  void set_module(const char *mod_name, char **mod_list);
  void set_init(const char *init_name);
  void add_native(char *, char *);
  char *type_mangle(DataType *t) {
    return t->print_mangle_default();
  }
  void cpp_member_func(char *,const char *, DataType *, ParmList *);
  void cpp_constructor(char *,const char *, ParmList *);
  void cpp_destructor(char *,const char *);
  void cpp_open_class(char *,const char *, char *, int strip);
  void cpp_close_class();
  void cpp_inherit(char **, int mode = INHERIT_ALL);
  void cpp_variable(char *,const char *, DataType *);
  void cpp_static_func(char *,const char *, DataType *, ParmList *);
  void cpp_declare_const(const char *,const char *, DataType *,const char *);
  void cpp_static_var(char *,const char *, DataType *);
  void pragma(char *, char *, char *);
  void cpp_class_decl(char *, char *,const char *);
  
};
