// -*- C++ -*-
// $RCSfile: oofCellLocator.C,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2013/04/26 19:12:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/oofCellLocator.h"

#include <vtkObjectFactory.h>
#include <vtkDataSet.h>
#include <vtkIdList.h>

typedef vtkIdList *vtkIdListPtr;
#define VTK_CELL_OUTSIDE 0
#define VTK_CELL_INSIDE 1

vtkCxxRevisionMacro(oofCellLocator, "$Revision: 1.1.2.3 $");

vtkStandardNewMacro(oofCellLocator);

void oofCellLocator::BuildLocatorInternal()
{
  double *bounds, length, cellBounds[6], *boundsPtr;
  vtkIdType numCells;
  int ndivs, product;
  int i, j, k, ijkMin[3], ijkMax[3];
  vtkIdType cellId, idx;
  int parentOffset;
  vtkIdList *octant;
  int numCellsPerBucket = this->NumberOfCellsPerNode;
  int prod, numOctants;
  double hTol[3];
  
  vtkDebugMacro( << "Subdividing octree..." );
  
  if ( !this->DataSet || (numCells = this->DataSet->GetNumberOfCells()) < 1 )
    {
    vtkErrorMacro( << "No cells to subdivide");
    return;
    }

  //  Make sure the appropriate data is available
  //
  if ( this->Tree )
    {
    this->FreeSearchStructure();
    }
  if ( this->CellHasBeenVisited )
    {
    delete [] this->CellHasBeenVisited;
    this->CellHasBeenVisited = NULL;
    }
  this->FreeCellBounds();
  
  //  Size the root cell.  Initialize cell data structure, compute
  //  level and divisions.
  //
  bounds = this->DataSet->GetBounds();
  length = this->DataSet->GetLength();
  for (i=0; i<3; i++)
    {
    this->Bounds[2*i] = bounds[2*i];
    this->Bounds[2*i+1] = bounds[2*i+1];
    // Bump out the bounds a little to prevent round off error from
    // making it seem that points on the edge are not in within the
    // bounding box.   
    this->Bounds[2*i] -= length/100.0;
    this->Bounds[2*i+1] += length/100.0;
    // The following block is the original from vtkCellLocator.cxx.
    // if ( (this->Bounds[2*i+1] - this->Bounds[2*i]) <= (length/1000.0) )
      // {
      // // bump out the bounds a little of if min==max
      // this->Bounds[2*i] -= length/100.0;
      // this->Bounds[2*i+1] += length/100.0;
      // }
    }
  
  if ( this->Automatic ) 
    {
    this->Level = static_cast<int>(
      ceil(log(static_cast<double>(numCells)/numCellsPerBucket) /
           (log(static_cast<double>(8.0)))));
    } 
  this->Level =(this->Level > this->MaxLevel ? this->MaxLevel : this->Level);
  
  // compute number of octants and number of divisions
  for (ndivs=1,prod=1,numOctants=1,i=0; i<this->Level; i++) 
    {
    ndivs *= 2;
    prod *= 8;
    numOctants += prod;
    }
  this->NumberOfDivisions = ndivs;
  this->NumberOfOctants = numOctants;

  this->Tree = new vtkIdListPtr[numOctants];
  memset (this->Tree, 0, numOctants*sizeof(vtkIdListPtr));
  
  this->CellHasBeenVisited = new unsigned char [ numCells ];
  this->ClearCellHasBeenVisited();
  this->QueryNumber = 0;

  if (this->CacheCellBounds)
    {
    this->StoreCellBounds();
    }
  
  //  Compute width of leaf octant in three directions
  //
  for (i=0; i<3; i++)
    {
    this->H[i] = (this->Bounds[2*i+1] - this->Bounds[2*i]) / ndivs;
    hTol[i] = this->H[i]/100.0;
    }

  //  Insert each cell into the appropriate octant.  Make sure cell
  //  falls within octant.
  //
  parentOffset = numOctants - (ndivs * ndivs * ndivs);
  product = ndivs * ndivs;
  boundsPtr = cellBounds;
  for (cellId=0; cellId<numCells; cellId++) 
    {
    if (this->CellBounds)
      {
      boundsPtr = this->CellBounds[cellId];
      }
    else
      {
      this->DataSet->GetCellBounds(cellId, cellBounds);
      }
    
    // find min/max locations of bounding box
    for (i=0; i<3; i++)
      {
      ijkMin[i] = static_cast<int>(
        (boundsPtr[2*i] - this->Bounds[2*i] - hTol[i])/ this->H[i]);
      ijkMax[i] = static_cast<int>(
        (boundsPtr[2*i+1] - this->Bounds[2*i] + hTol[i]) / this->H[i]);
      
      if (ijkMin[i] < 0)
        {
        ijkMin[i] = 0;
        }
      if (ijkMax[i] >= ndivs)
        {
        ijkMax[i] = ndivs-1;
        }
      }
    
    // each octant inbetween min/max point may have cell in it
    for ( k = ijkMin[2]; k <= ijkMax[2]; k++ )
      {
      for ( j = ijkMin[1]; j <= ijkMax[1]; j++ )
        {
        for ( i = ijkMin[0]; i <= ijkMax[0]; i++ )
          {
          idx = parentOffset + i + j*ndivs + k*product;
          this->MarkParents(reinterpret_cast<void*>(VTK_CELL_INSIDE),i,j,k,
                            ndivs,this->Level);
          octant = this->Tree[idx];
          if ( ! octant )
            {
            octant = vtkIdList::New();
            octant->Allocate(numCellsPerBucket,numCellsPerBucket/2);
            this->Tree[idx] = octant;
            }
          octant->InsertNextId(cellId);
          }
        }
      }
    
    } //for all cells
  
  this->BuildTime.Modified();
}
