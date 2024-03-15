// Copyright (c) 2023, RTE (https://www.rte-france.com)
// See AUTHORS.txt
// This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
// If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
// you can obtain one at http://mozilla.org/MPL/2.0/.
// SPDX-License-Identifier: MPL-2.0
// This file is part of LightSim2grid, LightSim2grid implements a c++ backend targeting the Grid2Op platform.

#ifndef DATADCLINE_H
#define DATADCLINE_H

#include <iostream>

#include "Utils.h"

#include "Eigen/Core"
#include "Eigen/Dense"
#include "Eigen/SparseCore"
#include "Eigen/SparseLU"

#include "DataGeneric.h"
#include "DataGen.h"


class DataDCLine : public DataGeneric
{
    public:
        class DCLineInfo
        {
            public:
                // members
                int id;  // id of the dcline
                bool connected;
                int bus_or_id;
                int bus_ex_id;
                real_type target_p_or_mw;
                real_type target_vm_or_pu;
                real_type target_vm_ex_pu;
                real_type loss_pct;
                real_type loss_mw;
                DataGen::GenInfo gen_or;
                DataGen::GenInfo gen_ex;

                bool has_res;
                real_type res_p_or_mw;
                real_type res_q_or_mvar;
                real_type res_v_or_kv;
                real_type res_theta_or_deg;
                real_type res_p_ex_mw;
                real_type res_q_ex_mvar;
                real_type res_v_ex_kv;
                real_type res_theta_ex_deg;

                DCLineInfo(const DataDCLine & r_data_dcline, int my_id):
                    id(-1),
                    connected(false),
                    bus_or_id(-1),
                    bus_ex_id(-1),
                    target_p_or_mw(0.),
                    target_vm_or_pu(0.),
                    target_vm_ex_pu(0.),
                    loss_pct(0.),
                    loss_mw(0.),
                    gen_or(r_data_dcline.from_gen_, my_id),
                    gen_ex(r_data_dcline.to_gen_, my_id),
                    has_res(false),
                    res_p_or_mw(0.),
                    res_q_or_mvar(0.),
                    res_v_or_kv(0.),
                    res_theta_or_deg(0.),
                    res_p_ex_mw(0.),
                    res_q_ex_mvar(0.),
                    res_v_ex_kv(0.),
                    res_theta_ex_deg(0.)
                {
                    if((my_id >= 0) & (my_id < r_data_dcline.nb()))
                    {
                        id = my_id;
                        loss_pct = r_data_dcline.loss_percent_(my_id);
                        loss_mw = r_data_dcline.loss_mw_(my_id);

                        bus_or_id = gen_or.bus_id;
                        target_p_or_mw = gen_or.target_p_mw;
                        target_vm_or_pu = gen_or.target_vm_pu;

                        bus_ex_id = gen_ex.bus_id;
                        target_vm_ex_pu = gen_ex.target_vm_pu;

                        has_res = gen_or.has_res;
                        if(has_res){
                            res_p_or_mw = gen_or.res_p_mw;
                            res_q_or_mvar = gen_or.res_q_mvar;
                            res_v_or_kv = gen_or.res_v_kv;
                            res_theta_or_deg = gen_or.res_theta_deg;
                            res_p_ex_mw = gen_ex.res_p_mw;
                            res_q_ex_mvar = gen_ex.res_q_mvar;
                            res_v_ex_kv = gen_ex.res_v_kv;
                            res_theta_ex_deg = gen_ex.res_theta_deg;
                        }
                    }

                }
        };
        typedef DCLineInfo DataInfo;

    private:
        typedef DataConstIterator<DataDCLine> DataDCLineConstIterator;

    public:
    typedef std::tuple<
               DataGen::StateRes,
               DataGen::StateRes,
               std::vector<double>, // loss_percent
               std::vector<double>, // vm_to_pu
               std::vector<bool> // loss_mw
               >  StateRes;

    int nb() const { return static_cast<int>(from_gen_.nb()); }

    // iterator
    typedef DataDCLineConstIterator const_iterator_type;
    const_iterator_type begin() const {return DataDCLineConstIterator(this, 0); }
    const_iterator_type end() const {return DataDCLineConstIterator(this, nb()); }
    DCLineInfo operator[](int id) const
    {
        if(id < 0)
        {
            throw std::range_error("You cannot ask for a negative dc line");
        }
        if(id >= nb())
        {
            throw std::range_error("DCLine out of bound. Not enough dc line on the grid.");
        }
        return DCLineInfo(*this, id);
    }

    // underlying generators are not pv when powerline is off
    DataDCLine(): from_gen_(false), to_gen_(false) {};

    // pickle
    DataDCLine::StateRes get_state() const;
    void set_state(DataDCLine::StateRes & my_state);

    // TODO min_p, max_p
    void init(const Eigen::VectorXi & branch_from_id,
              const Eigen::VectorXi & branch_to_id,
              const RealVect & p_mw,
              const RealVect & loss_percent,
              const RealVect & loss_mw,
              const RealVect & vm_or_pu,
              const RealVect & vm_ex_pu,
              const RealVect & min_q_or,
              const RealVect & max_q_or,
              const RealVect & min_q_ex,
              const RealVect & max_q_ex
              );

    // accessor / modifiers
    void deactivate(int dcline_id, bool & need_reset) {
        _deactivate(dcline_id, status_, need_reset);
        from_gen_.deactivate(dcline_id, need_reset);
        to_gen_.deactivate(dcline_id, need_reset);
        }
    void reactivate(int dcline_id, bool & need_reset) {
        _reactivate(dcline_id, status_, need_reset);
        from_gen_.reactivate(dcline_id, need_reset);
        to_gen_.reactivate(dcline_id, need_reset);
        }
    void change_bus_or(int dcline_id, int new_bus_id, bool & need_reset, int nb_bus) {
        from_gen_.change_bus(dcline_id, new_bus_id, need_reset, nb_bus);}
    void change_bus_ex(int dcline_id, int new_bus_id, bool & need_reset, int nb_bus) {
        to_gen_.change_bus(dcline_id, new_bus_id, need_reset, nb_bus);}
    int get_bus_or(int dcline_id) {return from_gen_.get_bus(dcline_id);}
    int get_bus_ex(int dcline_id) {return to_gen_.get_bus(dcline_id);}
    real_type get_qmin_or(int dcline_id) {return from_gen_.get_qmin(dcline_id);}
    real_type get_qmax_or(int dcline_id) {return  from_gen_.get_qmax(dcline_id);}
    real_type get_qmin_ex(int dcline_id) {return to_gen_.get_qmin(dcline_id);}
    real_type get_qmax_ex(int dcline_id) {return  to_gen_.get_qmax(dcline_id);}

    real_type get_to_mw(int dcline_id, real_type from_mw){
        // TODO set it to load convention instead of gen convention as in lightsim2grid
        real_type new_p_ext = from_mw >= 0 ? 
                              -(from_mw + loss_mw_(dcline_id)) / (1.0 - 0.01 * loss_percent_(dcline_id)) :
                              -from_mw * (1.0 - 0.01 * loss_percent_(dcline_id)) - loss_mw_(dcline_id)
                              ;
        return new_p_ext;
    }
    void change_p(int dcline_id, real_type new_p, bool & need_reset){
        from_gen_.change_p(dcline_id, -1.0 * new_p, need_reset);

        to_gen_.change_p(dcline_id, -1.0 * get_to_mw(dcline_id, new_p), need_reset);
    }
    void change_v_or(int dcline_id, real_type new_v_pu, bool & need_reset){
        from_gen_.change_v(dcline_id, new_v_pu, need_reset);
    }
    void change_v_ex(int dcline_id, real_type new_v_pu, bool & need_reset){
        to_gen_.change_v(dcline_id, new_v_pu, need_reset);
    }

    // solver stuff
    virtual void fillSbus(CplxVect & Sbus, const std::vector<int> & id_grid_to_solver, bool ac) const{
        from_gen_.fillSbus(Sbus, id_grid_to_solver, ac);   
        to_gen_.fillSbus(Sbus, id_grid_to_solver, ac);   
    } 

    virtual void fillpv(std::vector<int>& bus_pv,
                        std::vector<bool> & has_bus_been_added,
                        Eigen::VectorXi & slack_bus_id_solver,
                        const std::vector<int> & id_grid_to_solver) const {
        from_gen_.fillpv(bus_pv, has_bus_been_added, slack_bus_id_solver, id_grid_to_solver);   
        to_gen_.fillpv(bus_pv, has_bus_been_added, slack_bus_id_solver, id_grid_to_solver);   
    }
    void init_q_vector(int nb_bus,
                       Eigen::VectorXi & total_gen_per_bus,
                       RealVect & total_q_min_per_bus,
                       RealVect & total_q_max_per_bus) const{
        from_gen_.init_q_vector(nb_bus, total_gen_per_bus, total_q_min_per_bus, total_q_max_per_bus);
        to_gen_.init_q_vector(nb_bus, total_gen_per_bus, total_q_min_per_bus, total_q_max_per_bus);
    }
    void compute_results(const Eigen::Ref<const RealVect> & Va,
                         const Eigen::Ref<const RealVect> & Vm,
                         const Eigen::Ref<const CplxVect> & V,
                         const std::vector<int> & id_grid_to_solver,
                         const RealVect & bus_vn_kv,
                         real_type sn_mva,
                         bool ac){
        from_gen_.compute_results(Va, Vm, V,
                                  id_grid_to_solver,
                                  bus_vn_kv, sn_mva, ac);
        to_gen_.compute_results(Va, Vm, V,
                                id_grid_to_solver,
                                bus_vn_kv, sn_mva, ac);
    }

    void reset_results(){
        from_gen_.reset_results();
        to_gen_.reset_results();
    }
    void set_q(const RealVect & reactive_mismatch,
               const std::vector<int> & id_grid_to_solver,
               bool ac,
               const Eigen::VectorXi & total_gen_per_bus,
               const RealVect & total_q_min_per_bus,
               const RealVect & total_q_max_per_bus){
        // TODO set it to load convention instead of gen convention as in lightsim2grid
        from_gen_.set_q(reactive_mismatch, id_grid_to_solver, ac, total_gen_per_bus, total_q_min_per_bus, total_q_max_per_bus);
        to_gen_.set_q(reactive_mismatch, id_grid_to_solver, ac, total_gen_per_bus, total_q_min_per_bus, total_q_max_per_bus);
    }
    void get_vm_for_dc(RealVect & Vm){
        from_gen_.get_vm_for_dc(Vm);
        to_gen_.get_vm_for_dc(Vm);
    }
    void set_vm_or(CplxVect & V, const std::vector<int> & id_grid_to_solver) const{
        from_gen_.set_vm(V, id_grid_to_solver);
    }
    void set_vm_ex(CplxVect & V, const std::vector<int> & id_grid_to_solver) const{
        to_gen_.set_vm(V, id_grid_to_solver);
    }

    /**
    this functions makes sure that the voltage magnitude of every connected bus is properly used to initialize
    the ac powerflow
    **/
    void set_vm(CplxVect & V, const std::vector<int> & id_grid_to_solver) const{
        from_gen_.set_vm(V, id_grid_to_solver);
        to_gen_.set_vm(V, id_grid_to_solver);
    }

    const std::vector<bool>& get_status() const {return status_;}
    const Eigen::VectorXi & get_bus_id_or() const {return from_gen_.get_bus_id();}
    const Eigen::VectorXi & get_bus_id_ex() const {return to_gen_.get_bus_id();}
    
    tuple3d get_or_res() const {return from_gen_.get_res();}
    tuple3d get_ex_res() const {return to_gen_.get_res();}
    Eigen::Ref<const RealVect> get_theta_or() const {return from_gen_.get_theta();}
    Eigen::Ref<const RealVect> get_theta_ex() const {return to_gen_.get_theta();}

    protected:
        // it is modeled as 2 generators that are "linked" together
        // see https://pandapower.readthedocs.io/en/v2.0.1/elements/dcline.html#electric-model
        DataGen from_gen_;
        DataGen to_gen_;
        RealVect loss_percent_;
        RealVect loss_mw_;
        std::vector<bool> status_;

};

#endif  //DATADCLINE_H