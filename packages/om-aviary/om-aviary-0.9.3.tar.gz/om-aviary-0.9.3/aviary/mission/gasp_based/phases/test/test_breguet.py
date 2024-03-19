import unittest
import os

import numpy as np
import openmdao.api as om
from openmdao.utils.assert_utils import (assert_check_partials,
                                         assert_near_equal)

from aviary.constants import GRAV_ENGLISH_LBM
from aviary.mission.gasp_based.phases.breguet import RangeComp
from aviary.variable_info.variables import Dynamic


class TestBreguetResults(unittest.TestCase):
    def setUp(self):
        nn = 10

        self.prob = om.Problem()
        self.prob.model.add_subsystem(
            "range_comp", RangeComp(num_nodes=nn), promotes=["*"])

        self.prob.setup(check=False, force_alloc_complex=True)

        self.prob.set_val("TAS_cruise", 458.8, units="kn")
        self.prob.set_val("mass", np.linspace(171481, 171481 - 10000, nn), units="lbm")
        self.prob.set_val(Dynamic.Mission.FUEL_FLOW_RATE_NEGATIVE_TOTAL, -
                          5870 * np.ones(nn,), units="lbm/h")

    def test_case1(self):

        tol = 1e-6
        self.prob.run_model()

        cruise_range = self.prob.get_val("cruise_range", units="NM")
        cruise_time = self.prob.get_val("cruise_time", units="s")

        t_expected = 6134.7240144
        r_expected = 781.83848643

        assert_near_equal(cruise_range[-1, ...], r_expected, tolerance=0.001)
        assert_near_equal(cruise_time[-1, ...], t_expected, tolerance=0.001)

        with np.printoptions(linewidth=1024):
            self.prob.model.list_outputs(prom_name=True, print_arrays=True)
            partial_data = self.prob.check_partials(method="cs")  # , out_stream=None)
        assert_check_partials(partial_data, atol=tol, rtol=tol)


class TestBreguetPartials(unittest.TestCase):
    def setUp(self):
        nn = 10

        self.prob = om.Problem()
        self.prob.model.add_subsystem(
            "range_comp", RangeComp(num_nodes=nn), promotes=["*"])

        self.prob.model.set_input_defaults(
            "TAS_cruise", 458.8 + 50 * np.random.rand(nn,), units="kn")
        self.prob.model.set_input_defaults(
            "mass", np.linspace(171481, 171481 - 10000, nn), units="lbm")
        self.prob.model.set_input_defaults(
            Dynamic.Mission.FUEL_FLOW_RATE_NEGATIVE_TOTAL, -5870 * np.ones(nn,), units="lbm/h")

        self.prob.setup(check=False, force_alloc_complex=True)

    def test_partials(self):

        tol = 1e-12
        self.prob.run_model()

        # cruise_range = self.prob.get_val("cruise_range", units="NM")
        # cruise_time = self.prob.get_val("cruise_time", units="s")

        # t_expected = 6134.7240144
        # r_expected = 781.83848643
        #
        # assert_near_equal(cruise_range[-1, ...], r_expected, tolerance=0.001)
        # assert_near_equal(cruise_time[-1, ...], t_expected, tolerance=0.001)

        with np.printoptions(linewidth=1024):
            self.prob.model.list_outputs(prom_name=True, print_arrays=True)
            partial_data = self.prob.check_partials(method="cs")  # , out_stream=None)
        assert_check_partials(partial_data, atol=tol, rtol=tol)


class TestBreguetResults(unittest.TestCase):
    def setUp(self):
        self.nn = nn = 100

        self.prob = om.Problem()
        self.prob.model.add_subsystem("range_comp",
                                      RangeComp(num_nodes=nn), promotes=["*"])

        self.prob.setup(check=False, force_alloc_complex=True)

        self.prob.set_val("TAS_cruise", 458.8, units="kn")
        self.prob.set_val("mass", np.linspace(171481, 171481 - 10000, nn), units="lbm")
        self.prob.set_val(Dynamic.Mission.FUEL_FLOW_RATE_NEGATIVE_TOTAL, -
                          5870 * np.ones(nn,), units="lbm/h")

    def test_results(self):
        self.prob.run_model()

        W = self.prob.get_val("mass", units="lbm") * GRAV_ENGLISH_LBM
        V = self.prob.get_val("TAS_cruise", units="kn")
        r = self.prob.get_val("cruise_range", units="NM")
        t = self.prob.get_val("cruise_time", units="h")
        fuel_flow = - \
            self.prob.get_val(
                Dynamic.Mission.FUEL_FLOW_RATE_NEGATIVE_TOTAL, units="lbm/h")

        v_avg = (V[:-1] + V[1:])/2
        fuel_flow_avg = (fuel_flow[:-1] + fuel_flow[1:])/2

        # Range should be equal to the product of initial speed in the segment and change in time
        assert_near_equal(np.diff(r), v_avg * np.diff(t), tolerance=1.0E-5)

        # time should satisfy: dt = -dW / fuel_flow
        assert_near_equal(np.diff(t), -np.diff(W) / fuel_flow_avg, tolerance=1.0E-6)


if __name__ == "__main__":
    unittest.main()
