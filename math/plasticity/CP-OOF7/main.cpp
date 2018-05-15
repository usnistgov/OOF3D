//
//  main.cpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

//                                  ==================              ======            ======
//                                  ==================              ======           ======
//                                  ==================              ======          ======
//                                  =======                         ======         ======
//                                  =======                         ======        ======
//                                  =======                         ======       ======
//                                  ==================              ======      ======
//                                  ==================              ======= ========
//                                  ==================              ======      ======
//                                            ========              ======       ======
//                                            ========              ======        ======
//                                            ========              ======         ======
//                                  ==================              ======          ======
//                                  ==================              ======           ======
//                                  ==================              ======            ======


#include <iostream>
#include <fstream>

#include "Mesh.hpp"
#include "MatInput.hpp"
#include "CrystalPlasticity.hpp"
#include "Material.hpp"
#include "Property.hpp"
#include "Orientation.hpp"

#include<Python/Python.h>
#include <fstream>

int main(int argc, const char * argv[]) {
    
    Py_Initialize();

    int n_dim = 3;
    
    int xelement = 1;
    int yelement = 1;
    int zelement = 1;
    
    std::ifstream inFile;
    inFile.open("cp.15");
    
    if (inFile.is_open()){
        
        Mesh mesh(inFile);

    
//    Mesh mesh(xelement,yelement,zelement);

    //--------------------- Select crystalline structure and constitutive mode and Materials Constants  -----------
        int tmp = 1;
        int tmpc = 1;
        MatType mtype;
        ConstType ctype;
        
        
        mtype = (MatType)tmp;
        ctype = (ConstType)tmpc;
        
        
        struct MatInput CPInput;
        CPInput.ctype = (ConstType)tmpc;
        CPInput.mtype = (MatType)tmp;
        int nom = static_cast<ConstType>(endconst);
        CPInput.MatProp[CPInput.ctype].prop.resize(nom);
        
        CPInput.MatProp[CPInput.ctype].prop(0) = 1.0;
        CPInput.MatProp[CPInput.ctype].prop(1) = 1.4;
        CPInput.MatProp[CPInput.ctype].prop(2) = 377.1e6;
        CPInput.MatProp[CPInput.ctype].prop(3) = 1.115;
        CPInput.MatProp[CPInput.ctype].prop(4) = 150.1e7;
        CPInput.MatProp[CPInput.ctype].prop(5) = 0.01;
        CPInput.MatProp[CPInput.ctype].prop(6) = 24.53e6;
        CPInput.MatProp[CPInput.ctype].prop(7) = 1.0;
        CPInput.MatProp[CPInput.ctype].prop(8) = 170.6e6;
        
        int ncijkl = static_cast<CijklConst>(numconst);
        
        CPInput.CijklConst.resize(ncijkl);
        CPInput.CijklConst(0) = 201.7e9;
        CPInput.CijklConst(1) = 134.4e9;
        CPInput.CijklConst(2) = 104.5e9;
        
        CPInput.Orientation.resize(3);
        CPInput.Orientation(0) = 0.0;
        CPInput.Orientation(1) = 0.0;
        CPInput.Orientation(2) = 0.0;
        
        //----------------------------------------------------------------------
        
        
        OrientationProp *op = OrientationType(&CPInput);
        
        CrystalPlasticity *cp = PlasticityType(&CPInput);
        
        Material *mtl = new Material();
        mtl->add_flux_property(cp);
        mtl->add_property(op);
        mtl->cross_reference();
        
        mesh.add_material_to_all(mtl);
        
        mesh.addfield("Displacement", n_dim,0.0);
        
        mesh.addeqn("Force",3,cp);
        
        mesh.make_stiffness();
        
        
        //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ BCs $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        //    std::vector<int> kbc_n , kbc_d;
        //    std::vector<double> kbc_v;
        /*
         mesh.kbc_n.push_back(0) , mesh.kbc_n.push_back(1) , mesh.kbc_n.push_back(4) , mesh.kbc_n.push_back(5) , mesh.kbc_n.push_back(0) ;
         mesh.kbc_n.push_back(0) , mesh.kbc_n.push_back(1) , mesh.kbc_n.push_back(2) , mesh.kbc_n.push_back(3) , mesh.kbc_n.push_back(6) ;
         mesh.kbc_n.push_back(7);
         
         mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(1) ;
         mesh.kbc_d.push_back(3) , mesh.kbc_d.push_back(3) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) ;
         mesh.kbc_d.push_back(2);
         
         mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) ;
         mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(1) , mesh.kbc_v.push_back(1) , mesh.kbc_v.push_back(1) ;
         mesh.kbc_v.push_back(1);
         */
        
        mesh.kbc_n.push_back(0) , mesh.kbc_n.push_back(1) , mesh.kbc_n.push_back(4) , mesh.kbc_n.push_back(5) ;
        mesh.kbc_n.push_back(0) , mesh.kbc_n.push_back(0) ;
        mesh.kbc_n.push_back(5) ;
        mesh.kbc_n.push_back(2) , mesh.kbc_n.push_back(3) , mesh.kbc_n.push_back(6) , mesh.kbc_n.push_back(7);
        
        mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2);
        mesh.kbc_d.push_back(1) , mesh.kbc_d.push_back(3);
        mesh.kbc_d.push_back(3) ;
        mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2) , mesh.kbc_d.push_back(2);
        
        mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0) ;
        mesh.kbc_v.push_back(0) , mesh.kbc_v.push_back(0);
        mesh.kbc_v.push_back(0) ;
        mesh.kbc_v.push_back(1) , mesh.kbc_v.push_back(1) , mesh.kbc_v.push_back(1) , mesh.kbc_v.push_back(1);

        mesh.nbc = mesh.kbc_n.size();
        
        int nstep = 100;
        
        Vector facload , strain_rate;
        facload.resize(nstep) , strain_rate.resize(nstep);
        facload = 0.5;
        strain_rate = 0.0001;
        
        std::ofstream myfile;
        myfile.open("SS22.txt");
        myfile<<0.0<<"   "<<0.0<<std::endl;
        
        for (int istep = 0 ; istep < nstep ; istep++){
            std::cout<<"istep = "<<istep+1<<std::endl;
            mesh.factor1 = facload(istep)*strain_rate(istep);
            mesh.new_setbcs();
            mesh.solve_nonlinear();
            mesh.user_print();
            myfile<<mesh.strainvol1<<"   "<<mesh.stressvol1/1.0e6<<std::endl;
            
            
        }
        
        myfile.close();
        
        
        FILE *fd = fopen("plot.py", "r");
        PyRun_SimpleFileEx(fd, "plot.py",1);
        
        
        
        Py_Finalize();
        
        inFile.close();
    }

    
    
    
    
    

    
    
    
    return 0;
}
