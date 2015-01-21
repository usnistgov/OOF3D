//
// Helper functions for GL-Library
%{

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

%}

GLfloat *newfv4(GLfloat a, GLfloat b, GLfloat c, GLfloat d);
void setfv4(GLfloat *fv, GLfloat a, GLfloat b, GLfloat c, GLfloat d);
void free(void *);
int Const(int);
int system(char *);

