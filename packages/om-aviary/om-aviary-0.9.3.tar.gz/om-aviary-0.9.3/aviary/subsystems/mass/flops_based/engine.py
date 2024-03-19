import numpy as np
import openmdao.api as om

from aviary.utils.aviary_values import AviaryValues
from aviary.variable_info.functions import add_aviary_input, add_aviary_output
from aviary.variable_info.variables import Aircraft

# TODO should additional misc mass be separated out into a separate component?


class EngineMass(om.ExplicitComponent):
    '''
    Calculate scaled engine mass and additional miscellaneous mass for a
    single named engine model.
    '''

    def initialize(self):
        self.options.declare(
            'aviary_options', types=AviaryValues,
            desc='collection of Aircraft/Mission specific options')

    def setup(self):
        count = len(self.options['aviary_options'].get_val('engine_models'))

        add_aviary_input(self, Aircraft.Engine.SCALED_SLS_THRUST, val=np.zeros(count))

        add_aviary_output(self, Aircraft.Engine.MASS, val=np.zeros(count))
        add_aviary_output(self, Aircraft.Engine.ADDITIONAL_MASS, val=np.zeros(count))
        add_aviary_output(self, Aircraft.Propulsion.TOTAL_ENGINE_MASS, val=0.0)

    def compute(self, inputs, outputs):
        aviary_options: AviaryValues = self.options['aviary_options']

        # cast to numpy arrays to ensure values are always correct type
        num_engines = np.array(aviary_options.get_val(Aircraft.Engine.NUM_ENGINES))
        scaling_parameter = np.array(aviary_options.get_val(Aircraft.Engine.MASS_SCALER))
        scale_mass = np.array(aviary_options.get_val(Aircraft.Engine.SCALE_MASS))
        addtl_mass_fraction = np.array(aviary_options.get_val(
            Aircraft.Engine.ADDITIONAL_MASS_FRACTION))
        ref_engine_mass = np.array(aviary_options.get_val(
            Aircraft.Engine.REFERENCE_MASS, units='lbm'))
        ref_thrust = np.array(aviary_options.get_val(
            Aircraft.Engine.REFERENCE_SLS_THRUST, units='lbf'))

        scaled_thrust = np.array(inputs[Aircraft.Engine.SCALED_SLS_THRUST])

        scale_idx = np.where(scale_mass)
        # indices where scaling is applied and scaling equation is used
        param_idx = np.where(scaling_parameter[scale_idx] >= 0.3)

        # default mass is reference mass
        # use dtype to make complex safe
        calc_mass = np.array(ref_engine_mass, dtype=scaled_thrust.dtype)

        # scale engine mass using equation chosen by value of user-provided mass scalar
        thrust_ratio = scaled_thrust / ref_thrust

        calc_mass[scale_idx] = ref_engine_mass[scale_idx] + (
            scaled_thrust[scale_idx] - ref_thrust[scale_idx]) * scaling_parameter[scale_idx]

        calc_mass[param_idx] = ref_engine_mass[param_idx] * \
            thrust_ratio[param_idx]**scaling_parameter[param_idx]

        addtl_mass = addtl_mass_fraction * calc_mass

        outputs[Aircraft.Engine.MASS] = calc_mass
        outputs[Aircraft.Propulsion.TOTAL_ENGINE_MASS] = sum(
            calc_mass * num_engines)
        outputs[Aircraft.Engine.ADDITIONAL_MASS] = addtl_mass

    def setup_partials(self):
        count = len(self.options['aviary_options'].get_val('engine_models'))
        shape = np.arange(count)

        self.declare_partials(Aircraft.Engine.MASS,
                              Aircraft.Engine.SCALED_SLS_THRUST,
                              rows=shape, cols=shape)
        self.declare_partials(
            Aircraft.Engine.ADDITIONAL_MASS,
            Aircraft.Engine.SCALED_SLS_THRUST,
            rows=shape, cols=shape)
        self.declare_partials(
            Aircraft.Propulsion.TOTAL_ENGINE_MASS,
            Aircraft.Engine.SCALED_SLS_THRUST)

    def compute_partials(self, inputs, J):
        aviary_options: AviaryValues = self.options['aviary_options']
        engine_models = aviary_options.get_val('engine_models')
        count = len(engine_models)

        num_engines = np.array(aviary_options.get_val(Aircraft.Engine.NUM_ENGINES))
        scaling_parameter = np.array(aviary_options.get_val(Aircraft.Engine.MASS_SCALER))
        scale_mass = np.array(aviary_options.get_val(Aircraft.Engine.SCALE_MASS))
        addtl_mass_fraction = np.array(aviary_options.get_val(
            Aircraft.Engine.ADDITIONAL_MASS_FRACTION))
        ref_engine_mass = np.array(aviary_options.get_val(
            Aircraft.Engine.REFERENCE_MASS, units='lbm'))
        ref_sls_thrust = np.array(aviary_options.get_val(
            Aircraft.Engine.REFERENCE_SLS_THRUST, units='lbf'))

        scaled_sls_thrust = np.array(inputs[Aircraft.Engine.SCALED_SLS_THRUST])

        thrust_ratio = scaled_sls_thrust / ref_sls_thrust

        # if the engine mass is not scaled, derivatives default to zero
        thrust_deriv = np.zeros(count, dtype=scaled_sls_thrust.dtype)

        # engine mass derivatives
        # indices where scaling is applied
        scale_idx = np.where(scale_mass)
        # indices where scaling is applied and scaling equation is used
        param_idx = np.where(scaling_parameter[scale_idx] >= 0.3)

        thrust_deriv[scale_idx] = scaling_parameter[scale_idx]
        scaled_mass = ref_engine_mass[param_idx] * \
            thrust_ratio[param_idx]**scaling_parameter[param_idx]
        thrust_deriv[param_idx] = (scaling_parameter[param_idx] *
                                   scaled_mass) / scaled_sls_thrust[param_idx]

        J[Aircraft.Engine.MASS,
            Aircraft.Engine.SCALED_SLS_THRUST
          ] = thrust_deriv

        J[Aircraft.Propulsion.TOTAL_ENGINE_MASS,
            Aircraft.Engine.SCALED_SLS_THRUST
          ] = thrust_deriv * num_engines

        J[Aircraft.Engine.ADDITIONAL_MASS,
            Aircraft.Engine.SCALED_SLS_THRUST
          ] = addtl_mass_fraction * thrust_deriv
