// Copyright (c) 2020, RTE (https://www.rte-france.com)
// See AUTHORS.txt
// This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
// If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
// you can obtain one at http://mozilla.org/MPL/2.0/.
// SPDX-License-Identifier: MPL-2.0
// This file is part of LightSim2grid, LightSim2grid implements a c++ backend targeting the Grid2Op platform.

#ifndef UTILS_H
#define UTILS_H

/**
Some typedef and other structures define here and used everywhere else
**/

#include <complex>
#include "Eigen/Core"

// typedef float real_type;  // type for real numbers: can be changed if installed from source
typedef double real_type;  // type for real numbers: can be changed if installed from source

typedef std::complex<real_type> cplx_type;  // type for complex number

typedef Eigen::Matrix<real_type, Eigen::Dynamic, 1> EigenPythonNumType;  // Eigen::VectorXd
typedef std::tuple<Eigen::Ref<const EigenPythonNumType>,
                   Eigen::Ref<const EigenPythonNumType>,
                   Eigen::Ref<const EigenPythonNumType> > tuple3d;
typedef std::tuple<Eigen::Ref<const EigenPythonNumType>,
                   Eigen::Ref<const EigenPythonNumType>,
                   Eigen::Ref<const EigenPythonNumType>,
                   Eigen::Ref<const EigenPythonNumType> > tuple4d;
typedef Eigen::Matrix<int, Eigen::Dynamic, 1> IntVect;
typedef Eigen::Matrix<real_type, Eigen::Dynamic, 1> RealVect;
typedef Eigen::Matrix<cplx_type, Eigen::Dynamic, 1> CplxVect;

// type of error in the different solvers
enum class ErrorType {NoError, SingularMatrix, TooManyIterations, InifiniteValue, SolverAnalyze, SolverFactor, SolverReFactor, SolverSolve, NotInitError, LicenseError};

// define some constant for compilation outside of "setup.py"
#ifndef VERSION_MAJOR
#define VERSION_MAJOR -1
#endif

#ifndef VERSION_MEDIUM
#define VERSION_MEDIUM -1
#endif

#ifndef VERSION_MINOR
#define VERSION_MINOR -1
#endif

#endif // UTILS_H
