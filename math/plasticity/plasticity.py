# -*- python -*-
# $RCSfile: plasticity.py,v $
# $Revision: 1.25 $
# $Author: reida $
# $Date: 2007/02/16 15:03:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 


# Prototype code for playing with plastic constitutive rules.  Has a
# local, custom-constructed mesh of fixed geometry, and various other
# cheats which bypass the full generality of OOF, with the idea of
# focussing on the plasticity part.

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
        self.auxdofs = []
        self.auxeldofs = {}
        self.elements = sets.Set()
    def __repr__(self):
        return "Node(%d,%f,%f)" % (self.index,
                                   self.position.x, self.position.y)
    def add_element(self, el):
        self.elements.add(el)
        self.eldofs[el]=[]
        self.auxeldofs[el]=[]
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
    def addauxdof(self,aux):
        self.auxdofs.append(aux)
    def addauxeldof(self,el,aux):
        self.auxeldofs[el].append(aux)
            
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
    # Auxiliary DOFs have no index in the master stiffness matrix,
    # so there's no corresponding index retrieval function.
    def aux(self,dofname):
        for a in self.auxdofs:
            if a.name==dofname:
                return a
    def auxel(self,el,dofname):
        for a in self.auxeldofs[el]:
            if a.name==dofname:
                return a

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

class AuxDof(Dof):
    def __repr__(self):
        return "AuxDof(%s,%d,%d)" % (self.name, self.index, self.size)
        
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
    def __repr__(self):
        return "Element(%d,%s)" % (self.index, self.nodes)
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
        return j11*j22-j21*j12

    # Return the relevant gausspoints, once they're computed.
    def gausspts(self):
        if not Element.gptable:
            # mpt = math.sqrt(3.0/5.0)
            # pts = [-mpt,0.0,mpt]
            # wts = [5.0/9.0, 8.0/9.0, 5.0/9.0]
            mpt = math.sqrt(1.0/3.0)
            pts = [-mpt,mpt]
            wts = [1.0,1.0]
            n = len(pts)
            for i in range(n):
                for j in range(n):
                    Element.gptable.append(
                        GaussPoint(pts[j],pts[i],wts[j]*wts[i]))
        return Element.gptable


# Plasticity utility class.  For the moment, assumes Von Mises yield
# and associated flow.  "Yield" is a reserved word in Python.
class Yeeld:
    ident = [[1.0,0,0],[0,1.0,0],[0,0,1.0]]
    def __init__(self,stress):
        self.yieldpt = stress # Scalar.
  
    # Scalar yield function as a function of the passed-in stress,
    # which is assumed to be a symmetric 3x3 tensor.
    def yeeld(self,stress):
        return math.sqrt(deviator(stress))-math.sqrt(2.0/3.0)*self.yieldpt

    # Tensor-valued derivative of the yield function at the passed-in
    # stress point.
    def dyeeld(self,stress):
        # 1/3 of the trace of the stress.
        t = (1.0/3.0)*sum( [stress[i][i] for i in range(3)] )
        dv = math.sqrt(deviator(stress))
        return [ [ (stress[i][j]-t*Yeeld.ident[i][j])/dv
                   for j in range(3) ] for i in range(3) ]
    
    # Four-index-tensor-valued second derivative of the yield function
    # at the indicated stress. 
    def d2yeeld(self,stress):
       # (1/3) of the trace of the stress.
        t = (1.0/3.0)*sum( [stress[i][i] for i in range(3)] )
        trm1 = [[[[ (stress[k][l]-t*Yeeld.ident[k][l])*
                    (stress[m][n]-t*Yeeld.ident[m][n])
                    for n in range(3) ]
                  for m in range(3) ]
                 for l in range(3) ]
                for k in range(3) ]
        trm2 = [[[[ Yeeld.ident[k][m]*Yeeld.ident[l][n] -
                    (1.0/3.0)*Yeeld.ident[m][n]*Yeeld.ident[k][l]
                    for n in range(3) ]
                  for m in range(3) ]
                 for l in range(3) ]
                for k in range(3) ]
        dv = math.sqrt(deviator(stress))
        dv3 = dv**3
        return [[[[ (-trm1[i][j][k][l]/dv3)+(trm2[i][j][k][l]/dv)
                    for l in range(3) ]
                  for k in range(3) ]
                 for j in range(3) ]
                for i in range(3) ]
    


# Compute the plastic strain increment at a particular point, given
# the input constitutive parameters and the starting stress and
# geometric strain.
def ycheck(cijkl,yld,stress):
    eps = 1.0e-10
    # Local return-mapping problem -- DOFs are, in order,
    # lambda, ep00,ep11,ep22,ep12,ep02,ep01 (voigt order).
    mtx = smallmatrix.SmallMatrix(7,7)
    rhs = smallmatrix.SmallMatrix(7,1)
    #
    ep = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    lmbda = 0.0
    #
    while 1:
        lstress = [ [ stress[i][j]-sum([ sum([ cijkl[i][j][k][l]*ep[voigt[k][l]] for l in range(3) ]) for k in range(3) ]) for j in range(3) ] for i in range(3) ]

        mtx.clear()
        rhs.clear()
        # Build right-hand-side, check for zeroness.
        rhs[0,0] = -yld.yeeld(lstress)
        dy = yld.dyeeld(lstress)
        d2y = yld.d2yeeld(lstress)
        for i in range(3):
            for j in range(i+1):
                rhs[voigt[i][j]+1,0] = -lmbda*dy[i][j]+ep[voigt[i][j]]

        mag = sum( [ rhs[i,0]**2 for i in range(rhs.rows()) ] )
        if mag<eps:
            break # out of while loop.

        # Build matrix. 
        # First row, consistency equation.
        for k in range(3):
            for l in range(3):
                col = voigt[k][l]+1
                mtx[0,col] += sum([ sum([ -dy[i][j]*cijkl[i][j][k][l] 
                                          for j in range(3) ])
                                    for i in range(3) ])
        # Subsequent rows:
        for i in range(3):
            for j in range(i+1):
                row = voigt[i][j]+1
                # Column zero, easy.
                mtx[row,0]=dy[i][j]
                for m in range(3):
                    for n in range(3):
                        col = voigt[m][n]+1
                        diag = 0.0
                        if i==m and j==n:
                            diag = 1.0
                        mtx[row,col] += sum([ sum([ -lmbda*d2y[i][j][k][l]*cijkl[k][l][m][n] for l in range(3) ]) for k in range(3) ])-diag

        # Solve the resulting linearized system.
        rr = mtx.solve(rhs)
        if rr==0:
            lmbda += rhs[0,0]
            for i in range(6):
                ep[i] += rhs[i+1,0]
        else:
            print "Error in solving, rr=", rr

    # Broke out of loop.
    return ep    
        
class Mesh:
    def __init__(self,xelements=5,yelements=5):
        self.nodelist = []
        self.ellist = []

        # Boundaries to which rather primitive conditions can be
        # applied.
        self.topnodes = []
        self.bottomnodes = []

        dx = 1.0/xelements
        dy = 1.0/yelements

        self.doflist = []
        self.auxlist = []
        self.freedofs = [] # Index list, doesn't actually contain dofs.
        
        # Master stiffness matrix is a dictionary indexed by tuples of
        # integers, whose values are floating-point numbers.
        self.matrix = {}
        self.rhs = {}
        
        node_index = 0
        for i in range(yelements+1):
            for j in range(xelements+1):
                node = Node(node_index,Position(j*dx,i*dy))
                self.nodelist.append(node)
                if i==0:
                    self.bottomnodes.append(node)
                if i==yelements:
                    self.topnodes.append(node)
                node_index += 1
                
        

        element_index = 0
        for i in range(yelements):
            for j in range(xelements):
                # Nodes stored in clockwise order.
                nodes = [self.nodelist[i*(xelements+1)+j],
                         self.nodelist[i*(xelements+1)+j+1],
                         self.nodelist[(i+1)*(xelements+1)+j+1],
                         self.nodelist[(i+1)*(xelements+1)+j]]
                                       
                self.ellist.append(Element(element_index,nodes))
                element_index += 1

    # Add a new field to be solved for.  For now, we just assume that
    # there is a corresponding equation for each DOF, and that it has
    # the same index.  Value, if supplied, must be a list, even for
    # scalar DOFs.
    def addfield(self, name, size, value=None):
        mtxsize = sum( [d.size for d in self.doflist] )
        count = 0
        for n in self.nodelist:
            newdof = Dof(name, mtxsize+count*size, size)
            if value is not None:
                for i in range(len(value)):
                    newdof.set(i,value[i])
            n.adddof(newdof)
            self.doflist.append(newdof)
            count += 1

    # Add an element-specific field.  
    def addelfield(self, name, size, value=None):
        mtxsize = sum( [d.size for d in self.doflist] )
        count = 0
        for n in self.nodelist:
            for e in n.elements:
                newdof = Dof(name, mtxsize+count*size, size)
                if value is not None:
                    for i in range(len(value)):
                        newdof.set(i,value[i])
                n.adddof(newdof)
                self.doflist.append(newdof)
                count += 1

    # Ordinary one-per-node auxiliary field.
    def addauxfield(self, name, size, value=None):
        listsize = sum( [a.size for a in self.auxlist] )
        count = 0
        for n in self.nodelist:
            newdof = AuxDof(name, listsize+count*size, size)
            if value is not None:
                for i in range(len(value)):
                    newdof.set(i,value[i])
            n.addauxdof(newdof)
            self.auxlist.append(newdof)
            count += 1

    # Add an element-specific auxiliary field.
    def addauxelfield(self, name, size, value=None):
        listsize = sum( [a.size for a in self.auxlist] )
        count = 0
        for n in self.nodelist:
            for e in n.elements:
                newdof = AuxDof(name, listsize+count*size, size)
                if value is not None:
                    for i in range(len(value)):
                        newdof.set(i,value[i])
                n.addauxeldof(e,newdof)
                self.auxlist.append(newdof)
                count += 1

    def clear(self):
        self.matrix = {}
        self.rhs = {}
        self.freedofs = []


    # Reset is like clear, but also removes all the fields.  There is
    # no facility for selectively removing fields.
    def reset(self):
        self.clear()
        self.doflist = []
        self.auxlist = []
        for n in self.nodelist:
            n.dofs = []
            n.auxdofs = []
            for e in n.elements:
                n.eldofs[e]=[]
                n.auxeldofs[e]=[]


        
    # Build the elastic contributions to the stiffness matrix.  In
    # OOF, individual properties do this, but this is not OOF, it is
    # merely OOFoid.  It could eventually be OOFtacular.
    def elastic(self,cijkl):
        for e in self.ellist:
            ndset = [(ii,e.nodes[ii]) for ii in range(len(e.nodes))]
            for (mudx,mu) in ndset:
                for i in range(2): 
                    row = mu.dofindex("Displacement")+i
                    for (nudx,nu) in ndset:
                        for k in range(2):
                            col = nu.dofindex("Displacement")+k
                            val = 0.0
                            for g in e.gausspts():
                                for j in range(2):
                                    for l in range(2):
                                        val-=cijkl[i][j][k][l]*e.dshapefn(mudx,j,g.xi,g.zeta)*e.dshapefn(nudx,l,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                            try:
                                self.matrix[(row,col)]+=val
                            except KeyError:
                                self.matrix[(row,col)]=val
                    # RHS contribution.
                    val = 0.0
                    for (nudx,nu) in ndset:
                        pstrain = nu.auxel(e,"Plastic Strain")
                        if pstrain is not None:
                            for g in e.gausspts():
                                for j in range(2): # Sum...
                                    for k in range(3):
                                        for l in range(3):
                                            val+=cijkl[i][j][k][l]*pstrain.get(voigt[k][l])*e.shapefn(nudx,g.xi,g.zeta)*e.dshapefn(mudx,j,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                    try:
                        self.rhs[row]+=val
                    except KeyError:
                        self.rhs[row]=val


    # Funciton for computing the value of each of the equations for
    # the current degrees of freedom.  Needed by the Newton-Raphson
    # solver, we think.
    def phi(self,cijkl,yfunc):
        phi = {}
        for e in self.ellist:
            ndset = [(ii,e.nodes[ii]) for ii in range(len(e.nodes))]
            for g in e.gausspts():

                # Preliminary: Compute stress and pcp at this gauss point.

                gstrain = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                epval = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                epival = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                pcpval = 0.0

                for (mudx,mu) in ndset:
                    disp = mu.dof("Displacement")
                    for k in range(2):
                        for l in range(2):
                            gstrain[k][l] += 0.5*(disp.get(k)*e.dshapefn(mudx,l,g.xi,g.zeta)+disp.get(l)*e.dshapefn(mudx,k,g.xi,g.zeta))
                    ep = mu.auxel(e,"Plastic Strain")
                    if ep is not None:
                        for k in range(3):
                            for l in range(3):
                                epval[k][l] += ep.get(voigt[k][l])*e.shapefn(mudx,g.xi,g.zeta)
                    epi = mu.eldof(e,"Plastic Strain Increment")
                    if epi is not None:
                        for k in range(3):
                            for l in range(3):
                                epival[k][l] += epi.get(voigt[k][l])*e.shapefn(mudx,g.xi,g.zeta)
                    pcp = mu.eldof(e,"Plastic Consistency Parameter")
                    if pcp is not None:
                        pcpval += pcp.get(0)*e.shapefn(mudx,g.xi,g.zeta)

                # Now we have all the strains, we know what to do.
                stress = [ [ sum([ sum([ cijkl[i][j][k][l]*(gstrain[k][l]-epval[k][l]-epival[k][l]) for l in range(3) ]) for k in range(3)]) for j in range(3) ] for i in range(3) ]

                # At this point, stress, epival, and pcpval are all
                # set for this gauss point.

                for (mudx,mu) in ndset:
                    
                    # Elastic equations.
                    for i in range(2):
                        row = mu.dofindex("Displacement")+i
                        val = 0.0
                        for j in range(2):
                            val -= e.dshapefn(mudx,j,g.xi,g.zeta)*stress[i][j]

                        val *= g.weight*e.jacobian(g.xi,g.zeta)
                        try:
                            phi[row]+=val
                        except KeyError:
                            phi[row]=val
                    
                    # Plastic consistency paramter equation.
                    pcp = mu.eldof(e,"Plastic Consistency Parameter")
                    if pcp is not None:
                        row = pcp.index
                        val = e.shapefn(mudx,g.xi,g.zeta)*yfunc.yeeld(stress)
                        val *= g.weight*e.jacobian(g.xi,g.zeta)
                        try:
                            phi[row]+=val
                        except KeyError:
                            phi[row]=val

                    # Consistency criterion.
                    epi = mu.eldof(e,"Plastic Strain Increment")
                    if epi is not None:
                        dy = yfunc.dyeeld(stress)
                        for i in range(3):
                            for j in range(i+1):
                                row = epi.index+voigt[i][j]
                                val = e.shapefn(mudx,g.xi,g.zeta)*(pcpval*dy[i][j] - epival[i][j])
                                val *= g.weight*e.jacobian(g.xi,g.zeta)
                                try:
                                    phi[row]+=val
                                except KeyError:
                                    phi[row]=val
        return phi

    # Make the plastic contributions to the master stiffness matrix.
    # Elastic contributions have already been made, including
    # subtracting off the plastic strain, but not the plastic strain
    # increment.
    def plastic(self,cijkl,yfunc):
        # Add dependence on plastic strain increment to "elastic" rows.
        for e in self.ellist:
            ndset = [(ii,e.nodes[ii]) for ii in range(len(e.nodes))]
            for (mudx,mu) in ndset:
                for i in range(2):
                    row = mu.dofindex("Displacement")+i
                    for (nudx,nu) in ndset:
                        epi = nu.eldofindex(e,"Plastic Strain Increment")
                        if epi is not None:
                            for k in range(3):
                                for l in range(3):  # Indexing.
                                    col = epi+voigt[k][l]  
                                    val = 0.0
                                    for g in e.gausspts():
                                        for j in range(2):
                                            val+=cijkl[i][j][k][l]*e.shapefn(nudx,g.xi,g.zeta)*e.dshapefn(mudx,j,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                                    try:
                                        self.matrix[(row,col)]+=val
                                    except KeyError:
                                        self.matrix[(row,col)]=val
        # Satisfy yield condition.
        for e in self.ellist:
            # print "Elements again."
            ndset = [(ii,e.nodes[ii]) for ii in range(len(e.nodes))]

            # Compute the local stress -- yield function and
            # derivatives take this as an argument.
            for g in e.gausspts():
                # Plastic strain is done separately because it's
                # needed later on. The real total strain is
                # gstrain-pstrain.
                gstrain = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                pstrain = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                for (mudx, mu) in ndset:
                    disp = mu.dof("Displacement")
                    for k in range(2):
                        for l in range(2):
                            gstrain[k][l]+=0.5*(disp.get(k)*e.dshapefn(mudx,l,g.xi,g.zeta)+disp.get(l)*e.dshapefn(mudx,k,g.xi,g.zeta))
                            
                    ep = mu.auxel(e,"Plastic Strain")
                    for k in range(3):
                        for l in range(3):
                            pstrain[k][l]+=e.shapefn(mudx,g.xi,g.zeta)* \
                                            ep.get(voigt[k][l])
                    epi = mu.eldof(e,"Plastic Strain Increment")
                    if epi is not None:
                        for k in range(3):
                            for l in range(3):
                                gstrain[k][l]-=e.shapefn(mudx,g.xi,g.zeta)* \
                                                epi.get(voigt[k][l])

                stress = [ [ sum( [ sum ( [ cijkl[i][j][k][l]*\
                                            (gstrain[k][l]-pstrain[k][l])
                                            for l in range(3) ])
                                    for k in range(3) ])
                             for j in range(3) ]
                           for i in range(3) ]
                
                pstress = [ [ sum( [ sum( [ -cijkl[i][j][k][l]*\
                                                pstrain[k][l]
                                              for l in range(3) ])
                                       for k in range(3) ])
                                  for j in range(3) ]
                                for i in range(3) ]

                dy = yfunc.dyeeld(stress) # 3x3 tensor
                ddy = yfunc.d2yeeld(stress) # 3x3x3x3 tensor

                # Stay inside the guasspoint loop.
                for (mudx, mu) in ndset:
                    row = mu.eldofindex(e,"Plastic Consistency Parameter")
                        
                    if row is not None:
                        
                        # Matrix contributions -- iterate over nodes again.
                        for (nudx, nu) in ndset:
                            # Displacement contribution.
                            disp = nu.dofindex("Displacement")
                            for k in range(2):
                                col = disp + k
                                val = 0.0

                                for l in range(2):
                                    for i in range(3):
                                        for j in range(3):
                                            val += e.shapefn(mudx,g.xi,g.zeta)*dy[i][j]*cijkl[i][j][k][l]*e.dshapefn(nudx,l,g.xi,g.zeta)

                                val *= g.weight*e.jacobian(g.xi,g.zeta)

                                try:
                                    self.matrix[(row,col)]+=val
                                except KeyError:
                                    self.matrix[(row,col)]=val
                                    
                            # Plastic strain increment contribution --
                            # still in nu loop.
                            epi = nu.eldofindex(e,"Plastic Strain Increment")
                            if epi is not None:
                                for k in range(3):
                                    for l in range(3): # Indexing.
                                        col = epi+voigt[k][l]
                                        val = 0.0
                                        for i in range(3):
                                            for j in range(3):
                                                val -= e.shapefn(mudx,g.xi,g.zeta)*dy[i][j]*cijkl[i][j][k][l]*e.shapefn(nudx,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                                        try:
                                            self.matrix[(row,col)]+=val
                                        except KeyError:
                                            self.matrix[(row,col)]=val

        # Satisfy consistency requirement.
        for e in self.ellist:
            ndset = [(ii,e.nodes[ii]) for ii in range(len(e.nodes))]
            for g in e.gausspts():
                # Compute strains, as before.
                strain = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                pstrain = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                pcpval = 0.0
                for (mudx, mu) in ndset:
                    disp = mu.dof("Displacement")
                    for k in range(2):
                        for l in range(2):
                            strain[k][l]+=e.dshapefn(mudx,l,g.xi,g.zeta)* \
                                           disp.get(k)
                    ep = mu.auxel(e,"Plastic Strain")
                    for k in range(3):
                        for l in range(3):
                            pstrain[k][l]+=e.shapefn(mudx,g.xi,g.zeta)* \
                                            ep.get(voigt[k][l])
                    epi = mu.eldof(e,"Plastic Strain Increment")
                    if epi is not None:
                        for k in range(3):
                            for l in range(3):
                                strain[k][l]-=e.shapefn(mudx,g.xi,g.zeta)* \
                                               epi.get(voigt[k][l])
                    pcp = mu.eldof(e,"Plastic Consistency Parameter")
                    if pcp is not None:
                        pcpval += e.shapefn(mudx,g.xi,g.zeta)*pcp.get(0)
                                
                stress = [ [ sum( [ sum ( [ cijkl[i][j][k][l]*\
                                            (strain[k][l]-pstrain[k][l])
                                            for l in range(3) ])
                                    for k in range(3) ])
                             for j in range(3) ]
                           for i in range(3) ]

                dy = yfunc.dyeeld(stress) # 3x3 tensor
                ddy = yfunc.d2yeeld(stress) # 3x3x3x3 tensor

                # Still inside the gausspoint loop, do nodes.
                
                for (mudx, mu) in ndset:
                    epi = mu.eldofindex(e,"Plastic Strain Increment")
                    if epi is not None:
                        for i in range(3):
                            for j in range(i+1):
                                row = epi+voigt[i][j]

                                for (nudx, nu) in ndset:

                                    # Consistency parameter.
                                    lmbda = mu.eldofindex(e,
                                    "Plastic Consistency Parameter")
                                    if lmbda is not None:
                                        col=lmbda
                                        val=e.shapefn(mudx,g.xi,g.zeta)*dy[i][j]*e.shapefn(nudx,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                                        try:
                                            self.matrix[(row,col)]+=val
                                        except KeyError:
                                            self.matrix[(row,col)]=val

                                    # Displacement.
                                    disp = mu.dofindex("Displacement")
                                    for m in range(2):
                                        col = disp+m
                                        val = 0.0
                                        for n in range(2):
                                            val += e.shapefn(mudx,g.xi,g.zeta)*pcpval*sum([ sum([ ddy[i][j][k][l]*cijkl[k][l][m][n] for l in range(3) ]) for k in range(3)])*e.dshapefn(nudx,n,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                                        try:
                                            self.matrix[(row,col)]+=val
                                        except KeyError:
                                            self.matrix[(row,col)]=val

                                    # Plastic strain increment --
                                    # don't clobber outer loop's epi
                                    # variable.
                                    epin = nu.eldofindex(e,
                                    "Plastic Strain Increment")
                                    if epin is not None:
                                        for m in range(3):
                                            for n in range(3):  # Indexing.
                                                col = epin + voigt[m][n]
                                                diag = 0.0
                                                if i==m and j==n:
                                                # if voigt[i][j]==voigt[m][n]:
                                                    diag = 1.0
                                                val = -e.shapefn(mudx,g.xi,g.zeta)*(pcpval*sum([ sum([ ddy[i][j][k][l]*cijkl[k][l][m][n] for l in range(3)]) for k in range(3) ])+diag)*e.shapefn(nudx,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                                                try:
                                                    self.matrix[(row,col)]+=val
                                                except KeyError:
                                                    self.matrix[(row,col)]=val
                                                
                                                    
    # Values are y offsets of the top and bottom boundaries, which are
    # assumed fixed to zero offset in the x direction.  If top is
    # None, then the top boundary is not fixed.
    def setbcs(self,top,bottom):
        self.topbc = top
        self.bottombc = bottom


    def set_freedofs(self):
        mtxsize = sum( [d.size for d in self.doflist] )
        self.freedofs = [-1]*mtxsize
        fixed_rhs = []
        for node in self.nodelist:
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
        # So now we have the list, compress it.
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
            for n in self.nodelist:
                for d in n.alldofs():
                    for k in range(d.size):
                        ref = self.freedofs[d.index+k]
                        if ref >= 0:
                            d.set(k,nr[ref,0])
                        else:
                            d.set(k,br[-(ref+1),0])
        else:
            print "Error in solving, return code is %d." % rr

    # Assumes a "Displacement" field and a semi-active "Plastic
    # Strain" field are present in the mesh.  First solves the elastic
    # problem, identifying the nodes for which plasticity is
    # appropriate, if any, then adds the appropriate extra degrees of
    # freedom to them, then runs a Newton-type solution iteration
    # until convergence.  The resulting increments of plastic strain
    # are added to the plastic strain DOFs in the mesh.
    def solve_plastic(self,cijkl,yld,epsilon=1.0e-10):
        self.solve_elastic(cijkl)

        # See where to yield -- criterion varies, but for today, we're
        # computing the interpolant of the yield function, and then
        # enforcing th e yield condition on any node whose amplitude
        # is positive.
        plastics = sets.Set()
        for e in self.ellist:
            nn = len(e.nodes)

            massmtx = smallmatrix.SmallMatrix(nn,nn)
            yldrhs = smallmatrix.SmallMatrix(nn,1)

            massmtx.clear()
            yldrhs.clear()
            
            # print "\n\nElement: ", e
            ndset = [(ii,e.nodes[ii]) for ii in range(nn)]
            for (ndx,nd) in ndset:

                yintegral = 0.0

                for g in e.gausspts():
                    gstrain = [[0,0,0],[0,0,0],[0,0,0]]
                    pstrain = [[0,0,0],[0,0,0],[0,0,0]]

                    # Find strain and pstrain at this gausspoint.
                    for (mdx,md) in ndset:
                        disp = md.dof("Displacement")
                        ux = disp.value[0]
                        uy = disp.value[1]
                        dstrain = [[
                            ux*e.dshapefn(mdx,0,g.xi,g.zeta),
                            0.5*(ux*e.dshapefn(mdx,1,g.xi,g.zeta) +
                                 uy*e.dshapefn(mdx,0,g.xi,g.zeta)),
                            0.0],
                                   [
                            0.5*(ux*e.dshapefn(mdx,1,g.xi,g.zeta) +
                                 uy*e.dshapefn(mdx,0,g.xi,g.zeta)),
                            uy*e.dshapefn(mdx,1,g.xi,g.zeta),
                            0.0],
                                   [0.0,0.0,0.0]]

                        dsfstrain = [0,0,0,0,0,0]
                        sfst = md.auxel(e,"Plastic Strain")
                        if sfst is not None:
                            sfval = e.shapefn(mdx,g.xi,g.zeta)
                            dsfstrain = [ x*sfval for x in sfst.value ]


                        gstrain = [ [ gstrain[i][j]+dstrain[i][j]
                                      for j in range(3) ]
                                    for i in range(3) ]

                        
                        pstrain = [ [ pstrain[i][j]+dsfstrain[voigt[i][j]]
                                      for j in range(3) ]
                                    for i in range(3)]

                        # Accumulate mass matrix as we go.
                        massmtx[ndx,mdx]+=e.shapefn(ndx,g.xi,g.zeta)*e.shapefn(mdx,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)
                        
                    # Now we have both strains at this gauss point --
                    # compute the stress here, and evaluate the yield
                    # function.
                    stress = [ [ sum( [ sum( [
                        cijkl[i][j][k][l]*(gstrain[k][l]-pstrain[k][l])
                        for l in range(3) ] )
                                        for k in range(3) ] ) 
                                 for j in range(3) ]
                               for i in range(3) ]

                    dy = yld.yeeld(stress)
                    yintegral += dy*e.shapefn(ndx,g.xi,g.zeta)*g.weight*e.jacobian(g.xi,g.zeta)


                # Now we have the y integral for node n.
                yldrhs[ndx,0]=yintegral
                
            # print "RHS: ", [ yldrhs[jj,0] for jj in range(yldrhs.rows()) ]
            # Finished the n-node loop, now we have the mass matrix
            # and the yield right-hand-side fully assembled.  Solve!
            rr = massmtx.solve(yldrhs)
            # print "Solution: ", [ yldrhs[jj,0] for
            #                       jj in range(yldrhs.rows()) ]
            if rr==0:
                for (ndx,nd) in ndset:
                    if yldrhs[ndx,0]>0:
                        plastics.add( (e,nd) )
            else:
                raise "Disaster!  Elemental mass matrix is singular!"


        # print
        # for (e,n) in plastics:
        #     print "Element %d, node %d." % (e.index, n.index)
        # Add plastic DOFs to node/element combos which require it.
        if len(plastics)==0:
            # print "All elastic, no yielding today."
            return

        mtxsize = sum( [d.size for d in self.doflist] )
        count = 0
        for (e,n) in plastics:
            newdof = Dof("Plastic Strain Increment",
                         mtxsize+count*6,6)
            n.addeldof(e,newdof)
            self.doflist.append(newdof)
            count += 1
            
        # And again for the Lagrange multiplier field, of size 1.
        mtxsize = sum( [d.size for d in self.doflist] )
        count = 0
        for (e,n) in plastics:
            newdof = Dof("Plastic Consistency Parameter",
                         mtxsize+count,1)
            n.addeldof(e,newdof)
            self.doflist.append(newdof)
            count += 1

        while 1:
            self.clear()

            # Build the self.freedof list for these DOFs.  This is so
            # that we can break out, if required, *before* rebuilding
            # the matrices, which is the expensive thing.
            (free_count, fixed_count, fixed_rhs) = self.set_freedofs()

            phidict = self.phi(cijkl,yld)
            phi = SmallMatrix(free_count,1)
            for n in self.nodelist:
                for d in n.alldofs():
                    for k in range(d.size):
                        ref = self.freedofs[d.index+k]
                        if ref >= 0:
                            phi[ref,0]=-phidict[d.index+k]
            
            mag = sum( [ phi[i,0]**2 for i in range(phi.rows()) ] )
            # print "Magnitude of phi: ", mag
            if mag < epsilon:
                break

            self.elastic(cijkl)
            # print "Built elastic part, now building plastic part."
            
            self.plastic(cijkl,yld)
            # print "Built the plastic part."

            # This rebuilds the freedof list, which is slightly
            # wasteful -- proper thing is to cache this data.
            (a,c,br,sr) = self.linearsystem()
            
            rr = a.solve(phi) # Writes solution into phi, mangles a.

            if rr==0:
                for n in self.nodelist:
                    for d in n.alldofs():
                        for k in range(d.size):
                            ref = self.freedofs[d.index+k]
                            if ref >= 0:
                                d.add(k,phi[ref,0])
                            else:
                                d.set(k,br[-(ref+1),0])
                mag = sum( [ phi[i,0]**2 for i in range(phi.rows()) ] )
                # print "Magnitude of increment: ", mag
            else:
                raise "Error in matrix solution, return code is %d." % rr


        # print "Converged."
        for n in self.nodelist:
            for e in n.elements:
                ep = n.auxel(e,"Plastic Strain")
                epi = n.eldof(e,"Plastic Strain Increment")
                if epi is not None:
                    for k in range(6): # Better be six...
                        ep.add(k,epi.get(k))

        # Now remove all the auxiliary DOFs.  Since they were
        # appended, we can do this by a process called "cheating", in
        # which we just delete them.  This doesn't mess up anyone
        # else's indexing, because they were appended within the scope
        # of this function.
        for n in self.nodelist:
            for e in n.elements:
                epi = n.eldof(e,"Plastic Strain Increment")
                if epi is not None:
                    n.eldofs[e].remove(epi)
                    self.doflist.remove(epi)
                lmbda = n.eldof(e,"Plastic Consistency Parameter")
                if lmbda is not None:
                    n.eldofs[e].remove(lmbda)
                    self.doflist.remove(lmbda)


    def draw(self):
        import visual
        frame = visual.frame()
        outline = visual.curve(frame=frame,
                               pos=[(0.0,0.0,0.0),(1.0,0.0,0.0),
                                    (1.0,1.0,0.0),(0.0,1.0,0.0),
                                    (0.0,0.0,0.0)],color=visual.color.red)
        for e in self.ellist:
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


    def dump_matrix(self,outfile):
        mtxsize = sum( [d.size for d in self.doflist] )
        for i in range(mtxsize):
            for j in range(mtxsize):
                try:
                    v = self.matrix[i,j]
                except KeyError:
                    pass
                else:
                    print >> outfile,i,j,v
                    
    # Routine for measuring how much force is exerted in the y
    # direction on the bottom boundary.  The bottom is chosen because,
    # in this rig, it always has a fixed boundary condition.
    def measure_force(self,cijkl):
        # Use three guass-points per segment in the usual way.
        mpt = math.sqrt(3.0/5.0)
        pts = [-mpt, 0.0, mpt]
        wts = [5.0/9.0, 8.0/9.0, 5.0/9.0]
        elcount = len(self.bottomnodes)-1
        force = 0.0
        for e in self.ellist[:elcount]: # Bottom row of elements.
            for (pt,wt) in zip(pts,wts):
                strain = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                for (ndx,nd) in [(ii,e.nodes[ii]) for ii in
                                 range(len(e.nodes))]:
                    disp = nd.dof("Displacement")
                    ux = disp.value[0]
                    uy = disp.value[1]
                    dstrain = [[
                        ux*e.dshapefn(ndx,0,pt,-1.0),
                        0.5*(ux*e.dshapefn(ndx,1,pt,-1.0) +
                             uy*e.dshapefn(ndx,0,pt,-1.0)),
                        0.0],
                               [
                        0.5*(ux*e.dshapefn(ndx,1,pt,-1.0) +
                             uy*e.dshapefn(ndx,0,pt,-1.0)),
                        uy*e.dshapefn(ndx,1,pt,-1.0),
                        0.0],
                               [0.0,0.0,0.0]]
                    dsfstrain = [0,0,0,0,0,0]
                    sfst = nd.auxel(e,"Plastic Strain")
                    if sfst is not None:
                        sfval = e.shapefn(ndx,pt,-1.0)
                        dsfstrain = [ x*sfval for x in sfst.value ]
                        
                    strain = [ [ strain[i][j]+
                                 dstrain[i][j]-
                                 dsfstrain[voigt[i][j]]
                                 for j in range(3) ]
                               for i in range(3) ]
                # Now we have the complete strain at this eval point.
                # Get the stress.
                stress = [ [ sum( [ sum( [
                    cijkl[i][j][k][l]*strain[k][l] for l in range(3) ] )
                                    for k in range(3) ] ) 
                             for j in range(3) ]
                           for i in range(3) ]

                # Relevant force component is the y component of the
                # tensor contracted with a unit vector pointing in the
                # y direction -- this is just the (1,1) component of
                # the tensor.
                force_inc = stress[1][1]
                # print force_inc
                # Last factor is the Jacobian. Since lower boundary is
                # fixed, it's just the ratio of the lengths of the
                # reference interval (2) to the length of the real
                # interval, which is 1/elcount.
                force += force_inc*wt*((1.0/elcount)/2.0)
        return force


    def dump_data(self,cijkl,yld,dxpts=5,dypts=5):
        dx = 2.0/float(dxpts)
        dy = 2.0/float(dypts)
        startx = -1.0+dx/2.0
        starty = -1.0+dy/2.0
        xevalpts = [ startx + i*dx for i in range(dxpts) ]
        yevalpts = [ starty + i*dy for i in range(dypts) ]

        ptset = [ (x,y) for x in xevalpts for y in yevalpts ]

        for e in self.ellist:
            ndset = [(ii,e.nodes[ii]) for ii in range(len(e.nodes))]
            for p in ptset:
                xi = p[0]
                zeta = p[1]
            
                strain = [[0,0,0],[0,0,0],[0,0,0]]
                pstrain = [[0,0,0],[0,0,0],[0,0,0]]
                for (ndx,nd) in ndset:
                    disp = nd.dof("Displacement")
                    ux = disp.value[0]
                    uy = disp.value[1]
                    dstrain = [[
                        ux*e.dshapefn(ndx,0,xi,zeta),
                        0.5*(ux*e.dshapefn(ndx,1,xi,zeta) +
                             uy*e.dshapefn(ndx,0,xi,zeta)),
                        0.0],
                               [
                        0.5*(ux*e.dshapefn(ndx,1,xi,zeta) +
                             uy*e.dshapefn(ndx,0,xi,zeta)),
                        uy*e.dshapefn(ndx,1,xi,zeta),
                        0.0],
                               [0.0,0.0,0.0]]
                    
                    dptstrian = [[0,0,0],[0,0,0],[0,0,0]]
                    sfst = nd.auxel(e,"Plastic Strain")
                    if sfst is not None:
                        sfval = e.shapefn(ndx,xi,zeta)
                        dsfstrain = [ x*sfval for x in sfst.value ]
                        
                        dpstrain = [ [ dsfstrain[voigt[i][j]]
                                       for j in range(3) ]
                                     for i in range(3) ]
                        
                        
                    pstrain = [ [ pstrain[i][j]+dpstrain[i][j]
                                  for j in range(3) ]
                                for i in range(3) ]
                    strain = [ [ strain[i][j]+
                                 dstrain[i][j]
                                 for j in range(3) ]
                               for i in range(3) ]
                # Now we have the strain at this eval point -- get stress.
                stress = [ [ sum( [ sum( [
                    cijkl[i][j][k][l]*(strain[k][l]-pstrain[k][l])
                    for l in range(3) ] )
                                    for k in range(3) ] ) 
                             for j in range(3) ]
                           for i in range(3) ]
                val = math.sqrt((3.0/2.0)*deviator(stress))
                # val = sum( [ stress[i][i] for i in range(3) ] )
                pt = e.frommaster(xi,zeta)
                print 
                print pt.x, pt.y, "Stress: ", stress
                print pt.x, pt.y, "Strain: ", strain
                print pt.x, pt.y, "Plastic: ", pstrain
                
    

    def draw_stress(self,cijkl,dxpts=5,dypts=5):
        import visual
        frame = visual.frame()
        outline = visual.curve(frame=frame,
                               pos=[(0.0,0.0,0.0),(1.0,0.0,0.0),
                                    (1.0,1.0,0.0),(0.0,1.0,0.0),
                                    (0.0,0.0,0.0)],color=visual.color.red)
        
        dx = 2.0/float(dxpts)
        dy = 2.0/float(dypts)
        startx = -1.0+dx/2.0
        starty = -1.0+dy/2.0
        xevalpts = [ startx + i*dx for i in range(dxpts) ]
        yevalpts = [ starty + i*dy for i in range(dypts) ]
        
        data = {}
        for e in self.ellist:
            ndset = [(ii,e.nodes[ii]) for ii in range(len(e.nodes))]
            for xi in xevalpts:
                for zeta in yevalpts:
                    strain = [[0,0,0],[0,0,0],[0,0,0]]
                    for (ndx,nd) in ndset:
                        disp = nd.dof("Displacement")
                        ux = disp.value[0]
                        uy = disp.value[1]
                        dstrain = [[
                            ux*e.dshapefn(ndx,0,xi,zeta),
                            0.5*(ux*e.dshapefn(ndx,1,xi,zeta) +
                                 uy*e.dshapefn(ndx,0,xi,zeta)),
                            0.0],
                                   [
                            0.5*(ux*e.dshapefn(ndx,1,xi,zeta) +
                                 uy*e.dshapefn(ndx,0,xi,zeta)),
                            uy*e.dshapefn(ndx,1,xi,zeta),
                            0.0],
                                   [0.0,0.0,0.0]]
                        dsfstrain = [0,0,0,0,0,0]
                        sfst = nd.auxel(e,"Plastic Strain")
                        if sfst is not None:
                            sfval = e.shapefn(ndx,xi,zeta)
                            dsfstrain = [ x*sfval for x in sfst.value ]
                            
                        strain = [ [ strain[i][j]+
                                     dstrain[i][j]-
                                     dsfstrain[voigt[i][j]]
                                     for j in range(3) ]
                                   for i in range(3) ]
                    # Now we have the strain at this eval point -- get stress.
                    stress = [ [ sum( [ sum( [
                        cijkl[i][j][k][l]*strain[k][l] for l in range(3) ] )
                                        for k in range(3) ] ) 
                                 for j in range(3) ]
                               for i in range(3) ]
                    val = math.sqrt((3.0/2.0)*deviator(stress))
                    # val = sum( [ stress[i][i] for i in range(3) ] )
                    pt = e.frommaster(xi,zeta)
                    data[(pt.x,pt.y)]=val

        # Go through the data and check out the scale.
        vmax = None
        vmin = None
        vsum = 0.0
        count = 0
        for v in data.values():
            vsum += v
            count += 1
            if vmax is None or v > vmax:
                vmax = v
            if vmin is None or v < vmin:
                vmin = v
        print "Min, max, avg: ", vmin, vmax, vsum/float(count)

        # Actually draw stuff.  Assumes undistorted elements are
        # square, which may not be a particularly robust assumption.

        # realdx = 1.0/(math.sqrt(len(self.ellist))*dpts)
        xels = len(self.bottomnodes)-1
        yels = len(self.ellist)/xels
        
        realdx = 1.0/float(xels*dxpts)
        realdy = 1.0/float(yels*dypts)

        for (p,v) in data.items():
            bdy = [ (p[0]-0.5*realdx,p[1]-0.5*realdy),
                    (p[0]+0.5*realdx,p[1]-0.5*realdy),
                    (p[0]+0.5*realdx,p[1]+0.5*realdy),
                    (p[0]-0.5*realdx,p[1]+0.5*realdy)]
            col = (v-vmin)/(vmax-vmin)
            visual.convex(frame=frame,pos=bdy,color=(col,col,col))
        return frame    
            
                    

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




def go(size):
    global m 
    y = Yeeld(0.1)
    c = Cijkl(0.5,0.25)
    m = Mesh(xelements=size,yelements=size)
    m.addfield("Displacement",2)
    m.addauxelfield("Plastic Strain",6,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for x in range(36):
        bcval = x*0.01
        # bcval = 0.180+x*0.002
        m.setbcs(bcval,0.0)
        m.solve_plastic(c,y)
        # m.dump_data(c,y)
        # for e in m.ellist:
        #     for n in e.nodes:
        #         ep = n.auxel(e,"Plastic Strain")
        #         print e.index, n.index, ep.value
        f = m.measure_force(c)
        print bcval,f
        sys.stdout.flush()

# For "default" isotropic elasticity and a yield stress of 0.1, and a
# five-element mesh, elements begin to yield when the top boundary
# displacement reaches 0.14, and by the time it gets to 0.20, the
# whole system will yield.  At y=0.135, only the four corner elements
# will yield -- this is a good place to start, probably.
if __name__=="__main__":
    size=5 # Default...
    try:
        opts, nonopts = getopt.getopt(sys.argv[1:],"s:")
    except getopt.GetOptError:
        print "Wrong/missing options, exiting."
        sys.exit(2)
    for o,a in opts:
        if o=="-s":
            size = int(a)
    go(size)

    
