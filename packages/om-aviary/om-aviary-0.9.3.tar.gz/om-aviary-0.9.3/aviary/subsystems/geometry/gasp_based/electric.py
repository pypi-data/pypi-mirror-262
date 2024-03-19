import openmdao.api as om

from aviary.utils.aviary_values import AviaryValues
from aviary.variable_info.functions import add_aviary_input, add_aviary_output
from aviary.variable_info.variables import Aircraft


class CableSize(om.ExplicitComponent):

    def initialize(self):

        self.options.declare(
            'aviary_options', types=AviaryValues,
            desc='collection of Aircraft/Mission specific options'
        )

    def setup(self):

        add_aviary_input(self, Aircraft.Engine.WING_LOCATIONS, val=0.35)

        add_aviary_input(self, Aircraft.Wing.SPAN, val=128)

        add_aviary_input(self, Aircraft.Fuselage.AVG_DIAMETER, val=10)

        add_aviary_output(self, Aircraft.Electrical.HYBRID_CABLE_LENGTH, val=0)

        self.declare_partials(
            Aircraft.Electrical.HYBRID_CABLE_LENGTH,
            [
                Aircraft.Engine.WING_LOCATIONS,
                Aircraft.Wing.SPAN,
            ],
        )

        self.declare_partials(
            Aircraft.Electrical.HYBRID_CABLE_LENGTH,
            Aircraft.Fuselage.AVG_DIAMETER,
            val=2.)

    def compute(self, inputs, outputs):

        eng_span_frac = inputs[Aircraft.Engine.WING_LOCATIONS]
        wingspan = inputs[Aircraft.Wing.SPAN]
        cabin_width = inputs[Aircraft.Fuselage.AVG_DIAMETER]

        outputs[Aircraft.Electrical.HYBRID_CABLE_LENGTH] = (
            eng_span_frac * wingspan + 2.0 * cabin_width
        )

    def compute_partials(self, inputs, J):

        eng_span_frac = inputs[Aircraft.Engine.WING_LOCATIONS]
        wingspan = inputs[Aircraft.Wing.SPAN]

        J[
            Aircraft.Electrical.HYBRID_CABLE_LENGTH,
            Aircraft.Engine.WING_LOCATIONS,
        ] = wingspan
        J[Aircraft.Electrical.HYBRID_CABLE_LENGTH, Aircraft.Wing.SPAN] = eng_span_frac
