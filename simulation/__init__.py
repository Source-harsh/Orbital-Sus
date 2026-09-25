"""
Orbital Sus simulation package.

Provides:
- spacecraft simulation
- scenario generation
- threat correlation
- threat state management
- simulated defensive response
- event replay
"""

from .simulator import SatelliteState, create_normal_state
from .simulation_runner import run_scenario

__all__ = [
    "SatelliteState",
    "create_normal_state",
    "run_scenario",
]