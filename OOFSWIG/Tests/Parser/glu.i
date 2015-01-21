%module glu
%{
#include <GL/glu.h>
%}
extern const GLubyte* gluErrorString (GLenum errorCode);

extern const GLubyte* gluGetString (GLenum name);

extern void gluOrtho2D (GLdouble left, GLdouble right, GLdouble bottom, GLdouble top);
extern void gluPerspective (GLdouble fovy, GLdouble aspect, GLdouble zNear, GLdouble zFar);
//
// extern void gluPickMatrix (GLdouble x, GLdouble y, GLdouble width, GLdouble height, GLint viewport[4]);
extern void gluLookAt (GLdouble eyex, GLdouble eyey, GLdouble eyez, GLdouble centerx, GLdouble centery, GLdouble centerz, GLdouble upx, GLdouble upy, GLdouble upz);
//
// extern int gluProject (GLdouble objx, GLdouble objy, GLdouble objz, const GLdouble modelMatrix[16], const GLdouble projMatrix[16], const GLint viewport[4], GLdouble *winx, GLdouble *winy, GLdouble *winz);
// extern int gluUnProject (GLdouble winx, GLdouble winy, GLdouble winz, const GLdouble modelMatrix[16], const GLdouble projMatrix[16], const GLint viewport[4], GLdouble *objx, GLdouble *objy, GLdouble *objz);

extern int gluScaleImage (GLenum format, GLint widthin, GLint heightin, GLenum typein, const void *datain, GLint widthout, GLint heightout, GLenum typeout, void *dataout);

extern int gluBuild1DMipmaps (GLenum target, GLint components, GLint width, GLenum format, GLenum type, const void *data);
extern int gluBuild2DMipmaps (GLenum target, GLint components, GLint width, GLint height, GLenum format, GLenum type, const void *data);

typedef struct GLUquadricObj GLUquadricObj;
extern GLUquadricObj* gluNewQuadric (void);
extern void gluDeleteQuadric (GLUquadricObj *state);
extern void gluQuadricNormals (GLUquadricObj *quadObject, GLenum normals);
extern void gluQuadricTexture (GLUquadricObj *quadObject, GLboolean textureCoords);
extern void gluQuadricOrientation (GLUquadricObj *quadObject, GLenum orientation);
extern void gluQuadricDrawStyle (GLUquadricObj *quadObject, GLenum drawStyle);
extern void gluCylinder (GLUquadricObj *qobj, GLdouble baseRadius, GLdouble topRadius, GLdouble height, GLint slices, GLint stacks);
extern void gluDisk (GLUquadricObj *qobj, GLdouble innerRadius, GLdouble outerRadius, GLint slices, GLint loops);
extern void gluPartialDisk (GLUquadricObj *qobj, GLdouble innerRadius, GLdouble outerRadius, GLint slices, GLint loops, GLdouble startAngle, GLdouble sweepAngle);
extern void gluSphere (GLUquadricObj *qobj, GLdouble radius, GLint slices, GLint stacks);
//
// extern void gluQuadricCallback (GLUquadricObj *qobj, GLenum which, void (*fn)());

typedef struct GLUtriangulatorObj GLUtriangulatorObj;
extern GLUtriangulatorObj* gluNewTess (void);
//
// extern void gluTessCallback (GLUtriangulatorObj *tobj, GLenum which, void (*fn)());
extern void gluDeleteTess (GLUtriangulatorObj *tobj);
extern void gluBeginPolygon (GLUtriangulatorObj *tobj);
extern void gluEndPolygon (GLUtriangulatorObj *tobj);
extern void gluNextContour (GLUtriangulatorObj *tobj, GLenum type);
//
// extern void gluTessVertex (GLUtriangulatorObj *tobj, GLdouble v[3], void *data);

typedef struct GLUnurbsObj GLUnurbsObj;

extern GLUnurbsObj* gluNewNurbsRenderer (void);
extern void gluDeleteNurbsRenderer (GLUnurbsObj *nobj);
extern void gluBeginSurface (GLUnurbsObj *nobj);
extern void gluBeginCurve (GLUnurbsObj *nobj);
extern void gluEndCurve (GLUnurbsObj *nobj);
extern void gluEndSurface (GLUnurbsObj *nobj);
extern void gluBeginTrim (GLUnurbsObj *nobj);
extern void gluEndTrim (GLUnurbsObj *nobj);
extern void gluPwlCurve (GLUnurbsObj *nobj, GLint count, GLfloat *array, GLint stride, GLenum type);
extern void gluNurbsCurve (GLUnurbsObj *nobj, GLint nknots, GLfloat *knot, GLint stride, GLfloat *ctlarray, GLint order, GLenum type);
extern void gluNurbsSurface (GLUnurbsObj *nobj, GLint sknot_count, GLfloat *sknot, GLint tknot_count, GLfloat *tknot, GLint s_stride, GLint t_stride, GLfloat *ctlarray, GLint sorder, GLint torder, GLenum type);
//
// extern void gluLoadSamplingMatrices (GLUnurbsObj *nobj, const GLfloat modelMatrix[16], const GLfloat projMatrix[16], const GLint viewport[4]);		
extern void gluNurbsProperty (GLUnurbsObj *nobj, GLenum property, GLfloat value);
extern void gluGetNurbsProperty (GLUnurbsObj *nobj, GLenum property, GLfloat *value);
//
// extern void gluNurbsCallback (GLUnurbsObj *nobj, GLenum which, void (*fn)());

#define GLU_INVALID_ENUM		100900
#define GLU_INVALID_VALUE		100901
#define GLU_OUT_OF_MEMORY		100902
#define GLU_INCOMPATIBLE_GL_VERSION	100903

#define GLU_VERSION 		100800
#define GLU_EXTENSIONS		100801

#define GLU_TRUE		GL_TRUE
#define GLU_FALSE		GL_FALSE

#define GLU_SMOOTH		100000
#define GLU_FLAT		100001
#define GLU_NONE		100002

#define GLU_POINT		100010
#define GLU_LINE		100011
#define GLU_FILL		100012
#define GLU_SILHOUETTE		100013

#define GLU_OUTSIDE		100020
#define GLU_INSIDE		100021

#define GLU_BEGIN 		100100		
#define GLU_VERTEX		100101		
#define GLU_END			100102		
#define GLU_ERROR		100103		
#define GLU_EDGE_FLAG		100104		

#define GLU_CW			100120
#define GLU_CCW			100121
#define GLU_INTERIOR		100122
#define GLU_EXTERIOR		100123
#define GLU_UNKNOWN		100124

#define GLU_TESS_ERROR1		100151
#define GLU_TESS_ERROR2		100152
#define GLU_TESS_ERROR3		100153
#define GLU_TESS_ERROR4		100154
#define GLU_TESS_ERROR5		100155
#define GLU_TESS_ERROR6		100156
#define GLU_TESS_ERROR7		100157
#define GLU_TESS_ERROR8		100158

#define GLU_AUTO_LOAD_MATRIX		100200
#define GLU_CULLING			100201
#define GLU_SAMPLING_TOLERANCE		100203
#define GLU_DISPLAY_MODE		100204
#define GLU_PARAMETRIC_TOLERANCE	100202
#define GLU_SAMPLING_METHOD		100205
#define GLU_U_STEP			100206
#define	GLU_V_STEP			100207

#define	GLU_PATH_LENGTH			100215
#define GLU_PARAMETRIC_ERROR		100216
#define GLU_DOMAIN_DISTANCE		100217

#define GLU_MAP1_TRIM_2		100210
#define GLU_MAP1_TRIM_3		100211

#define GLU_OUTLINE_POLYGON	100240
#define GLU_OUTLINE_PATCH	100241

#define GLU_NURBS_ERROR1	100251
#define GLU_NURBS_ERROR2	100252
#define GLU_NURBS_ERROR3	100253
#define GLU_NURBS_ERROR4	100254
#define GLU_NURBS_ERROR5	100255
#define GLU_NURBS_ERROR6	100256
#define GLU_NURBS_ERROR7	100257
#define GLU_NURBS_ERROR8	100258
#define GLU_NURBS_ERROR9	100259
#define GLU_NURBS_ERROR10	100260
#define GLU_NURBS_ERROR11	100261
#define GLU_NURBS_ERROR12	100262
#define GLU_NURBS_ERROR13	100263
#define GLU_NURBS_ERROR14	100264
#define GLU_NURBS_ERROR15	100265
#define GLU_NURBS_ERROR16	100266
#define GLU_NURBS_ERROR17	100267
#define GLU_NURBS_ERROR18	100268
#define GLU_NURBS_ERROR19	100269
#define GLU_NURBS_ERROR20	100270
#define GLU_NURBS_ERROR21	100271
#define GLU_NURBS_ERROR22	100272
#define GLU_NURBS_ERROR23	100273
#define GLU_NURBS_ERROR24	100274
#define GLU_NURBS_ERROR25	100275
#define GLU_NURBS_ERROR26	100276
#define GLU_NURBS_ERROR27	100277
#define GLU_NURBS_ERROR28	100278
#define GLU_NURBS_ERROR29	100279
#define GLU_NURBS_ERROR30	100280
#define GLU_NURBS_ERROR31	100281
#define GLU_NURBS_ERROR32	100282
#define GLU_NURBS_ERROR33	100283
#define GLU_NURBS_ERROR34	100284
#define GLU_NURBS_ERROR35	100285
#define GLU_NURBS_ERROR36	100286
#define GLU_NURBS_ERROR37	100287

