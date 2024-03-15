// Copyright (c) 2020, RTE (https://www.rte-france.com)
// See AUTHORS.txt
// This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
// If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
// you can obtain one at http://mozilla.org/MPL/2.0/.
// SPDX-License-Identifier: MPL-2.0
// This file is part of LightSim2grid, LightSim2grid implements a c++ backend targeting the Grid2Op platform.

#ifndef DATATRAFO_H
#define DATATRAFO_H

#include "Utils.h"

#include "Eigen/Core"
#include "Eigen/Dense"
#include "Eigen/SparseCore"
#include "Eigen/SparseLU"


#include "DataGeneric.h"

/**
This class is a container for all transformers on the grid.
Transformers are modeled "in pi" here. If your trafo are given in a "t" model (like in pandapower
for example) use the DataConverter class.

The convention used for the transformer is the same as in pandapower:
https://pandapower.readthedocs.io/en/latest/elements/trafo.html

and for modeling of the Ybus matrix:
https://pandapower.readthedocs.io/en/latest/elements/trafo.html#electric-model
**/
class DataTrafo : public DataGeneric
{
    public:
        class TrafoInfo
        {
            public:
                // members
                int id;  // id of the generator
                bool connected;
                int bus_hv_id;
                int bus_lv_id;
                real_type r_pu;
                real_type x_pu;
                cplx_type h_pu;
                bool is_tap_hv_side;
                real_type ratio;
                real_type shift_rad;

                bool has_res;
                real_type res_p_hv_mw;
                real_type res_q_hv_mvar;
                real_type res_v_hv_kv;
                real_type res_a_hv_ka;
                real_type res_theta_hv_deg;
                real_type res_p_lv_mw;
                real_type res_q_lv_mvar;
                real_type res_v_lv_kv;
                real_type res_a_lv_ka;
                real_type res_theta_lv_deg;

                TrafoInfo(const DataTrafo & r_data_trafo, int my_id):
                id(-1),
                connected(false),
                bus_hv_id(-1),
                bus_lv_id(-1),
                r_pu(-1.0),
                x_pu(-1.0),
                h_pu(0., 0.),
                is_tap_hv_side(true),
                ratio(-1.0),
                shift_rad(-1.0),
                has_res(false),
                res_p_hv_mw(0.),
                res_q_hv_mvar(0.),
                res_v_hv_kv(0.),
                res_a_hv_ka(0.),
                res_theta_hv_deg(0.),
                res_p_lv_mw(0.),
                res_q_lv_mvar(0.),
                res_v_lv_kv(0.),
                res_a_lv_ka(0.),
                res_theta_lv_deg(0.)
                {
                    if((my_id >= 0) & (my_id < r_data_trafo.nb()))
                    {
                        id = my_id;
                        connected = r_data_trafo.status_[my_id];
                        bus_hv_id = r_data_trafo.bus_hv_id_.coeff(my_id);
                        bus_lv_id = r_data_trafo.bus_lv_id_.coeff(my_id);
                        r_pu = r_data_trafo.r_.coeff(my_id);
                        x_pu = r_data_trafo.x_.coeff(my_id);
                        h_pu = r_data_trafo.h_.coeff(my_id);
                        is_tap_hv_side = r_data_trafo.is_tap_hv_side_[my_id];
                        ratio = r_data_trafo.ratio_.coeff(my_id);
                        shift_rad = r_data_trafo.shift_.coeff(my_id);

                        has_res = r_data_trafo.res_p_hv_.size() > 0;
                        if(has_res)
                        {
                            res_p_hv_mw = r_data_trafo.res_p_hv_.coeff(my_id);
                            res_q_hv_mvar = r_data_trafo.res_q_hv_.coeff(my_id);
                            res_v_hv_kv = r_data_trafo.res_v_hv_.coeff(my_id);
                            res_a_hv_ka = r_data_trafo.res_a_hv_.coeff(my_id);
                            res_p_lv_mw = r_data_trafo.res_p_lv_.coeff(my_id);
                            res_q_lv_mvar = r_data_trafo.res_q_lv_.coeff(my_id);
                            res_v_lv_kv = r_data_trafo.res_v_lv_.coeff(my_id);
                            res_a_lv_ka = r_data_trafo.res_a_lv_.coeff(my_id);
                            res_theta_hv_deg = r_data_trafo.res_theta_lv_.coeff(my_id);
                            res_theta_lv_deg = r_data_trafo.res_theta_hv_.coeff(my_id);
                        }
                    }
                }
        };
        typedef TrafoInfo DataInfo;

    private:
        typedef DataConstIterator<DataTrafo> DataTrafoConstIterator;

    public:
    typedef std::tuple<
               std::vector<real_type>, // branch_r
               std::vector<real_type>, // branch_x
               std::vector<cplx_type >, // branch_h
               std::vector<int>, // branch_from_id
               std::vector<int>, // branch_to_id
               std::vector<bool> , // status_
               std::vector<real_type>, // ratio_
               std::vector<bool> , // is_tap_hv_side
               std::vector<real_type> // shift_
           >  StateRes;

    DataTrafo() {};

    void init(const RealVect & trafo_r,
                           const RealVect & trafo_x,
                           const CplxVect & trafo_b,
                           const RealVect & trafo_tap_step_pct,
            //                        const RealVect & trafo_tap_step_degree,
                           const RealVect & trafo_tap_pos,
                           const RealVect & trafo_shift_degree,
                           const std::vector<bool> & trafo_tap_hv,  // is tap on high voltage (true) or low voltate
                           const Eigen::VectorXi & trafo_hv_id,
                           const Eigen::VectorXi & trafo_lv_id
              );
    //pickle
    DataTrafo::StateRes get_state() const;
    void set_state(DataTrafo::StateRes & my_state );

    int nb() const { return static_cast<int>(r_.size()); }

    // make it iterable
    typedef DataTrafoConstIterator const_iterator_type;
    const_iterator_type begin() const {return DataTrafoConstIterator(this, 0); }
    const_iterator_type end() const {return DataTrafoConstIterator(this, nb()); }
    TrafoInfo operator[](int id) const
    {
        if(id < 0)
        {
            throw std::range_error("You cannot ask for a transformer with negative id");
        }
        if(id >= nb())
        {
            throw std::range_error("Generator out of bound. Not enough transformers on the grid.");
        }
        return TrafoInfo(*this, id);
    }

    // method used within lightsim
    void deactivate(int trafo_id, bool & need_reset) {_deactivate(trafo_id, status_, need_reset);}
    void reactivate(int trafo_id, bool & need_reset) {_reactivate(trafo_id, status_, need_reset);}
    void change_bus_hv(int trafo_id, int new_bus_id, bool & need_reset, int nb_bus) {_change_bus(trafo_id, new_bus_id, bus_hv_id_, need_reset, nb_bus);}
    void change_bus_lv(int trafo_id, int new_bus_id, bool & need_reset, int nb_bus) {_change_bus(trafo_id, new_bus_id, bus_lv_id_, need_reset, nb_bus);}
    int get_bus_hv(int trafo_id) {return _get_bus(trafo_id, status_, bus_hv_id_);}
    int get_bus_lv(int trafo_id) {return _get_bus(trafo_id, status_, bus_lv_id_);}

    virtual void fillYbus_spmat(Eigen::SparseMatrix<cplx_type> & res, bool ac, const std::vector<int> & id_grid_to_solver);
    virtual void fillYbus(std::vector<Eigen::Triplet<cplx_type> > & res,
                          bool ac,
                          const std::vector<int> & id_grid_to_solver,
                          real_type sn_mva) const;
    virtual void fillBp_Bpp(std::vector<Eigen::Triplet<real_type> > & Bp,
                            std::vector<Eigen::Triplet<real_type> > & Bpp,
                            const std::vector<int> & id_grid_to_solver,
                            real_type sn_mva,
                            FDPFMethod xb_or_bx) const;
    virtual void hack_Sbus_for_dc_phase_shifter(CplxVect & Sbus, bool ac, const std::vector<int> & id_grid_to_solver);  // needed for dc mode

    void compute_results(const Eigen::Ref<const RealVect> & Va,
                         const Eigen::Ref<const RealVect> & Vm,
                         const Eigen::Ref<const CplxVect> & V,
                         const std::vector<int> & id_grid_to_solver,
                         const RealVect & bus_vn_kv,
                         real_type sn_mva,
                         bool ac);
    void reset_results();

    tuple4d get_res_hv() const {return tuple4d(res_p_hv_, res_q_hv_, res_v_hv_, res_a_hv_);}
    tuple4d get_res_lv() const {return tuple4d(res_p_lv_, res_q_lv_, res_v_lv_, res_a_lv_);}
    Eigen::Ref<const RealVect> get_theta_hv() const {return res_theta_hv_;}
    Eigen::Ref<const RealVect> get_theta_lv() const {return res_theta_lv_;}
    Eigen::Ref<const Eigen::VectorXi> get_bus_from() const {return bus_hv_id_;}
    Eigen::Ref<const Eigen::VectorXi> get_bus_to() const {return bus_lv_id_;}

    // model paramters
    Eigen::Ref<const CplxVect> yac_ff() const {return yac_ff_;}
    Eigen::Ref<const CplxVect> yac_ft() const {return yac_ft_;}
    Eigen::Ref<const CplxVect> yac_tf() const {return yac_tf_;}
    Eigen::Ref<const CplxVect> yac_tt() const {return yac_tt_;}

    Eigen::Ref<const CplxVect> ydc_ff() const {return ydc_ff_;}
    Eigen::Ref<const CplxVect> ydc_ft() const {return ydc_ft_;}
    Eigen::Ref<const CplxVect> ydc_tf() const {return ydc_tf_;}
    Eigen::Ref<const CplxVect> ydc_tt() const {return ydc_tt_;}
    Eigen::Ref<const RealVect> dc_x_tau_shift() const {return dc_x_tau_shift_;}
    
    const std::vector<bool>& get_status() const {return status_;}

    protected:
        void _update_model_coeffs();
        
    protected:
        // physical properties
        RealVect r_;
        RealVect x_;
        CplxVect h_;
        std::vector<bool> is_tap_hv_side_;  // whether the tap is hav side or not

        // input data
        Eigen::VectorXi bus_hv_id_;
        Eigen::VectorXi bus_lv_id_;
        std::vector<bool> status_;
        RealVect ratio_;  // transformer ratio
        RealVect shift_;  // phase shifter (in radian !)

        //output data
        RealVect res_p_hv_;  // in MW
        RealVect res_q_hv_;  // in MVar
        RealVect res_v_hv_;  // in kV
        RealVect res_a_hv_;  // in kA
        RealVect res_p_lv_;  // in MW
        RealVect res_q_lv_;  // in MVar
        RealVect res_v_lv_;  // in kV
        RealVect res_a_lv_;  // in kA
        RealVect res_theta_hv_;  // in degree
        RealVect res_theta_lv_;  // in degree

        // model coefficients
        CplxVect yac_ff_;
        CplxVect yac_ft_;
        CplxVect yac_tf_;
        CplxVect yac_tt_;

        CplxVect ydc_ff_;
        CplxVect ydc_ft_;
        CplxVect ydc_tf_;
        CplxVect ydc_tt_;
        RealVect dc_x_tau_shift_;
};

#endif  //DATATRAFO_H
