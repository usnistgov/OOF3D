/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"

#include "gifplot.h"
extern PixMap *new_PixMap(int ,int ,int ,int );
extern void delete_PixMap(PixMap *);
extern void PixMap_set(PixMap *,int ,int ,int );
C++ CLASS DECLARATION : struct ColorMap
C++ CLASS DECLARATION : struct FrameBuffer
WRAPPER : PixMap *new_PixMap(int ,int ,int ,int );

WRAPPER : void delete_PixMap(PixMap *);

WRAPPER : void PixMap_set(PixMap *,int ,int ,int );

C++ CLASS DECLARATION : struct Plot2D
C++ CLASS DECLARATION : struct Plot3D
C++ CLASS START : struct ColorMap  ========================================

        ATTRIBUTE     : char * cmap; 
        ATTRIBUTE     : char * name; 
        CONSTRUCTOR   : ColorMap *ColorMap(char *);
        DESTRUCTOR    : ~ColorMap();
        MEMBER FUNC   : void default();

        MEMBER FUNC   : void assign(int ,int ,int ,int );

        MEMBER FUNC   : int getitem(int );

        MEMBER FUNC   : void setitem(int ,int );

        MEMBER FUNC   : int write(char *);

C++ CLASS END ===================================================

C++ CLASS START : struct FrameBuffer  ========================================

        ATTRIBUTE     : unsigned int  height; 
        ATTRIBUTE     : unsigned int  width; 
        ATTRIBUTE     : int  xmin; 
        ATTRIBUTE     : int  ymin; 
        ATTRIBUTE     : int  xmax; 
        ATTRIBUTE     : int  ymax; 
        CONSTRUCTOR   : FrameBuffer *FrameBuffer(unsigned int ,unsigned int );
        DESTRUCTOR    : ~FrameBuffer();
        MEMBER FUNC   : void resize(int ,int );

        MEMBER FUNC   : void clear(Pixel );

        MEMBER FUNC   : void plot(int ,int ,Pixel );

        MEMBER FUNC   : void horizontal(int ,int ,int ,Pixel );

        MEMBER FUNC   : void horizontalinterp(int ,int ,int ,Pixel ,Pixel );

        MEMBER FUNC   : void vertical(int ,int ,int ,Pixel );

        MEMBER FUNC   : void box(int ,int ,int ,int ,Pixel );

        MEMBER FUNC   : void solidbox(int ,int ,int ,int ,Pixel );

        MEMBER FUNC   : void interpbox(int ,int ,int ,int ,Pixel ,Pixel ,Pixel ,Pixel );

        MEMBER FUNC   : void circle(int ,int ,int ,Pixel );

        MEMBER FUNC   : void solidcircle(int ,int ,int ,Pixel );

        MEMBER FUNC   : void line(int ,int ,int ,int ,Pixel );

        MEMBER FUNC   : void setclip(int ,int ,int ,int );

        MEMBER FUNC   : void noclip();

        MEMBER FUNC   : int makeGIF(ColorMap *,void *,unsigned int );

        MEMBER FUNC   : void zresize(int ,int );

        MEMBER FUNC   : void zclear();

        MEMBER FUNC   : void drawchar(int ,int ,int ,int ,char ,int );

        MEMBER FUNC   : void drawstring(int ,int ,int ,int ,char *,int );

        MEMBER FUNC   : void drawpixmap(PixMap *,int ,int ,int ,int );

        MEMBER FUNC   : int writeGIF(ColorMap *,char *);

C++ CLASS END ===================================================

C++ CLASS START : struct Plot2D  ========================================

        ATTRIBUTE     : FrameBuffer * frame; 
        ATTRIBUTE     : int  view_xmin; 
        ATTRIBUTE     : int  view_ymin; 
        ATTRIBUTE     : int  view_xmax; 
        ATTRIBUTE     : int  view_ymax; 
        ATTRIBUTE     : double  xmin; 
        ATTRIBUTE     : double  ymin; 
        ATTRIBUTE     : double  xmax; 
        ATTRIBUTE     : double  ymax; 
        ATTRIBUTE     : int  xscale; 
        ATTRIBUTE     : int  yscale; 
        CONSTRUCTOR   : Plot2D *Plot2D(FrameBuffer *,double ,double ,double ,double );
        DESTRUCTOR    : ~Plot2D();
        MEMBER FUNC   : Plot2D *copy();

        MEMBER FUNC   : void clear(Pixel );

        MEMBER FUNC   : void setview(int ,int ,int ,int );

        MEMBER FUNC   : void setrange(double ,double ,double ,double );

        MEMBER FUNC   : void setscale(int ,int );

        MEMBER FUNC   : void plot(double ,double ,Pixel );

        MEMBER FUNC   : void box(double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void solidbox(double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void interpbox(double ,double ,double ,double ,Pixel ,Pixel ,Pixel ,Pixel );

        MEMBER FUNC   : void circle(double ,double ,double ,Pixel );

        MEMBER FUNC   : void solidcircle(double ,double ,double ,Pixel );

        MEMBER FUNC   : void line(double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void start();

        MEMBER FUNC   : void drawpixmap(PixMap *,double ,double ,Pixel ,Pixel );

        MEMBER FUNC   : void xaxis(double ,double ,double ,int ,Pixel );

        MEMBER FUNC   : void yaxis(double ,double ,double ,int ,Pixel );

C++ CLASS END ===================================================

C++ CLASS START : struct Plot3D  ========================================

        ATTRIBUTE     : FrameBuffer * frame; 
        ATTRIBUTE     : int  view_xmin; 
        ATTRIBUTE     : int  view_ymin; 
        ATTRIBUTE     : int  view_xmax; 
        ATTRIBUTE     : int  view_ymax; 
        ATTRIBUTE     : double  xmin; 
        ATTRIBUTE     : double  ymin; 
        ATTRIBUTE     : double  zmin; 
        ATTRIBUTE     : double  xmax; 
        ATTRIBUTE     : double  ymax; 
        ATTRIBUTE     : double  zmax; 
        ATTRIBUTE     : double  xcenter; 
        ATTRIBUTE     : double  ycenter; 
        ATTRIBUTE     : double  zcenter; 
        ATTRIBUTE     : double  fovy; 
        ATTRIBUTE     : double  aspect; 
        ATTRIBUTE     : double  znear; 
        ATTRIBUTE     : double  zfar; 
        ATTRIBUTE     : double  lookatz; 
        ATTRIBUTE     : double  xshift; 
        ATTRIBUTE     : double  yshift; 
        CONSTRUCTOR   : Plot3D *Plot3D(FrameBuffer *,double ,double ,double ,double ,double ,double );
        DESTRUCTOR    : ~Plot3D();
        MEMBER FUNC   : Plot3D *copy();

        MEMBER FUNC   : void clear(Pixel );

        MEMBER FUNC   : void perspective(double ,double ,double );

        MEMBER FUNC   : void lookat(double );

        MEMBER FUNC   : void autoperspective(double );

        MEMBER FUNC   : void rotx(double );

        MEMBER FUNC   : void roty(double );

        MEMBER FUNC   : void rotz(double );

        MEMBER FUNC   : void rotl(double );

        MEMBER FUNC   : void rotr(double );

        MEMBER FUNC   : void rotd(double );

        MEMBER FUNC   : void rotu(double );

        MEMBER FUNC   : void rotc(double );

        MEMBER FUNC   : void zoom(double );

        MEMBER FUNC   : void left(double );

        MEMBER FUNC   : void right(double );

        MEMBER FUNC   : void down(double );

        MEMBER FUNC   : void up(double );

        MEMBER FUNC   : void center(double ,double );

        MEMBER FUNC   : void plot(double ,double ,double ,Pixel );

        MEMBER FUNC   : void setview(int ,int ,int ,int );

        MEMBER FUNC   : void start();

        MEMBER FUNC   : void line(double ,double ,double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void triangle(double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void solidtriangle(double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void interptriangle(double ,double ,double ,Pixel ,double ,double ,double ,Pixel ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void quad(double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void solidquad(double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void interpquad(double ,double ,double ,Pixel ,double ,double ,double ,Pixel ,double ,double ,double ,Pixel ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void solidsphere(double ,double ,double ,double ,Pixel );

        MEMBER FUNC   : void outlinesphere(double ,double ,double ,double ,Pixel ,Pixel );

C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_struct_Plot3D","_Plot3D",0},
    { "_ColorMap","_struct_ColorMap",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_float","_Zvalue",0},
    { "_Pixel","_unsigned_char",0},
    { "_Plot2D","_struct_Plot2D",0},
    { "_Plot3D","_struct_Plot3D",0},
    { "_FrameBuffer","_struct_FrameBuffer",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_int",0},
    { "_struct_ColorMap","_ColorMap",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_char","_Pixel",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_struct_FrameBuffer","_FrameBuffer",0},
    { "_Zvalue","_float",0},
    { "_struct_Plot2D","_Plot2D",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD CONSTANT   : (int ) BLACK = 0
     ADD CONSTANT   : (int ) WHITE = 1
     ADD CONSTANT   : (int ) RED = 2
     ADD CONSTANT   : (int ) GREEN = 3
     ADD CONSTANT   : (int ) BLUE = 4
     ADD CONSTANT   : (int ) YELLOW = 5
     ADD CONSTANT   : (int ) CYAN = 6
     ADD CONSTANT   : (int ) MAGENTA = 7
     ADD CONSTANT   : (int ) HORIZONTAL = 1
     ADD CONSTANT   : (int ) VERTICAL = 2
     ADD COMMAND    : new_PixMap --> PixMap *new_PixMap(int ,int ,int ,int );
     ADD COMMAND    : delete_PixMap --> void delete_PixMap(PixMap *);
     ADD COMMAND    : PixMap_set --> void PixMap_set(PixMap *,int ,int ,int );
     ADD CONSTANT   : (int ) TRANSPARENT = 0
     ADD CONSTANT   : (int ) FOREGROUND = 1
     ADD CONSTANT   : (int ) BACKGROUND = 2
     ADD CONSTANT   : (int ) LINEAR = 10
     ADD CONSTANT   : (int ) LOG = 11
     ADD CONSTANT   : (PixMap *) SQUARE = &PixMap_SQUARE
     ADD CONSTANT   : (PixMap *) TRIANGLE = &PixMap_TRIANGLE
     ADD CONSTANT   : (PixMap *) CROSS = &PixMap_CROSS

     // C++ CLASS START : struct ColorMap
     ADD MEMBER     : cmap --> char * cmap; 
     ADD MEMBER     : name --> char * name; 
     ADD CONSTRUCT  : ColorMap --> ColorMap *ColorMap(char *);
     ADD DESTRUCT  : ColorMap --> ~ColorMap();
     ADD MEMBER FUN : default --> void default();
     ADD MEMBER FUN : assign --> void assign(int ,int ,int ,int );
     ADD MEMBER FUN : __getitem__ --> int getitem(int );
     ADD MEMBER FUN : __setitem__ --> void setitem(int ,int );
     ADD MEMBER FUN : write --> int write(char *);
     // C++ CLASS END 


     // C++ CLASS START : struct FrameBuffer
     ADD MEMBER     : height --> unsigned int  height; 
     ADD MEMBER     : width --> unsigned int  width; 
     ADD MEMBER     : xmin --> int  xmin; 
     ADD MEMBER     : ymin --> int  ymin; 
     ADD MEMBER     : xmax --> int  xmax; 
     ADD MEMBER     : ymax --> int  ymax; 
     ADD CONSTRUCT  : FrameBuffer --> FrameBuffer *FrameBuffer(unsigned int ,unsigned int );
     ADD DESTRUCT  : FrameBuffer --> ~FrameBuffer();
     ADD MEMBER FUN : resize --> void resize(int ,int );
     ADD MEMBER FUN : clear --> void clear(Pixel );
     ADD MEMBER FUN : plot --> void plot(int ,int ,Pixel );
     ADD MEMBER FUN : horizontal --> void horizontal(int ,int ,int ,Pixel );
     ADD MEMBER FUN : horizontalinterp --> void horizontalinterp(int ,int ,int ,Pixel ,Pixel );
     ADD MEMBER FUN : vertical --> void vertical(int ,int ,int ,Pixel );
     ADD MEMBER FUN : box --> void box(int ,int ,int ,int ,Pixel );
     ADD MEMBER FUN : solidbox --> void solidbox(int ,int ,int ,int ,Pixel );
     ADD MEMBER FUN : interpbox --> void interpbox(int ,int ,int ,int ,Pixel ,Pixel ,Pixel ,Pixel );
     ADD MEMBER FUN : circle --> void circle(int ,int ,int ,Pixel );
     ADD MEMBER FUN : solidcircle --> void solidcircle(int ,int ,int ,Pixel );
     ADD MEMBER FUN : line --> void line(int ,int ,int ,int ,Pixel );
     ADD MEMBER FUN : setclip --> void setclip(int ,int ,int ,int );
     ADD MEMBER FUN : noclip --> void noclip();
     ADD MEMBER FUN : makeGIF --> int makeGIF(ColorMap *,void *,unsigned int );
     ADD MEMBER FUN : zresize --> void zresize(int ,int );
     ADD MEMBER FUN : zclear --> void zclear();
     ADD MEMBER FUN : drawchar --> void drawchar(int ,int ,int ,int ,char ,int );
     ADD MEMBER FUN : drawstring --> void drawstring(int ,int ,int ,int ,char *,int );
     ADD MEMBER FUN : drawpixmap --> void drawpixmap(PixMap *,int ,int ,int ,int );
     ADD MEMBER FUN : writeGIF --> int writeGIF(ColorMap *,char *);
     // C++ CLASS END 


     // C++ CLASS START : struct Plot2D
     ADD MEMBER     : frame --> FrameBuffer * frame; 
     ADD MEMBER     : view_xmin --> int  view_xmin; 
     ADD MEMBER     : view_ymin --> int  view_ymin; 
     ADD MEMBER     : view_xmax --> int  view_xmax; 
     ADD MEMBER     : view_ymax --> int  view_ymax; 
     ADD MEMBER     : xmin --> double  xmin; 
     ADD MEMBER     : ymin --> double  ymin; 
     ADD MEMBER     : xmax --> double  xmax; 
     ADD MEMBER     : ymax --> double  ymax; 
     ADD MEMBER     : xscale --> int  xscale; 
     ADD MEMBER     : yscale --> int  yscale; 
     ADD CONSTRUCT  : Plot2D --> Plot2D *Plot2D(FrameBuffer *,double ,double ,double ,double );
     ADD DESTRUCT  : Plot2D --> ~Plot2D();
     ADD MEMBER FUN : copy --> Plot2D *copy();
     ADD MEMBER FUN : clear --> void clear(Pixel );
     ADD MEMBER FUN : setview --> void setview(int ,int ,int ,int );
     ADD MEMBER FUN : setrange --> void setrange(double ,double ,double ,double );
     ADD MEMBER FUN : setscale --> void setscale(int ,int );
     ADD MEMBER FUN : plot --> void plot(double ,double ,Pixel );
     ADD MEMBER FUN : box --> void box(double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : solidbox --> void solidbox(double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : interpbox --> void interpbox(double ,double ,double ,double ,Pixel ,Pixel ,Pixel ,Pixel );
     ADD MEMBER FUN : circle --> void circle(double ,double ,double ,Pixel );
     ADD MEMBER FUN : solidcircle --> void solidcircle(double ,double ,double ,Pixel );
     ADD MEMBER FUN : line --> void line(double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : start --> void start();
     ADD MEMBER FUN : drawpixmap --> void drawpixmap(PixMap *,double ,double ,Pixel ,Pixel );
     ADD MEMBER FUN : xaxis --> void xaxis(double ,double ,double ,int ,Pixel );
     ADD MEMBER FUN : yaxis --> void yaxis(double ,double ,double ,int ,Pixel );
     // C++ CLASS END 


     // C++ CLASS START : struct Plot3D
     ADD MEMBER     : frame --> FrameBuffer * frame; 
     ADD MEMBER     : view_xmin --> int  view_xmin; 
     ADD MEMBER     : view_ymin --> int  view_ymin; 
     ADD MEMBER     : view_xmax --> int  view_xmax; 
     ADD MEMBER     : view_ymax --> int  view_ymax; 
     ADD MEMBER     : xmin --> double  xmin; 
     ADD MEMBER     : ymin --> double  ymin; 
     ADD MEMBER     : zmin --> double  zmin; 
     ADD MEMBER     : xmax --> double  xmax; 
     ADD MEMBER     : ymax --> double  ymax; 
     ADD MEMBER     : zmax --> double  zmax; 
     ADD MEMBER     : xcenter --> double  xcenter; 
     ADD MEMBER     : ycenter --> double  ycenter; 
     ADD MEMBER     : zcenter --> double  zcenter; 
     ADD MEMBER     : fovy --> double  fovy; 
     ADD MEMBER     : aspect --> double  aspect; 
     ADD MEMBER     : znear --> double  znear; 
     ADD MEMBER     : zfar --> double  zfar; 
     ADD MEMBER     : lookatz --> double  lookatz; 
     ADD MEMBER     : xshift --> double  xshift; 
     ADD MEMBER     : yshift --> double  yshift; 
     ADD CONSTRUCT  : Plot3D --> Plot3D *Plot3D(FrameBuffer *,double ,double ,double ,double ,double ,double );
     ADD DESTRUCT  : Plot3D --> ~Plot3D();
     ADD MEMBER FUN : copy --> Plot3D *copy();
     ADD MEMBER FUN : clear --> void clear(Pixel );
     ADD MEMBER FUN : perspective --> void perspective(double ,double ,double );
     ADD MEMBER FUN : lookat --> void lookat(double );
     ADD MEMBER FUN : autoperspective --> void autoperspective(double );
     ADD MEMBER FUN : rotx --> void rotx(double );
     ADD MEMBER FUN : roty --> void roty(double );
     ADD MEMBER FUN : rotz --> void rotz(double );
     ADD MEMBER FUN : rotl --> void rotl(double );
     ADD MEMBER FUN : rotr --> void rotr(double );
     ADD MEMBER FUN : rotd --> void rotd(double );
     ADD MEMBER FUN : rotu --> void rotu(double );
     ADD MEMBER FUN : rotc --> void rotc(double );
     ADD MEMBER FUN : zoom --> void zoom(double );
     ADD MEMBER FUN : left --> void left(double );
     ADD MEMBER FUN : right --> void right(double );
     ADD MEMBER FUN : down --> void down(double );
     ADD MEMBER FUN : up --> void up(double );
     ADD MEMBER FUN : center --> void center(double ,double );
     ADD MEMBER FUN : plot --> void plot(double ,double ,double ,Pixel );
     ADD MEMBER FUN : setview --> void setview(int ,int ,int ,int );
     ADD MEMBER FUN : start --> void start();
     ADD MEMBER FUN : line --> void line(double ,double ,double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : triangle --> void triangle(double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : solidtriangle --> void solidtriangle(double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : interptriangle --> void interptriangle(double ,double ,double ,Pixel ,double ,double ,double ,Pixel ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : quad --> void quad(double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : solidquad --> void solidquad(double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : interpquad --> void interpquad(double ,double ,double ,Pixel ,double ,double ,double ,Pixel ,double ,double ,double ,Pixel ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : solidsphere --> void solidsphere(double ,double ,double ,double ,Pixel );
     ADD MEMBER FUN : outlinesphere --> void outlinesphere(double ,double ,double ,double ,Pixel ,Pixel );
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
