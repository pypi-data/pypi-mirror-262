# Copyright 2024 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
from __future__ import annotations

from typing import Any

from .base import fire_opal_workflow


@fire_opal_workflow("benchmark_workflow")
def benchmark(
    ibm_device_name: str,
    benchmark_config: dict[str, Any],
    hub: str,
    group: str,
    project: str,
    ibmq_token: str,
) -> dict:
    """
    Runs the Fire Opal benchmark suite.

    Parameters
    ----------
    ibm_device_name : str
        Description.
    benchmark_config : Dict[str, Any]
        Description.
    hub : str
        Description.
    group : str
        Description.
    project : str
        Description.
    ibmq_token : str
        Description.

    Returns
    -------
    dict
        The output of the benchmarking workflow.
    """
    return {
        "ibm_device_name": ibm_device_name,
        "benchmark_config": benchmark_config,
        "hub": hub,
        "group": group,
        "project": project,
        "ibmq_token": ibmq_token,
    }
