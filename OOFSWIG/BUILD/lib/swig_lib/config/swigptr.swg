/* swigptr.cfg
 * $Header: /users/langer/FE/CVSoof/OOF2/OOFSWIG/swig_lib/config/swigptr.swg,v 1.1.2.2 2014/06/27 20:30:21 langer Exp $
 *
 * This file contains two functions :
 *
 *       void  _swig_make_hex(char *_c, void *_ptr, char *type)
 *       char *_swig_get_hex(char *_c, void **ptr, char *type)
 *
 * These are used to convert pointers to and from pointer strings
 * and to perform type checking.
 *
 * You can remap these functions by making a file called "swigptr.cfg" in
 * your the same directory as the interface file you are wrapping.
 *
 * IMPORTANT !!! the function _swig_get_hex returns a non-null char pointer
 * in the event of a type error (this is used to generate an error message).
 * If a type is successfully parsed, a NULL pointer is returned.
 *
 * $Log: swigptr.swg,v $
 * Revision 1.1.2.2  2014/06/27 20:30:21  langer
 * Copied Lulu's modified swig into OOFSWIG, and changed setup.py so that
 * it automatically builds and uses it.  The --with-swig option to setup.py
 * is still respected, if it's given, but it shouldn't be necessary any more.
 *
 * Changed make_dist so that the swig output files aren't included in
 * the distribution, and removed the --skip-swig option from setup.py.
 * Since everybody has swig now, it's no longer necessary.  This will
 * make the build take a little bit longer, but users won't have to
 * combine the build and install steps anymore.
 *
 * Removed the bit in pyexp.swg that suppressed the warnings that the old
 * swig code generated.  This means that if you use --with-swig, you'll
 * probably get lots of warnings.
 *
 * Added some explicit (char*) casts in PyObject_CallMethod calls in
 * swig typemaps, to get rid of warnings in swig generated code.
 * For unknown reasons, PyObject_CallMethod has char * arguments instead
 * of const char* arguments.   Other similar Python API calls use const.
 *
 * Revision 1.1  2014/06/25 18:45:37  lck
 * *** empty log message ***
 *
 * Revision 1.1.1.1  1999/02/28 02:00:53  beazley
 * Swig1.1
 *
 * Revision 1.5  1996/08/01 16:28:56  dmb
 * Took out unused "dt" variable.
 *
 * Revision 1.4  1996/07/23 14:38:42  dmb
 * Minor change to handling of NULL pointers.
 *
 * Revision 1.3  1996/07/17 15:26:08  dmb
 * Made a minor bug fix so pointers of form _0_Type could be used
 * (as described in the manual).   Disable by compiling with -DNO_ZERO.
 *
 * Revision 1.2  1996/06/10 23:42:10  beazley
 * Added const qualifier.
 *
# Revision 1.1  1996/05/22  17:17:47  beazley
# Initial revision
#
 */

static void 
_swig_make_hex (char *_c, const void *_ptr, char *type)
{
  static char _hex[16] =
  {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
   'a', 'b', 'c', 'd', 'e', 'f'};
  unsigned long _p, _s;
  char _result[128], *_r;
  _r = _result;
  _p = (unsigned long) _ptr;
  if (_p > 0)
    {
      while (_p > 0)
	{
	  _s = _p & 0xf;
	  *(_r++) = _hex[_s];
	  _p = _p >> 4;
	}
      *_r = '_';
      while (_r >= _result)
	*(_c++) = *(_r--);
    }
  else
    {
      strcpy (_c, "NULL");
    }
  if (_ptr)
    strcpy (_c, type);
}

/* A forward reference; */

static char ***swig_ptr_derived = 0;

static char *
_swig_get_hex (char *_c, void **ptr, char *_t)
{
  unsigned long _p;
  char temp_type[256];
  char *_tt;
  char **eq;
  int i, j, n;
  _p = 0;
  if (*_c == '_')
    {
      _c++;
      while (*_c)
	{
	  if ((*_c >= '0') && (*_c <= '9'))
	    _p = (_p << 4) + (*_c - '0');
	  else if ((*_c >= 'a') && (*_c <= 'f'))
	    _p = (_p << 4) + ((*_c - 'a') + 10);
	  else
	    break;
	  _c++;
	}
#ifdef NO_ZERO
      if (_p == 0)
	{
	  return (char *) _c;
	}
#endif
      _tt = _c;
      if (_t)
	{
	  if (strcmp (_c, _t))
	    {
	      /* Have a type mismatch, we're going to have to do some
	         searching here */
	      i = 0;
	      if (swig_ptr_derived)
		{
		  while (swig_ptr_derived[i])
		    {
		      eq = swig_ptr_derived[i];
		      /* Check type */
		      if (strncmp (_t, eq[0], strlen (eq[0])) == 0)
			{
			  /* Found derived type list for this. */
			  n = strlen (eq[0]);
			  j = 1;
			  while (eq[j])
			    {
			      sprintf (temp_type, "%s%s", eq[j], _t + n);
			      if (strcmp (_c, temp_type) == 0)
				{
				  *ptr = (void *) _p;
				  return (char *) 0;
				}
			      j++;
			    }
			}
		      i++;
		    }
		}
	      *ptr = (void *) _p;
	      return _tt;
	    }
	  else
	    {
	      *ptr = (void *) _p;
	      return (char *) 0;
	    }
	}
      else
	{
	  *ptr = (void *) _p;
	  return (char *) 0;
	}
    }
  else {
#ifdef ALLOW_NULL
      if (strcmp (_c, "NULL") == 0)
	{
	  *ptr = (void *) 0;
	  return (char *) 0;
	}
#endif
      *ptr = (void *) 0;	
      return _c;
    }
}
