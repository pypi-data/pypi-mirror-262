import unittest

import numpy as np
import openmdao.api as om
from dymos.models.atmosphere.atmos_1976 import USatm1976Comp
from openmdao.utils.assert_utils import (assert_check_partials,
                                         assert_near_equal)

from aviary.constants import RHO_SEA_LEVEL_METRIC
from aviary.mission.gasp_based.ode.unsteady_solved.unsteady_solved_flight_conditions import \
    UnsteadySolvedFlightConditions
from aviary.variable_info.enums import SpeedType
from aviary.variable_info.variables import Dynamic, Mission


class TestUnsteadyFlightConditions(unittest.TestCase):

    def _test_unsteady_flight_conditions(self, ground_roll=False, input_speed_type=SpeedType.TAS):
        nn = 5

        p = om.Problem()

        p.model.add_subsystem("atmos",
                              USatm1976Comp(num_nodes=nn),
                              promotes_inputs=["*", ("h", Dynamic.Mission.ALTITUDE)],
                              promotes_outputs=["*", ("sos", Dynamic.Mission.SPEED_OF_SOUND)])

        p.model.add_subsystem("fc",
                              UnsteadySolvedFlightConditions(num_nodes=nn,
                                                             ground_roll=ground_roll,
                                                             input_speed_type=input_speed_type),
                              promotes_inputs=["*"],
                              promotes_outputs=["*"])

        p.setup(force_alloc_complex=True)

        if input_speed_type is SpeedType.TAS:
            p.set_val(Dynamic.Mission.ALTITUDE, 37500, units="ft")
            p.set_val("TAS", 250, units="kn")
            p.set_val("dTAS_dr", np.zeros(nn), units="kn/km")
        elif input_speed_type is SpeedType.EAS:
            p.set_val(Dynamic.Mission.ALTITUDE, 37500, units="ft")
            p.set_val("EAS", 250, units="kn")
            p.set_val("dEAS_dr", np.zeros(nn), units="kn/km")
        else:
            p.set_val(Dynamic.Mission.ALTITUDE, 37500, units="ft")
            p.set_val(Dynamic.Mission.MACH, 0.78, units="unitless")
            p.set_val("dmach_dr", np.zeros(nn), units="unitless/km")

        p.run_model()

        mach = p.get_val(Dynamic.Mission.MACH)
        eas = p.get_val("EAS")
        tas = p.get_val("TAS", units="m/s")
        sos = p.get_val(Dynamic.Mission.SPEED_OF_SOUND, units="m/s")
        rho = p.get_val("rho", units="kg/m**3")
        rho_sl = RHO_SEA_LEVEL_METRIC
        dTAS_dt_approx = p.get_val("dTAS_dt_approx")

        assert_near_equal(mach, tas/sos)
        assert_near_equal(eas, tas * np.sqrt(rho / rho_sl))
        assert_near_equal(dTAS_dt_approx, np.zeros(nn))

        p.run_model()

        with np.printoptions(linewidth=1024):
            cpd = p.check_partials(method="cs")
        assert_check_partials(cpd)

    def test_unsteady_flight_conditions(self):

        for ground_roll in True, False:
            for in_type in [SpeedType.TAS, SpeedType.EAS, SpeedType.MACH]:
                with self.subTest(msg=f"ground_roll={ground_roll} in_type={in_type}"):
                    self._test_unsteady_flight_conditions(
                        ground_roll=ground_roll, input_speed_type=in_type)
