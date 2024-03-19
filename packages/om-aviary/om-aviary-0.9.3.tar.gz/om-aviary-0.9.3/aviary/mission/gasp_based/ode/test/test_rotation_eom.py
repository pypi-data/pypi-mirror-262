import unittest
import os

import numpy as np
import openmdao.api as om
from openmdao.utils.assert_utils import assert_check_partials

from aviary.mission.gasp_based.ode.rotation_eom import RotationEOM
from aviary.variable_info.variables import Aircraft, Dynamic


class RotationEOMTestCase(unittest.TestCase):
    def setUp(self):

        self.prob = om.Problem()
        self.prob.model.add_subsystem("group", RotationEOM(num_nodes=2), promotes=["*"])
        self.prob.model.set_input_defaults(
            Dynamic.Mission.MASS, val=175400 * np.ones(2), units="lbm"
        )
        self.prob.model.set_input_defaults(
            Dynamic.Mission.THRUST_TOTAL, val=22000 * np.ones(2), units="lbf"
        )
        self.prob.model.set_input_defaults(
            Dynamic.Mission.LIFT, val=200 * np.ones(2), units="lbf")
        self.prob.model.set_input_defaults(
            Dynamic.Mission.DRAG, val=10000 * np.ones(2), units="lbf")
        self.prob.model.set_input_defaults(
            Dynamic.Mission.VELOCITY, val=10 * np.ones(2), units="ft/s")
        self.prob.model.set_input_defaults(
            Dynamic.Mission.FLIGHT_PATH_ANGLE, val=np.zeros(2), units="rad")
        self.prob.model.set_input_defaults(Aircraft.Wing.INCIDENCE, val=0, units="deg")
        self.prob.model.set_input_defaults("alpha", val=np.zeros(2), units="deg")

        self.prob.setup(check=False, force_alloc_complex=True)

    def test_case1(self):

        tol = 1e-6
        self.prob.run_model()

        partial_data = self.prob.check_partials(out_stream=None, method="cs")
        assert_check_partials(partial_data, atol=1e-12, rtol=1e-12)


if __name__ == "__main__":
    unittest.main()
