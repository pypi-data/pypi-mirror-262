// Copyright (c) 2023, RTE (https://www.rte-france.com)
// See AUTHORS.txt
// This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
// If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
// you can obtain one at http://mozilla.org/MPL/2.0/.
// SPDX-License-Identifier: MPL-2.0
// This file is part of LightSim2grid, LightSim2grid implements a c++ backend targeting the Grid2Op platform.

#include "DataDCLine.h"
#include <iostream>
#include <sstream>

DataDCLine::StateRes DataDCLine::get_state() const
{
    std::vector<real_type> loss_percent(loss_percent_.begin(), loss_percent_.end());
    std::vector<real_type> loss_mw(loss_mw_.begin(), loss_mw_.end());
     std::vector<bool> status = status_;
    DataDCLine::StateRes res(from_gen_.get_state(),
                             to_gen_.get_state(),
                             loss_percent,
                             loss_mw,
                             status);
    return res;
}

void DataDCLine::set_state(DataDCLine::StateRes & my_state){
    reset_results();
    from_gen_.set_state(std::get<0>(my_state));
    to_gen_.set_state(std::get<1>(my_state));
    std::vector<real_type> & loss_percent = std::get<2>(my_state);
    std::vector<real_type> & loss_mw = std::get<3>(my_state);
    std::vector<bool> & status = std::get<4>(my_state);
    status_ = status;
    loss_percent_ = RealVect::Map(&loss_percent[0], loss_percent.size());
    loss_mw_ = RealVect::Map(&loss_mw[0], loss_percent.size());
}

void DataDCLine::init(const Eigen::VectorXi & branch_from_id,
                      const Eigen::VectorXi & branch_to_id,
                      const RealVect & p_mw,
                      const RealVect & loss_percent,
                      const RealVect & loss_mw,
                      const RealVect & vm_or_pu,
                      const RealVect & vm_ex_pu,
                      const RealVect & min_q_or,
                      const RealVect & max_q_or,
                      const RealVect & min_q_ex,
                      const RealVect & max_q_ex){
    loss_percent_ = loss_percent;
    loss_mw_ = loss_mw;
    status_ = std::vector<bool>(branch_from_id.size(), true);

    from_gen_.init(p_mw, vm_or_pu, min_q_or, max_q_or, branch_from_id);
    RealVect p_ex = p_mw;
    unsigned int size_ = p_mw.size();
    for(unsigned int i = 0; i < size_; ++i){
        p_ex(i) = get_to_mw(i, p_ex(i));
    }
    to_gen_.init(p_ex, vm_ex_pu, min_q_ex, max_q_ex, branch_to_id);
}
