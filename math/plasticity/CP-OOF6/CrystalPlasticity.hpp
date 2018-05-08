//
//  CrystalPlasticity.hpp
//  CP6
//
//  Created by Keshavarzhadad, Shahriyar on 4/26/18.
//  Copyright © 2018 Keshavarzhadad, Shahriyar. All rights reserved.
//

#ifndef CrystalPlasticity_hpp
#define CrystalPlasticity_hpp

#include <stdio.h>
#include <cmath>

#include "MatInput.hpp"
#include "ConstitutiveModel.hpp"
#include "Flux.hpp"
#include "Tensor.hpp"
#include "Orientation.hpp"
#include "ElementData.hpp"
#include "PlasticData.hpp"
#include "SlipData.hpp"
#include "GptPlasticData.hpp"
#include "PowerLaw.hpp"
#include "CauchyStress.hpp"


class PlasticData;
class SlipData;

class CrystalPlasticity : public Flux{
    
public:
    
    CrystalPlasticity(ConstitutiveModel *cm) : ConstModel(cm) , Flux("Stress","Displacemenr","Plasticity",9) {};
    CrystalPlasticity() : Flux("Stress","Displacemenr","Plasticity",9) {};
    virtual void calculate_schmid_tensor() = 0;
    void Orientation(OrientationProp *);

    MatInput* cpi;
    ConstitutiveModel* ConstModel;
    Tensor2d qrot;
    Tensor3d schmid;
    
//    void cross_reference(Material *);
    void cross_reference(Material *);

    virtual void begin_element(Element *, Mesh *);
    
    PlasticData *pd;
    SlipData *sd;

    GptSlipData *usd;
//    GptPlasticData *upd;

    void calc_F(Tensor2d coorElement, Tensor2d shpg,int nnode);
    void calc_A();
    void calc_B();
//    CauchyStress* cauchy;
    void calc_C();
    void stress_trial();
    
    void iterSecPio();
    void resolvedshear(Tensor2d &Stress);
    void SPKStress();
    void GTMat();
    void RJMat();
    Tensor2d reduce_mat(Tensor4d as_mat);
    Vector reduce_vec(Tensor2d as_star);
    Tensor2d inflate_vec(Vector as_vec);
    
    void W_mat();
    void polardecomp();
    Tensor4d inflate_ten(Tensor2d as_ten);
    Tensor2d reduce_wmat(Tensor4d as_mat);
    Tensor2d Dep;

    virtual void make_linear_system(Element *el,GaussPoint* gpti,int gp_index);

    CauchyStress* cauchy;
    GptPlasticData *upd;

private:
    
    double const_pi = acos(-1.0);
     int n_dim = 3;
    Tensor3d B_alpha , C_alpha;
    Tensor2d A_mat;
    Tensor2d S_trial;
    Tensor2d shpg;
    
    Tensor4d delta_kron4d;
    Tensor3d GT_mat;
    Tensor4d RJ_mat;
    Tensor2d RJ_reduced;

    Tensor2d Stretch;
    Tensor2d Rotation;
 //   Tensor4d w_mat;


    virtual void user_print(GaussPoint* gpti,int gp_index);


};

CrystalPlasticity* PlasticityType(MatInput *CPIn);
OrientationProp * OrientationType(MatInput *CPIn);

#endif /* CrystalPlasticity_hpp */
