// Copyright (c) 2020, RTE (https://www.rte-france.com)
// See AUTHORS.txt
// This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
// If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
// you can obtain one at http://mozilla.org/MPL/2.0/.
// SPDX-License-Identifier: MPL-2.0
// This file is part of LightSim2grid, LightSim2grid implements a c++ backend targeting the Grid2Op platform.

#ifndef DATAGEN_H
#define DATAGEN_H

#include <iostream>
#include <vector> 

#include "Utils.h"

#include "Eigen/Core"
#include "Eigen/Dense"
#include "Eigen/SparseCore"
#include "Eigen/SparseLU"

#include "DataGeneric.h"

/**
This class represents the list of all generators.

The convention used for the generator is the same as in pandapower:
https://pandapower.readthedocs.io/en/latest/elements/gen.html

and for modeling of the Ybus matrix:
https://pandapower.readthedocs.io/en/latest/elements/gen.html#electric-model
**/
class DataGen: public DataGeneric
{
    public:
    class GenInfo
    {
        public:
            // members
            // TODO add some const here (value should not be changed !) !!!
            int id;  // id of the generator
            bool connected;
            int bus_id;
            bool is_slack;
            real_type slack_weight;

            real_type target_p_mw;
            real_type target_vm_pu;
            real_type min_q_mvar;
            real_type max_q_mvar;
            bool has_res;
            real_type res_p_mw;
            real_type res_q_mvar;
            real_type res_v_kv;
            real_type res_theta_deg;

            GenInfo(const DataGen & r_data_gen, int my_id):
            id(-1),
            connected(false),
            bus_id(-1),
            is_slack(false),
            slack_weight(-1.0),
            target_p_mw(0.),
            target_vm_pu(0.),
            min_q_mvar(0.),
            max_q_mvar(0.),
            has_res(false),
            res_p_mw(0.),
            res_q_mvar(0.),
            res_v_kv(0.),
            res_theta_deg(0.)
            {
                if((my_id >= 0) & (my_id < r_data_gen.nb()))
                {
                    id = my_id;
                    connected = r_data_gen.status_[my_id];
                    bus_id = r_data_gen.bus_id_[my_id];
                    is_slack = r_data_gen.gen_slackbus_[my_id];
                    slack_weight = r_data_gen.gen_slack_weight_[my_id];

                    target_p_mw = r_data_gen.p_mw_.coeff(my_id);
                    target_vm_pu = r_data_gen.vm_pu_.coeff(my_id);
                    min_q_mvar = r_data_gen.min_q_.coeff(my_id);
                    max_q_mvar = r_data_gen.max_q_.coeff(my_id);

                    has_res = r_data_gen.res_p_.size() > 0;
                    if(has_res)
                    {
                        res_p_mw = r_data_gen.res_p_.coeff(my_id);
                        res_q_mvar = r_data_gen.res_q_.coeff(my_id);
                        res_v_kv = r_data_gen.res_v_.coeff(my_id);
                        res_theta_deg = r_data_gen.res_theta_.coeff(my_id);
                    }
                }
            }
    };
    typedef GenInfo DataInfo;

    private:
    typedef DataConstIterator<DataGen> DataGenConstIterator;

    public:
    typedef std::tuple<
       bool,
       std::vector<real_type>, // p_mw
       std::vector<real_type>, // vm_pu_
       std::vector<real_type>, // min_q_
       std::vector<real_type>, // max_q_
       std::vector<int>, // bus_id
       std::vector<bool>, // status
       std::vector<bool>, // gen_slackbus
       std::vector<real_type> // gen_slack_weight_
       >  StateRes;

    DataGen():turnedoff_gen_pv_(true){};
    DataGen(bool turnedoff_gen_pv):turnedoff_gen_pv_(turnedoff_gen_pv) {};

    // TODO add pmin and pmax here !
    void init(const RealVect & generators_p,
              const RealVect & generators_v,
              const RealVect & generators_min_q,
              const RealVect & generators_max_q,
              const Eigen::VectorXi & generators_bus_id
              );

    int nb() const { return static_cast<int>(p_mw_.size()); }

    // iterator
    typedef DataGenConstIterator const_iterator_type;
    const_iterator_type begin() const {return DataGenConstIterator(this, 0); }
    const_iterator_type end() const {return DataGenConstIterator(this, nb()); }
    GenInfo operator[](int id) const
    {
        if(id < 0)
        {
            throw std::range_error("You cannot ask for a negative generator");
        }
        if(id >= nb())
        {
            throw std::range_error("Generator out of bound. Not enough generator on the grid.");
        }
        return GenInfo(*this, id);
    }

    // pickle
    DataGen::StateRes get_state() const;
    void set_state(DataGen::StateRes & my_state );

    // slack handling
    /**
    we suppose that the data are correct (ie gen_id in the proper range, and weight > 0.)
    This is checked in GridModel, and not at this stage
    **/
    void add_slackbus(int gen_id, real_type weight){
        gen_slackbus_[gen_id] = true;
        gen_slack_weight_[gen_id] = weight;
    }
    void remove_slackbus(int gen_id){
        gen_slackbus_[gen_id] = false;
        gen_slack_weight_[gen_id] = 0.;
    }
    /**
    Retrieve the normalized (=sum to 1.000) slack weights for all the buses
    **/
    RealVect get_slack_weights(Eigen::Index nb_bus_solver, const std::vector<int> & id_grid_to_solver);

    std::vector<int> get_slack_bus_id() const;
    void set_p_slack(const RealVect& node_mismatch, const std::vector<int> & id_grid_to_solver);

    // modification
    void turnedoff_no_pv(){turnedoff_gen_pv_=false;}  // turned off generators are not pv
    void turnedoff_pv(){turnedoff_gen_pv_=true;}  // turned off generators are pv
    bool get_turnedoff_gen_pv() const {return turnedoff_gen_pv_;}
    void update_slack_weights(Eigen::Ref<Eigen::Array<bool, Eigen::Dynamic, Eigen::RowMajor> > could_be_slack,
                              bool & need_reset);

    void deactivate(int gen_id, bool & need_reset) {_deactivate(gen_id, status_, need_reset);}
    void reactivate(int gen_id, bool & need_reset) {_reactivate(gen_id, status_, need_reset);}
    void change_bus(int gen_id, int new_bus_id, bool & need_reset, int nb_bus) {_change_bus(gen_id, new_bus_id, bus_id_, need_reset, nb_bus);}
    int get_bus(int gen_id) {return _get_bus(gen_id, status_, bus_id_);}
    real_type get_qmin(int gen_id) {return min_q_.coeff(gen_id);}
    real_type get_qmax(int gen_id) {return max_q_.coeff(gen_id);}
    void change_p(int gen_id, real_type new_p, bool & need_reset);
    void change_v(int gen_id, real_type new_v_pu, bool & need_reset);

    virtual void fillSbus(CplxVect & Sbus, const std::vector<int> & id_grid_to_solver, bool ac) const;
    virtual void fillpv(std::vector<int>& bus_pv,
                        std::vector<bool> & has_bus_been_added,
                        Eigen::VectorXi & slack_bus_id_solver,
                        const std::vector<int> & id_grid_to_solver) const;
    void init_q_vector(int nb_bus,
                       Eigen::VectorXi & total_gen_per_bus,
                       RealVect & total_q_min_per_bus,
                       RealVect & total_q_max_per_bus) const; // delta_q_per_gen_

    void compute_results(const Eigen::Ref<const RealVect> & Va,
                         const Eigen::Ref<const RealVect> & Vm,
                         const Eigen::Ref<const CplxVect> & V,
                         const std::vector<int> & id_grid_to_solver,
                         const RealVect & bus_vn_kv,
                         real_type sn_mva,
                         bool ac);
    void reset_results();
    void set_q(const RealVect & reactive_mismatch,
               const std::vector<int> & id_grid_to_solver,
               bool ac,
               const Eigen::VectorXi & total_gen_per_bus,
               const RealVect & total_q_min_per_bus,
               const RealVect & total_q_max_per_bus);

    void get_vm_for_dc(RealVect & Vm);
    /**
    this functions makes sure that the voltage magnitude of every connected bus is properly used to initialize
    the ac powerflow
    **/
    void set_vm(CplxVect & V, const std::vector<int> & id_grid_to_solver) const;

    tuple3d get_res() const {return tuple3d(res_p_, res_q_, res_v_);}
    Eigen::Ref<const RealVect> get_theta() const {return res_theta_;}

    const std::vector<bool>& get_status() const {return status_;}
    const Eigen::VectorXi & get_bus_id() const {return bus_id_;}

    void cout_v(){
        for(const auto & el : vm_pu_){
            std::cout << "V " << el << std::endl;
        }
    }
    protected:
        // physical properties

        // input data
        RealVect p_mw_;
        RealVect vm_pu_;
        RealVect min_q_;
        RealVect max_q_;
        Eigen::VectorXi bus_id_;
        std::vector<bool> status_;

        // remember which generators are "slack bus"
        std::vector<bool> gen_slackbus_;  // say for each generator if it's a slack or not
        std::vector<real_type> gen_slack_weight_;

        // intermediate data
        // Eigen::VectorXi total_gen_per_bus_;
        RealVect bus_slack_weight_;  // do not sum to 1., for each node of the grid, say the raw contribution for the generator

        //output data
        RealVect res_p_;  // in MW
        RealVect res_q_;  // in MVar
        RealVect res_v_;  // in kV
        RealVect res_theta_;  // in deg (and not rad)

        // different parameter of the behaviour of the class
        bool turnedoff_gen_pv_;  // are turned off generators (including one with p=0) pv ?
};

#endif  //DATAGEN_H
