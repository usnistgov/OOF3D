# -*- python -*-
# $RCSfile: plas6.py,v $
# $Revision: 1.6 $
# $Author: reida $
# $Date: 2007/09/18 15:21:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

# This file, which from the devasatingly creative nomenclature you
# will deduce is the successor of plas5.py, does point-wise plastic
# constitutive rules, has hardening, but solves the constrained
# nonlinear system "all-up", i.e. it doesn't do local plastic
# relaxation at the individual gausspoints, it applies all the
# pointwise constraints simultaneously and solves.


import math, sets, string, sys, getopt

import smallmatrix
import position

Position = position.Position
SmallMatrix = smallmatrix.SmallMatrix

class Node:
    def __init__(self,idx,pos):
        self.index = idx
        self.position = pos
        self.dofs = []
        self.eldofs = {}
        self.elements = sets.Set()
    def __repr__(self):
        return "Node(%d,%f,%f)" % (self.index,
                                   self.position.x, self.position.y)
    def add_element(self, el):
        self.elements.add(el)
        self.eldofs[el]=[]
    def get_elements(self):
        return self.elements

    def alldofs(self):
        res = self.dofs[:]
        for v in self.eldofs.values():
            res+=v
        return res

    def adddof(self,dof):
        self.dofs.append(dof)
    def addeldof(self,el,dof):
        self.eldofs[el].append(dof)
            
    def dofindex(self,dofname):
        for d in self.dofs:
            if d.name==dofname:
                return d.index
    def eldofindex(self,el,dofname):
        for d in self.eldofs[el]:
            if d.name==dofname:
                return d.index
    def dof(self,dofname):
        for d in self.dofs:
            if d.name==dofname:
                return d
    def eldof(self,el,dofname):
        for d in self.eldofs[el]:
            if d.name==dofname:
                return d



# This is a combination of the field and dof functionality in OOF.
# The index is the starting index for this DOF in the master stiffness
# matrix, and the size is the number of slots it uses.
class Dof:
    def __init__(self, name, index, size):
        self.name = name
        self.index = index
        self.size = size
        self.value = [0.0]*size
    def set(self,idx,v):
        self.value[idx] = v
    def add(self,idx,v):
        self.value[idx] += v
    def get(self,idx):
        return self.value[idx]
    def __repr__(self):
        return "Dof(%s,%d,%d)" % (self.name, self.index, self.size)

# GPDofs live in the mesh, and contain plastic degrees of freedom,
# like the accumulated plastic strain, the local yield surface radius,
# and the local yield surface center.  They are always free DOFs.
class GPDof(Dof):
    def __init__(self, name, element, gausspt, index, size):
        self.name = name
        self.element = element
        self.gausspt = gausspt
        Dof.__init__(self, name, index, size)
    def __repr__(self):
        return "GPDof(%s,%s,%s,%d,%d)" % (self.name, `self.element`,
                                          `self.gausspt`, self.index,
                                          self.size)
    
    
        
# Quad shape functions.

def qsf0(xi,zeta):
    return 0.25*(xi-1.0)*(zeta-1.0)
def qsf1(xi,zeta):
    return -0.25*(xi+1.0)*(zeta-1.0)
def qsf2(xi,zeta):
    return 0.25*(xi+1.0)*(zeta+1.0)
def qsf3(xi,zeta):
    return -0.25*(xi-1.0)*(zeta+1.0)

# Quad shape function derivatives, with respect to master coords.
def dqsf0d1(xi,zeta):
    return 0.25*(zeta-1.0)
def dqsf0d2(xi,zeta):
    return 0.25*(xi-1.0)

def dqsf1d1(xi,zeta):
    return -0.25*(zeta-1.0)
def dqsf1d2(xi,zeta):
    return -0.25*(xi+1.0)

def dqsf2d1(xi,zeta):
    return 0.25*(zeta+1.0)
def dqsf2d2(xi,zeta):
    return 0.25*(xi+1.0)

def dqsf3d1(xi,zeta):
    return -0.25*(zeta+1.0)
def dqsf3d2(xi,zeta):
    return -0.25*(xi-1.0)

class GaussPoint:
    def __init__(self,xi,zeta,weight):
        self.xi = xi
        self.zeta = zeta
        self.weight = weight
    def __repr__(self):
        return "GaussPoint(%g,%g,%g)" % (self.xi, self.zeta, self.weight)


class Element:
    gptable = []
    def __init__(self,idx,nodelist=[]):
        self.index = idx
        self.nodes = nodelist[:]
        self.sfns = [qsf0,qsf1,qsf2,qsf3]
        self.dsfns = [[dqsf0d1,dqsf0d2],[dqsf1d1,dqsf1d2],
                      [dqsf2d1,dqsf2d2],[dqsf3d1,dqsf3d2]]
        for n in self.nodes:
            n.add_element(self)

        # Gauss-point-specific data.  Initialize plastic strain field
        # to be zero.
        self.gpdata = {}
        for p in self.gausspts():
            # Data are the local gamma, the six components of plastic
            # strain, and the six components of the yield surface
            # center.
            self.gpdata[p]=[0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

        # Use shape-functions directly to represent the stress.  The
        # shape functions are capable of representing lower-order
        # objects, so in principle this should not create any
        # difficulties, and is convenient.  They are only used on a
        # per-element basis, of course.
        mmtx = smallmatrix.SmallMatrix(4,4)
        rmtx = smallmatrix.SmallMatrix(4,4)
        mmtx.clear()
        rmtx.clear()
        for i in range(4):
            rmtx[i,i]=1.0 # Identity matrix.
            for j in range(4):
                res = 0.0
                for p in self.gausspts():
                    res += self.shapefn(i,p.xi,p.zeta)* \
                           self.shapefn(j,p.xi,p.zeta)* \
                           p.weight*self.jacobian(p.xi,p.zeta)
                mmtx[i,j]=res
        r = mmtx.solve(rmtx)
        if r!=0:
            print >> sys.stderr, \
                  "Element mass matrix is singular, run for the hills!"
        else:
            self.s_mtx = rmtx


    def __repr__(self):
        return "Element(%d,%s)" % (self.index, [n.index for n in self.nodes])
    # Evaluate a shape function at a master-space coordinate.
    def shapefn(self,i,xi,zeta):
        return self.sfns[i](xi,zeta)
    # Derivative of shape function i wrt component j in master space.
    def masterdshapefn(self,i,j,xi,zeta):
        return self.dsfns[i][j](xi,zeta)
    # Lab-space derivative of the shape function wrt lab component j.
    def dshapefn(self,i,j,xi,zeta):
        (j11,j12,j21,j22) = self.jacobianmtx(xi,zeta)
        det = j11*j22 - j12*j21
        dfdxi = self.dsfns[i][0](xi,zeta)
        dfdzeta = self.dsfns[i][1](xi,zeta)
        dxy = ( (j22*dfdxi-j12*dfdzeta)/det,
                (-j21*dfdxi+j11*dfdzeta)/det )
        return dxy[j]
        
    # The master-to-lab transformation.
    def frommaster(self,xi,zeta):
        xpos = sum( [self.sfns[i](xi,zeta)*self.nodes[i].position.x
                     for i in range(4)] )
        ypos = sum( [self.sfns[i](xi,zeta)*self.nodes[i].position.y
                     for i in range(4)] )
        return Position(xpos,ypos)
    # Jacobian of the master-to-undistorted transformation.
    def jacobianmtx(self,xi,zeta):
        j11 = sum( [ self.dsfns[i][0](xi,zeta)*self.nodes[i].position.x
                     for i in range(4)] )
        j12 = sum( [ self.dsfns[i][0](xi,zeta)*self.nodes[i].position.y
                     for i in range(4)] )
        j21 = sum( [ self.dsfns[i][1](xi,zeta)*self.nodes[i].position.x
                     for i in range(4)] )
        j22 = sum( [ self.dsfns[i][1](xi,zeta)*self.nodes[i].position.y
                     for i in range(4)] )
        return (j11,j12,j21,j22)

    def jacobian(self,xi,zeta):
        (j11,j12,j21,j22) = self.jacobianmtx(xi,zeta)
        res = j11*j22-j21*j12
        return res

    # Return the relevant gausspoints, once they're computed.
    def gausspts(self):
        if not Element.gptable:
            # 
            # Three per dimension...
            mpt = math.sqrt(3.0/5.0)
            pts = [-mpt,0.0,mpt]
            wts = [5.0/9.0, 8.0/9.0, 5.0/9.0]
            n = len(pts)
            for i in range(n):
                for j in range(n):
                    Element.gptable.append(
                        GaussPoint(pts[j],pts[i],wts[j]*wts[i]))
        return Element.gptable



# Plasticity utility class, objects for the plastic consistency
# computation.  For the moment, assumes Von Mises yield.  "Yield" is a
# reserved word in Python.
class Yeeld:
    def __init__(self,stress,c,k):
        self.yieldpt = stress # Scalar.
        # TODO: Generalize these to more-than-linear hardening.
        self.iso_c = c  # Isotropic hardening coefficient.
        self.kine_k = k # Kinematic hardening coefficient.
  
    # Scalar yield function as a function of the passed-in stress,
    # which is assumed to be a symmetric 3x3 tensor, the center of the
    # yield surface, also a symmetric 3x3 tensor (traceless, but
    # that's not enforced here), and the isotropic hardening, which we
    # call gamma.
    def yeeld(self,stress,center,gamma):
        offset = [ [ stress[i][j]-center[i][j] for j in range(3) ]
                   for i in range(3) ]
        return math.sqrt(deviator(offset)) - \
               math.sqrt(2.0/3.0)*(self.yieldpt) - gamma

    # Tensor-valued derivative of the yield function at the passed-in
    # stress point and center, with respect to the passed-in stress.
    # Does not depend on isotropic hardening.
    def dyeeld(self,stress,center):
        offset = [ [ stress[i][j]-center[i][j] for j in range(3) ]
                   for i in range(3) ]
        # 1/3 of the trace of the stress.
        t = (1.0/3.0)*sum( [offset[i][i] for i in range(3)] )
        dv = math.sqrt(deviator(offset))
        return [ [ (offset[i][j]-t*ident[i][j])/dv
                   for j in range(3) ] for i in range(3) ]


    # Independent computation of the flow rule, in principle, but not
    # in fact.
    def flow(self,stress,center):
        return self.dyeeld(stress,center)
    
    # Four-index-tensor-valued second derivative of the yield function
    # at the indicated stress and center.
    def dflow(self,stress,center):
        offset = [ [ stress[i][j]-center[i][j] for j in range(3) ]
                   for i in range(3) ]
       # (1/3) of the trace of the stress.
        t = (1.0/3.0)*sum( [offset[i][i] for i in range(3)] )
        trm1 = [[[[ (offset[k][l]-t*ident[k][l])*
                    (offset[m][n]-t*ident[m][n])
                    for n in range(3) ]
                  for m in range(3) ]
                 for l in range(3) ]
                for k in range(3) ]
        trm2 = [[[[ ident[k][m]*ident[l][n] -
                    (1.0/3.0)*ident[m][n]*ident[k][l]
                    for n in range(3) ]
                  for m in range(3) ]
                 for l in range(3) ]
                for k in range(3) ]
        dv = math.sqrt(deviator(offset))
        dv3 = dv**3
        return [[[[ (-trm1[i][j][k][l]/dv3)+(trm2[i][j][k][l]/dv)
                    for l in range(3) ]
                  for k in range(3) ]
                 for j in range(3) ]
                for i in range(3) ]

    # Isotropic hardening, a function of plastic strain increment.
    def isohard(self,dstrain):
        mag = sum([ sum([ dstrain[i][j]*dstrain[i][j]
                          for j in range(3) ])
                    for i in range(3) ])
        return math.sqrt(mag)*self.iso_c

    # Derivative of the isotropic hardening with respect to the
    # components of the strain increment.
    def disohard(self,dstrain):
        mag = sum([ sum([ dstrain[i][j]*dstrain[i][j]
                          for j in range(3) ])
                    for i in range(3) ])
        if mag==0.0:
            return [ [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

        return [ [ self.iso_c*dstrain[i][j]/math.sqrt(mag)
                   for j in range(3) ] for i in range(3) ]

    # Kinematic hardening, also a function of the plastic strain
    # increment.
    def khard(self,dstrain):
        return [ [ self.kine_k*dstrain[i][j] for j in range(3) ]
                 for i in range(3) ]

    # Derivatives with respect to the plastic strain increment.
    def dkhard(self,dstrain):
        return [ [ [ [ self.kine_k*ident[i][k]*ident[j][l]
                       for l in range(3) ]
                     for k in range(3) ]
                   for j in range(3) ]
                 for i in range(3) ]
    
        


# Utility function -- compute the plastic strain increment at a
# particular point, given the input constitutive parameters and the
# starting stress and geometric strain.  For linear elasticity, you do
# not need to know the initial plastic strain, if any -- the increment
# only depends on the initial stress, which implicitly contains that
# data.  "gamma" is the isotropic offset to the yield function, and
# center is the modified center point of the surface.  gamma is a
# scalar, and center is a symmetric tensor.
def ycheck(cijkl,yld,stress,center,gamma):
    eps = 1.0e-10
    # Local return-mapping problem -- DOFs are, in order,
    # lambda, ep00,ep11,ep22,ep12,ep02,ep01 (voigt order).
    mtx = smallmatrix.SmallMatrix(14,14)
    rhs = smallmatrix.SmallMatrix(14,1)
    #
    # The variables occur in this order.
    lmbda = 0.0
    dgamma = 0.0
    ep = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    dcenter = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    #
    icount = 0
    while icount < 100:
        icount += 1
        lstress = [ [ stress[i][j]-sum([ sum([ cijkl[i][j][k][l]*ep[voigt[k][l]] for l in range(3) ]) for k in range(3) ]) for j in range(3) ] for i in range(3) ]

        mtx.clear()
        rhs.clear()

        # Short for "current center"...
        ccenter = [ [ center[i][j]+dcenter[voigt[i][j]]
                      for j in range(3) ] for i in range(3) ]
        eptensor = [ [ ep[voigt[i][j]] for j in range(3) ]
                     for i in range(3) ]
        dy = yld.dyeeld(lstress,ccenter)
        flow = yld.flow(lstress,ccenter)
        dflow = yld.dflow(lstress,ccenter)

        ihard = yld.isohard(eptensor)
        dihard = yld.disohard(eptensor)

        khard = yld.khard(eptensor)
        dkhard = yld.dkhard(eptensor)
        
        # Build right-hand-side, check for zeroness.
        rhs[0,0] = -yld.yeeld(lstress,ccenter,gamma+dgamma)

        rhs[1,0] = -dgamma + ihard
        # rhs[1,0] = -dgamma + yld.iso_c*sq_epmag

      
        for i in range(3):
            for j in range(i+1):
                rhs[voigt[i][j]+2,0] = -lmbda*flow[i][j]+ep[voigt[i][j]]


        for i in range(3):
            for j in range(i+1):
                rhs[voigt[i][j]+8,0] = -dcenter[voigt[i][j]] + khard[i][j]
        # print "\nRHS: ", [ rhs[i,0] for i in range(rhs.rows()) ]
        
        mag = sum( [ rhs[i,0]**2 for i in range(rhs.rows()) ] )
        if mag<eps:
            break # out of while loop.

        # Build matrix. 
        # First row, consistency equation.
        mtx[0,1] = -1.0 # Derivative of yield function wrt delta-gamma.
        for k in range(3):
            for l in range(3):
                col = voigt[k][l]+2
                mtx[0,col] += sum([ sum([ -dy[i][j]*cijkl[i][j][k][l] 
                                          for j in range(3) ])
                                    for i in range(3) ])
                
                col = voigt[k][l]+8
                # Derivative of yield function wrt delta-c components.
                mtx[0,col] -= dy[k][l]
               
                                                      
        # Second row, isotropic hardening.  No dependence on ccenter.
        mtx[1,1]=1.0
        for k in range(3):
            for l in range(3):
                col = voigt[k][l]+2
                mtx[1,col] += -dihard[k][l]

                    
        # Third through eights rows, flow rule.
        for i in range(3):
            for j in range(i+1):
                row = voigt[i][j]+2
                # Column zero, easy.
                mtx[row,0]=dy[i][j]
                for m in range(3):
                    for n in range(3):
                        col = voigt[m][n]+2
                        diag = 0.0
                        if i==m and j==n:
                            diag = 1.0
                        mtx[row,col] += sum([ sum([ -lmbda*dflow[i][j][k][l]*cijkl[k][l][m][n] for l in range(3) ]) for k in range(3) ])-diag

                        col = voigt[m][n]+8
                        mtx[row,col] += -lmbda*dflow[i][j][m][n]

        # Ninth through fourteenth rows, kinematic hardening.
        for i in range(3):
            for j in range(i+1):
                row = voigt[i][j]+8
                mtx[row,row]=1.0 # Diagonal part, deriv wrt c's.
                # Component-wise match-up.
                for k in range(3):
                    for l in range(3):
                        col = voigt[k][l]+2
                        mtx[row,col] = -dkhard[i][j][k][l]
                

        # Solve the resulting linearized system.
        # for mtxi in range(8):
        #     print [ mtx[mtxi,j] for j in range(8) ]
        rr = mtx.solve(rhs)
        if rr==0:
            # print "Increments: ", [ rhs[i,0] for i in range(8) ]
            lmbda += rhs[0,0]
            dgamma += rhs[1,0]
            for i in range(6):
                ep[i] += rhs[i+2,0]
                dcenter[i] += rhs[i+8,0]
                
            # print "Soln: ", [lmbda, dgamma] + [ep[i] for i in range(6)] 
        else:
            print >> sys.stderr, "Error in solving in ycheck, rr=", rr

    else:
        print >> sys.stderr, "Error, ycheck loop did not converge."
    # Broke out of loop.
    return [dgamma]+ep+dcenter    



# Elastic constitutive bookkeeppiinngg.


voigt = [[0,5,4],
         [5,1,3],
         [4,3,2]]


def Cij(lmbda,mu):
    # Canonical: lmbda=0.5, mu=0.25, gives c11=1.0,c12=0.5.
    c11 = lmbda + 2.0*mu
    c12 = lmbda
    c44 = 0.5*(c11-c12)
    return [[c11, c12, c12, 0.0, 0.0, 0.0],
            [c12, c11, c12, 0.0, 0.0, 0.0],
            [c12, c12, c11, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, c44, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, c44, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, c44]]


def Cijkl(lmbda,mu):
    cij = Cij(lmbda,mu)
    return [ [ [ [ cij[voigt[i][j]][voigt[k][l]] for l in range(3) ]
                  for k in range(3) ] for j in range(3) ] for i in range(3) ]

          

# Plastic utility function.
def deviator(stress):
    return sum(
        [ sum( [ stress[i][j]**2 for j in range(3) ] )
          for i in range(3) ] ) - \
         (1.0/3.0)*(sum([ stress[i][i] for i in range(3)])**2)

# Utility tensor.
ident = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]



#
# MESH begins here....
##############################################################


        
class Mesh:
    # nx and ny are numbers of elements, not nodes.
    def __init__(self,nx=5,ny=5):
        self.nodes = []
        self.elements = []
        self.topnodes = []
        self.bottomnodes = []

        dx = 1.0/float(nx)
        dy = 1.0/float(ny)

        # Generate nodes, raster fashion, from bottom to top.  i is
        # like an "y" coordinate, and j is like a "x".
        for i in range(nx+1):
            for j in range(ny+1):
                nd = Node(len(self.nodes),position.Position(j*dx,i*dy))
                self.nodes.append(nd)
                if i==0:
                    self.bottomnodes.append(nd)
                if i==ny:
                    self.topnodes.append(nd)
                    
        # Generate elements, raster fashion -- i is "y" coordinate, j
        # is "x", again.
        for i in range(ny):
            for j in range(nx):
                startnode = i*(nx+1)+j
                el = Element(len(self.elements),
                             nodelist = [ self.nodes[startnode],
                                          self.nodes[startnode+1],
                                          self.nodes[startnode+1+(nx+1)],
                                          self.nodes[startnode+(nx+1)] ] )
                self.elements.append(el)

        # Add the DOFs directly here, on the bold assumption that we
        # know what we're doing.  In fact, we only need to add the
        # displacement DOFs, everything else is handled in a special
        # way.
        
        self.dofs = []
        self.dofindex = 0
        for n in self.nodes:
            # start_index = sum( [ x.size for x in self.dofs ] )
            start_index = self.dofindex
            
            disdof = Dof("Displacement",start_index,2)
            self.dofs.append(disdof)
            n.adddof(disdof)

            self.dofindex = start_index + 2
            
        self.gpdofs = []
        self.gpdofdict = {}

    def clear(self):
        self.matrix = {}
        self.rhs = {}
        self.freedofs = []

    # For now, we assume that gpdofs are only added after all the
    # regular dofs are already in place, so we can figure out the
    # index in a sensible way.  The magic number 14 is the number of
    # DOFs associated with each GPDof object -- the local yield
    # surface radius, the six components of the plastic strain, the
    # six coordinates of the yield surface centroid in stress space,
    # and one Lagrange multiplier for the return-mapping algorithm.
    def add_gpdof(self, el, gp):
        index = self.dofindex + len(self.gpdofs)*14  
        gpd = GPDof("Plasticity",el,gp,index,14)
        # The gp_dof values are *increments* to the plastic strain,
        # they start out at zero.
        for i in range(14):
            gpd.set(i,0.0)
        self.gpdofdict[gp]=gpd

    def clear_gpdofs(self):
        self.gpdofs = []
        self.gpdofdict = {}

    # Builds the elastic master stiffness matrix. 
    def elastic(self,cijkl):
        for e in self.elements:
            nodeset = [(e.nodes[ii],ii) for ii in range(4)]
            for p in e.gausspts():
                jack = e.jacobian(p.xi,p.zeta)*p.weight
                for (nd,ndx) in nodeset:
                    ndof = nd.dof("Displacement")
                    for i in range(ndof.size):
                        row = ndof.index+i

                        # Do RHS.
                        try:
                            val = self.rhs[row]
                        except KeyError:
                            val = 0.0
                            self.rhs[row]=0.0

                        res = 0.0
                        for j in range(2):
                            resj = e.dshapefn(ndx,j,p.xi,p.zeta)
                            for k in range(3):
                                for l in range(3):
                                    # Plastic strain contribution.
                                    res += resj*cijkl[i][j][k][l]*e.gpdata[p][voigt[k][l]+1]
                        val += res*jack
                        self.rhs[row] = val 

                        # Actual matrix:
                        for (md, mdx) in nodeset:
                            
                            # In-plane strain contributions to stress.
                            mdof = md.dof("Displacement")
                            for k in range(mdof.size):
                                col = mdof.index+k

                                try:
                                    val = self.matrix[row,col]
                                except KeyError:
                                    val = 0.0
                                    self.matrix[row,col] = 0.0
                                
                                pres = 0.0
                                for j in range(2):
                                    presj = e.dshapefn(ndx,j,p.xi,p.zeta)
                                    for l in range(2):
                                        pres += presj*cijkl[i][j][k][l]*e.dshapefn(mdx,l,p.xi,p.zeta)
                                val -= pres*jack
                                self.matrix[row,col]=val


        return self.matrix


    # Builds the plastic stiffness matrix for the Newton-Raphson
    # solver.  Assumes that the DOF values are already in the DOF
    # objects in self.dofs and self.gpdofs.
    def plastic(self, cijkl, yld):
        print "Entering plastic function."
        self.clear() # Clears matrix, rhs, and freedofs.

        for e in self.elements:
            print "Building matrix for element ", e.index
            nodeset = [(e.nodes[ii],ii) for ii in range(4)]
            for p in e.gausspts():
                jack = e.jacobian(p.xi,p.zeta)*p.weight
                self.plastic_rhs(jack,nodeset,e,p,cijkl,yld)
                self.plastic_mtx(jack,nodeset,e,p,cijkl,yld)


    def plastic_mtx(self,jack,nodeset,e,p,cijkl,yld):

        try:
            gpdof = self.gpdofdict[p]
        except KeyError:
            pass
        else:
            gpdof = None
            
        # Nodal equations first.
        for (nd,ndx) in nodeset:
            ndof = nd.dof("Displacement")
            for i in range(ndof.size):
                row = ndof.index + i

                # Nodal entries first.

                for (md,mdx) in nodeset:
                    mdof = md.dof("Displacement")
                    for k in range(mdof.size):
                        col = mdof.index + k

                        mtxval = 0.0
                        
                        for j in range(2):
                            dsfn = e.dshapefn(ndx,j,p.xi,p.zeta)
                            for l in range(2):
                                mtxval += cijkl[i][j][k][l]*\
                                          e.dshapefn(mdx,l,p.xi,p.zeta)*\
                                          dsfn
                        try:
                            self.matrix[row,col] -= mtxval*jack
                        except KeyError:
                            self.matrix[row,col] = -mtxval*jack
                            
                # Gausspoint entries, if any.
                if gpdof:
                    for j in range(2):
                        dsfn = e.dshapefn(ndx,j,p.xi,p.zeta)
                        for k in range(3):
                            for l in range(3):
                                col = gpdof.index+voigt[k][l]+1
                                mtxval = cijkl[i][j][k][l]*dsfn
                                try:
                                    self.matrix[row,col] += mtxval*jack
                                except KeyError:
                                    self.matrix[row,col] = mtxval*jack

        
        # Pointwise equations.
        if gpdof:
            # Current values of useful quantities at this gausspoint.
            cstress = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
            ccenter = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
            for i in range(3):
                for j in range(3):
                    v = 0.0
                    for (md,mdx) in nodeset:
                        dof = md.dof("Displacement")
                        for k in range(2):
                            for l in range(2):
                                v += cijkl[i][j][k][l]*\
                                     e.dshapefn(mdx,l,p.xi,p.zeta)*\
                                     dof.value[k]
                    for k in range(3):
                        for l in range(3):
                            v -= cijkl[i][j][k][l]*e.gpdata[p][voigt[k][l]+1]
                            v -= cijkl[i][j][k][l]*gpdof.value[voigt[k][l]+1]
                    cstress[i][j] += v

                    ccij = e.gpdata[p][voigt[i][j]+7]
                    ccij += gpdof.value[voigt[i][j]+7]
                    ccenter[i][j] += ccij

            # Current plastic strain increment, as a tensor.
            dep = [ [ gpdof.value[voigt[i][j]+1] for j in range(3) ]
                    for i in range(3) ]

            # Various "derived" quantities.
            dy = yld.dyeeld(cstress,ccenter)  # 3x3 tensor
            flow = yld.flow(cstress,ccenter)  # 3x3 tensor
            dflow = yld.dflow(cstress,ccenter)  # 3x3x3x3, deriv wrt 1st arg.

            ihard = yld.isohard(dep)    # Scalar
            dihard = yld.disohard(dep)  # 3x3 tensor, deriv wrt dep.
            
            khard = yld.khard(dep)      # 3x3 tensor
            dkhard = yld.dkhard(dep)    # 3x3x3x3 tensor, deriv wrt dep.

            lmbda = gpdof.value[13]     # Lagrange multiplier.
                
            # Isotropic hardening.
            row = gpdof.index
            try:
                self.matrix[row,row] += 1.0
            except KeyError:
                self.matrix[row,row] = 1.0

            ep_increment = [ [ gpdof.value[voigt[i][j]+1] for j in range(3) ]
                             for i in range(3) ]
            dihard = yld.disohard(ep_increment)
            for i in range(3):
                for j in range(3):
                    col = gpdof.index+voigt[i][j]+1
                    try:
                        self.matrix[row,col] -= dihard[i][j]
                    except KeyError:
                        self.matrix[row,col] = -dihard[i][j]

            # Flow rule.
            for i in range(3):
                for j in range(i+1):
                    row = gpdof.index+voigt[i][j]+1
                    # Deriv wrt lmbda.
                    try:
                        self.matrix[row,gpdof.index+13] += dy[i][j]
                    except KeyError:
                        self.matrix[row,gpdof.index+13] = dy[i][j]
                        
                    # Diagonal term from dep contribution.
                    try:
                        self.matrix[row,gpdof.index+voigt[i][j]+1] -= 1.0
                    excpet KeyError:
                        self.matrix[row,gpdof.index+voigt[i][j]+1] = -1.0

                    # Principal pointwise term.
                    for m in range(3):
                        for n in range(3):
                            col = gpdof.index + voigt[m][n] + 1
                            mtxval = sum([ sum([ -lmbda*dflow[i][j][k][l]*cijkl[k][l][m][n] for l in range(3)]) for k in range(3) ])
                            try:
                                self.matrix[row,col] += mtxval
                            except KeyError:
                                self.matrix[row,col] = mtxval

                            col = gpdof.index + voigt[m][m] + 7
                            mtxval = -lmbda*dflow[i][j][m][n]
                            try:
                                self.matrix[row,col] += mtxval
                            except KeyError:
                                self.matrix[row,col] = mtxval

                    # Derivatives wrt nodal DOFs.
                    # Abandoning this effort....

                    
            # Kinematic hardening.

            # Consistency equation.

            
    def plastic_rhs(self,jack,nodeset,e,p,cijkl,yld):
        for (nd,ndx) in nodeset:
            # Iterate over nodal DOFs for rows.
            ndof = nd.dof("Displacement")
            for i in range(ndof.size):
                row = ndof.index + i
                
                # For the Newton solver, the RHS is the value of the
                # equation, not just the constant part of it.

                res = 0.0
                for j in range(2):
                    resj = 0.0
                    
                    for (md,mdx) in nodeset:
                        mdof = md.dof("Displacement")
                        for k in range(2):
                            for l in range(2):
                                resj += cijkl[i][j][k][l]*\
                                        e.dshapefn(mdx,l,p.xi,p.zeta)*\
                                        mdof.value[k]


                    for k in range(3):
                        for l in range(3):
                            resj -= cijkl[i][j][k][l]*\
                                    e.gpdata[p][voigt[k][l]+1]


                    try:
                        gpdof = self.gpdofdict[p]
                    except KeyError:
                        pass
                    else:
                        for k in range(3):
                            for l in range(3):
                                resj -= cijkl[i][j][k][l]*\
                                         gpdof.value[voigt[k][l]+1]
                        
                    res += resj*e.dshapefn(ndx,j,p.xi,p.zeta)
                        
                    try:
                        self.rhs[row] -= res*jack
                    except KeyError:
                        self.rhs[row] = -res*jack
                        
        # If this gausspoint has an associated gpdof, then
        # there are 14 equations for it.  They are, in order,
        # the isotropic hardening equation, the flow rule, the
        # kinetmatic hardening equation, and the yield
        # condition.
        try:
            gpdof = self.gpdofdict[p]
        except KeyError:
            pass
        else:
            local_lambda = gpdof.value[13]
            local_gamma = gpdof.value[0] + e.gpdata[p][0]
            local_stress = self.epstress(e,p,cijkl,gpdof=gpdof)
            local_dcenter = [ [ gpdof.value[voigt[i][j]+7]
                                for j in range(3) ]
                              for i in range(3) ]
            local_center = [ [ e.gpdata[p][voigt[i][j]+7]
                               + local_dcenter[i][j]
                               for j in range(3) ]
                             for i in range(3) ]
            local_dep = [ [ gpdof.value[voigt[i][j]+1]
                            for j in range(3) ]
                          for i in range(3) ]
            # Isotropic hardening equation.
            inc =  gpdof.value[0] - yld.isohard(local_dep)
            try:
                self.rhs[gpdof.index] += inc
            except KeyError:
                self.rhs[gpdof.index] = inc


            # Flow rule.
            flow = yld.flow(local_stress, local_center)
            for i in range(3):
                for j in range(i+1):
                    inc = local_lambda*flow[i][j]-local_dep[i][j]
                    try:
                        self.rhs[gpdof.index+voigt[i][j]+1] += inc
                    except KeyError:
                         self.rhs[gpdof.index+voigt[i][j]+1] = inc
                    
            # Kinematic hardening equation.
            lkhard = yld.khard(local_dep)
            for i in range(3):
                for j in range(i+1):
                    inc = local_dcenter[i][j] - lkhard[i][j]
                    try:
                        self.rhs[gpdof.index+voigt[i][j]+7] += inc
                    except KeyError:
                        self.rhs[gpdof.index+voigt[i][j]+7] = inc
                    
            # Actual yield condition.
            inc = yld.yeeld(local_stress, local_center, local_gamma)
            try:
                self.rhs[gpdof.index+13] += inc
            except KeyError:
                self.rhs[gpdof.index+13] = inc
            
    

                        

    def dump_matrix(self,outfile):
        mtxsize = sum( [d.size for d in self.dofs] )
        for i in range(mtxsize):
            for j in range(mtxsize):
                try:
                    v = self.matrix[i,j]
                except KeyError:
                    pass
                else:
                    print >> outfile,i,j,v


    def setbcs(self,top,bottom):
        self.topbc = top
        self.bottombc = bottom



    # freedofs and linearsystem taken from more general mesh, in which
    # non-displacement DOFs can exist.  The scheme here is to set up
    # all the DOFs as free, and then remove those DOFs with name
    # "Displacement" which are not free.  As long as you start with
    # all the DOFs, you don't need to know the names of any of the
    # others.
    def set_freedofs(self):
        alldofs = self.dofs + self.gpdofs
        mtxsize = sum( [d.size for d in alldofs] )
        self.freedofs = [-1]*mtxsize
        fixed_rhs = []
        for node in self.nodes:
            for dof in node.alldofs():
                add = False
                if dof.name!="Displacement":
                    add = True
                else: # dof.name *is* "Displacement"
                    if (not (node in self.topnodes) and \
                        not (node in self.bottomnodes)) \
                        or ( (node in self.topnodes) and \
                             self.topbc is None):
                        add = True
                    else: # Fixed DOF, add to fixed-rhs list.
                        fixed_rhs.append(0.0)
                        if node in self.topnodes:
                            fixed_rhs.append(self.topbc)
                        else:
                            fixed_rhs.append(self.bottombc)
                if add:
                    for k in range(dof.index, dof.index+dof.size):
                        self.freedofs[k]=k
                        
        # GPDofs are not nodal, add them separately here.
        for dof in self.gpdofs:
            for k in range(dof.index, dof.index+dof.size):
                self.freedofs[k]=k
            
        # So now we have the list, compress it.  Unlike OOF, both DOF
        # types are enumerated in a single list, free DOFs having
        # non-negative values, and fixed dofs having negative ones.
        free_count = 0
        fixed_count = -1
        for idx in range(len(self.freedofs)):
            if self.freedofs[idx]!=-1:
                self.freedofs[idx]=free_count
                free_count+=1
            else:
                self.freedofs[idx]=fixed_count
                fixed_count-=1

        return (free_count, fixed_count, fixed_rhs)


    def linearsystem(self):
        (free_count, fixed_count, fixed_rhs) = self.set_freedofs()
        
        amtx = SmallMatrix(free_count,free_count)
        cmtx = SmallMatrix(free_count,-(fixed_count+1))
        brhs = SmallMatrix(len(fixed_rhs),1)
        srhs = SmallMatrix(free_count,1)

        amtx.clear()
        cmtx.clear()
        brhs.clear()
        srhs.clear()
    
        for ((i,j),v) in self.matrix.items():
            if self.freedofs[i]>=0 and self.freedofs[j]>=0:
                amtx[self.freedofs[i],self.freedofs[j]]=v
            else:
                if self.freedofs[i]>=0 and self.freedofs[j]<0:
                    cmtx[self.freedofs[i],-(self.freedofs[j]+1)]=v

        for i in range(len(fixed_rhs)):
            brhs[i,0]=fixed_rhs[i]

        for (i,v) in self.rhs.items():
            if self.freedofs[i]>=0:
                srhs[self.freedofs[i],0]=v

        # System to solve is: amtx + cmtx.brhs = srhs
        return (amtx,cmtx,brhs,srhs)


    # Assumes the "Displacement" field has been added to the mesh, but
    # has no other requirements.  Builds the Master Stiffness Matrix,
    # applies boundary conditions, and fills in the displacement DOFs
    # with the resulting solution.
    def solve_elastic(self,cijkl):
        self.clear()
        self.elastic(cijkl)
        (a,c,br,sr) = self.linearsystem()
        nr = (c*br)*(-1.0)-sr # Sign.

        if a.rows()!=0:
            rr = a.solve(nr)
        else:
            rr = 0 # Degenerate case, set to "solved". 
            
        if rr==0:
            for n in self.nodes:
                for d in n.alldofs():
                    for k in range(d.size):
                        ref = self.freedofs[d.index+k]
                        if ref >= 0:
                            d.set(k,nr[ref,0])
                        else:
                            d.set(k,br[-(ref+1),0])
        else:
            print >> sys.stderr, \
                  "Error in solving elastically, return code is %d." % rr


    # Helper function to measure stress.
    def epstress(self,e,p,cijkl,gpdof=None):
        pstrain = e.gpdata[p][1:7]
        stress = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
        for i in range(3):
            for j in range(3):
                for k in range(2):
                    for l in range(2):
                        for m in range(4):
                            stress[i][j] += cijkl[i][j][k][l]*e.nodes[m].dof("Displacement").get(k)*e.dshapefn(m,l,p.xi,p.zeta)

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        stress[i][j] -= cijkl[i][j][k][l]*pstrain[voigt[k][l]]


        if gpdof:
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        for l in range(3):
                            stress[i][j] -= cijkl[i][j][k][l]*gpdof.value[voigt[k][l]+1]

        return stress


        

    def measure_stress(self,cijkl):
        for e in self.elements:
            for p in e.gausspts():
                stress = self.epstress(e,p,cijkl)
                
                print "\nGausspoint: ", p
                print "Stress: ", stress



    # Difference from plas5 is mostly here.  To solve the plastic
    # system, we first solve the elastic system, then iterate over the
    # guasspoints, and for each violation of the yield condition, add
    # a constraint equation, and then solve the resulting larger,
    # global nonlinear system.  It is at least theoretically possible
    # that the resulting system will violate the yield condition at
    # unconstrainted points.  This is one of the questions we want to
    # answer.

    def solve_plastic(self,cijkl,yld):
        # First, solve the elastic problem.  Solve_elastic writes the
        # displacement values back into the DOFs.
        print "Starting plastic solution."
        self.solve_elastic(cijkl)
        print "Solved elastic system."

        # Compute the stress at all the gausspoints.
        for e in self.elements:
            for p in e.gausspts():
                stress = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                gamma = e.gpdata[p][0]
                pstrain = e.gpdata[p][1:7]
                center = [ [ e.gpdata[p][voigt[ii][jj]+7]
                             for jj in range(3) ] for ii in range(3) ]
                for i in range(3):
                    for j in range(3):
                        for k in range(2):
                            for l in range(2):
                                for m in range(4):
                                    stress[i][j] += cijkl[i][j][k][l]*e.nodes[m].dof("Displacement").get(k)*e.dshapefn(m,l,p.xi,p.zeta)
                                            
                        for k in range(3):
                            for l in range(3):
                                stress[i][j] -= cijkl[i][j][k][l]*pstrain[voigt[k][l]]

                yf = yld.yeeld(stress,center,gamma)

                if yf>0: # Point is outside the yield surface...
                    print "Adding plastic gausspoint."
                    self.add_gpdof(e,p)

        # Build the plastic matrix for these DOFs.  It's in
        # self.matrix and self.rhs after this function returns.
        self.plastic(cijkl,yld)

    
        
        
                            
                

    def draw(self):
        import visual
        frame = visual.frame()
        outline = visual.curve(frame=frame,
                               pos=[(0.0,0.0,0.0),(1.0,0.0,0.0),
                                    (1.0,1.0,0.0),(0.0,1.0,0.0),
                                    (0.0,0.0,0.0)],color=visual.color.red)
        for e in self.elements:
            outline = []
            for n in e.nodes:
                for d in n.dofs:
                    if d.name=="Displacement":
                        outline.append( (n.position.x + d.value[0],
                                         n.position.y + d.value[1],
                                         0.0) )
                        break
                else:
                    outline.append( (n.position.x, n.position.y,0.0) )
            outline.append(outline[0])
            visual.curve(frame=frame,pos=outline)
        return frame

    def measure_force(self,cijkl):
        # Use three guass-points per segment in the usual way.
        mpt = math.sqrt(3.0/5.0)
        pts = [-mpt, 0.0, mpt]
        wts = [5.0/9.0, 8.0/9.0, 5.0/9.0]
        elcount = len(self.bottomnodes)-1
        force = 0.0
        for e in self.elements[:elcount]: # Bottom row of elements.
            # Plastic strain is interpolated -- epcfs[i,j] is ith
            # shape function coefficient of jth (voigt) component of
            # plastic stress.
            epcfs = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

            eprhs = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

            # Compute integrals of plastic strain function (from
            # gausspoint data) times shape functions, for each plastic
            # strain component.
            for p in e.gausspts():
                jack = p.weight*e.jacobian(p.xi,p.zeta)
                pdata = e.gpdata[p]
                for c in range(6):
                    for i in range(4):
                        # Plastic strain starts at 2nd position in pdata.
                        eprhs[i][c] += pdata[c+1]*e.shapefn(i,p.xi,p.zeta)*jack
                        
            # Now compute the amplitudes of the shape function
            # interpolant, by multiplying by the inverse mass matrix
            # of the element.
            for c in range(6):
                for s in range(4):
                    for t in range(4):
                        epcfs[s][c] += e.s_mtx[s,t]*eprhs[t][c]

            for (pt,wt) in zip(pts,wts):
                force_inc = 0.0
                # Construct the full strain tensor.
                et = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
                for i in range(2):
                    for j in range(2):
                        for s in range(4):
                            et[i][j] += e.nodes[s].dof("Displacement").get(i)*e.dshapefn(s,j,pt,-1)
                    
                for i in range(3):
                    for j in range(3):
                        for s in range(4):
                            et[i][j] -= epcfs[s][voigt[i][j]]*e.shapefn(s,pt,-1)
                # Now we have total strain, compute stress.  We only
                # actually care about the 11 component of stress,
                # i.e. the force along the y axis.
                s11 = 0.0
                for k in range(3):
                    for l in range(3):
                        s11 += cijkl[1][1][k][l]*et[k][l]

                # The wacky second factor is the jacobian for the
                # one-dimensional integral.
                force += s11*wt*((1.0/elcount)/2.0)
                
        return force
                            

def sysplastk(m,c,y,b):
    m.setbcs(b,0.0)
    m.solve_plastic(c,y)
    f = m.measure_force(c)
    print b,f
    sys.stdout.flush()

def go():
    m = Mesh(3,3)
    c = Cijkl(0.5,0.25)
    y = Yeeld(0.1,0.0,0.0)
    for i in range(31):
        b = i*0.01
        sysplastk(m,c,y,i*0.01)
    return m

def basic(b):
    m = Mesh(3,3)
    c = Cijkl(0.5,0.25)
    y = Yeeld(0.1,0.0,0.0)
    m.setbcs(b,0.0)
    m.solve_plastic(c,y)


# More basic than sysplastk, just runs ycheck at a point and doesn't
# know about the mesh.
def plastk(amp, dstrain, c, y, pstrain, fcenter, gamma):
    delta = 0.01
    # Assert total strain.
    strain = [ [ (amp*delta)*dstrain[ii][jj]
                 for jj in range(3) ] for ii in range(3) ]
    
    stress = [ [ sum([ sum([
        c[ii][jj][kk][ll]*(strain[kk][ll]-pstrain[kk][ll])
        for ll in range(3) ]) for kk in range(3) ])
                 for jj in range(3) ] for ii in range(3) ]
    
    p = y.yeeld(stress,fcenter,gamma)
    if p > 0:
        res = ycheck(c,y,stress,fcenter,gamma)
        gamma += res[0]
        pstrain = [ [ pstrain[ii][jj]+res[voigt[ii][jj]+1]
                      for jj in range(3) ] for ii in range(3)  ]
        fcenter = [ [ fcenter[ii][jj]+res[voigt[ii][jj]+7]
                      for jj in range(3) ] for ii in range(3) ]

        stress = [ [ sum([ sum([
            c[ii][jj][kk][ll]*(strain[kk][ll]-pstrain[kk][ll])
            for ll in range(3) ]) for kk in range(3) ])
                     for jj in range(3) ] for ii in range(3) ]
        
    print "Strain: ", strain
    print "Plastic strain: ", pstrain

    return (pstrain, fcenter, gamma)




def test():
    dstrain = [[0.1, 1.0, 0.0], [1.0,0.1,0.0],[0.0,0.0,0.1]]
    # dstrain = [[1.1, 0.0, 0.0], [0.0,-0.9,0.0],[0.0,0.0,0.1]]

    pstrain = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    gamma = 0.0
    center = [[ 0.0,  0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

    c = Cijkl(0.5,0.25)
    y = Yeeld(0.05,0.0,0.1)

    for i in range(25):
        (pstrain,center,gamma)=plastk(i,dstrain,c,y,pstrain,center,gamma)
    # for i in range(15,-15,-1):
    #     (pstrain,center,gamma)=plastk(i,dstrain,c,y,pstrain,center,gamma)
    # for i in range(-15,15):
    #     (pstrain,center,gamma)=plastk(i,dstrain,c,y,pstrain,center,gamma)
    # for i in range(15,-15,-1):
    #     (pstrain,center,gamma)=plastk(i,dstrain,c,y,pstrain,center,gamma)

if __name__=="__main__":
    basic(0.2)
#     go()

    
