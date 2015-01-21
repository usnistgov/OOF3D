/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"


#include <GL/gl.h>
extern void glAccum(GLenum ,GLfloat );
extern void glAlphaFunc(GLenum ,GLclampf );
extern void glBegin(GLenum );
extern void glBitmap(GLsizei ,GLsizei ,GLfloat ,GLfloat ,GLfloat ,GLfloat ,const GLubyte *);
extern void glBlendColorEXT(GLclampf ,GLclampf ,GLclampf ,GLclampf );
extern void glBlendEquationEXT(GLenum );
extern void glBlendFunc(GLenum ,GLenum );
extern void glCallList(GLuint );
extern void glCallLists(GLsizei ,GLenum ,const GLvoid *);
extern void glClear(GLbitfield );
extern void glClearAccum(GLfloat ,GLfloat ,GLfloat ,GLfloat );
extern void glClearColor(GLclampf ,GLclampf ,GLclampf ,GLclampf );
extern void glClearDepth(GLclampd );
extern void glClearIndex(GLfloat );
extern void glClearStencil(GLint );
extern void glClipPlane(GLenum ,const GLdouble *);
extern void glColor3b(GLbyte ,GLbyte ,GLbyte );
extern void glColor3bv(const GLbyte *);
extern void glColor3d(GLdouble ,GLdouble ,GLdouble );
extern void glColor3dv(const GLdouble *);
extern void glColor3f(GLfloat ,GLfloat ,GLfloat );
extern void glColor3fv(const GLfloat *);
extern void glColor3i(GLint ,GLint ,GLint );
extern void glColor3iv(const GLint *);
extern void glColor3s(GLshort ,GLshort ,GLshort );
extern void glColor3sv(const GLshort *);
extern void glColor3ub(GLubyte ,GLubyte ,GLubyte );
extern void glColor3ubv(const GLubyte *);
extern void glColor3ui(GLuint ,GLuint ,GLuint );
extern void glColor3uiv(const GLuint *);
extern void glColor3us(GLushort ,GLushort ,GLushort );
extern void glColor3usv(const GLushort *);
extern void glColor4b(GLbyte ,GLbyte ,GLbyte ,GLbyte );
extern void glColor4bv(const GLbyte *);
extern void glColor4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void glColor4dv(const GLdouble *);
extern void glColor4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
extern void glColor4fv(const GLfloat *);
extern void glColor4i(GLint ,GLint ,GLint ,GLint );
extern void glColor4iv(const GLint *);
extern void glColor4s(GLshort ,GLshort ,GLshort ,GLshort );
extern void glColor4sv(const GLshort *);
extern void glColor4ub(GLubyte ,GLubyte ,GLubyte ,GLubyte );
extern void glColor4ubv(const GLubyte *);
extern void glColor4ui(GLuint ,GLuint ,GLuint ,GLuint );
extern void glColor4uiv(const GLuint *);
extern void glColor4us(GLushort ,GLushort ,GLushort ,GLushort );
extern void glColor4usv(const GLushort *);
extern void glColorMask(GLboolean ,GLboolean ,GLboolean ,GLboolean );
extern void glColorMaterial(GLenum ,GLenum );
extern void glCopyPixels(GLint ,GLint ,GLsizei ,GLsizei ,GLenum );
extern void glCullFace(GLenum );
extern void glDeleteLists(GLuint ,GLsizei );
extern void glDepthFunc(GLenum );
extern void glDepthMask(GLboolean );
extern void glDepthRange(GLclampd ,GLclampd );
extern void glDisable(GLenum );
extern void glDrawBuffer(GLenum );
extern void glDrawPixels(GLsizei ,GLsizei ,GLenum ,GLenum ,const GLvoid *);
extern void glEdgeFlag(GLboolean );
extern void glEdgeFlagv(const GLboolean *);
extern void glEnable(GLenum );
extern void glEnd();
extern void glEndList();
extern void glEvalCoord1d(GLdouble );
extern void glEvalCoord1dv(const GLdouble *);
extern void glEvalCoord1f(GLfloat );
extern void glEvalCoord1fv(const GLfloat *);
extern void glEvalCoord2d(GLdouble ,GLdouble );
extern void glEvalCoord2dv(const GLdouble *);
extern void glEvalCoord2f(GLfloat ,GLfloat );
extern void glEvalCoord2fv(const GLfloat *);
extern void glEvalMesh1(GLenum ,GLint ,GLint );
extern void glEvalMesh2(GLenum ,GLint ,GLint ,GLint ,GLint );
extern void glEvalPoint1(GLint );
extern void glEvalPoint2(GLint ,GLint );
extern void glFeedbackBuffer(GLsizei ,GLenum ,GLfloat *);
extern void glFinish();
extern void glFlush();
extern void glFogf(GLenum ,GLfloat );
extern void glFogfv(GLenum ,const GLfloat *);
extern void glFogi(GLenum ,GLint );
extern void glFogiv(GLenum ,const GLint *);
extern void glFrontFace(GLenum );
extern void glFrustum(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern GLuint glGenLists(GLsizei );
extern void glGetBooleanv(GLenum ,GLboolean *);
extern void glGetClipPlane(GLenum ,GLdouble *);
extern void glGetDoublev(GLenum ,GLdouble *);
extern GLenum glGetError();
extern void glGetFloatv(GLenum ,GLfloat *);
extern void glGetIntegerv(GLenum ,GLint *);
extern void glGetLightfv(GLenum ,GLenum ,GLfloat *);
extern void glGetLightiv(GLenum ,GLenum ,GLint *);
extern void glGetMapdv(GLenum ,GLenum ,GLdouble *);
extern void glGetMapfv(GLenum ,GLenum ,GLfloat *);
extern void glGetMapiv(GLenum ,GLenum ,GLint *);
extern void glGetMaterialfv(GLenum ,GLenum ,GLfloat *);
extern void glGetMaterialiv(GLenum ,GLenum ,GLint *);
extern void glGetPixelMapfv(GLenum ,GLfloat *);
extern void glGetPixelMapuiv(GLenum ,GLuint *);
extern void glGetPixelMapusv(GLenum ,GLushort *);
extern void glGetPolygonStipple(GLubyte *);
extern const GLubyte *glGetString(GLenum );
extern void glGetTexEnvfv(GLenum ,GLenum ,GLfloat *);
extern void glGetTexEnviv(GLenum ,GLenum ,GLint *);
extern void glGetTexGendv(GLenum ,GLenum ,GLdouble *);
extern void glGetTexGenfv(GLenum ,GLenum ,GLfloat *);
extern void glGetTexGeniv(GLenum ,GLenum ,GLint *);
extern void glGetTexImage(GLenum ,GLint ,GLenum ,GLenum ,GLvoid *);
extern void glGetTexLevelParameterfv(GLenum ,GLint ,GLenum ,GLfloat *);
extern void glGetTexLevelParameteriv(GLenum ,GLint ,GLenum ,GLint *);
extern void glGetTexParameterfv(GLenum ,GLenum ,GLfloat *);
extern void glGetTexParameteriv(GLenum ,GLenum ,GLint *);
extern void glHint(GLenum ,GLenum );
extern void glIndexMask(GLuint );
extern void glIndexd(GLdouble );
extern void glIndexdv(const GLdouble *);
extern void glIndexf(GLfloat );
extern void glIndexfv(const GLfloat *);
extern void glIndexi(GLint );
extern void glIndexiv(const GLint *);
extern void glIndexs(GLshort );
extern void glIndexsv(const GLshort *);
extern void glInitNames();
extern GLboolean glIsEnabled(GLenum );
extern GLboolean glIsList(GLuint );
extern void glLightModelf(GLenum ,GLfloat );
extern void glLightModelfv(GLenum ,const GLfloat *);
extern void glLightModeli(GLenum ,GLint );
extern void glLightModeliv(GLenum ,const GLint *);
extern void glLightf(GLenum ,GLenum ,GLfloat );
extern void glLightfv(GLenum ,GLenum ,const GLfloat *);
extern void glLighti(GLenum ,GLenum ,GLint );
extern void glLightiv(GLenum ,GLenum ,const GLint *);
extern void glLineStipple(GLint ,GLushort );
extern void glLineWidth(GLfloat );
extern void glListBase(GLuint );
extern void glLoadIdentity();
extern void glLoadMatrixd(const GLdouble *);
extern void glLoadMatrixf(const GLfloat *);
extern void glLoadName(GLuint );
extern void glLogicOp(GLenum );
extern void glMap1d(GLenum ,GLdouble ,GLdouble ,GLint ,GLint ,const GLdouble *);
extern void glMap1f(GLenum ,GLfloat ,GLfloat ,GLint ,GLint ,const GLfloat *);
extern void glMap2d(GLenum ,GLdouble ,GLdouble ,GLint ,GLint ,GLdouble ,GLdouble ,GLint ,GLint ,const GLdouble *);
extern void glMap2f(GLenum ,GLfloat ,GLfloat ,GLint ,GLint ,GLfloat ,GLfloat ,GLint ,GLint ,const GLfloat *);
extern void glMapGrid1d(GLint ,GLdouble ,GLdouble );
extern void glMapGrid1f(GLint ,GLfloat ,GLfloat );
extern void glMapGrid2d(GLint ,GLdouble ,GLdouble ,GLint ,GLdouble ,GLdouble );
extern void glMapGrid2f(GLint ,GLfloat ,GLfloat ,GLint ,GLfloat ,GLfloat );
extern void glMaterialf(GLenum ,GLenum ,GLfloat );
extern void glMaterialfv(GLenum ,GLenum ,const GLfloat *);
extern void glMateriali(GLenum ,GLenum ,GLint );
extern void glMaterialiv(GLenum ,GLenum ,const GLint *);
extern void glMatrixMode(GLenum );
extern void glMultMatrixd(const GLdouble *);
extern void glMultMatrixf(const GLfloat *);
extern void glNewList(GLuint ,GLenum );
extern void glNormal3b(GLbyte ,GLbyte ,GLbyte );
extern void glNormal3bv(const GLbyte *);
extern void glNormal3d(GLdouble ,GLdouble ,GLdouble );
extern void glNormal3dv(const GLdouble *);
extern void glNormal3f(GLfloat ,GLfloat ,GLfloat );
extern void glNormal3fv(const GLfloat *);
extern void glNormal3i(GLint ,GLint ,GLint );
extern void glNormal3iv(const GLint *);
extern void glNormal3s(GLshort ,GLshort ,GLshort );
extern void glNormal3sv(const GLshort *);
extern void glOrtho(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void glPassThrough(GLfloat );
extern void glPixelMapfv(GLenum ,GLint ,const GLfloat *);
extern void glPixelMapuiv(GLenum ,GLint ,const GLuint *);
extern void glPixelMapusv(GLenum ,GLint ,const GLushort *);
extern void glPixelStoref(GLenum ,GLfloat );
extern void glPixelStorei(GLenum ,GLint );
extern void glPixelTransferf(GLenum ,GLfloat );
extern void glPixelTransferi(GLenum ,GLint );
extern void glPixelZoom(GLfloat ,GLfloat );
extern void glPointSize(GLfloat );
extern void glPolygonMode(GLenum ,GLenum );
extern void glPolygonOffsetEXT(GLfloat ,GLfloat );
extern void glPolygonStipple(const GLubyte *);
extern void glPopAttrib();
extern void glPopMatrix();
extern void glPopName();
extern void glPushAttrib(GLbitfield );
extern void glPushMatrix();
extern void glPushName(GLuint );
extern void glRasterPos2d(GLdouble ,GLdouble );
extern void glRasterPos2dv(const GLdouble *);
extern void glRasterPos2f(GLfloat ,GLfloat );
extern void glRasterPos2fv(const GLfloat *);
extern void glRasterPos2i(GLint ,GLint );
extern void glRasterPos2iv(const GLint *);
extern void glRasterPos2s(GLshort ,GLshort );
extern void glRasterPos2sv(const GLshort *);
extern void glRasterPos3d(GLdouble ,GLdouble ,GLdouble );
extern void glRasterPos3dv(const GLdouble *);
extern void glRasterPos3f(GLfloat ,GLfloat ,GLfloat );
extern void glRasterPos3fv(const GLfloat *);
extern void glRasterPos3i(GLint ,GLint ,GLint );
extern void glRasterPos3iv(const GLint *);
extern void glRasterPos3s(GLshort ,GLshort ,GLshort );
extern void glRasterPos3sv(const GLshort *);
extern void glRasterPos4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void glRasterPos4dv(const GLdouble *);
extern void glRasterPos4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
extern void glRasterPos4fv(const GLfloat *);
extern void glRasterPos4i(GLint ,GLint ,GLint ,GLint );
extern void glRasterPos4iv(const GLint *);
extern void glRasterPos4s(GLshort ,GLshort ,GLshort ,GLshort );
extern void glRasterPos4sv(const GLshort *);
extern void glReadBuffer(GLenum );
extern void glReadPixels(GLint ,GLint ,GLsizei ,GLsizei ,GLenum ,GLenum ,GLvoid *);
extern void glRectd(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void glRectdv(const GLdouble *,const GLdouble *);
extern void glRectf(GLfloat ,GLfloat ,GLfloat ,GLfloat );
extern void glRectfv(const GLfloat *,const GLfloat *);
extern void glRecti(GLint ,GLint ,GLint ,GLint );
extern void glRectiv(const GLint *,const GLint *);
extern void glRects(GLshort ,GLshort ,GLshort ,GLshort );
extern void glRectsv(const GLshort *,const GLshort *);
extern GLint glRenderMode(GLenum );
extern void glRotated(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void glRotatef(GLfloat ,GLfloat ,GLfloat ,GLfloat );
extern void glScaled(GLdouble ,GLdouble ,GLdouble );
extern void glScalef(GLfloat ,GLfloat ,GLfloat );
extern void glScissor(GLint ,GLint ,GLsizei ,GLsizei );
extern void glSelectBuffer(GLsizei ,GLuint *);
extern void glShadeModel(GLenum );
extern void glStencilFunc(GLenum ,GLint ,GLuint );
extern void glStencilMask(GLuint );
extern void glStencilOp(GLenum ,GLenum ,GLenum );
extern void glTexCoord1d(GLdouble );
extern void glTexCoord1dv(const GLdouble *);
extern void glTexCoord1f(GLfloat );
extern void glTexCoord1fv(const GLfloat *);
extern void glTexCoord1i(GLint );
extern void glTexCoord1iv(const GLint *);
extern void glTexCoord1s(GLshort );
extern void glTexCoord1sv(const GLshort *);
extern void glTexCoord2d(GLdouble ,GLdouble );
extern void glTexCoord2dv(const GLdouble *);
extern void glTexCoord2f(GLfloat ,GLfloat );
extern void glTexCoord2fv(const GLfloat *);
extern void glTexCoord2i(GLint ,GLint );
extern void glTexCoord2iv(const GLint *);
extern void glTexCoord2s(GLshort ,GLshort );
extern void glTexCoord2sv(const GLshort *);
extern void glTexCoord3d(GLdouble ,GLdouble ,GLdouble );
extern void glTexCoord3dv(const GLdouble *);
extern void glTexCoord3f(GLfloat ,GLfloat ,GLfloat );
extern void glTexCoord3fv(const GLfloat *);
extern void glTexCoord3i(GLint ,GLint ,GLint );
extern void glTexCoord3iv(const GLint *);
extern void glTexCoord3s(GLshort ,GLshort ,GLshort );
extern void glTexCoord3sv(const GLshort *);
extern void glTexCoord4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void glTexCoord4dv(const GLdouble *);
extern void glTexCoord4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
extern void glTexCoord4fv(const GLfloat *);
extern void glTexCoord4i(GLint ,GLint ,GLint ,GLint );
extern void glTexCoord4iv(const GLint *);
extern void glTexCoord4s(GLshort ,GLshort ,GLshort ,GLshort );
extern void glTexCoord4sv(const GLshort *);
extern void glTexEnvf(GLenum ,GLenum ,GLfloat );
extern void glTexEnvfv(GLenum ,GLenum ,const GLfloat *);
extern void glTexEnvi(GLenum ,GLenum ,GLint );
extern void glTexEnviv(GLenum ,GLenum ,const GLint *);
extern void glTexGend(GLenum ,GLenum ,GLdouble );
extern void glTexGendv(GLenum ,GLenum ,const GLdouble *);
extern void glTexGenf(GLenum ,GLenum ,GLfloat );
extern void glTexGenfv(GLenum ,GLenum ,const GLfloat *);
extern void glTexGeni(GLenum ,GLenum ,GLint );
extern void glTexGeniv(GLenum ,GLenum ,const GLint *);
extern void glTexImage1D(GLenum ,GLint ,GLint ,GLsizei ,GLint ,GLenum ,GLenum ,const GLvoid *);
extern void glTexImage2D(GLenum ,GLint ,GLint ,GLsizei ,GLsizei ,GLint ,GLenum ,GLenum ,const GLvoid *);
extern void glTexParameterf(GLenum ,GLenum ,GLfloat );
extern void glTexParameterfv(GLenum ,GLenum ,const GLfloat *);
extern void glTexParameteri(GLenum ,GLenum ,GLint );
extern void glTexParameteriv(GLenum ,GLenum ,const GLint *);
extern void glTranslated(GLdouble ,GLdouble ,GLdouble );
extern void glTranslatef(GLfloat ,GLfloat ,GLfloat );
extern void glVertex2d(GLdouble ,GLdouble );
extern void glVertex2dv(const GLdouble *);
extern void glVertex2f(GLfloat ,GLfloat );
extern void glVertex2fv(const GLfloat *);
extern void glVertex2i(GLint ,GLint );
extern void glVertex2iv(const GLint *);
extern void glVertex2s(GLshort ,GLshort );
extern void glVertex2sv(const GLshort *);
extern void glVertex3d(GLdouble ,GLdouble ,GLdouble );
extern void glVertex3dv(const GLdouble *);
extern void glVertex3f(GLfloat ,GLfloat ,GLfloat );
extern void glVertex3fv(const GLfloat *);
extern void glVertex3i(GLint ,GLint ,GLint );
extern void glVertex3iv(const GLint *);
extern void glVertex3s(GLshort ,GLshort ,GLshort );
extern void glVertex3sv(const GLshort *);
extern void glVertex4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void glVertex4dv(const GLdouble *);
extern void glVertex4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
extern void glVertex4fv(const GLfloat *);
extern void glVertex4i(GLint ,GLint ,GLint ,GLint );
extern void glVertex4iv(const GLint *);
extern void glVertex4s(GLshort ,GLshort ,GLshort ,GLshort );
extern void glVertex4sv(const GLshort *);
extern void glViewport(GLint ,GLint ,GLsizei ,GLsizei );

#include <GL/glu.h>
extern const GLubyte *gluErrorString(GLenum );
extern const GLubyte *gluGetString(GLenum );
extern void gluOrtho2D(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void gluPerspective(GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern void gluLookAt(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );
extern int gluScaleImage(GLenum ,GLint ,GLint ,GLenum ,const void *,GLint ,GLint ,GLenum ,void *);
extern int gluBuild1DMipmaps(GLenum ,GLint ,GLint ,GLenum ,GLenum ,const void *);
extern int gluBuild2DMipmaps(GLenum ,GLint ,GLint ,GLint ,GLenum ,GLenum ,const void *);
extern GLUquadricObj *gluNewQuadric();
extern void gluDeleteQuadric(GLUquadricObj *);
extern void gluQuadricNormals(GLUquadricObj *,GLenum );
extern void gluQuadricTexture(GLUquadricObj *,GLboolean );
extern void gluQuadricOrientation(GLUquadricObj *,GLenum );
extern void gluQuadricDrawStyle(GLUquadricObj *,GLenum );
extern void gluCylinder(GLUquadricObj *,GLdouble ,GLdouble ,GLdouble ,GLint ,GLint );
extern void gluDisk(GLUquadricObj *,GLdouble ,GLdouble ,GLint ,GLint );
extern void gluPartialDisk(GLUquadricObj *,GLdouble ,GLdouble ,GLint ,GLint ,GLdouble ,GLdouble );
extern void gluSphere(GLUquadricObj *,GLdouble ,GLint ,GLint );
extern GLUtriangulatorObj *gluNewTess();
extern void gluDeleteTess(GLUtriangulatorObj *);
extern void gluBeginPolygon(GLUtriangulatorObj *);
extern void gluEndPolygon(GLUtriangulatorObj *);
extern void gluNextContour(GLUtriangulatorObj *,GLenum );
extern GLUnurbsObj *gluNewNurbsRenderer();
extern void gluDeleteNurbsRenderer(GLUnurbsObj *);
extern void gluBeginSurface(GLUnurbsObj *);
extern void gluBeginCurve(GLUnurbsObj *);
extern void gluEndCurve(GLUnurbsObj *);
extern void gluEndSurface(GLUnurbsObj *);
extern void gluBeginTrim(GLUnurbsObj *);
extern void gluEndTrim(GLUnurbsObj *);
extern void gluPwlCurve(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLenum );
extern void gluNurbsCurve(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLfloat *,GLint ,GLenum );
extern void gluNurbsSurface(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLfloat *,GLint ,GLint ,GLfloat *,GLint ,GLint ,GLenum );
extern void gluNurbsProperty(GLUnurbsObj *,GLenum ,GLfloat );
extern void gluGetNurbsProperty(GLUnurbsObj *,GLenum ,GLfloat *);


GLfloat *newfv4(GLfloat a, GLfloat b, GLfloat c, GLfloat d) {
  GLfloat *f;
  
  f = (GLfloat *) malloc(4*sizeof(GLfloat));
  f[0] = a;
  f[1] = b;
  f[2] = c;
  f[3] = d;
  return f;
}

void setfv4(GLfloat *fv, GLfloat a, GLfloat b, GLfloat c, GLfloat d) {
  fv[0] = a;
  fv[1] = b;
  fv[2] = c;
  fv[3] = d;
}

int Const(int a) {
  return a;
}


#include "aux.h"
extern void auxInitDisplayMode(GLenum );
extern void auxInitPosition(int ,int ,int ,int );
extern GLenum auxInitWindow(char *);
extern void auxCloseWindow();
extern void auxQuit();
extern void auxSwapBuffers();
extern void auxWireSphere(GLdouble );
extern void auxSolidSphere(GLdouble );
extern void auxWireCube(GLdouble );
extern void auxSolidCube(GLdouble );
extern void auxWireBox(GLdouble ,GLdouble ,GLdouble );
extern void auxSolidBox(GLdouble ,GLdouble ,GLdouble );
extern void auxWireTorus(GLdouble ,GLdouble );
extern void auxSolidTorus(GLdouble ,GLdouble );
extern void auxWireCylinder(GLdouble ,GLdouble );
extern void auxSolidCylinder(GLdouble ,GLdouble );
extern void auxWireIcosahedron(GLdouble );
extern void auxSolidIcosahedron(GLdouble );
extern void auxWireOctahedron(GLdouble );
extern void auxSolidOctahedron(GLdouble );
extern void auxWireTetrahedron(GLdouble );
extern void auxSolidTetrahedron(GLdouble );
extern void auxWireDodecahedron(GLdouble );
extern void auxSolidDodecahedron(GLdouble );
extern void auxWireCone(GLdouble ,GLdouble );
extern void auxSolidCone(GLdouble ,GLdouble );
extern void auxWireTeapot(GLdouble );
extern void auxSolidTeapot(GLdouble );


#include <string.h>

/* Create an integer array of given size */

static int *array_int(int size) {
  return (int *) malloc(size*sizeof(int));
}

static int get_int(int *array_int, int index) {
  if (array_int) 
    return (array_int[index]);
  else 
    return 0;
}

static int set_int(int *array_int, int index, int val) {
  if (array_int)
    return (array_int[index] = val);
  else
    return 0;
}

/* Create double precision arrays */

static double *array_double(int size) {
  return (double *) malloc(size*sizeof(double));
}

static double get_double(double *array_double, int index) {
  if (array_double) 
    return (array_double[index]);
  else 
    return 0;
}

static double set_double(double *array_double, int index, double val) {
  if (array_double)
    return (array_double[index] = val);
  else
    return 0;
}


/* Create float arrays */

static float *array_float(int size) {
  return (float *) malloc(size*sizeof(float));
}

static float get_float(float *array_float, int index) {
  if (array_float) 
    return (array_float[index]);
  else 
    return 0;
}

static float set_float(float *array_float, int index, float val) {
  if (array_float)
    return (array_float[index] = val);
  else
    return 0;
}


/* Create byte arrays */

typedef unsigned char byte;

static byte *array_byte(int size) {
  return (byte *) malloc(size*sizeof(byte));
}

static byte get_byte(byte *array_byte, int index) {
  if (array_byte) 
    return (array_byte[index]);
  else 
    return 0;
}

static byte set_byte(byte *array_byte, int index, byte val) {
  if (array_byte)
    return (array_byte[index] = val);
  else
    return 0;
}

/* Create character string arrays */

static char **array_string(int size) {
  char **a;
  int i;

  a = (char **) malloc(size*sizeof(char *));
  for (i = 0; i < size; i++)
    a[i] = 0;
  return a;
}

static char *get_string(char **array_string, int index) {
  if (array_string) 
    return (array_string[index]);
  else 
    return "";
}

static char *set_string(char **array_string, int index, char * val) {
  if (array_string) {
    if (array_string[index]) free(array_string[index]);
    if (strlen(val) > 0) {
      array_string[index] = (char *) malloc(strlen(val)+1);
      strcpy(array_string[index],val);
      return array_string[index];
    } else {
      array_string[index] = 0;
      return val;
    }
  }
  else
    return val;
  }

WRAPPER : void glAccum(GLenum ,GLfloat );

WRAPPER : void glAlphaFunc(GLenum ,GLclampf );

WRAPPER : void glBegin(GLenum );

WRAPPER : void glBitmap(GLsizei ,GLsizei ,GLfloat ,GLfloat ,GLfloat ,GLfloat ,const GLubyte *);

WRAPPER : void glBlendColorEXT(GLclampf ,GLclampf ,GLclampf ,GLclampf );

WRAPPER : void glBlendEquationEXT(GLenum );

WRAPPER : void glBlendFunc(GLenum ,GLenum );

WRAPPER : void glCallList(GLuint );

WRAPPER : void glCallLists(GLsizei ,GLenum ,const GLvoid *);

WRAPPER : void glClear(GLbitfield );

WRAPPER : void glClearAccum(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glClearColor(GLclampf ,GLclampf ,GLclampf ,GLclampf );

WRAPPER : void glClearDepth(GLclampd );

WRAPPER : void glClearIndex(GLfloat );

WRAPPER : void glClearStencil(GLint );

WRAPPER : void glClipPlane(GLenum ,const GLdouble *);

WRAPPER : void glColor3b(GLbyte ,GLbyte ,GLbyte );

WRAPPER : void glColor3bv(const GLbyte *);

WRAPPER : void glColor3d(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glColor3dv(const GLdouble *);

WRAPPER : void glColor3f(GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glColor3fv(const GLfloat *);

WRAPPER : void glColor3i(GLint ,GLint ,GLint );

WRAPPER : void glColor3iv(const GLint *);

WRAPPER : void glColor3s(GLshort ,GLshort ,GLshort );

WRAPPER : void glColor3sv(const GLshort *);

WRAPPER : void glColor3ub(GLubyte ,GLubyte ,GLubyte );

WRAPPER : void glColor3ubv(const GLubyte *);

WRAPPER : void glColor3ui(GLuint ,GLuint ,GLuint );

WRAPPER : void glColor3uiv(const GLuint *);

WRAPPER : void glColor3us(GLushort ,GLushort ,GLushort );

WRAPPER : void glColor3usv(const GLushort *);

WRAPPER : void glColor4b(GLbyte ,GLbyte ,GLbyte ,GLbyte );

WRAPPER : void glColor4bv(const GLbyte *);

WRAPPER : void glColor4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glColor4dv(const GLdouble *);

WRAPPER : void glColor4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glColor4fv(const GLfloat *);

WRAPPER : void glColor4i(GLint ,GLint ,GLint ,GLint );

WRAPPER : void glColor4iv(const GLint *);

WRAPPER : void glColor4s(GLshort ,GLshort ,GLshort ,GLshort );

WRAPPER : void glColor4sv(const GLshort *);

WRAPPER : void glColor4ub(GLubyte ,GLubyte ,GLubyte ,GLubyte );

WRAPPER : void glColor4ubv(const GLubyte *);

WRAPPER : void glColor4ui(GLuint ,GLuint ,GLuint ,GLuint );

WRAPPER : void glColor4uiv(const GLuint *);

WRAPPER : void glColor4us(GLushort ,GLushort ,GLushort ,GLushort );

WRAPPER : void glColor4usv(const GLushort *);

WRAPPER : void glColorMask(GLboolean ,GLboolean ,GLboolean ,GLboolean );

WRAPPER : void glColorMaterial(GLenum ,GLenum );

WRAPPER : void glCopyPixels(GLint ,GLint ,GLsizei ,GLsizei ,GLenum );

WRAPPER : void glCullFace(GLenum );

WRAPPER : void glDeleteLists(GLuint ,GLsizei );

WRAPPER : void glDepthFunc(GLenum );

WRAPPER : void glDepthMask(GLboolean );

WRAPPER : void glDepthRange(GLclampd ,GLclampd );

WRAPPER : void glDisable(GLenum );

WRAPPER : void glDrawBuffer(GLenum );

WRAPPER : void glDrawPixels(GLsizei ,GLsizei ,GLenum ,GLenum ,const GLvoid *);

WRAPPER : void glEdgeFlag(GLboolean );

WRAPPER : void glEdgeFlagv(const GLboolean *);

WRAPPER : void glEnable(GLenum );

WRAPPER : void glEnd();

WRAPPER : void glEndList();

WRAPPER : void glEvalCoord1d(GLdouble );

WRAPPER : void glEvalCoord1dv(const GLdouble *);

WRAPPER : void glEvalCoord1f(GLfloat );

WRAPPER : void glEvalCoord1fv(const GLfloat *);

WRAPPER : void glEvalCoord2d(GLdouble ,GLdouble );

WRAPPER : void glEvalCoord2dv(const GLdouble *);

WRAPPER : void glEvalCoord2f(GLfloat ,GLfloat );

WRAPPER : void glEvalCoord2fv(const GLfloat *);

WRAPPER : void glEvalMesh1(GLenum ,GLint ,GLint );

WRAPPER : void glEvalMesh2(GLenum ,GLint ,GLint ,GLint ,GLint );

WRAPPER : void glEvalPoint1(GLint );

WRAPPER : void glEvalPoint2(GLint ,GLint );

WRAPPER : void glFeedbackBuffer(GLsizei ,GLenum ,GLfloat *);

WRAPPER : void glFinish();

WRAPPER : void glFlush();

WRAPPER : void glFogf(GLenum ,GLfloat );

WRAPPER : void glFogfv(GLenum ,const GLfloat *);

WRAPPER : void glFogi(GLenum ,GLint );

WRAPPER : void glFogiv(GLenum ,const GLint *);

WRAPPER : void glFrontFace(GLenum );

WRAPPER : void glFrustum(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : GLuint glGenLists(GLsizei );

WRAPPER : void glGetBooleanv(GLenum ,GLboolean *);

WRAPPER : void glGetClipPlane(GLenum ,GLdouble *);

WRAPPER : void glGetDoublev(GLenum ,GLdouble *);

WRAPPER : GLenum glGetError();

WRAPPER : void glGetFloatv(GLenum ,GLfloat *);

WRAPPER : void glGetIntegerv(GLenum ,GLint *);

WRAPPER : void glGetLightfv(GLenum ,GLenum ,GLfloat *);

WRAPPER : void glGetLightiv(GLenum ,GLenum ,GLint *);

WRAPPER : void glGetMapdv(GLenum ,GLenum ,GLdouble *);

WRAPPER : void glGetMapfv(GLenum ,GLenum ,GLfloat *);

WRAPPER : void glGetMapiv(GLenum ,GLenum ,GLint *);

WRAPPER : void glGetMaterialfv(GLenum ,GLenum ,GLfloat *);

WRAPPER : void glGetMaterialiv(GLenum ,GLenum ,GLint *);

WRAPPER : void glGetPixelMapfv(GLenum ,GLfloat *);

WRAPPER : void glGetPixelMapuiv(GLenum ,GLuint *);

WRAPPER : void glGetPixelMapusv(GLenum ,GLushort *);

WRAPPER : void glGetPolygonStipple(GLubyte *);

WRAPPER : const GLubyte *glGetString(GLenum );

WRAPPER : void glGetTexEnvfv(GLenum ,GLenum ,GLfloat *);

WRAPPER : void glGetTexEnviv(GLenum ,GLenum ,GLint *);

WRAPPER : void glGetTexGendv(GLenum ,GLenum ,GLdouble *);

WRAPPER : void glGetTexGenfv(GLenum ,GLenum ,GLfloat *);

WRAPPER : void glGetTexGeniv(GLenum ,GLenum ,GLint *);

WRAPPER : void glGetTexImage(GLenum ,GLint ,GLenum ,GLenum ,GLvoid *);

WRAPPER : void glGetTexLevelParameterfv(GLenum ,GLint ,GLenum ,GLfloat *);

WRAPPER : void glGetTexLevelParameteriv(GLenum ,GLint ,GLenum ,GLint *);

WRAPPER : void glGetTexParameterfv(GLenum ,GLenum ,GLfloat *);

WRAPPER : void glGetTexParameteriv(GLenum ,GLenum ,GLint *);

WRAPPER : void glHint(GLenum ,GLenum );

WRAPPER : void glIndexMask(GLuint );

WRAPPER : void glIndexd(GLdouble );

WRAPPER : void glIndexdv(const GLdouble *);

WRAPPER : void glIndexf(GLfloat );

WRAPPER : void glIndexfv(const GLfloat *);

WRAPPER : void glIndexi(GLint );

WRAPPER : void glIndexiv(const GLint *);

WRAPPER : void glIndexs(GLshort );

WRAPPER : void glIndexsv(const GLshort *);

WRAPPER : void glInitNames();

WRAPPER : GLboolean glIsEnabled(GLenum );

WRAPPER : GLboolean glIsList(GLuint );

WRAPPER : void glLightModelf(GLenum ,GLfloat );

WRAPPER : void glLightModelfv(GLenum ,const GLfloat *);

WRAPPER : void glLightModeli(GLenum ,GLint );

WRAPPER : void glLightModeliv(GLenum ,const GLint *);

WRAPPER : void glLightf(GLenum ,GLenum ,GLfloat );

WRAPPER : void glLightfv(GLenum ,GLenum ,const GLfloat *);

WRAPPER : void glLighti(GLenum ,GLenum ,GLint );

WRAPPER : void glLightiv(GLenum ,GLenum ,const GLint *);

WRAPPER : void glLineStipple(GLint ,GLushort );

WRAPPER : void glLineWidth(GLfloat );

WRAPPER : void glListBase(GLuint );

WRAPPER : void glLoadIdentity();

WRAPPER : void glLoadMatrixd(const GLdouble *);

WRAPPER : void glLoadMatrixf(const GLfloat *);

WRAPPER : void glLoadName(GLuint );

WRAPPER : void glLogicOp(GLenum );

WRAPPER : void glMap1d(GLenum ,GLdouble ,GLdouble ,GLint ,GLint ,const GLdouble *);

WRAPPER : void glMap1f(GLenum ,GLfloat ,GLfloat ,GLint ,GLint ,const GLfloat *);

WRAPPER : void glMap2d(GLenum ,GLdouble ,GLdouble ,GLint ,GLint ,GLdouble ,GLdouble ,GLint ,GLint ,const GLdouble *);

WRAPPER : void glMap2f(GLenum ,GLfloat ,GLfloat ,GLint ,GLint ,GLfloat ,GLfloat ,GLint ,GLint ,const GLfloat *);

WRAPPER : void glMapGrid1d(GLint ,GLdouble ,GLdouble );

WRAPPER : void glMapGrid1f(GLint ,GLfloat ,GLfloat );

WRAPPER : void glMapGrid2d(GLint ,GLdouble ,GLdouble ,GLint ,GLdouble ,GLdouble );

WRAPPER : void glMapGrid2f(GLint ,GLfloat ,GLfloat ,GLint ,GLfloat ,GLfloat );

WRAPPER : void glMaterialf(GLenum ,GLenum ,GLfloat );

WRAPPER : void glMaterialfv(GLenum ,GLenum ,const GLfloat *);

WRAPPER : void glMateriali(GLenum ,GLenum ,GLint );

WRAPPER : void glMaterialiv(GLenum ,GLenum ,const GLint *);

WRAPPER : void glMatrixMode(GLenum );

WRAPPER : void glMultMatrixd(const GLdouble *);

WRAPPER : void glMultMatrixf(const GLfloat *);

WRAPPER : void glNewList(GLuint ,GLenum );

WRAPPER : void glNormal3b(GLbyte ,GLbyte ,GLbyte );

WRAPPER : void glNormal3bv(const GLbyte *);

WRAPPER : void glNormal3d(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glNormal3dv(const GLdouble *);

WRAPPER : void glNormal3f(GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glNormal3fv(const GLfloat *);

WRAPPER : void glNormal3i(GLint ,GLint ,GLint );

WRAPPER : void glNormal3iv(const GLint *);

WRAPPER : void glNormal3s(GLshort ,GLshort ,GLshort );

WRAPPER : void glNormal3sv(const GLshort *);

WRAPPER : void glOrtho(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glPassThrough(GLfloat );

WRAPPER : void glPixelMapfv(GLenum ,GLint ,const GLfloat *);

WRAPPER : void glPixelMapuiv(GLenum ,GLint ,const GLuint *);

WRAPPER : void glPixelMapusv(GLenum ,GLint ,const GLushort *);

WRAPPER : void glPixelStoref(GLenum ,GLfloat );

WRAPPER : void glPixelStorei(GLenum ,GLint );

WRAPPER : void glPixelTransferf(GLenum ,GLfloat );

WRAPPER : void glPixelTransferi(GLenum ,GLint );

WRAPPER : void glPixelZoom(GLfloat ,GLfloat );

WRAPPER : void glPointSize(GLfloat );

WRAPPER : void glPolygonMode(GLenum ,GLenum );

WRAPPER : void glPolygonOffsetEXT(GLfloat ,GLfloat );

WRAPPER : void glPolygonStipple(const GLubyte *);

WRAPPER : void glPopAttrib();

WRAPPER : void glPopMatrix();

WRAPPER : void glPopName();

WRAPPER : void glPushAttrib(GLbitfield );

WRAPPER : void glPushMatrix();

WRAPPER : void glPushName(GLuint );

WRAPPER : void glRasterPos2d(GLdouble ,GLdouble );

WRAPPER : void glRasterPos2dv(const GLdouble *);

WRAPPER : void glRasterPos2f(GLfloat ,GLfloat );

WRAPPER : void glRasterPos2fv(const GLfloat *);

WRAPPER : void glRasterPos2i(GLint ,GLint );

WRAPPER : void glRasterPos2iv(const GLint *);

WRAPPER : void glRasterPos2s(GLshort ,GLshort );

WRAPPER : void glRasterPos2sv(const GLshort *);

WRAPPER : void glRasterPos3d(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glRasterPos3dv(const GLdouble *);

WRAPPER : void glRasterPos3f(GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glRasterPos3fv(const GLfloat *);

WRAPPER : void glRasterPos3i(GLint ,GLint ,GLint );

WRAPPER : void glRasterPos3iv(const GLint *);

WRAPPER : void glRasterPos3s(GLshort ,GLshort ,GLshort );

WRAPPER : void glRasterPos3sv(const GLshort *);

WRAPPER : void glRasterPos4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glRasterPos4dv(const GLdouble *);

WRAPPER : void glRasterPos4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glRasterPos4fv(const GLfloat *);

WRAPPER : void glRasterPos4i(GLint ,GLint ,GLint ,GLint );

WRAPPER : void glRasterPos4iv(const GLint *);

WRAPPER : void glRasterPos4s(GLshort ,GLshort ,GLshort ,GLshort );

WRAPPER : void glRasterPos4sv(const GLshort *);

WRAPPER : void glReadBuffer(GLenum );

WRAPPER : void glReadPixels(GLint ,GLint ,GLsizei ,GLsizei ,GLenum ,GLenum ,GLvoid *);

WRAPPER : void glRectd(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glRectdv(const GLdouble *,const GLdouble *);

WRAPPER : void glRectf(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glRectfv(const GLfloat *,const GLfloat *);

WRAPPER : void glRecti(GLint ,GLint ,GLint ,GLint );

WRAPPER : void glRectiv(const GLint *,const GLint *);

WRAPPER : void glRects(GLshort ,GLshort ,GLshort ,GLshort );

WRAPPER : void glRectsv(const GLshort *,const GLshort *);

WRAPPER : GLint glRenderMode(GLenum );

WRAPPER : void glRotated(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glRotatef(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glScaled(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glScalef(GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glScissor(GLint ,GLint ,GLsizei ,GLsizei );

WRAPPER : void glSelectBuffer(GLsizei ,GLuint *);

WRAPPER : void glShadeModel(GLenum );

WRAPPER : void glStencilFunc(GLenum ,GLint ,GLuint );

WRAPPER : void glStencilMask(GLuint );

WRAPPER : void glStencilOp(GLenum ,GLenum ,GLenum );

WRAPPER : void glTexCoord1d(GLdouble );

WRAPPER : void glTexCoord1dv(const GLdouble *);

WRAPPER : void glTexCoord1f(GLfloat );

WRAPPER : void glTexCoord1fv(const GLfloat *);

WRAPPER : void glTexCoord1i(GLint );

WRAPPER : void glTexCoord1iv(const GLint *);

WRAPPER : void glTexCoord1s(GLshort );

WRAPPER : void glTexCoord1sv(const GLshort *);

WRAPPER : void glTexCoord2d(GLdouble ,GLdouble );

WRAPPER : void glTexCoord2dv(const GLdouble *);

WRAPPER : void glTexCoord2f(GLfloat ,GLfloat );

WRAPPER : void glTexCoord2fv(const GLfloat *);

WRAPPER : void glTexCoord2i(GLint ,GLint );

WRAPPER : void glTexCoord2iv(const GLint *);

WRAPPER : void glTexCoord2s(GLshort ,GLshort );

WRAPPER : void glTexCoord2sv(const GLshort *);

WRAPPER : void glTexCoord3d(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glTexCoord3dv(const GLdouble *);

WRAPPER : void glTexCoord3f(GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glTexCoord3fv(const GLfloat *);

WRAPPER : void glTexCoord3i(GLint ,GLint ,GLint );

WRAPPER : void glTexCoord3iv(const GLint *);

WRAPPER : void glTexCoord3s(GLshort ,GLshort ,GLshort );

WRAPPER : void glTexCoord3sv(const GLshort *);

WRAPPER : void glTexCoord4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glTexCoord4dv(const GLdouble *);

WRAPPER : void glTexCoord4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glTexCoord4fv(const GLfloat *);

WRAPPER : void glTexCoord4i(GLint ,GLint ,GLint ,GLint );

WRAPPER : void glTexCoord4iv(const GLint *);

WRAPPER : void glTexCoord4s(GLshort ,GLshort ,GLshort ,GLshort );

WRAPPER : void glTexCoord4sv(const GLshort *);

WRAPPER : void glTexEnvf(GLenum ,GLenum ,GLfloat );

WRAPPER : void glTexEnvfv(GLenum ,GLenum ,const GLfloat *);

WRAPPER : void glTexEnvi(GLenum ,GLenum ,GLint );

WRAPPER : void glTexEnviv(GLenum ,GLenum ,const GLint *);

WRAPPER : void glTexGend(GLenum ,GLenum ,GLdouble );

WRAPPER : void glTexGendv(GLenum ,GLenum ,const GLdouble *);

WRAPPER : void glTexGenf(GLenum ,GLenum ,GLfloat );

WRAPPER : void glTexGenfv(GLenum ,GLenum ,const GLfloat *);

WRAPPER : void glTexGeni(GLenum ,GLenum ,GLint );

WRAPPER : void glTexGeniv(GLenum ,GLenum ,const GLint *);

WRAPPER : void glTexImage1D(GLenum ,GLint ,GLint ,GLsizei ,GLint ,GLenum ,GLenum ,const GLvoid *);

WRAPPER : void glTexImage2D(GLenum ,GLint ,GLint ,GLsizei ,GLsizei ,GLint ,GLenum ,GLenum ,const GLvoid *);

WRAPPER : void glTexParameterf(GLenum ,GLenum ,GLfloat );

WRAPPER : void glTexParameterfv(GLenum ,GLenum ,const GLfloat *);

WRAPPER : void glTexParameteri(GLenum ,GLenum ,GLint );

WRAPPER : void glTexParameteriv(GLenum ,GLenum ,const GLint *);

WRAPPER : void glTranslated(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glTranslatef(GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glVertex2d(GLdouble ,GLdouble );

WRAPPER : void glVertex2dv(const GLdouble *);

WRAPPER : void glVertex2f(GLfloat ,GLfloat );

WRAPPER : void glVertex2fv(const GLfloat *);

WRAPPER : void glVertex2i(GLint ,GLint );

WRAPPER : void glVertex2iv(const GLint *);

WRAPPER : void glVertex2s(GLshort ,GLshort );

WRAPPER : void glVertex2sv(const GLshort *);

WRAPPER : void glVertex3d(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glVertex3dv(const GLdouble *);

WRAPPER : void glVertex3f(GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glVertex3fv(const GLfloat *);

WRAPPER : void glVertex3i(GLint ,GLint ,GLint );

WRAPPER : void glVertex3iv(const GLint *);

WRAPPER : void glVertex3s(GLshort ,GLshort ,GLshort );

WRAPPER : void glVertex3sv(const GLshort *);

WRAPPER : void glVertex4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void glVertex4dv(const GLdouble *);

WRAPPER : void glVertex4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void glVertex4fv(const GLfloat *);

WRAPPER : void glVertex4i(GLint ,GLint ,GLint ,GLint );

WRAPPER : void glVertex4iv(const GLint *);

WRAPPER : void glVertex4s(GLshort ,GLshort ,GLshort ,GLshort );

WRAPPER : void glVertex4sv(const GLshort *);

WRAPPER : void glViewport(GLint ,GLint ,GLsizei ,GLsizei );

WRAPPER : const GLubyte *gluErrorString(GLenum );

WRAPPER : const GLubyte *gluGetString(GLenum );

WRAPPER : void gluOrtho2D(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void gluPerspective(GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : void gluLookAt(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );

WRAPPER : int gluScaleImage(GLenum ,GLint ,GLint ,GLenum ,const void *,GLint ,GLint ,GLenum ,void *);

WRAPPER : int gluBuild1DMipmaps(GLenum ,GLint ,GLint ,GLenum ,GLenum ,const void *);

WRAPPER : int gluBuild2DMipmaps(GLenum ,GLint ,GLint ,GLint ,GLenum ,GLenum ,const void *);

WRAPPER : GLUquadricObj *gluNewQuadric();

WRAPPER : void gluDeleteQuadric(GLUquadricObj *);

WRAPPER : void gluQuadricNormals(GLUquadricObj *,GLenum );

WRAPPER : void gluQuadricTexture(GLUquadricObj *,GLboolean );

WRAPPER : void gluQuadricOrientation(GLUquadricObj *,GLenum );

WRAPPER : void gluQuadricDrawStyle(GLUquadricObj *,GLenum );

WRAPPER : void gluCylinder(GLUquadricObj *,GLdouble ,GLdouble ,GLdouble ,GLint ,GLint );

WRAPPER : void gluDisk(GLUquadricObj *,GLdouble ,GLdouble ,GLint ,GLint );

WRAPPER : void gluPartialDisk(GLUquadricObj *,GLdouble ,GLdouble ,GLint ,GLint ,GLdouble ,GLdouble );

WRAPPER : void gluSphere(GLUquadricObj *,GLdouble ,GLint ,GLint );

WRAPPER : GLUtriangulatorObj *gluNewTess();

WRAPPER : void gluDeleteTess(GLUtriangulatorObj *);

WRAPPER : void gluBeginPolygon(GLUtriangulatorObj *);

WRAPPER : void gluEndPolygon(GLUtriangulatorObj *);

WRAPPER : void gluNextContour(GLUtriangulatorObj *,GLenum );

WRAPPER : GLUnurbsObj *gluNewNurbsRenderer();

WRAPPER : void gluDeleteNurbsRenderer(GLUnurbsObj *);

WRAPPER : void gluBeginSurface(GLUnurbsObj *);

WRAPPER : void gluBeginCurve(GLUnurbsObj *);

WRAPPER : void gluEndCurve(GLUnurbsObj *);

WRAPPER : void gluEndSurface(GLUnurbsObj *);

WRAPPER : void gluBeginTrim(GLUnurbsObj *);

WRAPPER : void gluEndTrim(GLUnurbsObj *);

WRAPPER : void gluPwlCurve(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLenum );

WRAPPER : void gluNurbsCurve(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLfloat *,GLint ,GLenum );

WRAPPER : void gluNurbsSurface(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLfloat *,GLint ,GLint ,GLfloat *,GLint ,GLint ,GLenum );

WRAPPER : void gluNurbsProperty(GLUnurbsObj *,GLenum ,GLfloat );

WRAPPER : void gluGetNurbsProperty(GLUnurbsObj *,GLenum ,GLfloat *);

WRAPPER : GLfloat *newfv4(GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void setfv4(GLfloat *,GLfloat ,GLfloat ,GLfloat ,GLfloat );

WRAPPER : void free(void *);

WRAPPER : int Const(int );

WRAPPER : int system(char *);

WRAPPER : void auxInitDisplayMode(GLenum );

WRAPPER : void auxInitPosition(int ,int ,int ,int );

WRAPPER : GLenum auxInitWindow(char *);

WRAPPER : void auxCloseWindow();

WRAPPER : void auxQuit();

WRAPPER : void auxSwapBuffers();

WRAPPER : void auxWireSphere(GLdouble );

WRAPPER : void auxSolidSphere(GLdouble );

WRAPPER : void auxWireCube(GLdouble );

WRAPPER : void auxSolidCube(GLdouble );

WRAPPER : void auxWireBox(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void auxSolidBox(GLdouble ,GLdouble ,GLdouble );

WRAPPER : void auxWireTorus(GLdouble ,GLdouble );

WRAPPER : void auxSolidTorus(GLdouble ,GLdouble );

WRAPPER : void auxWireCylinder(GLdouble ,GLdouble );

WRAPPER : void auxSolidCylinder(GLdouble ,GLdouble );

WRAPPER : void auxWireIcosahedron(GLdouble );

WRAPPER : void auxSolidIcosahedron(GLdouble );

WRAPPER : void auxWireOctahedron(GLdouble );

WRAPPER : void auxSolidOctahedron(GLdouble );

WRAPPER : void auxWireTetrahedron(GLdouble );

WRAPPER : void auxSolidTetrahedron(GLdouble );

WRAPPER : void auxWireDodecahedron(GLdouble );

WRAPPER : void auxSolidDodecahedron(GLdouble );

WRAPPER : void auxWireCone(GLdouble ,GLdouble );

WRAPPER : void auxSolidCone(GLdouble ,GLdouble );

WRAPPER : void auxWireTeapot(GLdouble );

WRAPPER : void auxSolidTeapot(GLdouble );

WRAPPER : int *array_int(int );

WRAPPER : int get_int(int *,int );

WRAPPER : int set_int(int *,int ,int );

WRAPPER : double *array_double(int );

WRAPPER : double get_double(double *,int );

WRAPPER : double set_double(double *,int ,double );

WRAPPER : float *array_float(int );

WRAPPER : float get_float(float *,int );

WRAPPER : float set_float(float *,int ,float );

WRAPPER : byte *array_byte(int );

WRAPPER : byte get_byte(byte *,int );

WRAPPER : byte set_byte(byte *,int ,byte );

WRAPPER : char **array_string(int );

WRAPPER : char *get_string(char **,int );

WRAPPER : char *set_string(char **,int ,char *);

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_GLfloat","_GLclampf",0},
    { "_GLfloat","_float",0},
    { "_signed_long","_long",0},
    { "_double","_GLclampd",0},
    { "_double","_GLdouble",0},
    { "_GLsizei","_GLuint",0},
    { "_GLsizei","_int",0},
    { "_GLsizei","_signed_int",0},
    { "_GLsizei","_unsigned_int",0},
    { "_GLsizei","_GLenum",0},
    { "_GLsizei","_GLbitfield",0},
    { "_GLsizei","_GLint",0},
    { "_GLbyte","_signed_char",0},
    { "_byte","_unsigned_char",0},
    { "_byte","_GLboolean",0},
    { "_byte","_GLubyte",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_GLenum","_GLuint",0},
    { "_GLenum","_GLsizei",0},
    { "_GLenum","_GLint",0},
    { "_GLenum","_GLbitfield",0},
    { "_GLenum","_unsigned_int",0},
    { "_GLenum","_int",0},
    { "_float","_GLclampf",0},
    { "_float","_GLfloat",0},
    { "_struct_GLUquadricObj","_GLUquadricObj",0},
    { "_struct_GLUtriangulatorObj","_GLUtriangulatorObj",0},
    { "_signed_char","_GLbyte",0},
    { "_GLuint","_unsigned_int",0},
    { "_GLuint","_int",0},
    { "_GLuint","_GLenum",0},
    { "_GLuint","_GLbitfield",0},
    { "_GLuint","_GLint",0},
    { "_GLuint","_GLsizei",0},
    { "_GLclampd","_double",0},
    { "_GLclampd","_GLdouble",0},
    { "_GLclampf","_float",0},
    { "_GLclampf","_GLfloat",0},
    { "_GLUtriangulatorObj","_struct_GLUtriangulatorObj",0},
    { "_GLbitfield","_GLuint",0},
    { "_GLbitfield","_GLsizei",0},
    { "_GLbitfield","_GLint",0},
    { "_GLbitfield","_unsigned_int",0},
    { "_GLbitfield","_int",0},
    { "_GLbitfield","_GLenum",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_GLsizei",0},
    { "_signed_int","_GLint",0},
    { "_signed_int","_int",0},
    { "_GLboolean","_byte",0},
    { "_GLboolean","_GLubyte",0},
    { "_GLboolean","_unsigned_char",0},
    { "_GLshort","_GLushort",0},
    { "_GLshort","_short",0},
    { "_GLshort","_signed_short",0},
    { "_GLshort","_unsigned_short",0},
    { "_GLUnurbsObj","_struct_GLUnurbsObj",0},
    { "_unsigned_short","_GLushort",0},
    { "_unsigned_short","_GLshort",0},
    { "_unsigned_short","_short",0},
    { "_GLushort","_unsigned_short",0},
    { "_GLushort","_short",0},
    { "_GLushort","_GLshort",0},
    { "_signed_short","_GLshort",0},
    { "_signed_short","_short",0},
    { "_unsigned_char","_byte",0},
    { "_unsigned_char","_GLubyte",0},
    { "_unsigned_char","_GLboolean",0},
    { "_unsigned_int","_GLuint",0},
    { "_unsigned_int","_GLsizei",0},
    { "_unsigned_int","_GLint",0},
    { "_unsigned_int","_GLbitfield",0},
    { "_unsigned_int","_GLenum",0},
    { "_unsigned_int","_int",0},
    { "_GLdouble","_GLclampd",0},
    { "_GLdouble","_double",0},
    { "_short","_GLushort",0},
    { "_short","_GLshort",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_GLuint",0},
    { "_int","_GLsizei",0},
    { "_int","_GLint",0},
    { "_int","_GLbitfield",0},
    { "_int","_GLenum",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_GLUquadricObj","_struct_GLUquadricObj",0},
    { "_GLint","_GLuint",0},
    { "_GLint","_GLsizei",0},
    { "_GLint","_int",0},
    { "_GLint","_signed_int",0},
    { "_GLint","_unsigned_int",0},
    { "_GLint","_GLenum",0},
    { "_GLint","_GLbitfield",0},
    { "_GLubyte","_byte",0},
    { "_GLubyte","_unsigned_char",0},
    { "_GLubyte","_GLboolean",0},
    { "_struct_GLUnurbsObj","_GLUnurbsObj",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD CONSTANT   : (int ) GL_CURRENT_BIT = 0x00000001
     ADD CONSTANT   : (int ) GL_POINT_BIT = 0x00000002
     ADD CONSTANT   : (int ) GL_LINE_BIT = 0x00000004
     ADD CONSTANT   : (int ) GL_POLYGON_BIT = 0x00000008
     ADD CONSTANT   : (int ) GL_POLYGON_STIPPLE_BIT = 0x00000010
     ADD CONSTANT   : (int ) GL_PIXEL_MODE_BIT = 0x00000020
     ADD CONSTANT   : (int ) GL_LIGHTING_BIT = 0x00000040
     ADD CONSTANT   : (int ) GL_FOG_BIT = 0x00000080
     ADD CONSTANT   : (int ) GL_DEPTH_BUFFER_BIT = 0x00000100
     ADD CONSTANT   : (int ) GL_ACCUM_BUFFER_BIT = 0x00000200
     ADD CONSTANT   : (int ) GL_STENCIL_BUFFER_BIT = 0x00000400
     ADD CONSTANT   : (int ) GL_VIEWPORT_BIT = 0x00000800
     ADD CONSTANT   : (int ) GL_TRANSFORM_BIT = 0x00001000
     ADD CONSTANT   : (int ) GL_ENABLE_BIT = 0x00002000
     ADD CONSTANT   : (int ) GL_COLOR_BUFFER_BIT = 0x00004000
     ADD CONSTANT   : (int ) GL_HINT_BIT = 0x00008000
     ADD CONSTANT   : (int ) GL_EVAL_BIT = 0x00010000
     ADD CONSTANT   : (int ) GL_LIST_BIT = 0x00020000
     ADD CONSTANT   : (int ) GL_TEXTURE_BIT = 0x00040000
     ADD CONSTANT   : (int ) GL_SCISSOR_BIT = 0x00080000
     ADD CONSTANT   : (int ) GL_ALL_ATTRIB_BITS = 0x000fffff
     ADD CONSTANT   : (int ) GL_FALSE = 0
     ADD CONSTANT   : (int ) GL_TRUE = 1
     ADD CONSTANT   : (int ) GL_POINTS = 0x0000
     ADD CONSTANT   : (int ) GL_LINES = 0x0001
     ADD CONSTANT   : (int ) GL_LINE_LOOP = 0x0002
     ADD CONSTANT   : (int ) GL_LINE_STRIP = 0x0003
     ADD CONSTANT   : (int ) GL_TRIANGLES = 0x0004
     ADD CONSTANT   : (int ) GL_TRIANGLE_STRIP = 0x0005
     ADD CONSTANT   : (int ) GL_TRIANGLE_FAN = 0x0006
     ADD CONSTANT   : (int ) GL_QUADS = 0x0007
     ADD CONSTANT   : (int ) GL_QUAD_STRIP = 0x0008
     ADD CONSTANT   : (int ) GL_POLYGON = 0x0009
     ADD CONSTANT   : (int ) GL_ACCUM = 0x0100
     ADD CONSTANT   : (int ) GL_LOAD = 0x0101
     ADD CONSTANT   : (int ) GL_RETURN = 0x0102
     ADD CONSTANT   : (int ) GL_MULT = 0x0103
     ADD CONSTANT   : (int ) GL_ADD = 0x0104
     ADD CONSTANT   : (int ) GL_NEVER = 0x0200
     ADD CONSTANT   : (int ) GL_LESS = 0x0201
     ADD CONSTANT   : (int ) GL_EQUAL = 0x0202
     ADD CONSTANT   : (int ) GL_LEQUAL = 0x0203
     ADD CONSTANT   : (int ) GL_GREATER = 0x0204
     ADD CONSTANT   : (int ) GL_NOTEQUAL = 0x0205
     ADD CONSTANT   : (int ) GL_GEQUAL = 0x0206
     ADD CONSTANT   : (int ) GL_ALWAYS = 0x0207
     ADD CONSTANT   : (int ) GL_ZERO = 0
     ADD CONSTANT   : (int ) GL_ONE = 1
     ADD CONSTANT   : (int ) GL_SRC_COLOR = 0x0300
     ADD CONSTANT   : (int ) GL_ONE_MINUS_SRC_COLOR = 0x0301
     ADD CONSTANT   : (int ) GL_SRC_ALPHA = 0x0302
     ADD CONSTANT   : (int ) GL_ONE_MINUS_SRC_ALPHA = 0x0303
     ADD CONSTANT   : (int ) GL_DST_ALPHA = 0x0304
     ADD CONSTANT   : (int ) GL_ONE_MINUS_DST_ALPHA = 0x0305
     ADD CONSTANT   : (int ) GL_DST_COLOR = 0x0306
     ADD CONSTANT   : (int ) GL_ONE_MINUS_DST_COLOR = 0x0307
     ADD CONSTANT   : (int ) GL_SRC_ALPHA_SATURATE = 0x0308
     ADD CONSTANT   : (int ) GL_NONE = 0
     ADD CONSTANT   : (int ) GL_FRONT_LEFT = 0x0400
     ADD CONSTANT   : (int ) GL_FRONT_RIGHT = 0x0401
     ADD CONSTANT   : (int ) GL_BACK_LEFT = 0x0402
     ADD CONSTANT   : (int ) GL_BACK_RIGHT = 0x0403
     ADD CONSTANT   : (int ) GL_FRONT = 0x0404
     ADD CONSTANT   : (int ) GL_BACK = 0x0405
     ADD CONSTANT   : (int ) GL_LEFT = 0x0406
     ADD CONSTANT   : (int ) GL_RIGHT = 0x0407
     ADD CONSTANT   : (int ) GL_FRONT_AND_BACK = 0x0408
     ADD CONSTANT   : (int ) GL_AUX0 = 0x0409
     ADD CONSTANT   : (int ) GL_AUX1 = 0x040A
     ADD CONSTANT   : (int ) GL_AUX2 = 0x040B
     ADD CONSTANT   : (int ) GL_AUX3 = 0x040C
     ADD CONSTANT   : (int ) GL_NO_ERROR = 0
     ADD CONSTANT   : (int ) GL_INVALID_ENUM = 0x0500
     ADD CONSTANT   : (int ) GL_INVALID_VALUE = 0x0501
     ADD CONSTANT   : (int ) GL_INVALID_OPERATION = 0x0502
     ADD CONSTANT   : (int ) GL_STACK_OVERFLOW = 0x0503
     ADD CONSTANT   : (int ) GL_STACK_UNDERFLOW = 0x0504
     ADD CONSTANT   : (int ) GL_OUT_OF_MEMORY = 0x0505
     ADD CONSTANT   : (int ) GL_2D = 0x0600
     ADD CONSTANT   : (int ) GL_3D = 0x0601
     ADD CONSTANT   : (int ) GL_3D_COLOR = 0x0602
     ADD CONSTANT   : (int ) GL_3D_COLOR_TEXTURE = 0x0603
     ADD CONSTANT   : (int ) GL_4D_COLOR_TEXTURE = 0x0604
     ADD CONSTANT   : (int ) GL_PASS_THROUGH_TOKEN = 0x0700
     ADD CONSTANT   : (int ) GL_POINT_TOKEN = 0x0701
     ADD CONSTANT   : (int ) GL_LINE_TOKEN = 0x0702
     ADD CONSTANT   : (int ) GL_POLYGON_TOKEN = 0x0703
     ADD CONSTANT   : (int ) GL_BITMAP_TOKEN = 0x0704
     ADD CONSTANT   : (int ) GL_DRAW_PIXEL_TOKEN = 0x0705
     ADD CONSTANT   : (int ) GL_COPY_PIXEL_TOKEN = 0x0706
     ADD CONSTANT   : (int ) GL_LINE_RESET_TOKEN = 0x0707
     ADD CONSTANT   : (int ) GL_EXP = 0x0800
     ADD CONSTANT   : (int ) GL_EXP2 = 0x0801
     ADD CONSTANT   : (int ) GL_CW = 0x0900
     ADD CONSTANT   : (int ) GL_CCW = 0x0901
     ADD CONSTANT   : (int ) GL_COEFF = 0x0A00
     ADD CONSTANT   : (int ) GL_ORDER = 0x0A01
     ADD CONSTANT   : (int ) GL_DOMAIN = 0x0A02
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_I = 0x0C70
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_S_TO_S = 0x0C71
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_R = 0x0C72
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_G = 0x0C73
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_B = 0x0C74
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_A = 0x0C75
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_R_TO_R = 0x0C76
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_G_TO_G = 0x0C77
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_B_TO_B = 0x0C78
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_A_TO_A = 0x0C79
     ADD CONSTANT   : (int ) GL_CURRENT_COLOR = 0x0B00
     ADD CONSTANT   : (int ) GL_CURRENT_INDEX = 0x0B01
     ADD CONSTANT   : (int ) GL_CURRENT_NORMAL = 0x0B02
     ADD CONSTANT   : (int ) GL_CURRENT_TEXTURE_COORDS = 0x0B03
     ADD CONSTANT   : (int ) GL_CURRENT_RASTER_COLOR = 0x0B04
     ADD CONSTANT   : (int ) GL_CURRENT_RASTER_INDEX = 0x0B05
     ADD CONSTANT   : (int ) GL_CURRENT_RASTER_TEXTURE_COORDS = 0x0B06
     ADD CONSTANT   : (int ) GL_CURRENT_RASTER_POSITION = 0x0B07
     ADD CONSTANT   : (int ) GL_CURRENT_RASTER_POSITION_VALID = 0x0B08
     ADD CONSTANT   : (int ) GL_CURRENT_RASTER_DISTANCE = 0x0B09
     ADD CONSTANT   : (int ) GL_POINT_SMOOTH = 0x0B10
     ADD CONSTANT   : (int ) GL_POINT_SIZE = 0x0B11
     ADD CONSTANT   : (int ) GL_POINT_SIZE_RANGE = 0x0B12
     ADD CONSTANT   : (int ) GL_POINT_SIZE_GRANULARITY = 0x0B13
     ADD CONSTANT   : (int ) GL_LINE_SMOOTH = 0x0B20
     ADD CONSTANT   : (int ) GL_LINE_WIDTH = 0x0B21
     ADD CONSTANT   : (int ) GL_LINE_WIDTH_RANGE = 0x0B22
     ADD CONSTANT   : (int ) GL_LINE_WIDTH_GRANULARITY = 0x0B23
     ADD CONSTANT   : (int ) GL_LINE_STIPPLE = 0x0B24
     ADD CONSTANT   : (int ) GL_LINE_STIPPLE_PATTERN = 0x0B25
     ADD CONSTANT   : (int ) GL_LINE_STIPPLE_REPEAT = 0x0B26
     ADD CONSTANT   : (int ) GL_LIST_MODE = 0x0B30
     ADD CONSTANT   : (int ) GL_MAX_LIST_NESTING = 0x0B31
     ADD CONSTANT   : (int ) GL_LIST_BASE = 0x0B32
     ADD CONSTANT   : (int ) GL_LIST_INDEX = 0x0B33
     ADD CONSTANT   : (int ) GL_POLYGON_MODE = 0x0B40
     ADD CONSTANT   : (int ) GL_POLYGON_SMOOTH = 0x0B41
     ADD CONSTANT   : (int ) GL_POLYGON_STIPPLE = 0x0B42
     ADD CONSTANT   : (int ) GL_EDGE_FLAG = 0x0B43
     ADD CONSTANT   : (int ) GL_CULL_FACE = 0x0B44
     ADD CONSTANT   : (int ) GL_CULL_FACE_MODE = 0x0B45
     ADD CONSTANT   : (int ) GL_FRONT_FACE = 0x0B46
     ADD CONSTANT   : (int ) GL_LIGHTING = 0x0B50
     ADD CONSTANT   : (int ) GL_LIGHT_MODEL_LOCAL_VIEWER = 0x0B51
     ADD CONSTANT   : (int ) GL_LIGHT_MODEL_TWO_SIDE = 0x0B52
     ADD CONSTANT   : (int ) GL_LIGHT_MODEL_AMBIENT = 0x0B53
     ADD CONSTANT   : (int ) GL_SHADE_MODEL = 0x0B54
     ADD CONSTANT   : (int ) GL_COLOR_MATERIAL_FACE = 0x0B55
     ADD CONSTANT   : (int ) GL_COLOR_MATERIAL_PARAMETER = 0x0B56
     ADD CONSTANT   : (int ) GL_COLOR_MATERIAL = 0x0B57
     ADD CONSTANT   : (int ) GL_FOG = 0x0B60
     ADD CONSTANT   : (int ) GL_FOG_INDEX = 0x0B61
     ADD CONSTANT   : (int ) GL_FOG_DENSITY = 0x0B62
     ADD CONSTANT   : (int ) GL_FOG_START = 0x0B63
     ADD CONSTANT   : (int ) GL_FOG_END = 0x0B64
     ADD CONSTANT   : (int ) GL_FOG_MODE = 0x0B65
     ADD CONSTANT   : (int ) GL_FOG_COLOR = 0x0B66
     ADD CONSTANT   : (int ) GL_DEPTH_RANGE = 0x0B70
     ADD CONSTANT   : (int ) GL_DEPTH_TEST = 0x0B71
     ADD CONSTANT   : (int ) GL_DEPTH_WRITEMASK = 0x0B72
     ADD CONSTANT   : (int ) GL_DEPTH_CLEAR_VALUE = 0x0B73
     ADD CONSTANT   : (int ) GL_DEPTH_FUNC = 0x0B74
     ADD CONSTANT   : (int ) GL_ACCUM_CLEAR_VALUE = 0x0B80
     ADD CONSTANT   : (int ) GL_STENCIL_TEST = 0x0B90
     ADD CONSTANT   : (int ) GL_STENCIL_CLEAR_VALUE = 0x0B91
     ADD CONSTANT   : (int ) GL_STENCIL_FUNC = 0x0B92
     ADD CONSTANT   : (int ) GL_STENCIL_VALUE_MASK = 0x0B93
     ADD CONSTANT   : (int ) GL_STENCIL_FAIL = 0x0B94
     ADD CONSTANT   : (int ) GL_STENCIL_PASS_DEPTH_FAIL = 0x0B95
     ADD CONSTANT   : (int ) GL_STENCIL_PASS_DEPTH_PASS = 0x0B96
     ADD CONSTANT   : (int ) GL_STENCIL_REF = 0x0B97
     ADD CONSTANT   : (int ) GL_STENCIL_WRITEMASK = 0x0B98
     ADD CONSTANT   : (int ) GL_MATRIX_MODE = 0x0BA0
     ADD CONSTANT   : (int ) GL_NORMALIZE = 0x0BA1
     ADD CONSTANT   : (int ) GL_VIEWPORT = 0x0BA2
     ADD CONSTANT   : (int ) GL_MODELVIEW_STACK_DEPTH = 0x0BA3
     ADD CONSTANT   : (int ) GL_PROJECTION_STACK_DEPTH = 0x0BA4
     ADD CONSTANT   : (int ) GL_TEXTURE_STACK_DEPTH = 0x0BA5
     ADD CONSTANT   : (int ) GL_MODELVIEW_MATRIX = 0x0BA6
     ADD CONSTANT   : (int ) GL_PROJECTION_MATRIX = 0x0BA7
     ADD CONSTANT   : (int ) GL_TEXTURE_MATRIX = 0x0BA8
     ADD CONSTANT   : (int ) GL_ATTRIB_STACK_DEPTH = 0x0BB0
     ADD CONSTANT   : (int ) GL_ALPHA_TEST = 0x0BC0
     ADD CONSTANT   : (int ) GL_ALPHA_TEST_FUNC = 0x0BC1
     ADD CONSTANT   : (int ) GL_ALPHA_TEST_REF = 0x0BC2
     ADD CONSTANT   : (int ) GL_DITHER = 0x0BD0
     ADD CONSTANT   : (int ) GL_BLEND_DST = 0x0BE0
     ADD CONSTANT   : (int ) GL_BLEND_SRC = 0x0BE1
     ADD CONSTANT   : (int ) GL_BLEND = 0x0BE2
     ADD CONSTANT   : (int ) GL_LOGIC_OP_MODE = 0x0BF0
     ADD CONSTANT   : (int ) GL_LOGIC_OP = 0x0BF1
     ADD CONSTANT   : (int ) GL_AUX_BUFFERS = 0x0C00
     ADD CONSTANT   : (int ) GL_DRAW_BUFFER = 0x0C01
     ADD CONSTANT   : (int ) GL_READ_BUFFER = 0x0C02
     ADD CONSTANT   : (int ) GL_SCISSOR_BOX = 0x0C10
     ADD CONSTANT   : (int ) GL_SCISSOR_TEST = 0x0C11
     ADD CONSTANT   : (int ) GL_INDEX_CLEAR_VALUE = 0x0C20
     ADD CONSTANT   : (int ) GL_INDEX_WRITEMASK = 0x0C21
     ADD CONSTANT   : (int ) GL_COLOR_CLEAR_VALUE = 0x0C22
     ADD CONSTANT   : (int ) GL_COLOR_WRITEMASK = 0x0C23
     ADD CONSTANT   : (int ) GL_INDEX_MODE = 0x0C30
     ADD CONSTANT   : (int ) GL_RGBA_MODE = 0x0C31
     ADD CONSTANT   : (int ) GL_DOUBLEBUFFER = 0x0C32
     ADD CONSTANT   : (int ) GL_STEREO = 0x0C33
     ADD CONSTANT   : (int ) GL_RENDER_MODE = 0x0C40
     ADD CONSTANT   : (int ) GL_PERSPECTIVE_CORRECTION_HINT = 0x0C50
     ADD CONSTANT   : (int ) GL_POINT_SMOOTH_HINT = 0x0C51
     ADD CONSTANT   : (int ) GL_LINE_SMOOTH_HINT = 0x0C52
     ADD CONSTANT   : (int ) GL_POLYGON_SMOOTH_HINT = 0x0C53
     ADD CONSTANT   : (int ) GL_FOG_HINT = 0x0C54
     ADD CONSTANT   : (int ) GL_TEXTURE_GEN_S = 0x0C60
     ADD CONSTANT   : (int ) GL_TEXTURE_GEN_T = 0x0C61
     ADD CONSTANT   : (int ) GL_TEXTURE_GEN_R = 0x0C62
     ADD CONSTANT   : (int ) GL_TEXTURE_GEN_Q = 0x0C63
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_I_SIZE = 0x0CB0
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_S_TO_S_SIZE = 0x0CB1
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_R_SIZE = 0x0CB2
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_G_SIZE = 0x0CB3
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_B_SIZE = 0x0CB4
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_I_TO_A_SIZE = 0x0CB5
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_R_TO_R_SIZE = 0x0CB6
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_G_TO_G_SIZE = 0x0CB7
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_B_TO_B_SIZE = 0x0CB8
     ADD CONSTANT   : (int ) GL_PIXEL_MAP_A_TO_A_SIZE = 0x0CB9
     ADD CONSTANT   : (int ) GL_UNPACK_SWAP_BYTES = 0x0CF0
     ADD CONSTANT   : (int ) GL_UNPACK_LSB_FIRST = 0x0CF1
     ADD CONSTANT   : (int ) GL_UNPACK_ROW_LENGTH = 0x0CF2
     ADD CONSTANT   : (int ) GL_UNPACK_SKIP_ROWS = 0x0CF3
     ADD CONSTANT   : (int ) GL_UNPACK_SKIP_PIXELS = 0x0CF4
     ADD CONSTANT   : (int ) GL_UNPACK_ALIGNMENT = 0x0CF5
     ADD CONSTANT   : (int ) GL_PACK_SWAP_BYTES = 0x0D00
     ADD CONSTANT   : (int ) GL_PACK_LSB_FIRST = 0x0D01
     ADD CONSTANT   : (int ) GL_PACK_ROW_LENGTH = 0x0D02
     ADD CONSTANT   : (int ) GL_PACK_SKIP_ROWS = 0x0D03
     ADD CONSTANT   : (int ) GL_PACK_SKIP_PIXELS = 0x0D04
     ADD CONSTANT   : (int ) GL_PACK_ALIGNMENT = 0x0D05
     ADD CONSTANT   : (int ) GL_MAP_COLOR = 0x0D10
     ADD CONSTANT   : (int ) GL_MAP_STENCIL = 0x0D11
     ADD CONSTANT   : (int ) GL_INDEX_SHIFT = 0x0D12
     ADD CONSTANT   : (int ) GL_INDEX_OFFSET = 0x0D13
     ADD CONSTANT   : (int ) GL_RED_SCALE = 0x0D14
     ADD CONSTANT   : (int ) GL_RED_BIAS = 0x0D15
     ADD CONSTANT   : (int ) GL_ZOOM_X = 0x0D16
     ADD CONSTANT   : (int ) GL_ZOOM_Y = 0x0D17
     ADD CONSTANT   : (int ) GL_GREEN_SCALE = 0x0D18
     ADD CONSTANT   : (int ) GL_GREEN_BIAS = 0x0D19
     ADD CONSTANT   : (int ) GL_BLUE_SCALE = 0x0D1A
     ADD CONSTANT   : (int ) GL_BLUE_BIAS = 0x0D1B
     ADD CONSTANT   : (int ) GL_ALPHA_SCALE = 0x0D1C
     ADD CONSTANT   : (int ) GL_ALPHA_BIAS = 0x0D1D
     ADD CONSTANT   : (int ) GL_DEPTH_SCALE = 0x0D1E
     ADD CONSTANT   : (int ) GL_DEPTH_BIAS = 0x0D1F
     ADD CONSTANT   : (int ) GL_MAX_EVAL_ORDER = 0x0D30
     ADD CONSTANT   : (int ) GL_MAX_LIGHTS = 0x0D31
     ADD CONSTANT   : (int ) GL_MAX_CLIP_PLANES = 0x0D32
     ADD CONSTANT   : (int ) GL_MAX_TEXTURE_SIZE = 0x0D33
     ADD CONSTANT   : (int ) GL_MAX_PIXEL_MAP_TABLE = 0x0D34
     ADD CONSTANT   : (int ) GL_MAX_ATTRIB_STACK_DEPTH = 0x0D35
     ADD CONSTANT   : (int ) GL_MAX_MODELVIEW_STACK_DEPTH = 0x0D36
     ADD CONSTANT   : (int ) GL_MAX_NAME_STACK_DEPTH = 0x0D37
     ADD CONSTANT   : (int ) GL_MAX_PROJECTION_STACK_DEPTH = 0x0D38
     ADD CONSTANT   : (int ) GL_MAX_TEXTURE_STACK_DEPTH = 0x0D39
     ADD CONSTANT   : (int ) GL_MAX_VIEWPORT_DIMS = 0x0D3A
     ADD CONSTANT   : (int ) GL_SUBPIXEL_BITS = 0x0D50
     ADD CONSTANT   : (int ) GL_INDEX_BITS = 0x0D51
     ADD CONSTANT   : (int ) GL_RED_BITS = 0x0D52
     ADD CONSTANT   : (int ) GL_GREEN_BITS = 0x0D53
     ADD CONSTANT   : (int ) GL_BLUE_BITS = 0x0D54
     ADD CONSTANT   : (int ) GL_ALPHA_BITS = 0x0D55
     ADD CONSTANT   : (int ) GL_DEPTH_BITS = 0x0D56
     ADD CONSTANT   : (int ) GL_STENCIL_BITS = 0x0D57
     ADD CONSTANT   : (int ) GL_ACCUM_RED_BITS = 0x0D58
     ADD CONSTANT   : (int ) GL_ACCUM_GREEN_BITS = 0x0D59
     ADD CONSTANT   : (int ) GL_ACCUM_BLUE_BITS = 0x0D5A
     ADD CONSTANT   : (int ) GL_ACCUM_ALPHA_BITS = 0x0D5B
     ADD CONSTANT   : (int ) GL_NAME_STACK_DEPTH = 0x0D70
     ADD CONSTANT   : (int ) GL_AUTO_NORMAL = 0x0D80
     ADD CONSTANT   : (int ) GL_MAP1_COLOR_4 = 0x0D90
     ADD CONSTANT   : (int ) GL_MAP1_INDEX = 0x0D91
     ADD CONSTANT   : (int ) GL_MAP1_NORMAL = 0x0D92
     ADD CONSTANT   : (int ) GL_MAP1_TEXTURE_COORD_1 = 0x0D93
     ADD CONSTANT   : (int ) GL_MAP1_TEXTURE_COORD_2 = 0x0D94
     ADD CONSTANT   : (int ) GL_MAP1_TEXTURE_COORD_3 = 0x0D95
     ADD CONSTANT   : (int ) GL_MAP1_TEXTURE_COORD_4 = 0x0D96
     ADD CONSTANT   : (int ) GL_MAP1_VERTEX_3 = 0x0D97
     ADD CONSTANT   : (int ) GL_MAP1_VERTEX_4 = 0x0D98
     ADD CONSTANT   : (int ) GL_MAP2_COLOR_4 = 0x0DB0
     ADD CONSTANT   : (int ) GL_MAP2_INDEX = 0x0DB1
     ADD CONSTANT   : (int ) GL_MAP2_NORMAL = 0x0DB2
     ADD CONSTANT   : (int ) GL_MAP2_TEXTURE_COORD_1 = 0x0DB3
     ADD CONSTANT   : (int ) GL_MAP2_TEXTURE_COORD_2 = 0x0DB4
     ADD CONSTANT   : (int ) GL_MAP2_TEXTURE_COORD_3 = 0x0DB5
     ADD CONSTANT   : (int ) GL_MAP2_TEXTURE_COORD_4 = 0x0DB6
     ADD CONSTANT   : (int ) GL_MAP2_VERTEX_3 = 0x0DB7
     ADD CONSTANT   : (int ) GL_MAP2_VERTEX_4 = 0x0DB8
     ADD CONSTANT   : (int ) GL_MAP1_GRID_DOMAIN = 0x0DD0
     ADD CONSTANT   : (int ) GL_MAP1_GRID_SEGMENTS = 0x0DD1
     ADD CONSTANT   : (int ) GL_MAP2_GRID_DOMAIN = 0x0DD2
     ADD CONSTANT   : (int ) GL_MAP2_GRID_SEGMENTS = 0x0DD3
     ADD CONSTANT   : (int ) GL_TEXTURE_1D = 0x0DE0
     ADD CONSTANT   : (int ) GL_TEXTURE_2D = 0x0DE1
     ADD CONSTANT   : (int ) GL_TEXTURE_WIDTH = 0x1000
     ADD CONSTANT   : (int ) GL_TEXTURE_HEIGHT = 0x1001
     ADD CONSTANT   : (int ) GL_TEXTURE_COMPONENTS = 0x1003
     ADD CONSTANT   : (int ) GL_TEXTURE_BORDER_COLOR = 0x1004
     ADD CONSTANT   : (int ) GL_TEXTURE_BORDER = 0x1005
     ADD CONSTANT   : (int ) GL_DONT_CARE = 0x1100
     ADD CONSTANT   : (int ) GL_FASTEST = 0x1101
     ADD CONSTANT   : (int ) GL_NICEST = 0x1102
     ADD CONSTANT   : (int ) GL_AMBIENT = 0x1200
     ADD CONSTANT   : (int ) GL_DIFFUSE = 0x1201
     ADD CONSTANT   : (int ) GL_SPECULAR = 0x1202
     ADD CONSTANT   : (int ) GL_POSITION = 0x1203
     ADD CONSTANT   : (int ) GL_SPOT_DIRECTION = 0x1204
     ADD CONSTANT   : (int ) GL_SPOT_EXPONENT = 0x1205
     ADD CONSTANT   : (int ) GL_SPOT_CUTOFF = 0x1206
     ADD CONSTANT   : (int ) GL_CONSTANT_ATTENUATION = 0x1207
     ADD CONSTANT   : (int ) GL_LINEAR_ATTENUATION = 0x1208
     ADD CONSTANT   : (int ) GL_QUADRATIC_ATTENUATION = 0x1209
     ADD CONSTANT   : (int ) GL_COMPILE = 0x1300
     ADD CONSTANT   : (int ) GL_COMPILE_AND_EXECUTE = 0x1301
     ADD CONSTANT   : (int ) GL_BYTE = 0x1400
     ADD CONSTANT   : (int ) GL_UNSIGNED_BYTE = 0x1401
     ADD CONSTANT   : (int ) GL_SHORT = 0x1402
     ADD CONSTANT   : (int ) GL_UNSIGNED_SHORT = 0x1403
     ADD CONSTANT   : (int ) GL_INT = 0x1404
     ADD CONSTANT   : (int ) GL_UNSIGNED_INT = 0x1405
     ADD CONSTANT   : (int ) GL_FLOAT = 0x1406
     ADD CONSTANT   : (int ) GL_2_BYTES = 0x1407
     ADD CONSTANT   : (int ) GL_3_BYTES = 0x1408
     ADD CONSTANT   : (int ) GL_4_BYTES = 0x1409
     ADD CONSTANT   : (int ) GL_CLEAR = 0x1500
     ADD CONSTANT   : (int ) GL_AND = 0x1501
     ADD CONSTANT   : (int ) GL_AND_REVERSE = 0x1502
     ADD CONSTANT   : (int ) GL_COPY = 0x1503
     ADD CONSTANT   : (int ) GL_AND_INVERTED = 0x1504
     ADD CONSTANT   : (int ) GL_NOOP = 0x1505
     ADD CONSTANT   : (int ) GL_XOR = 0x1506
     ADD CONSTANT   : (int ) GL_OR = 0x1507
     ADD CONSTANT   : (int ) GL_NOR = 0x1508
     ADD CONSTANT   : (int ) GL_EQUIV = 0x1509
     ADD CONSTANT   : (int ) GL_INVERT = 0x150A
     ADD CONSTANT   : (int ) GL_OR_REVERSE = 0x150B
     ADD CONSTANT   : (int ) GL_COPY_INVERTED = 0x150C
     ADD CONSTANT   : (int ) GL_OR_INVERTED = 0x150D
     ADD CONSTANT   : (int ) GL_NAND = 0x150E
     ADD CONSTANT   : (int ) GL_SET = 0x150F
     ADD CONSTANT   : (int ) GL_EMISSION = 0x1600
     ADD CONSTANT   : (int ) GL_SHININESS = 0x1601
     ADD CONSTANT   : (int ) GL_AMBIENT_AND_DIFFUSE = 0x1602
     ADD CONSTANT   : (int ) GL_COLOR_INDEXES = 0x1603
     ADD CONSTANT   : (int ) GL_MODELVIEW = 0x1700
     ADD CONSTANT   : (int ) GL_PROJECTION = 0x1701
     ADD CONSTANT   : (int ) GL_TEXTURE = 0x1702
     ADD CONSTANT   : (int ) GL_COLOR = 0x1800
     ADD CONSTANT   : (int ) GL_DEPTH = 0x1801
     ADD CONSTANT   : (int ) GL_STENCIL = 0x1802
     ADD CONSTANT   : (int ) GL_COLOR_INDEX = 0x1900
     ADD CONSTANT   : (int ) GL_STENCIL_INDEX = 0x1901
     ADD CONSTANT   : (int ) GL_DEPTH_COMPONENT = 0x1902
     ADD CONSTANT   : (int ) GL_RED = 0x1903
     ADD CONSTANT   : (int ) GL_GREEN = 0x1904
     ADD CONSTANT   : (int ) GL_BLUE = 0x1905
     ADD CONSTANT   : (int ) GL_ALPHA = 0x1906
     ADD CONSTANT   : (int ) GL_RGB = 0x1907
     ADD CONSTANT   : (int ) GL_RGBA = 0x1908
     ADD CONSTANT   : (int ) GL_LUMINANCE = 0x1909
     ADD CONSTANT   : (int ) GL_LUMINANCE_ALPHA = 0x190A
     ADD CONSTANT   : (int ) GL_BITMAP = 0x1A00
     ADD CONSTANT   : (int ) GL_POINT = 0x1B00
     ADD CONSTANT   : (int ) GL_LINE = 0x1B01
     ADD CONSTANT   : (int ) GL_FILL = 0x1B02
     ADD CONSTANT   : (int ) GL_RENDER = 0x1C00
     ADD CONSTANT   : (int ) GL_FEEDBACK = 0x1C01
     ADD CONSTANT   : (int ) GL_SELECT = 0x1C02
     ADD CONSTANT   : (int ) GL_FLAT = 0x1D00
     ADD CONSTANT   : (int ) GL_SMOOTH = 0x1D01
     ADD CONSTANT   : (int ) GL_KEEP = 0x1E00
     ADD CONSTANT   : (int ) GL_REPLACE = 0x1E01
     ADD CONSTANT   : (int ) GL_INCR = 0x1E02
     ADD CONSTANT   : (int ) GL_DECR = 0x1E03
     ADD CONSTANT   : (int ) GL_VENDOR = 0x1F00
     ADD CONSTANT   : (int ) GL_RENDERER = 0x1F01
     ADD CONSTANT   : (int ) GL_VERSION = 0x1F02
     ADD CONSTANT   : (int ) GL_EXTENSIONS = 0x1F03
     ADD CONSTANT   : (int ) GL_S = 0x2000
     ADD CONSTANT   : (int ) GL_T = 0x2001
     ADD CONSTANT   : (int ) GL_R = 0x2002
     ADD CONSTANT   : (int ) GL_Q = 0x2003
     ADD CONSTANT   : (int ) GL_MODULATE = 0x2100
     ADD CONSTANT   : (int ) GL_DECAL = 0x2101
     ADD CONSTANT   : (int ) GL_TEXTURE_ENV_MODE = 0x2200
     ADD CONSTANT   : (int ) GL_TEXTURE_ENV_COLOR = 0x2201
     ADD CONSTANT   : (int ) GL_TEXTURE_ENV = 0x2300
     ADD CONSTANT   : (int ) GL_EYE_LINEAR = 0x2400
     ADD CONSTANT   : (int ) GL_OBJECT_LINEAR = 0x2401
     ADD CONSTANT   : (int ) GL_SPHERE_MAP = 0x2402
     ADD CONSTANT   : (int ) GL_TEXTURE_GEN_MODE = 0x2500
     ADD CONSTANT   : (int ) GL_OBJECT_PLANE = 0x2501
     ADD CONSTANT   : (int ) GL_EYE_PLANE = 0x2502
     ADD CONSTANT   : (int ) GL_NEAREST = 0x2600
     ADD CONSTANT   : (int ) GL_LINEAR = 0x2601
     ADD CONSTANT   : (int ) GL_NEAREST_MIPMAP_NEAREST = 0x2700
     ADD CONSTANT   : (int ) GL_LINEAR_MIPMAP_NEAREST = 0x2701
     ADD CONSTANT   : (int ) GL_NEAREST_MIPMAP_LINEAR = 0x2702
     ADD CONSTANT   : (int ) GL_LINEAR_MIPMAP_LINEAR = 0x2703
     ADD CONSTANT   : (int ) GL_TEXTURE_MAG_FILTER = 0x2800
     ADD CONSTANT   : (int ) GL_TEXTURE_MIN_FILTER = 0x2801
     ADD CONSTANT   : (int ) GL_TEXTURE_WRAP_S = 0x2802
     ADD CONSTANT   : (int ) GL_TEXTURE_WRAP_T = 0x2803
     ADD CONSTANT   : (int ) GL_CLAMP = 0x2900
     ADD CONSTANT   : (int ) GL_REPEAT = 0x2901
     ADD CONSTANT   : (int ) GL_CLIP_PLANE0 = 0x3000
     ADD CONSTANT   : (int ) GL_CLIP_PLANE1 = 0x3001
     ADD CONSTANT   : (int ) GL_CLIP_PLANE2 = 0x3002
     ADD CONSTANT   : (int ) GL_CLIP_PLANE3 = 0x3003
     ADD CONSTANT   : (int ) GL_CLIP_PLANE4 = 0x3004
     ADD CONSTANT   : (int ) GL_CLIP_PLANE5 = 0x3005
     ADD CONSTANT   : (int ) GL_LIGHT0 = 0x4000
     ADD CONSTANT   : (int ) GL_LIGHT1 = 0x4001
     ADD CONSTANT   : (int ) GL_LIGHT2 = 0x4002
     ADD CONSTANT   : (int ) GL_LIGHT3 = 0x4003
     ADD CONSTANT   : (int ) GL_LIGHT4 = 0x4004
     ADD CONSTANT   : (int ) GL_LIGHT5 = 0x4005
     ADD CONSTANT   : (int ) GL_LIGHT6 = 0x4006
     ADD CONSTANT   : (int ) GL_LIGHT7 = 0x4007
     ADD CONSTANT   : (int ) GL_EXT_abgr = 1
     ADD CONSTANT   : (int ) GL_EXT_blend_color = 1
     ADD CONSTANT   : (int ) GL_EXT_blend_logic_op = 1
     ADD CONSTANT   : (int ) GL_EXT_blend_minmax = 1
     ADD CONSTANT   : (int ) GL_EXT_blend_subtract = 1
     ADD CONSTANT   : (int ) GL_EXT_convolution = 1
     ADD CONSTANT   : (int ) GL_EXT_histogram = 1
     ADD CONSTANT   : (int ) GL_EXT_polygon_offset = 1
     ADD CONSTANT   : (int ) GL_EXT_subtexture = 1
     ADD CONSTANT   : (int ) GL_EXT_texture = 1
     ADD CONSTANT   : (int ) GL_EXT_texture3D = 1
     ADD CONSTANT   : (int ) GL_SGIS_detail_texture = 1
     ADD CONSTANT   : (int ) GL_SGIS_multisample = 1
     ADD CONSTANT   : (int ) GL_SGIS_sharpen_texture = 1
     ADD CONSTANT   : (int ) GL_ABGR_EXT = 0x8000
     ADD CONSTANT   : (int ) GL_CONSTANT_COLOR_EXT = 0x8001
     ADD CONSTANT   : (int ) GL_ONE_MINUS_CONSTANT_COLOR_EXT = 0x8002
     ADD CONSTANT   : (int ) GL_CONSTANT_ALPHA_EXT = 0x8003
     ADD CONSTANT   : (int ) GL_ONE_MINUS_CONSTANT_ALPHA_EXT = 0x8004
     ADD CONSTANT   : (int ) GL_BLEND_COLOR_EXT = 0x8005
     ADD CONSTANT   : (int ) GL_FUNC_ADD_EXT = 0x8006
     ADD CONSTANT   : (int ) GL_MIN_EXT = 0x8007
     ADD CONSTANT   : (int ) GL_MAX_EXT = 0x8008
     ADD CONSTANT   : (int ) GL_BLEND_EQUATION_EXT = 0x8009
     ADD CONSTANT   : (int ) GL_FUNC_SUBTRACT_EXT = 0x800A
     ADD CONSTANT   : (int ) GL_FUNC_REVERSE_SUBTRACT_EXT = 0x800B
     ADD CONSTANT   : (int ) GL_CONVOLUTION_1D_EXT = 0x8010
     ADD CONSTANT   : (int ) GL_CONVOLUTION_2D_EXT = 0x8011
     ADD CONSTANT   : (int ) GL_SEPARABLE_2D_EXT = 0x8012
     ADD CONSTANT   : (int ) GL_CONVOLUTION_BORDER_MODE_EXT = 0x8013
     ADD CONSTANT   : (int ) GL_CONVOLUTION_FILTER_SCALE_EXT = 0x8014
     ADD CONSTANT   : (int ) GL_CONVOLUTION_FILTER_BIAS_EXT = 0x8015
     ADD CONSTANT   : (int ) GL_REDUCE_EXT = 0x8016
     ADD CONSTANT   : (int ) GL_CONVOLUTION_FORMAT_EXT = 0x8017
     ADD CONSTANT   : (int ) GL_CONVOLUTION_WIDTH_EXT = 0x8018
     ADD CONSTANT   : (int ) GL_CONVOLUTION_HEIGHT_EXT = 0x8019
     ADD CONSTANT   : (int ) GL_MAX_CONVOLUTION_WIDTH_EXT = 0x801A
     ADD CONSTANT   : (int ) GL_MAX_CONVOLUTION_HEIGHT_EXT = 0x801B
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_RED_SCALE_EXT = 0x801C
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_GREEN_SCALE_EXT = 0x801D
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_BLUE_SCALE_EXT = 0x801E
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_ALPHA_SCALE_EXT = 0x801F
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_RED_BIAS_EXT = 0x8020
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_GREEN_BIAS_EXT = 0x8021
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_BLUE_BIAS_EXT = 0x8022
     ADD CONSTANT   : (int ) GL_POST_CONVOLUTION_ALPHA_BIAS_EXT = 0x8023
     ADD CONSTANT   : (int ) GL_HISTOGRAM_EXT = 0x8024
     ADD CONSTANT   : (int ) GL_PROXY_HISTOGRAM_EXT = 0x8025
     ADD CONSTANT   : (int ) GL_HISTOGRAM_WIDTH_EXT = 0x8026
     ADD CONSTANT   : (int ) GL_HISTOGRAM_FORMAT_EXT = 0x8027
     ADD CONSTANT   : (int ) GL_HISTOGRAM_RED_SIZE_EXT = 0x8028
     ADD CONSTANT   : (int ) GL_HISTOGRAM_GREEN_SIZE_EXT = 0x8029
     ADD CONSTANT   : (int ) GL_HISTOGRAM_BLUE_SIZE_EXT = 0x802A
     ADD CONSTANT   : (int ) GL_HISTOGRAM_ALPHA_SIZE_EXT = 0x802B
     ADD CONSTANT   : (int ) GL_HISTOGRAM_LUMINANCE_SIZE_EXT = 0x802C
     ADD CONSTANT   : (int ) GL_HISTOGRAM_SINK_EXT = 0x802D
     ADD CONSTANT   : (int ) GL_MINMAX_EXT = 0x802E
     ADD CONSTANT   : (int ) GL_MINMAX_FORMAT_EXT = 0x802F
     ADD CONSTANT   : (int ) GL_MINMAX_SINK_EXT = 0x8030
     ADD CONSTANT   : (int ) GL_TABLE_TOO_LARGE_EXT = 0x8031
     ADD CONSTANT   : (int ) GL_POLYGON_OFFSET_EXT = 0x8037
     ADD CONSTANT   : (int ) GL_POLYGON_OFFSET_FACTOR_EXT = 0x8038
     ADD CONSTANT   : (int ) GL_POLYGON_OFFSET_BIAS_EXT = 0x8039
     ADD CONSTANT   : (int ) GL_ALPHA4_EXT = 0x803B
     ADD CONSTANT   : (int ) GL_ALPHA8_EXT = 0x803C
     ADD CONSTANT   : (int ) GL_ALPHA12_EXT = 0x803D
     ADD CONSTANT   : (int ) GL_ALPHA16_EXT = 0x803E
     ADD CONSTANT   : (int ) GL_LUMINANCE4_EXT = 0x803F
     ADD CONSTANT   : (int ) GL_LUMINANCE8_EXT = 0x8040
     ADD CONSTANT   : (int ) GL_LUMINANCE12_EXT = 0x8041
     ADD CONSTANT   : (int ) GL_LUMINANCE16_EXT = 0x8042
     ADD CONSTANT   : (int ) GL_LUMINANCE4_ALPHA4_EXT = 0x8043
     ADD CONSTANT   : (int ) GL_LUMINANCE6_ALPHA2_EXT = 0x8044
     ADD CONSTANT   : (int ) GL_LUMINANCE8_ALPHA8_EXT = 0x8045
     ADD CONSTANT   : (int ) GL_LUMINANCE12_ALPHA4_EXT = 0x8046
     ADD CONSTANT   : (int ) GL_LUMINANCE12_ALPHA12_EXT = 0x8047
     ADD CONSTANT   : (int ) GL_LUMINANCE16_ALPHA16_EXT = 0x8048
     ADD CONSTANT   : (int ) GL_INTENSITY_EXT = 0x8049
     ADD CONSTANT   : (int ) GL_INTENSITY4_EXT = 0x804A
     ADD CONSTANT   : (int ) GL_INTENSITY8_EXT = 0x804B
     ADD CONSTANT   : (int ) GL_INTENSITY12_EXT = 0x804C
     ADD CONSTANT   : (int ) GL_INTENSITY16_EXT = 0x804D
     ADD CONSTANT   : (int ) GL_RGB2_EXT = 0x804E
     ADD CONSTANT   : (int ) GL_RGB4_EXT = 0x804F
     ADD CONSTANT   : (int ) GL_RGB5_EXT = 0x8050
     ADD CONSTANT   : (int ) GL_RGB8_EXT = 0x8051
     ADD CONSTANT   : (int ) GL_RGB10_EXT = 0x8052
     ADD CONSTANT   : (int ) GL_RGB12_EXT = 0x8053
     ADD CONSTANT   : (int ) GL_RGB16_EXT = 0x8054
     ADD CONSTANT   : (int ) GL_RGBA2_EXT = 0x8055
     ADD CONSTANT   : (int ) GL_RGBA4_EXT = 0x8056
     ADD CONSTANT   : (int ) GL_RGB5_A1_EXT = 0x8057
     ADD CONSTANT   : (int ) GL_RGBA8_EXT = 0x8058
     ADD CONSTANT   : (int ) GL_RGB10_A2_EXT = 0x8059
     ADD CONSTANT   : (int ) GL_RGBA12_EXT = 0x805A
     ADD CONSTANT   : (int ) GL_RGBA16_EXT = 0x805B
     ADD CONSTANT   : (int ) GL_TEXTURE_RED_SIZE_EXT = 0x805C
     ADD CONSTANT   : (int ) GL_TEXTURE_GREEN_SIZE_EXT = 0x805D
     ADD CONSTANT   : (int ) GL_TEXTURE_BLUE_SIZE_EXT = 0x805E
     ADD CONSTANT   : (int ) GL_TEXTURE_ALPHA_SIZE_EXT = 0x805F
     ADD CONSTANT   : (int ) GL_TEXTURE_LUMINANCE_SIZE_EXT = 0x8060
     ADD CONSTANT   : (int ) GL_TEXTURE_INTENSITY_SIZE_EXT = 0x8061
     ADD CONSTANT   : (int ) GL_REPLACE_EXT = 0x8062
     ADD CONSTANT   : (int ) GL_PROXY_TEXTURE_1D_EXT = 0x8063
     ADD CONSTANT   : (int ) GL_PROXY_TEXTURE_2D_EXT = 0x8064
     ADD CONSTANT   : (int ) GL_TEXTURE_TOO_LARGE_EXT = 0x8065
     ADD CONSTANT   : (int ) GL_PACK_SKIP_IMAGES_EXT = 0x806B
     ADD CONSTANT   : (int ) GL_PACK_IMAGE_HEIGHT_EXT = 0x806C
     ADD CONSTANT   : (int ) GL_UNPACK_SKIP_IMAGES_EXT = 0x806D
     ADD CONSTANT   : (int ) GL_UNPACK_IMAGE_HEIGHT_EXT = 0x806E
     ADD CONSTANT   : (int ) GL_TEXTURE_3D_EXT = 0x806F
     ADD CONSTANT   : (int ) GL_PROXY_TEXTURE_3D_EXT = 0x8070
     ADD CONSTANT   : (int ) GL_TEXTURE_DEPTH_EXT = 0x8071
     ADD CONSTANT   : (int ) GL_TEXTURE_WRAP_R_EXT = 0x8072
     ADD CONSTANT   : (int ) GL_MAX_3D_TEXTURE_SIZE_EXT = 0x8073
     ADD CONSTANT   : (int ) GL_DETAIL_TEXTURE_2D_SGIS = 0x8095
     ADD CONSTANT   : (int ) GL_DETAIL_TEXTURE_2D_BINDING_SGIS = 0x8096
     ADD CONSTANT   : (int ) GL_LINEAR_DETAIL_SGIS = 0x8097
     ADD CONSTANT   : (int ) GL_LINEAR_DETAIL_ALPHA_SGIS = 0x8098
     ADD CONSTANT   : (int ) GL_LINEAR_DETAIL_COLOR_SGIS = 0x8099
     ADD CONSTANT   : (int ) GL_DETAIL_TEXTURE_LEVEL_SGIS = 0x809A
     ADD CONSTANT   : (int ) GL_DETAIL_TEXTURE_MODE_SGIS = 0x809B
     ADD CONSTANT   : (int ) GL_DETAIL_TEXTURE_FUNC_POINTS_SGIS = 0x809C
     ADD CONSTANT   : (int ) GL_MULTISAMPLE_BIT_EXT = 0x20000000
     ADD CONSTANT   : (int ) GL_MULTISAMPLE_SGIS = 0x809D
     ADD CONSTANT   : (int ) GL_SAMPLE_ALPHA_TO_MASK_SGIS = 0x809E
     ADD CONSTANT   : (int ) GL_SAMPLE_ALPHA_TO_ONE_SGIS = 0x809F
     ADD CONSTANT   : (int ) GL_SAMPLE_MASK_SGIS = 0x80A0
     ADD CONSTANT   : (int ) GL_1PASS_SGIS = 0x80A1
     ADD CONSTANT   : (int ) GL_2PASS_0_SGIS = 0x80A2
     ADD CONSTANT   : (int ) GL_2PASS_1_SGIS = 0x80A3
     ADD CONSTANT   : (int ) GL_4PASS_0_SGIS = 0x80A4
     ADD CONSTANT   : (int ) GL_4PASS_1_SGIS = 0x80A5
     ADD CONSTANT   : (int ) GL_4PASS_2_SGIS = 0x80A6
     ADD CONSTANT   : (int ) GL_4PASS_3_SGIS = 0x80A7
     ADD CONSTANT   : (int ) GL_SAMPLE_BUFFERS_SGIS = 0x80A8
     ADD CONSTANT   : (int ) GL_SAMPLES_SGIS = 0x80A9
     ADD CONSTANT   : (int ) GL_SAMPLE_MASK_VALUE_SGIS = 0x80AA
     ADD CONSTANT   : (int ) GL_SAMPLE_MASK_INVERT_SGIS = 0x80AB
     ADD CONSTANT   : (int ) GL_SAMPLE_PATTERN_SGIS = 0x80AC
     ADD CONSTANT   : (int ) GL_LINEAR_SHARPEN_SGIS = 0x80AD
     ADD CONSTANT   : (int ) GL_LINEAR_SHARPEN_ALPHA_SGIS = 0x80AE
     ADD CONSTANT   : (int ) GL_LINEAR_SHARPEN_COLOR_SGIS = 0x80AF
     ADD CONSTANT   : (int ) GL_SHARPEN_TEXTURE_FUNC_POINTS_SGIS = 0x80B0
     ADD COMMAND    : glAccum --> void glAccum(GLenum ,GLfloat );
     ADD COMMAND    : glAlphaFunc --> void glAlphaFunc(GLenum ,GLclampf );
     ADD COMMAND    : glBegin --> void glBegin(GLenum );
     ADD COMMAND    : glBitmap --> void glBitmap(GLsizei ,GLsizei ,GLfloat ,GLfloat ,GLfloat ,GLfloat ,const GLubyte *);
     ADD COMMAND    : glBlendColorEXT --> void glBlendColorEXT(GLclampf ,GLclampf ,GLclampf ,GLclampf );
     ADD COMMAND    : glBlendEquationEXT --> void glBlendEquationEXT(GLenum );
     ADD COMMAND    : glBlendFunc --> void glBlendFunc(GLenum ,GLenum );
     ADD COMMAND    : glCallList --> void glCallList(GLuint );
     ADD COMMAND    : glCallLists --> void glCallLists(GLsizei ,GLenum ,const GLvoid *);
     ADD COMMAND    : glClear --> void glClear(GLbitfield );
     ADD COMMAND    : glClearAccum --> void glClearAccum(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glClearColor --> void glClearColor(GLclampf ,GLclampf ,GLclampf ,GLclampf );
     ADD COMMAND    : glClearDepth --> void glClearDepth(GLclampd );
     ADD COMMAND    : glClearIndex --> void glClearIndex(GLfloat );
     ADD COMMAND    : glClearStencil --> void glClearStencil(GLint );
     ADD COMMAND    : glClipPlane --> void glClipPlane(GLenum ,const GLdouble *);
     ADD COMMAND    : glColor3b --> void glColor3b(GLbyte ,GLbyte ,GLbyte );
     ADD COMMAND    : glColor3bv --> void glColor3bv(const GLbyte *);
     ADD COMMAND    : glColor3d --> void glColor3d(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glColor3dv --> void glColor3dv(const GLdouble *);
     ADD COMMAND    : glColor3f --> void glColor3f(GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glColor3fv --> void glColor3fv(const GLfloat *);
     ADD COMMAND    : glColor3i --> void glColor3i(GLint ,GLint ,GLint );
     ADD COMMAND    : glColor3iv --> void glColor3iv(const GLint *);
     ADD COMMAND    : glColor3s --> void glColor3s(GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glColor3sv --> void glColor3sv(const GLshort *);
     ADD COMMAND    : glColor3ub --> void glColor3ub(GLubyte ,GLubyte ,GLubyte );
     ADD COMMAND    : glColor3ubv --> void glColor3ubv(const GLubyte *);
     ADD COMMAND    : glColor3ui --> void glColor3ui(GLuint ,GLuint ,GLuint );
     ADD COMMAND    : glColor3uiv --> void glColor3uiv(const GLuint *);
     ADD COMMAND    : glColor3us --> void glColor3us(GLushort ,GLushort ,GLushort );
     ADD COMMAND    : glColor3usv --> void glColor3usv(const GLushort *);
     ADD COMMAND    : glColor4b --> void glColor4b(GLbyte ,GLbyte ,GLbyte ,GLbyte );
     ADD COMMAND    : glColor4bv --> void glColor4bv(const GLbyte *);
     ADD COMMAND    : glColor4d --> void glColor4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glColor4dv --> void glColor4dv(const GLdouble *);
     ADD COMMAND    : glColor4f --> void glColor4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glColor4fv --> void glColor4fv(const GLfloat *);
     ADD COMMAND    : glColor4i --> void glColor4i(GLint ,GLint ,GLint ,GLint );
     ADD COMMAND    : glColor4iv --> void glColor4iv(const GLint *);
     ADD COMMAND    : glColor4s --> void glColor4s(GLshort ,GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glColor4sv --> void glColor4sv(const GLshort *);
     ADD COMMAND    : glColor4ub --> void glColor4ub(GLubyte ,GLubyte ,GLubyte ,GLubyte );
     ADD COMMAND    : glColor4ubv --> void glColor4ubv(const GLubyte *);
     ADD COMMAND    : glColor4ui --> void glColor4ui(GLuint ,GLuint ,GLuint ,GLuint );
     ADD COMMAND    : glColor4uiv --> void glColor4uiv(const GLuint *);
     ADD COMMAND    : glColor4us --> void glColor4us(GLushort ,GLushort ,GLushort ,GLushort );
     ADD COMMAND    : glColor4usv --> void glColor4usv(const GLushort *);
     ADD COMMAND    : glColorMask --> void glColorMask(GLboolean ,GLboolean ,GLboolean ,GLboolean );
     ADD COMMAND    : glColorMaterial --> void glColorMaterial(GLenum ,GLenum );
     ADD COMMAND    : glCopyPixels --> void glCopyPixels(GLint ,GLint ,GLsizei ,GLsizei ,GLenum );
     ADD COMMAND    : glCullFace --> void glCullFace(GLenum );
     ADD COMMAND    : glDeleteLists --> void glDeleteLists(GLuint ,GLsizei );
     ADD COMMAND    : glDepthFunc --> void glDepthFunc(GLenum );
     ADD COMMAND    : glDepthMask --> void glDepthMask(GLboolean );
     ADD COMMAND    : glDepthRange --> void glDepthRange(GLclampd ,GLclampd );
     ADD COMMAND    : glDisable --> void glDisable(GLenum );
     ADD COMMAND    : glDrawBuffer --> void glDrawBuffer(GLenum );
     ADD COMMAND    : glDrawPixels --> void glDrawPixels(GLsizei ,GLsizei ,GLenum ,GLenum ,const GLvoid *);
     ADD COMMAND    : glEdgeFlag --> void glEdgeFlag(GLboolean );
     ADD COMMAND    : glEdgeFlagv --> void glEdgeFlagv(const GLboolean *);
     ADD COMMAND    : glEnable --> void glEnable(GLenum );
     ADD COMMAND    : glEnd --> void glEnd();
     ADD COMMAND    : glEndList --> void glEndList();
     ADD COMMAND    : glEvalCoord1d --> void glEvalCoord1d(GLdouble );
     ADD COMMAND    : glEvalCoord1dv --> void glEvalCoord1dv(const GLdouble *);
     ADD COMMAND    : glEvalCoord1f --> void glEvalCoord1f(GLfloat );
     ADD COMMAND    : glEvalCoord1fv --> void glEvalCoord1fv(const GLfloat *);
     ADD COMMAND    : glEvalCoord2d --> void glEvalCoord2d(GLdouble ,GLdouble );
     ADD COMMAND    : glEvalCoord2dv --> void glEvalCoord2dv(const GLdouble *);
     ADD COMMAND    : glEvalCoord2f --> void glEvalCoord2f(GLfloat ,GLfloat );
     ADD COMMAND    : glEvalCoord2fv --> void glEvalCoord2fv(const GLfloat *);
     ADD COMMAND    : glEvalMesh1 --> void glEvalMesh1(GLenum ,GLint ,GLint );
     ADD COMMAND    : glEvalMesh2 --> void glEvalMesh2(GLenum ,GLint ,GLint ,GLint ,GLint );
     ADD COMMAND    : glEvalPoint1 --> void glEvalPoint1(GLint );
     ADD COMMAND    : glEvalPoint2 --> void glEvalPoint2(GLint ,GLint );
     ADD COMMAND    : glFeedbackBuffer --> void glFeedbackBuffer(GLsizei ,GLenum ,GLfloat *);
     ADD COMMAND    : glFinish --> void glFinish();
     ADD COMMAND    : glFlush --> void glFlush();
     ADD COMMAND    : glFogf --> void glFogf(GLenum ,GLfloat );
     ADD COMMAND    : glFogfv --> void glFogfv(GLenum ,const GLfloat *);
     ADD COMMAND    : glFogi --> void glFogi(GLenum ,GLint );
     ADD COMMAND    : glFogiv --> void glFogiv(GLenum ,const GLint *);
     ADD COMMAND    : glFrontFace --> void glFrontFace(GLenum );
     ADD COMMAND    : glFrustum --> void glFrustum(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glGenLists --> GLuint glGenLists(GLsizei );
     ADD COMMAND    : glGetBooleanv --> void glGetBooleanv(GLenum ,GLboolean *);
     ADD COMMAND    : glGetClipPlane --> void glGetClipPlane(GLenum ,GLdouble *);
     ADD COMMAND    : glGetDoublev --> void glGetDoublev(GLenum ,GLdouble *);
     ADD COMMAND    : glGetError --> GLenum glGetError();
     ADD COMMAND    : glGetFloatv --> void glGetFloatv(GLenum ,GLfloat *);
     ADD COMMAND    : glGetIntegerv --> void glGetIntegerv(GLenum ,GLint *);
     ADD COMMAND    : glGetLightfv --> void glGetLightfv(GLenum ,GLenum ,GLfloat *);
     ADD COMMAND    : glGetLightiv --> void glGetLightiv(GLenum ,GLenum ,GLint *);
     ADD COMMAND    : glGetMapdv --> void glGetMapdv(GLenum ,GLenum ,GLdouble *);
     ADD COMMAND    : glGetMapfv --> void glGetMapfv(GLenum ,GLenum ,GLfloat *);
     ADD COMMAND    : glGetMapiv --> void glGetMapiv(GLenum ,GLenum ,GLint *);
     ADD COMMAND    : glGetMaterialfv --> void glGetMaterialfv(GLenum ,GLenum ,GLfloat *);
     ADD COMMAND    : glGetMaterialiv --> void glGetMaterialiv(GLenum ,GLenum ,GLint *);
     ADD COMMAND    : glGetPixelMapfv --> void glGetPixelMapfv(GLenum ,GLfloat *);
     ADD COMMAND    : glGetPixelMapuiv --> void glGetPixelMapuiv(GLenum ,GLuint *);
     ADD COMMAND    : glGetPixelMapusv --> void glGetPixelMapusv(GLenum ,GLushort *);
     ADD COMMAND    : glGetPolygonStipple --> void glGetPolygonStipple(GLubyte *);
     ADD COMMAND    : glGetString --> const GLubyte *glGetString(GLenum );
     ADD COMMAND    : glGetTexEnvfv --> void glGetTexEnvfv(GLenum ,GLenum ,GLfloat *);
     ADD COMMAND    : glGetTexEnviv --> void glGetTexEnviv(GLenum ,GLenum ,GLint *);
     ADD COMMAND    : glGetTexGendv --> void glGetTexGendv(GLenum ,GLenum ,GLdouble *);
     ADD COMMAND    : glGetTexGenfv --> void glGetTexGenfv(GLenum ,GLenum ,GLfloat *);
     ADD COMMAND    : glGetTexGeniv --> void glGetTexGeniv(GLenum ,GLenum ,GLint *);
     ADD COMMAND    : glGetTexImage --> void glGetTexImage(GLenum ,GLint ,GLenum ,GLenum ,GLvoid *);
     ADD COMMAND    : glGetTexLevelParameterfv --> void glGetTexLevelParameterfv(GLenum ,GLint ,GLenum ,GLfloat *);
     ADD COMMAND    : glGetTexLevelParameteriv --> void glGetTexLevelParameteriv(GLenum ,GLint ,GLenum ,GLint *);
     ADD COMMAND    : glGetTexParameterfv --> void glGetTexParameterfv(GLenum ,GLenum ,GLfloat *);
     ADD COMMAND    : glGetTexParameteriv --> void glGetTexParameteriv(GLenum ,GLenum ,GLint *);
     ADD COMMAND    : glHint --> void glHint(GLenum ,GLenum );
     ADD COMMAND    : glIndexMask --> void glIndexMask(GLuint );
     ADD COMMAND    : glIndexd --> void glIndexd(GLdouble );
     ADD COMMAND    : glIndexdv --> void glIndexdv(const GLdouble *);
     ADD COMMAND    : glIndexf --> void glIndexf(GLfloat );
     ADD COMMAND    : glIndexfv --> void glIndexfv(const GLfloat *);
     ADD COMMAND    : glIndexi --> void glIndexi(GLint );
     ADD COMMAND    : glIndexiv --> void glIndexiv(const GLint *);
     ADD COMMAND    : glIndexs --> void glIndexs(GLshort );
     ADD COMMAND    : glIndexsv --> void glIndexsv(const GLshort *);
     ADD COMMAND    : glInitNames --> void glInitNames();
     ADD COMMAND    : glIsEnabled --> GLboolean glIsEnabled(GLenum );
     ADD COMMAND    : glIsList --> GLboolean glIsList(GLuint );
     ADD COMMAND    : glLightModelf --> void glLightModelf(GLenum ,GLfloat );
     ADD COMMAND    : glLightModelfv --> void glLightModelfv(GLenum ,const GLfloat *);
     ADD COMMAND    : glLightModeli --> void glLightModeli(GLenum ,GLint );
     ADD COMMAND    : glLightModeliv --> void glLightModeliv(GLenum ,const GLint *);
     ADD COMMAND    : glLightf --> void glLightf(GLenum ,GLenum ,GLfloat );
     ADD COMMAND    : glLightfv --> void glLightfv(GLenum ,GLenum ,const GLfloat *);
     ADD COMMAND    : glLighti --> void glLighti(GLenum ,GLenum ,GLint );
     ADD COMMAND    : glLightiv --> void glLightiv(GLenum ,GLenum ,const GLint *);
     ADD COMMAND    : glLineStipple --> void glLineStipple(GLint ,GLushort );
     ADD COMMAND    : glLineWidth --> void glLineWidth(GLfloat );
     ADD COMMAND    : glListBase --> void glListBase(GLuint );
     ADD COMMAND    : glLoadIdentity --> void glLoadIdentity();
     ADD COMMAND    : glLoadMatrixd --> void glLoadMatrixd(const GLdouble *);
     ADD COMMAND    : glLoadMatrixf --> void glLoadMatrixf(const GLfloat *);
     ADD COMMAND    : glLoadName --> void glLoadName(GLuint );
     ADD COMMAND    : glLogicOp --> void glLogicOp(GLenum );
     ADD COMMAND    : glMap1d --> void glMap1d(GLenum ,GLdouble ,GLdouble ,GLint ,GLint ,const GLdouble *);
     ADD COMMAND    : glMap1f --> void glMap1f(GLenum ,GLfloat ,GLfloat ,GLint ,GLint ,const GLfloat *);
     ADD COMMAND    : glMap2d --> void glMap2d(GLenum ,GLdouble ,GLdouble ,GLint ,GLint ,GLdouble ,GLdouble ,GLint ,GLint ,const GLdouble *);
     ADD COMMAND    : glMap2f --> void glMap2f(GLenum ,GLfloat ,GLfloat ,GLint ,GLint ,GLfloat ,GLfloat ,GLint ,GLint ,const GLfloat *);
     ADD COMMAND    : glMapGrid1d --> void glMapGrid1d(GLint ,GLdouble ,GLdouble );
     ADD COMMAND    : glMapGrid1f --> void glMapGrid1f(GLint ,GLfloat ,GLfloat );
     ADD COMMAND    : glMapGrid2d --> void glMapGrid2d(GLint ,GLdouble ,GLdouble ,GLint ,GLdouble ,GLdouble );
     ADD COMMAND    : glMapGrid2f --> void glMapGrid2f(GLint ,GLfloat ,GLfloat ,GLint ,GLfloat ,GLfloat );
     ADD COMMAND    : glMaterialf --> void glMaterialf(GLenum ,GLenum ,GLfloat );
     ADD COMMAND    : glMaterialfv --> void glMaterialfv(GLenum ,GLenum ,const GLfloat *);
     ADD COMMAND    : glMateriali --> void glMateriali(GLenum ,GLenum ,GLint );
     ADD COMMAND    : glMaterialiv --> void glMaterialiv(GLenum ,GLenum ,const GLint *);
     ADD COMMAND    : glMatrixMode --> void glMatrixMode(GLenum );
     ADD COMMAND    : glMultMatrixd --> void glMultMatrixd(const GLdouble *);
     ADD COMMAND    : glMultMatrixf --> void glMultMatrixf(const GLfloat *);
     ADD COMMAND    : glNewList --> void glNewList(GLuint ,GLenum );
     ADD COMMAND    : glNormal3b --> void glNormal3b(GLbyte ,GLbyte ,GLbyte );
     ADD COMMAND    : glNormal3bv --> void glNormal3bv(const GLbyte *);
     ADD COMMAND    : glNormal3d --> void glNormal3d(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glNormal3dv --> void glNormal3dv(const GLdouble *);
     ADD COMMAND    : glNormal3f --> void glNormal3f(GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glNormal3fv --> void glNormal3fv(const GLfloat *);
     ADD COMMAND    : glNormal3i --> void glNormal3i(GLint ,GLint ,GLint );
     ADD COMMAND    : glNormal3iv --> void glNormal3iv(const GLint *);
     ADD COMMAND    : glNormal3s --> void glNormal3s(GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glNormal3sv --> void glNormal3sv(const GLshort *);
     ADD COMMAND    : glOrtho --> void glOrtho(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glPassThrough --> void glPassThrough(GLfloat );
     ADD COMMAND    : glPixelMapfv --> void glPixelMapfv(GLenum ,GLint ,const GLfloat *);
     ADD COMMAND    : glPixelMapuiv --> void glPixelMapuiv(GLenum ,GLint ,const GLuint *);
     ADD COMMAND    : glPixelMapusv --> void glPixelMapusv(GLenum ,GLint ,const GLushort *);
     ADD COMMAND    : glPixelStoref --> void glPixelStoref(GLenum ,GLfloat );
     ADD COMMAND    : glPixelStorei --> void glPixelStorei(GLenum ,GLint );
     ADD COMMAND    : glPixelTransferf --> void glPixelTransferf(GLenum ,GLfloat );
     ADD COMMAND    : glPixelTransferi --> void glPixelTransferi(GLenum ,GLint );
     ADD COMMAND    : glPixelZoom --> void glPixelZoom(GLfloat ,GLfloat );
     ADD COMMAND    : glPointSize --> void glPointSize(GLfloat );
     ADD COMMAND    : glPolygonMode --> void glPolygonMode(GLenum ,GLenum );
     ADD COMMAND    : glPolygonOffsetEXT --> void glPolygonOffsetEXT(GLfloat ,GLfloat );
     ADD COMMAND    : glPolygonStipple --> void glPolygonStipple(const GLubyte *);
     ADD COMMAND    : glPopAttrib --> void glPopAttrib();
     ADD COMMAND    : glPopMatrix --> void glPopMatrix();
     ADD COMMAND    : glPopName --> void glPopName();
     ADD COMMAND    : glPushAttrib --> void glPushAttrib(GLbitfield );
     ADD COMMAND    : glPushMatrix --> void glPushMatrix();
     ADD COMMAND    : glPushName --> void glPushName(GLuint );
     ADD COMMAND    : glRasterPos2d --> void glRasterPos2d(GLdouble ,GLdouble );
     ADD COMMAND    : glRasterPos2dv --> void glRasterPos2dv(const GLdouble *);
     ADD COMMAND    : glRasterPos2f --> void glRasterPos2f(GLfloat ,GLfloat );
     ADD COMMAND    : glRasterPos2fv --> void glRasterPos2fv(const GLfloat *);
     ADD COMMAND    : glRasterPos2i --> void glRasterPos2i(GLint ,GLint );
     ADD COMMAND    : glRasterPos2iv --> void glRasterPos2iv(const GLint *);
     ADD COMMAND    : glRasterPos2s --> void glRasterPos2s(GLshort ,GLshort );
     ADD COMMAND    : glRasterPos2sv --> void glRasterPos2sv(const GLshort *);
     ADD COMMAND    : glRasterPos3d --> void glRasterPos3d(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glRasterPos3dv --> void glRasterPos3dv(const GLdouble *);
     ADD COMMAND    : glRasterPos3f --> void glRasterPos3f(GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glRasterPos3fv --> void glRasterPos3fv(const GLfloat *);
     ADD COMMAND    : glRasterPos3i --> void glRasterPos3i(GLint ,GLint ,GLint );
     ADD COMMAND    : glRasterPos3iv --> void glRasterPos3iv(const GLint *);
     ADD COMMAND    : glRasterPos3s --> void glRasterPos3s(GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glRasterPos3sv --> void glRasterPos3sv(const GLshort *);
     ADD COMMAND    : glRasterPos4d --> void glRasterPos4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glRasterPos4dv --> void glRasterPos4dv(const GLdouble *);
     ADD COMMAND    : glRasterPos4f --> void glRasterPos4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glRasterPos4fv --> void glRasterPos4fv(const GLfloat *);
     ADD COMMAND    : glRasterPos4i --> void glRasterPos4i(GLint ,GLint ,GLint ,GLint );
     ADD COMMAND    : glRasterPos4iv --> void glRasterPos4iv(const GLint *);
     ADD COMMAND    : glRasterPos4s --> void glRasterPos4s(GLshort ,GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glRasterPos4sv --> void glRasterPos4sv(const GLshort *);
     ADD COMMAND    : glReadBuffer --> void glReadBuffer(GLenum );
     ADD COMMAND    : glReadPixels --> void glReadPixels(GLint ,GLint ,GLsizei ,GLsizei ,GLenum ,GLenum ,GLvoid *);
     ADD COMMAND    : glRectd --> void glRectd(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glRectdv --> void glRectdv(const GLdouble *,const GLdouble *);
     ADD COMMAND    : glRectf --> void glRectf(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glRectfv --> void glRectfv(const GLfloat *,const GLfloat *);
     ADD COMMAND    : glRecti --> void glRecti(GLint ,GLint ,GLint ,GLint );
     ADD COMMAND    : glRectiv --> void glRectiv(const GLint *,const GLint *);
     ADD COMMAND    : glRects --> void glRects(GLshort ,GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glRectsv --> void glRectsv(const GLshort *,const GLshort *);
     ADD COMMAND    : glRenderMode --> GLint glRenderMode(GLenum );
     ADD COMMAND    : glRotated --> void glRotated(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glRotatef --> void glRotatef(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glScaled --> void glScaled(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glScalef --> void glScalef(GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glScissor --> void glScissor(GLint ,GLint ,GLsizei ,GLsizei );
     ADD COMMAND    : glSelectBuffer --> void glSelectBuffer(GLsizei ,GLuint *);
     ADD COMMAND    : glShadeModel --> void glShadeModel(GLenum );
     ADD COMMAND    : glStencilFunc --> void glStencilFunc(GLenum ,GLint ,GLuint );
     ADD COMMAND    : glStencilMask --> void glStencilMask(GLuint );
     ADD COMMAND    : glStencilOp --> void glStencilOp(GLenum ,GLenum ,GLenum );
     ADD COMMAND    : glTexCoord1d --> void glTexCoord1d(GLdouble );
     ADD COMMAND    : glTexCoord1dv --> void glTexCoord1dv(const GLdouble *);
     ADD COMMAND    : glTexCoord1f --> void glTexCoord1f(GLfloat );
     ADD COMMAND    : glTexCoord1fv --> void glTexCoord1fv(const GLfloat *);
     ADD COMMAND    : glTexCoord1i --> void glTexCoord1i(GLint );
     ADD COMMAND    : glTexCoord1iv --> void glTexCoord1iv(const GLint *);
     ADD COMMAND    : glTexCoord1s --> void glTexCoord1s(GLshort );
     ADD COMMAND    : glTexCoord1sv --> void glTexCoord1sv(const GLshort *);
     ADD COMMAND    : glTexCoord2d --> void glTexCoord2d(GLdouble ,GLdouble );
     ADD COMMAND    : glTexCoord2dv --> void glTexCoord2dv(const GLdouble *);
     ADD COMMAND    : glTexCoord2f --> void glTexCoord2f(GLfloat ,GLfloat );
     ADD COMMAND    : glTexCoord2fv --> void glTexCoord2fv(const GLfloat *);
     ADD COMMAND    : glTexCoord2i --> void glTexCoord2i(GLint ,GLint );
     ADD COMMAND    : glTexCoord2iv --> void glTexCoord2iv(const GLint *);
     ADD COMMAND    : glTexCoord2s --> void glTexCoord2s(GLshort ,GLshort );
     ADD COMMAND    : glTexCoord2sv --> void glTexCoord2sv(const GLshort *);
     ADD COMMAND    : glTexCoord3d --> void glTexCoord3d(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glTexCoord3dv --> void glTexCoord3dv(const GLdouble *);
     ADD COMMAND    : glTexCoord3f --> void glTexCoord3f(GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glTexCoord3fv --> void glTexCoord3fv(const GLfloat *);
     ADD COMMAND    : glTexCoord3i --> void glTexCoord3i(GLint ,GLint ,GLint );
     ADD COMMAND    : glTexCoord3iv --> void glTexCoord3iv(const GLint *);
     ADD COMMAND    : glTexCoord3s --> void glTexCoord3s(GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glTexCoord3sv --> void glTexCoord3sv(const GLshort *);
     ADD COMMAND    : glTexCoord4d --> void glTexCoord4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glTexCoord4dv --> void glTexCoord4dv(const GLdouble *);
     ADD COMMAND    : glTexCoord4f --> void glTexCoord4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glTexCoord4fv --> void glTexCoord4fv(const GLfloat *);
     ADD COMMAND    : glTexCoord4i --> void glTexCoord4i(GLint ,GLint ,GLint ,GLint );
     ADD COMMAND    : glTexCoord4iv --> void glTexCoord4iv(const GLint *);
     ADD COMMAND    : glTexCoord4s --> void glTexCoord4s(GLshort ,GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glTexCoord4sv --> void glTexCoord4sv(const GLshort *);
     ADD COMMAND    : glTexEnvf --> void glTexEnvf(GLenum ,GLenum ,GLfloat );
     ADD COMMAND    : glTexEnvfv --> void glTexEnvfv(GLenum ,GLenum ,const GLfloat *);
     ADD COMMAND    : glTexEnvi --> void glTexEnvi(GLenum ,GLenum ,GLint );
     ADD COMMAND    : glTexEnviv --> void glTexEnviv(GLenum ,GLenum ,const GLint *);
     ADD COMMAND    : glTexGend --> void glTexGend(GLenum ,GLenum ,GLdouble );
     ADD COMMAND    : glTexGendv --> void glTexGendv(GLenum ,GLenum ,const GLdouble *);
     ADD COMMAND    : glTexGenf --> void glTexGenf(GLenum ,GLenum ,GLfloat );
     ADD COMMAND    : glTexGenfv --> void glTexGenfv(GLenum ,GLenum ,const GLfloat *);
     ADD COMMAND    : glTexGeni --> void glTexGeni(GLenum ,GLenum ,GLint );
     ADD COMMAND    : glTexGeniv --> void glTexGeniv(GLenum ,GLenum ,const GLint *);
     ADD COMMAND    : glTexImage1D --> void glTexImage1D(GLenum ,GLint ,GLint ,GLsizei ,GLint ,GLenum ,GLenum ,const GLvoid *);
     ADD COMMAND    : glTexImage2D --> void glTexImage2D(GLenum ,GLint ,GLint ,GLsizei ,GLsizei ,GLint ,GLenum ,GLenum ,const GLvoid *);
     ADD COMMAND    : glTexParameterf --> void glTexParameterf(GLenum ,GLenum ,GLfloat );
     ADD COMMAND    : glTexParameterfv --> void glTexParameterfv(GLenum ,GLenum ,const GLfloat *);
     ADD COMMAND    : glTexParameteri --> void glTexParameteri(GLenum ,GLenum ,GLint );
     ADD COMMAND    : glTexParameteriv --> void glTexParameteriv(GLenum ,GLenum ,const GLint *);
     ADD COMMAND    : glTranslated --> void glTranslated(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glTranslatef --> void glTranslatef(GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glVertex2d --> void glVertex2d(GLdouble ,GLdouble );
     ADD COMMAND    : glVertex2dv --> void glVertex2dv(const GLdouble *);
     ADD COMMAND    : glVertex2f --> void glVertex2f(GLfloat ,GLfloat );
     ADD COMMAND    : glVertex2fv --> void glVertex2fv(const GLfloat *);
     ADD COMMAND    : glVertex2i --> void glVertex2i(GLint ,GLint );
     ADD COMMAND    : glVertex2iv --> void glVertex2iv(const GLint *);
     ADD COMMAND    : glVertex2s --> void glVertex2s(GLshort ,GLshort );
     ADD COMMAND    : glVertex2sv --> void glVertex2sv(const GLshort *);
     ADD COMMAND    : glVertex3d --> void glVertex3d(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glVertex3dv --> void glVertex3dv(const GLdouble *);
     ADD COMMAND    : glVertex3f --> void glVertex3f(GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glVertex3fv --> void glVertex3fv(const GLfloat *);
     ADD COMMAND    : glVertex3i --> void glVertex3i(GLint ,GLint ,GLint );
     ADD COMMAND    : glVertex3iv --> void glVertex3iv(const GLint *);
     ADD COMMAND    : glVertex3s --> void glVertex3s(GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glVertex3sv --> void glVertex3sv(const GLshort *);
     ADD COMMAND    : glVertex4d --> void glVertex4d(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : glVertex4dv --> void glVertex4dv(const GLdouble *);
     ADD COMMAND    : glVertex4f --> void glVertex4f(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : glVertex4fv --> void glVertex4fv(const GLfloat *);
     ADD COMMAND    : glVertex4i --> void glVertex4i(GLint ,GLint ,GLint ,GLint );
     ADD COMMAND    : glVertex4iv --> void glVertex4iv(const GLint *);
     ADD COMMAND    : glVertex4s --> void glVertex4s(GLshort ,GLshort ,GLshort ,GLshort );
     ADD COMMAND    : glVertex4sv --> void glVertex4sv(const GLshort *);
     ADD COMMAND    : glViewport --> void glViewport(GLint ,GLint ,GLsizei ,GLsizei );
     ADD COMMAND    : gluErrorString --> const GLubyte *gluErrorString(GLenum );
     ADD COMMAND    : gluGetString --> const GLubyte *gluGetString(GLenum );
     ADD COMMAND    : gluOrtho2D --> void gluOrtho2D(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : gluPerspective --> void gluPerspective(GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : gluLookAt --> void gluLookAt(GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : gluScaleImage --> int gluScaleImage(GLenum ,GLint ,GLint ,GLenum ,const void *,GLint ,GLint ,GLenum ,void *);
     ADD COMMAND    : gluBuild1DMipmaps --> int gluBuild1DMipmaps(GLenum ,GLint ,GLint ,GLenum ,GLenum ,const void *);
     ADD COMMAND    : gluBuild2DMipmaps --> int gluBuild2DMipmaps(GLenum ,GLint ,GLint ,GLint ,GLenum ,GLenum ,const void *);
     ADD COMMAND    : gluNewQuadric --> GLUquadricObj *gluNewQuadric();
     ADD COMMAND    : gluDeleteQuadric --> void gluDeleteQuadric(GLUquadricObj *);
     ADD COMMAND    : gluQuadricNormals --> void gluQuadricNormals(GLUquadricObj *,GLenum );
     ADD COMMAND    : gluQuadricTexture --> void gluQuadricTexture(GLUquadricObj *,GLboolean );
     ADD COMMAND    : gluQuadricOrientation --> void gluQuadricOrientation(GLUquadricObj *,GLenum );
     ADD COMMAND    : gluQuadricDrawStyle --> void gluQuadricDrawStyle(GLUquadricObj *,GLenum );
     ADD COMMAND    : gluCylinder --> void gluCylinder(GLUquadricObj *,GLdouble ,GLdouble ,GLdouble ,GLint ,GLint );
     ADD COMMAND    : gluDisk --> void gluDisk(GLUquadricObj *,GLdouble ,GLdouble ,GLint ,GLint );
     ADD COMMAND    : gluPartialDisk --> void gluPartialDisk(GLUquadricObj *,GLdouble ,GLdouble ,GLint ,GLint ,GLdouble ,GLdouble );
     ADD COMMAND    : gluSphere --> void gluSphere(GLUquadricObj *,GLdouble ,GLint ,GLint );
     ADD COMMAND    : gluNewTess --> GLUtriangulatorObj *gluNewTess();
     ADD COMMAND    : gluDeleteTess --> void gluDeleteTess(GLUtriangulatorObj *);
     ADD COMMAND    : gluBeginPolygon --> void gluBeginPolygon(GLUtriangulatorObj *);
     ADD COMMAND    : gluEndPolygon --> void gluEndPolygon(GLUtriangulatorObj *);
     ADD COMMAND    : gluNextContour --> void gluNextContour(GLUtriangulatorObj *,GLenum );
     ADD COMMAND    : gluNewNurbsRenderer --> GLUnurbsObj *gluNewNurbsRenderer();
     ADD COMMAND    : gluDeleteNurbsRenderer --> void gluDeleteNurbsRenderer(GLUnurbsObj *);
     ADD COMMAND    : gluBeginSurface --> void gluBeginSurface(GLUnurbsObj *);
     ADD COMMAND    : gluBeginCurve --> void gluBeginCurve(GLUnurbsObj *);
     ADD COMMAND    : gluEndCurve --> void gluEndCurve(GLUnurbsObj *);
     ADD COMMAND    : gluEndSurface --> void gluEndSurface(GLUnurbsObj *);
     ADD COMMAND    : gluBeginTrim --> void gluBeginTrim(GLUnurbsObj *);
     ADD COMMAND    : gluEndTrim --> void gluEndTrim(GLUnurbsObj *);
     ADD COMMAND    : gluPwlCurve --> void gluPwlCurve(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLenum );
     ADD COMMAND    : gluNurbsCurve --> void gluNurbsCurve(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLfloat *,GLint ,GLenum );
     ADD COMMAND    : gluNurbsSurface --> void gluNurbsSurface(GLUnurbsObj *,GLint ,GLfloat *,GLint ,GLfloat *,GLint ,GLint ,GLfloat *,GLint ,GLint ,GLenum );
     ADD COMMAND    : gluNurbsProperty --> void gluNurbsProperty(GLUnurbsObj *,GLenum ,GLfloat );
     ADD COMMAND    : gluGetNurbsProperty --> void gluGetNurbsProperty(GLUnurbsObj *,GLenum ,GLfloat *);
     ADD CONSTANT   : (int ) GLU_INVALID_ENUM = 100900
     ADD CONSTANT   : (int ) GLU_INVALID_VALUE = 100901
     ADD CONSTANT   : (int ) GLU_OUT_OF_MEMORY = 100902
     ADD CONSTANT   : (int ) GLU_INCOMPATIBLE_GL_VERSION = 100903
     ADD CONSTANT   : (int ) GLU_VERSION = 100800
     ADD CONSTANT   : (int ) GLU_EXTENSIONS = 100801
     ADD CONSTANT   : (int ) GLU_TRUE = (1)
     ADD CONSTANT   : (int ) GLU_FALSE = (0)
     ADD CONSTANT   : (int ) GLU_SMOOTH = 100000
     ADD CONSTANT   : (int ) GLU_FLAT = 100001
     ADD CONSTANT   : (int ) GLU_NONE = 100002
     ADD CONSTANT   : (int ) GLU_POINT = 100010
     ADD CONSTANT   : (int ) GLU_LINE = 100011
     ADD CONSTANT   : (int ) GLU_FILL = 100012
     ADD CONSTANT   : (int ) GLU_SILHOUETTE = 100013
     ADD CONSTANT   : (int ) GLU_OUTSIDE = 100020
     ADD CONSTANT   : (int ) GLU_INSIDE = 100021
     ADD CONSTANT   : (int ) GLU_BEGIN = 100100
     ADD CONSTANT   : (int ) GLU_VERTEX = 100101
     ADD CONSTANT   : (int ) GLU_END = 100102
     ADD CONSTANT   : (int ) GLU_ERROR = 100103
     ADD CONSTANT   : (int ) GLU_EDGE_FLAG = 100104
     ADD CONSTANT   : (int ) GLU_CW = 100120
     ADD CONSTANT   : (int ) GLU_CCW = 100121
     ADD CONSTANT   : (int ) GLU_INTERIOR = 100122
     ADD CONSTANT   : (int ) GLU_EXTERIOR = 100123
     ADD CONSTANT   : (int ) GLU_UNKNOWN = 100124
     ADD CONSTANT   : (int ) GLU_TESS_ERROR1 = 100151
     ADD CONSTANT   : (int ) GLU_TESS_ERROR2 = 100152
     ADD CONSTANT   : (int ) GLU_TESS_ERROR3 = 100153
     ADD CONSTANT   : (int ) GLU_TESS_ERROR4 = 100154
     ADD CONSTANT   : (int ) GLU_TESS_ERROR5 = 100155
     ADD CONSTANT   : (int ) GLU_TESS_ERROR6 = 100156
     ADD CONSTANT   : (int ) GLU_TESS_ERROR7 = 100157
     ADD CONSTANT   : (int ) GLU_TESS_ERROR8 = 100158
     ADD CONSTANT   : (int ) GLU_AUTO_LOAD_MATRIX = 100200
     ADD CONSTANT   : (int ) GLU_CULLING = 100201
     ADD CONSTANT   : (int ) GLU_SAMPLING_TOLERANCE = 100203
     ADD CONSTANT   : (int ) GLU_DISPLAY_MODE = 100204
     ADD CONSTANT   : (int ) GLU_PARAMETRIC_TOLERANCE = 100202
     ADD CONSTANT   : (int ) GLU_SAMPLING_METHOD = 100205
     ADD CONSTANT   : (int ) GLU_U_STEP = 100206
     ADD CONSTANT   : (int ) GLU_V_STEP = 100207
     ADD CONSTANT   : (int ) GLU_PATH_LENGTH = 100215
     ADD CONSTANT   : (int ) GLU_PARAMETRIC_ERROR = 100216
     ADD CONSTANT   : (int ) GLU_DOMAIN_DISTANCE = 100217
     ADD CONSTANT   : (int ) GLU_MAP1_TRIM_2 = 100210
     ADD CONSTANT   : (int ) GLU_MAP1_TRIM_3 = 100211
     ADD CONSTANT   : (int ) GLU_OUTLINE_POLYGON = 100240
     ADD CONSTANT   : (int ) GLU_OUTLINE_PATCH = 100241
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR1 = 100251
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR2 = 100252
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR3 = 100253
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR4 = 100254
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR5 = 100255
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR6 = 100256
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR7 = 100257
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR8 = 100258
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR9 = 100259
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR10 = 100260
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR11 = 100261
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR12 = 100262
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR13 = 100263
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR14 = 100264
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR15 = 100265
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR16 = 100266
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR17 = 100267
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR18 = 100268
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR19 = 100269
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR20 = 100270
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR21 = 100271
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR22 = 100272
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR23 = 100273
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR24 = 100274
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR25 = 100275
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR26 = 100276
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR27 = 100277
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR28 = 100278
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR29 = 100279
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR30 = 100280
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR31 = 100281
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR32 = 100282
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR33 = 100283
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR34 = 100284
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR35 = 100285
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR36 = 100286
     ADD CONSTANT   : (int ) GLU_NURBS_ERROR37 = 100287
     ADD COMMAND    : newfv4 --> GLfloat *newfv4(GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : setfv4 --> void setfv4(GLfloat *,GLfloat ,GLfloat ,GLfloat ,GLfloat );
     ADD COMMAND    : free --> void free(void *);
     ADD COMMAND    : Const --> int Const(int );
     ADD COMMAND    : system --> int system(char *);
     ADD CONSTANT   : (int ) AUX_RGB = 0
     ADD CONSTANT   : (int ) AUX_RGBA = (0)
     ADD CONSTANT   : (int ) AUX_INDEX = 1
     ADD CONSTANT   : (int ) AUX_SINGLE = 0
     ADD CONSTANT   : (int ) AUX_DOUBLE = 2
     ADD CONSTANT   : (int ) AUX_DIRECT = 0
     ADD CONSTANT   : (int ) AUX_INDIRECT = 4
     ADD CONSTANT   : (int ) AUX_SINGLE_RGBA = 0
     ADD CONSTANT   : (int ) AUX_DOUBLE_RGBA = 2
     ADD CONSTANT   : (int ) AUX_ACCUM = 8
     ADD CONSTANT   : (int ) AUX_ALPHA = 16
     ADD CONSTANT   : (int ) AUX_DEPTH = 32
     ADD CONSTANT   : (int ) AUX_STENCIL = 64
     ADD CONSTANT   : (int ) AUX_AUX = 128
     ADD CONSTANT   : (int ) AUX_EXPOSE = 1
     ADD CONSTANT   : (int ) AUX_CONFIG = 2
     ADD CONSTANT   : (int ) AUX_DRAW = 4
     ADD CONSTANT   : (int ) AUX_KEYEVENT = 8
     ADD CONSTANT   : (int ) AUX_MOUSEDOWN = 16
     ADD CONSTANT   : (int ) AUX_MOUSEUP = 32
     ADD CONSTANT   : (int ) AUX_MOUSELOC = 64
     ADD CONSTANT   : (int ) AUX_WINDOWX = 0
     ADD CONSTANT   : (int ) AUX_WINDOWY = 1
     ADD CONSTANT   : (int ) AUX_MOUSEX = 0
     ADD CONSTANT   : (int ) AUX_MOUSEY = 1
     ADD CONSTANT   : (int ) AUX_MOUSESTATUS = 3
     ADD CONSTANT   : (int ) AUX_KEY = 0
     ADD CONSTANT   : (int ) AUX_KEYSTATUS = 1
     ADD CONSTANT   : (int ) AUX_LEFTBUTTON = 1
     ADD CONSTANT   : (int ) AUX_RIGHTBUTTON = 2
     ADD CONSTANT   : (int ) AUX_MIDDLEBUTTON = 4
     ADD CONSTANT   : (int ) AUX_SHIFT = 1
     ADD CONSTANT   : (int ) AUX_CONTROL = 2
     ADD CONSTANT   : (int ) AUX_RETURN = 0x0D
     ADD CONSTANT   : (int ) AUX_ESCAPE = 0x1B
     ADD CONSTANT   : (int ) AUX_SPACE = 0x20
     ADD CONSTANT   : (int ) AUX_LEFT = 0x25
     ADD CONSTANT   : (int ) AUX_UP = 0x26
     ADD CONSTANT   : (int ) AUX_RIGHT = 0x27
     ADD CONSTANT   : (int ) AUX_DOWN = 0x28
     ADD CONSTANT   : (int ) AUX_FD = 1
     ADD CONSTANT   : (int ) AUX_COLORMAP = 3
     ADD CONSTANT   : (int ) AUX_GREYSCALEMAP = 4
     ADD CONSTANT   : (int ) AUX_FOGMAP = 5
     ADD CONSTANT   : (int ) AUX_ONECOLOR = 6
     ADD CONSTANT   : (int ) AUX_BLACK = AUX_BLACK
     ADD CONSTANT   : (int ) AUX_RED = AUX_RED
     ADD CONSTANT   : (int ) AUX_GREEN = AUX_GREEN
     ADD CONSTANT   : (int ) AUX_YELLOW = AUX_YELLOW
     ADD CONSTANT   : (int ) AUX_BLUE = AUX_BLUE
     ADD CONSTANT   : (int ) AUX_MAGENTA = AUX_MAGENTA
     ADD CONSTANT   : (int ) AUX_CYAN = AUX_CYAN
     ADD CONSTANT   : (int ) AUX_WHITE = AUX_WHITE
     ADD COMMAND    : auxInitDisplayMode --> void auxInitDisplayMode(GLenum );
     ADD COMMAND    : auxInitPosition --> void auxInitPosition(int ,int ,int ,int );
     ADD COMMAND    : auxInitWindow --> GLenum auxInitWindow(char *);
     ADD COMMAND    : auxCloseWindow --> void auxCloseWindow();
     ADD COMMAND    : auxQuit --> void auxQuit();
     ADD COMMAND    : auxSwapBuffers --> void auxSwapBuffers();
     ADD COMMAND    : auxWireSphere --> void auxWireSphere(GLdouble );
     ADD COMMAND    : auxSolidSphere --> void auxSolidSphere(GLdouble );
     ADD COMMAND    : auxWireCube --> void auxWireCube(GLdouble );
     ADD COMMAND    : auxSolidCube --> void auxSolidCube(GLdouble );
     ADD COMMAND    : auxWireBox --> void auxWireBox(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : auxSolidBox --> void auxSolidBox(GLdouble ,GLdouble ,GLdouble );
     ADD COMMAND    : auxWireTorus --> void auxWireTorus(GLdouble ,GLdouble );
     ADD COMMAND    : auxSolidTorus --> void auxSolidTorus(GLdouble ,GLdouble );
     ADD COMMAND    : auxWireCylinder --> void auxWireCylinder(GLdouble ,GLdouble );
     ADD COMMAND    : auxSolidCylinder --> void auxSolidCylinder(GLdouble ,GLdouble );
     ADD COMMAND    : auxWireIcosahedron --> void auxWireIcosahedron(GLdouble );
     ADD COMMAND    : auxSolidIcosahedron --> void auxSolidIcosahedron(GLdouble );
     ADD COMMAND    : auxWireOctahedron --> void auxWireOctahedron(GLdouble );
     ADD COMMAND    : auxSolidOctahedron --> void auxSolidOctahedron(GLdouble );
     ADD COMMAND    : auxWireTetrahedron --> void auxWireTetrahedron(GLdouble );
     ADD COMMAND    : auxSolidTetrahedron --> void auxSolidTetrahedron(GLdouble );
     ADD COMMAND    : auxWireDodecahedron --> void auxWireDodecahedron(GLdouble );
     ADD COMMAND    : auxSolidDodecahedron --> void auxSolidDodecahedron(GLdouble );
     ADD COMMAND    : auxWireCone --> void auxWireCone(GLdouble ,GLdouble );
     ADD COMMAND    : auxSolidCone --> void auxSolidCone(GLdouble ,GLdouble );
     ADD COMMAND    : auxWireTeapot --> void auxWireTeapot(GLdouble );
     ADD COMMAND    : auxSolidTeapot --> void auxSolidTeapot(GLdouble );
     ADD COMMAND    : array_int --> int *array_int(int );
     ADD COMMAND    : get_int --> int get_int(int *,int );
     ADD COMMAND    : set_int --> int set_int(int *,int ,int );
     ADD COMMAND    : array_double --> double *array_double(int );
     ADD COMMAND    : get_double --> double get_double(double *,int );
     ADD COMMAND    : set_double --> double set_double(double *,int ,double );
     ADD COMMAND    : array_float --> float *array_float(int );
     ADD COMMAND    : get_float --> float get_float(float *,int );
     ADD COMMAND    : set_float --> float set_float(float *,int ,float );
     ADD COMMAND    : array_byte --> byte *array_byte(int );
     ADD COMMAND    : get_byte --> byte get_byte(byte *,int );
     ADD COMMAND    : set_byte --> byte set_byte(byte *,int ,byte );
     ADD COMMAND    : array_string --> char **array_string(int );
     ADD COMMAND    : get_string --> char *get_string(char **,int );
     ADD COMMAND    : set_string --> char *set_string(char **,int ,char *);
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
