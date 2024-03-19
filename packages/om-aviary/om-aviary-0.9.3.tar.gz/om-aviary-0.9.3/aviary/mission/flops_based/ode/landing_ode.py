'''
Define the ODEs for landing.

Classes
-------
FlareODE : the ODE for the flare phase of landing
'''
import numpy as np
import openmdao.api as om
from dymos.models.atmosphere.atmos_1976 import USatm1976Comp

from aviary.mission.flops_based.ode.landing_eom import FlareEOM, StallSpeed
from aviary.mission.flops_based.ode.takeoff_ode import TakeoffODE as _TakeoffODE
from aviary.mission.gasp_based.flight_conditions import FlightConditions
from aviary.utils.aviary_values import AviaryValues
from aviary.utils.functions import set_aviary_initial_values, promote_aircraft_and_mission_vars
from aviary.variable_info.variables import Aircraft, Dynamic, Mission
from aviary.variable_info.variables_in import VariablesIn


class ExternalSubsystemGroup(om.Group):
    def configure(self):
        promote_aircraft_and_mission_vars(self)


class LandingODE(_TakeoffODE):
    '''
    Define the ODE for most phases of landing.
    '''
    # region : derived type customization points
    stall_speed_lift_coefficient_name = Mission.Landing.LIFT_COEFFICIENT_MAX
    # endregion : derived type customization points


class FlareODE(om.Group):
    '''
    Define the ODE for the flare phase of landing.
    '''

    def initialize(self):
        options = self.options

        options.declare(
            'num_nodes', default=1, types=int,
            desc='Number of nodes to be evaluated in the RHS')

        options.declare(
            'aviary_options', types=AviaryValues,
            desc='collection of Aircraft/Mission specific options')

        self.options.declare(
            'subsystem_options', types=dict, default={},
            desc='dictionary of parameters to be passed to the subsystem builders')

        self.options.declare(
            'core_subsystems',
            desc='list of core subsystem builder instances to be added to the ODE'
        )
        self.options.declare(
            'external_subsystems', default=[],
            desc='list of external subsystem builder instances to be added to the ODE')

    def setup(self):
        options = self.options

        nn = options["num_nodes"]
        aviary_options = options['aviary_options']
        subsystem_options = options['subsystem_options']
        core_subsystems = options['core_subsystems']

        self.add_subsystem(
            'input_port', VariablesIn(aviary_options=aviary_options),
            promotes_inputs=['*'], promotes_outputs=['*'])

        self.add_subsystem(
            "USatm",
            USatm1976Comp(num_nodes=nn),
            promotes_inputs=[("h", Dynamic.Mission.ALTITUDE)],
            promotes_outputs=[
                "rho", ("sos", Dynamic.Mission.SPEED_OF_SOUND), ("temp",
                                                                 Dynamic.Mission.TEMPERATURE),
                ("pres", Dynamic.Mission.STATIC_PRESSURE), "viscosity"])

        self.add_subsystem(
            "fc",
            FlightConditions(num_nodes=nn),
            promotes_inputs=["rho", Dynamic.Mission.SPEED_OF_SOUND,
                             ("TAS", Dynamic.Mission.VELOCITY)],
            promotes_outputs=[Dynamic.Mission.DYNAMIC_PRESSURE, Dynamic.Mission.MACH, "EAS"])

        # NOTE: the following are potentially signficant differences in implementation
        # between FLOPS and Aviary:
        #    - FLOPS detailed takeoff/landing assumes constant mass for the duration of
        #      that specific analysis.
        #    - Aviary implementation of FLOPS based detailed takeoff/landing will allow
        #      mass to vary as needed as a function of time and variation in related
        #      optimization control variables.
        self.add_subsystem(
            "stall_speed", StallSpeed(num_nodes=nn),
            promotes_inputs=[
                "mass",
                ("density", "rho"),
                ('area', Aircraft.Wing.AREA),
                ("lift_coefficient_max", Mission.Landing.LIFT_COEFFICIENT_MAX),
            ],
            promotes_outputs=[("stall_speed", "v_stall")])

        base_options = {'num_nodes': nn, 'aviary_inputs': aviary_options}

        for subsystem in core_subsystems:
            # check if subsystem_options has entry for a subsystem of this name
            if subsystem.name in subsystem_options:
                kwargs = subsystem_options[subsystem.name]
            else:
                kwargs = {}

            kwargs.update(base_options)
            system = subsystem.build_mission(**kwargs)

            if system is not None:
                self.add_subsystem(subsystem.name,
                                   system,
                                   promotes_inputs=subsystem.mission_inputs(**kwargs),
                                   promotes_outputs=subsystem.mission_outputs(**kwargs))

        # Create a lightly modified version of an OM group to add external subsystems
        # to the ODE with a special configure() method that promotes
        # all aircraft:* and mission:* variables to the ODE.
        external_subsystem_group = ExternalSubsystemGroup()
        add_subsystem_group = False

        for subsystem in self.options['external_subsystems']:
            subsystem_mission = subsystem.build_mission(
                num_nodes=nn, aviary_inputs=aviary_options)
            if subsystem_mission is not None:
                add_subsystem_group = True
                external_subsystem_group.add_subsystem(subsystem.name, subsystem_mission)

        # Only add the external subsystem group if it has at least one subsystem.
        # Without this logic there'd be an empty OM group added to the ODE.
        if add_subsystem_group:
            self.add_subsystem(
                name='external_subsystems',
                subsys=external_subsystem_group,
                promotes_inputs=['*'],
                promotes_outputs=['*'])

        kwargs = {
            'num_nodes': nn,
            'aviary_options':  options['aviary_options']}

        self.add_subsystem(
            'eoms',
            FlareEOM(**kwargs),
            promotes_inputs=[
                Dynamic.Mission.FLIGHT_PATH_ANGLE, Dynamic.Mission.VELOCITY, Dynamic.Mission.MASS, Dynamic.Mission.LIFT,
                Dynamic.Mission.THRUST_TOTAL, Dynamic.Mission.DRAG, 'angle_of_attack',
                'angle_of_attack_rate', Mission.Landing.FLARE_RATE
            ],
            promotes_outputs=[
                Dynamic.Mission.DISTANCE_RATE, Dynamic.Mission.ALTITUDE_RATE, Dynamic.Mission.VELOCITY_RATE,
                Dynamic.Mission.FLIGHT_PATH_ANGLE_RATE, 'forces_perpendicular',
                'required_thrust', 'net_alpha_rate'
            ]
        )

        self.add_subsystem(
            'comp_v_ratio',
            om.ExecComp(
                'v_over_v_stall = v / v_stall',
                v_over_v_stall={'units': 'unitless', 'shape': nn},
                v={'units': 'm/s', 'shape': nn},
                # NOTE: FLOPS detailed takeoff stall speed is not dynamic - see above
                v_stall={'units': 'm/s', 'shape': nn}),
            promotes_inputs=[('v', Dynamic.Mission.VELOCITY), 'v_stall'],
            promotes_outputs=['v_over_v_stall'])

        self.set_input_defaults(Dynamic.Mission.ALTITUDE, np.zeros(nn), 'm')
        self.set_input_defaults(Dynamic.Mission.VELOCITY, np.zeros(nn), 'm/s')

        set_aviary_initial_values(self, aviary_options)
