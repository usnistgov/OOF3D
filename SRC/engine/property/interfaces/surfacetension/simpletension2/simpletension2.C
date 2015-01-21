// -*- C++ -*-
// $RCSfile: simpletension2.C,v $
// $Revision: 1.3.10.2 $
// $Author: fyc $
// $Date: 2014/07/29 21:22:32 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include "common/doublevec.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/linearizedsystem.h"
#include "engine/material.h"
#include "engine/node.h"
#include "engine/smallsystem.h"
#include "engine/sparsemat.h"
#include "simpletension2.h"

SimpleTension2::SimpleTension2(PyObject *reg, const std::string &nm,
			       double k_left, double T_c_left,
			       double k_right, double T_c_right)
  : InterfaceProperty(nm,reg),
    _k_left(k_left), _T_c_left(T_c_left),
    _k_right(k_right), _T_c_right(T_c_right)
{
}

int SimpleTension2::integration_order(const CSubProblem*, const Element *el)
  const
{
  return 0;
}

// TODO 3.1: TDEP This needs to be checked to make sure it still does the
// right thing given the time-dependency changes made to the
// LinearSystem object.  Also, these properties really ought to work
// through the flux or equation contribution mechanism, so that the
// equation object can make the contribution to the linear system.

// TODO 3.1: The body of end_element has been commented out, because it
// required a LinearizedSystem argument, which end_element doesn't
// have anymore (and can't have, if it's to be used when computing
// Outputs).  Surface tension should be computed in the proper
// context, which is *not* in end_element.

void SimpleTension2::end_element(const CSubProblem* pSubp, const Element* pElem)
{
//   double k_T_c_left=_k_left*_T_c_left;
//   double k_T_c_right=_k_right*_T_c_right;

//   SparseMat mtx = ls->getK();
//   DoubleVec &rhs = ls->get_body_rhs();
//   const std::vector<Node*>& nodelist=pElem->get_nodelist();
//   int nnodes=pElem->nnodes();
//   FuncNode* pFuncNode1=(FuncNode*)nodelist[0];
//   FuncNode* pFuncNode2=(FuncNode*)nodelist[nnodes-1];
//   Equation& ForceBalance=*Equation::getEquation("Force_Balance");
//   //Field& Displacement=*Field::getField("Displacement");
//   Field& Temperature=*Field::getField("Temperature");

// //   if(!(pFuncNode1->hasEquation(ForceBalance)
// //        && pFuncNode1->hasField(Displacement)
// //        && pFuncNode2->hasEquation(ForceBalance)
// //        && pFuncNode2->hasField(Displacement)))
// //     {
// //       //TODO 3.1: This check might not be necessary
// //       return;
// //     }

//   //Get the unit vector pointing from node2 to node1
//   double ux=pFuncNode1->position().x-pFuncNode2->position().x;
//   double uy=pFuncNode1->position().y-pFuncNode2->position().y;
//   double mag=sqrt(ux*ux+uy*uy);
//   ux/=mag;
//   uy/=mag;

//   //First set the rhs of the row for node1
//   //x-component of the nodal equation at node1
//   int rowno1=pSubp->map_forward_index(ForceBalance,*pFuncNode1,0);
//   //y-component of the nodal equation at node1
//   int rowno2=pSubp->map_forward_index(ForceBalance,*pFuncNode1,1);
//   rhs[rowno1]-=k_T_c_left*ux;
//   rhs[rowno2]-=k_T_c_left*uy;
//   int colno=Temperature(pFuncNode1,0)->dofindex();
//   mtx.insert(rowno1,colno, -_k_left*ux);
//   mtx.insert(rowno2,colno, -_k_left*uy);

//   //Set the rhs of the row for node2
//   //x-component of the nodal equation at node2
//   rowno1=pSubp->map_forward_index(ForceBalance,*pFuncNode2,0);
//   //y-component of the nodal equation at node2
//   rowno2=pSubp->map_forward_index(ForceBalance,*pFuncNode2,1);
//   rhs[rowno1]+=k_T_c_left*ux;
//   rhs[rowno2]+=k_T_c_left*uy;
//   colno=Temperature(pFuncNode2,0)->dofindex();
//   mtx.insert(rowno1,colno, _k_left*ux);
//   mtx.insert(rowno2,colno, _k_left*uy);

//   //
//   // Repeat above procedure for the nodes on the 'other' side of the InterfaceElement.
//   // These two sets of nodes (nodelist, nodelist2) may be identical.
//   //
//   InterfaceElement* pInterfaceElement=(InterfaceElement*)pElem;//Sure that this is an InterfaceElement object
//   const std::vector<Node*>& nodelist2=pInterfaceElement->get_nodelist2();
//   pFuncNode1=(FuncNode*)nodelist2[0];
//   pFuncNode2=(FuncNode*)nodelist2[nnodes-1];
// //   Equation& ForceBalance=*Equation::getEquation("Force_Balance");
// //   Field& Temperature=*Field::getField("Temperature");

//   //Get the unit vector pointing from node2 to node1
// //   double ux=pFuncNode1->position().x-pFuncNode2->position().x;
// //   double uy=pFuncNode1->position().y-pFuncNode2->position().y;
// //   double mag=sqrt(ux*ux+uy*uy);
// //   ux/=mag;
// //   uy/=mag;

//   //First set the rhs of the row for node1
//   //x-component of the nodal equation at node1
//   rowno1=pSubp->map_forward_index(ForceBalance,*pFuncNode1,0);
//   //y-component of the nodal equation at node1
//   rowno2=pSubp->map_forward_index(ForceBalance,*pFuncNode1,1);
//   rhs[rowno1]-=k_T_c_right*ux;
//   rhs[rowno2]-=k_T_c_right*uy;
//   colno=Temperature(pFuncNode1,0)->dofindex();
//   mtx.insert(rowno1,colno, -_k_right*ux);
//   mtx.insert(rowno2,colno, -_k_right*uy);

//   //Set the rhs of the row for node2
//   //x-component of the nodal equation at node2
//   rowno1=pSubp->map_forward_index(ForceBalance,*pFuncNode2,0);
//   //y-component of the nodal equation at node2
//   rowno2=pSubp->map_forward_index(ForceBalance,*pFuncNode2,1);
//   rhs[rowno1]+=k_T_c_right*ux;
//   rhs[rowno2]+=k_T_c_right*uy;
//   colno=Temperature(pFuncNode2,0)->dofindex();
//   mtx.insert(rowno1,colno, +_k_right*ux);
//   mtx.insert(rowno2,colno, +_k_right*uy);

//   return;

// #if 0
//   //Old stuff
//   //
//   //Implement continuity and jump conditions
//   //
//   std::vector<Field*> &all_fields=Field::all();//ALL fields
//   //std::vector<CompoundField*>* pFieldlist=pSubp->all_compound_fields();
//   std::vector<Equation*>* pEqnlist=pSubp->all_equations();//Equations defined ON THE SUBPROBLEM
//   InterfaceElement* pInterfaceElement=(InterfaceElement*)pElem;//Sure that this is an InterfaceElement object
//   const std::vector<Node*>& nodelist2=pInterfaceElement->get_nodelist2();
//   if(_interfaceproperty0==1)//Only one interface property in the material can do this
//     {
//       //The nodal equations for the continuity conditions should start at an offset
//       //determined by the fields defined in interface properties.
//       //
//       int offset=0;
//       for(std::map<const Field*,int>::iterator it=_interfacefieldsmap.begin();
// 	  it!=_interfacefieldsmap.end();it++)
// 	{
// 	  const Field& fld=*(it->first);
// 	  offset+=fld.ndof();
// 	}
//       for(int i=0;i<nnodes;i++)
// 	{
// 	  FuncNode* pFuncNode1=(FuncNode*)nodelist[i];//main edgement nodes
// 	  FuncNode* pFuncNode2=(FuncNode*)nodelist2[i];//'partner' nodes
// 	  if(pFuncNode1==pFuncNode2)//skeleton node wasn't split
// 	    continue;
// 	  //Add the rows of the matrix corresponding to the nodal
// 	  //equations at the two nodes, so that the resulting solution
// 	  //is not biased toward one side of the interface.
// 	  for(std::vector<Equation*>::iterator it=pEqnlist->begin();
// 	      it!=pEqnlist->end();it++)
// 	    {
// //  	      if((*it)->classname()=="PlaneFluxEquation")
// //  		continue;
// 	      int ndofs=(*it)->ndof();
// 	      for(int j=0;j<ndofs;j++)
// 		{
// 		  int rowno1=pSubp->map_forward_index(*(*it),*pFuncNode1,j);
// 		  int rowno2=pSubp->map_forward_index(*(*it),*pFuncNode2,j);
// 		  double tmp1,tmp2;
// 		  for(int k=0;k<mtx.ncols();k++)
// 		    {
// 		      if(mtx.is_nonempty_col(k))
// 			{
// 			  tmp1=mtx(rowno1,k);
// 			  tmp2=mtx(rowno2,k);
// 			  mtx(rowno1,k)+=tmp2;
// 			  mtx(rowno2,k)+=tmp1;
// 			}
// 		    }
// 		  tmp1=rhs[rowno1];
// 		  tmp2=rhs[rowno2];
// 		  rhs[rowno1]+=tmp2;
// 		  rhs[rowno2]+=tmp1;
// 		}
// 	    }
// 	  //Implement continuity for fields (dofs) not in _interfacefieldsmap
// 	  int ccount=offset;
// 	  for(std::vector<Field*>::iterator it1=all_fields.begin();
// 	      it1!=all_fields.end();it1++)
// 	    {
// 	      Field* pField1=*it1;
// 	      int nfieldcomps=pField1->ndof();
// 	      if(pSubp->is_active_field(*pField1))
// 		{
// 		  for(int fieldcomp=0;fieldcomp<nfieldcomps;fieldcomp++)
// 		    {
// 		      bool found=false;
// 		      for(std::map<const Field*,int>::iterator it2=_interfacefieldsmap.begin();
// 			  it2!=_interfacefieldsmap.end();it2++)
// 			{
// 			  const Field* pField2=it2->first;
// 			  if(pField1==pField2)
// 			    {
// 			      found=true;
// 			      break;
// 			    }
// 			}
// 		      if(!found)
// 			{
// 			  Equation* pEqn=0;
// 			  int eqncomp=0;
// 			  int ccount2=0;
// 			  bool found2=false;
// 			  for(std::vector<Equation*>::iterator it3=pEqnlist->begin();
// 			      it3!=pEqnlist->end();it3++)
// 			    {
// // 			      if((*it3)->classname()=="PlaneFluxEquation")
// // 				continue;
// 			      int ndofs=(*it3)->ndof();
// 			      for(int j=0;j<ndofs;j++)
// 				{
// 				  if(ccount==ccount2)
// 				    {
// 				      pEqn=*it3;
// 				      eqncomp=j;
// 				      found2=true;
// 				      break;
// 				    }
// 				  ccount2++;
// 				}
// 			      if(found2)
// 				{
// 				  break;
// 				}
// 			    }
// 			  if(!found2)
// 			    {
// 			      throw ErrProgrammingError("TangIna!",
// 							__FILE__, __LINE__);
// 			    }

// 			  int rowno=pSubp->map_forward_index(*pEqn,*pFuncNode2,eqncomp);
// 			  for(int k=0;k<mtx.ncols();k++)
// 			    {
// 			      if(mtx.is_nonempty_col(k))
// 				{
// 				  mtx(rowno,k)=0;
// 				}
// 			    }

// 			  DegreeOfFreedom* pDOF1=(*pField1)(pFuncNode1,fieldcomp);
// 			  DegreeOfFreedom* pDOF2=(*pField1)(pFuncNode2,fieldcomp);
// 			  mtx(rowno,pDOF1->dofindex())=1;
// 			  mtx(rowno,pDOF2->dofindex())=-1;
// 			  rhs[rowno]=0;
// 			  ccount++;
// 			}
// 		    }
// 		}
// 	    }
// 	}
//     }

//   //Let this property do its thing with the continuity (or jump) of its
//   //own field
//   int offset=0;
//   for(std::map<const Field*,int>::iterator it=_interfacefieldsmap.begin();
//       it!=_interfacefieldsmap.end();it++)
//     {
//       const Field* pField=it->first;
//       if(pField==fields_required()[0])
// 	{
// 	  break;
// 	}
//       offset+=pField->ndof();
//     }
//   int nfieldcomps=fields_required()[0]->ndof();
//   for(int i=0;i<nnodes;i++)
//     {
//       FuncNode* pFuncNode1=(FuncNode*)nodelist[i];//main edgement nodes
//       FuncNode* pFuncNode2=(FuncNode*)nodelist2[i];//'partner' nodes
//       if(pFuncNode1==pFuncNode2)//skeleton node wasn't split
// 	continue;

//       for(int fieldcomp=0;fieldcomp<nfieldcomps;fieldcomp++)
// 	{
// 	  int ccount=0;
// 	  bool found=false;
// 	  for(std::vector<Equation*>::iterator it=pEqnlist->begin();
// 	      it!=pEqnlist->end();it++)
// 	    {
// 	      int neqncomps=(*it)->ndof();
// 	      for(int eqncomp=0;eqncomp<neqncomps;eqncomp++)
// 		{
// 		  if(ccount==offset+fieldcomp)
// 		    {
// 		      //Got an available nodal equation to replace
// 		      int rowno=pSubp->map_forward_index(*(*it),*pFuncNode2,eqncomp);

// 		      //Remember to zero the row first
// 		      for(int k=0;k<mtx.ncols();k++)
// 			{
// 			  //This check is important for subproblems
// 			  if(mtx.is_nonempty_col(k))
// 			    {
// 			      mtx(rowno,k)=0;
// 			    }
// 			}

// 		      DegreeOfFreedom* pDOF1=(*fields_required()[0])(pFuncNode1,fieldcomp);
// 		      DegreeOfFreedom* pDOF2=(*fields_required()[0])(pFuncNode2,fieldcomp);
// 		      //Write the continuity (or jump) condition
// 		      mtx(rowno,pDOF1->dofindex())=1;
// 		      mtx(rowno,pDOF2->dofindex())=-1;
// 		      rhs[rowno]=0;
// 		      found=true;
// 		      break;
// 		    }
// 		  ccount++;
// 		}
// 	      if(found)
// 		{
// 		  break;
// 		}
// 	    }
// 	}
//     }

//   delete pEqnlist;
// #endif
}

void SimpleTension2::cross_reference(Material* pMat)
{
  return;

#if 0
  //Find those interface properties and get the list of fields
  //that they use.
  _interfacefieldsmap.clear();
  _interfaceproperty0=0;
  for(int i=0;i<pMat->nProperties();i++)
    {
      Property* pProp=pMat->getProperty(i);
      InterfaceProperty* pIProp=dynamic_cast<InterfaceProperty*>(pProp);
      if(pIProp!=0)//Interface property?
	{
	  if(i==0 && pIProp->classname()==classname())
	    {
	      _interfaceproperty0=1;
	    }
	  _interfacefieldsmap[pIProp->fields_required()[0]]=1;
	}
    }
#endif
}

void SimpleTension2::post_process(CSubProblem* pSubp, const Element *pElem) const
{
}

void SimpleTension2::flux_matrix(const FEMesh*, const Element*,
				 const ElementFuncNodeIterator&,
				 const Flux*, const MasterPosition&,
				 double time, SmallSystem *fluxdata)
  const
{
  //Do nothing
}

void SimpleTension2::flux_offset(const FEMesh*, const Element*,
				 const Flux*,
				 const MasterPosition&,
				 double time,
				 SmallSystem *fluxdata)
    const
{
  //Do nothing
}

void SimpleTension2::output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*)
    const
{
}
