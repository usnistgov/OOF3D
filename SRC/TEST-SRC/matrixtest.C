#include "stiffnessmatrix.h"
#include "sparselink.h"
#include "automatrix.h"
#include "csrmatrix.h"
#include "SparseLib++/comprow.h"
#include <iostream>

int main(int, char**) {
//   SparseLinkMatrix<double> x(3,3);
  StiffnessMatrix x(0, 3, 3);
  x(0,0) = 3;
  CSRmatrix c(x);
  std::cout << c.nrows() << " " << c.ncols() << " " << c.nnz() << std::endl;
  std::cout << c << std::endl;
}
