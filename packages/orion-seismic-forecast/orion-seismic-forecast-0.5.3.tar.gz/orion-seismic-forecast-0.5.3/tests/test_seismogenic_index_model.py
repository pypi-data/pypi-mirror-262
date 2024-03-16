# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import pytest
import numpy as np
import os
from scipy.stats import pareto
import sys
from pathlib import Path

package_path = os.path.abspath(Path(__file__).resolve().parents[1])
mod_path = os.path.abspath(os.path.join(package_path, 'src'))
sys.path.append(mod_path)
strive_path = os.path.abspath(os.path.join(package_path, '..', 'strive', 'src'))
sys.path.append(strive_path)


def test_seismogenic_index_model():
    np.random.seed(100)
    from orion.forecast_models import seismogenic_index_model
    SI = seismogenic_index_model.SeismogenicIndexModel()
    SI.process_inputs()

    # Create dummy data
    dpdt = np.random.rand(2, 1, 1)    ## Nt, Nx, Ny
    event_count = np.random.randint(1, 50, size=dpdt.shape)
    b_value = 1.0
    magnitude_completeness = -1.0

    si, si_rate_cum = SI.seismogenic_index(dpdt, event_count, b_value, magnitude_completeness)

    assert si == pytest.approx(1.07629596, abs=1e-6)
    assert si_rate_cum[-1] == pytest.approx(16, abs=1e-6)
