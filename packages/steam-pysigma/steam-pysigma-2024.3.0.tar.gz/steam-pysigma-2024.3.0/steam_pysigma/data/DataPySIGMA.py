from typing import Dict, List, Union, Literal, Optional

from pydantic import BaseModel

from steam_pysigma.data.DataRoxieParser import RoxieData


class MultipoleMono(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Mono']
    bare_cable_width: Optional[float] = None
    bare_cable_height_mean: Optional[float] = None
    th_insulation_along_height: Optional[float] = None
    th_insulation_along_width: Optional[float] = None
    Rc: Optional[float] = None
    Ra: Optional[float] = None
    bare_cable_height_low: Optional[float] = None
    bare_cable_height_high: Optional[float] = None
    n_strands: Optional[int] = None
    n_strands_per_layers: Optional[int] = None
    n_strand_layers: Optional[int] = None
    strand_twist_pitch: Optional[float] = None
    width_core: Optional[float] = None
    height_core: Optional[float] = None
    strand_twist_pitch_angle: Optional[float] = None
    f_inner_voids: Optional[float] = None
    f_outer_voids: Optional[float] = None


class MultipoleRibbon(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Ribbon']
    bare_cable_width: Optional[float] = None
    bare_cable_height_mean: Optional[float] = None
    th_insulation_along_height: Optional[float] = None
    th_insulation_along_width: Optional[float] = None
    Rc: Optional[float] = None
    Ra: Optional[float] = None
    bare_cable_height_low: Optional[float] = None
    bare_cable_height_high: Optional[float] = None
    n_strands: Optional[int] = None
    n_strands_per_layers: Optional[int] = None
    n_strand_layers: Optional[int] = None
    strand_twist_pitch: Optional[float] = None
    width_core: Optional[float] = None
    height_core: Optional[float] = None
    strand_twist_pitch_angle: Optional[float] = None
    f_inner_voids: Optional[float] = None
    f_outer_voids: Optional[float] = None


class MultipoleRutherford(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Rutherford']
    bare_cable_width: Optional[float] = None
    bare_cable_height_mean: Optional[float] = None
    th_insulation_along_height: Optional[float] = None
    th_insulation_along_width: Optional[float] = None
    Rc: Optional[float] = None
    Ra: Optional[float] = None
    bare_cable_height_low: Optional[float] = None
    bare_cable_height_high: Optional[float] = None
    n_strands: Optional[int] = None
    n_strands_per_layers: Optional[int] = None
    n_strand_layers: Optional[int] = None
    strand_twist_pitch: Optional[float] = None
    width_core: Optional[float] = None
    height_core: Optional[float] = None
    strand_twist_pitch_angle: Optional[float] = None
    f_inner_voids: Optional[float] = None
    f_outer_voids: Optional[float] = None


class MultipoleRoxieGeometry(BaseModel):
    """
        Class for FiQuS multipole Roxie data (.geom)
    """
    Roxie_Data: RoxieData = RoxieData()


class Jc_FitSIGMA(BaseModel):
    type: Optional[str] = None
    C1_CUDI1: Optional[float] = None
    C2_CUDI1: Optional[float] = None


class StrandSIGMA(BaseModel):
    filament_diameter: Optional[float] = None
    diameter: Optional[float] = None
    f_Rho_effective: Optional[float] = None
    fil_twist_pitch: Optional[float] = None
    RRR: Optional[float] = None
    T_ref_RRR_high: Optional[float] = None
    Cu_noCu_in_strand: Optional[float] = None


class MultipoleGeneralSetting(BaseModel):
    """
        Class for general information on the case study
    """
    I_ref: Optional[List[float]] = None


class MultipoleConductor(BaseModel):
    """
        Class for conductor type
    """
    cable: Union[MultipoleRutherford, MultipoleRibbon, MultipoleMono] = {'type': 'Rutherford'}
    strand: StrandSIGMA = StrandSIGMA()
    Jc_fit: Jc_FitSIGMA = Jc_FitSIGMA()


class MultipoleModelDataSetting(BaseModel):
    """
        Class for model data
    """
    general_parameters: MultipoleGeneralSetting = MultipoleGeneralSetting()
    conductors: Dict[str, MultipoleConductor] = {}


class MultipoleSettings(BaseModel):
    """
        Class for FiQuS multipole settings (.set)
    """
    Model_Data_GS: MultipoleModelDataSetting = MultipoleModelDataSetting()


class SourcesClass(BaseModel):
    bh_curve_source: Optional[str] = None


class GeneralParametersClass(BaseModel):
    magnet_name: Optional[str] = None
    T_initial: Optional[float] = None
    magnetic_length: Optional[float] = None


class PowerSupply(BaseModel):
    I_initial: Optional[float] = None


class SIGMAGeometry(BaseModel):
    """
        Class for Roxie data
    """
    Roxie_Data: RoxieData = RoxieData()


class QuenchHeaters(BaseModel):
    N_strips: Optional[int] = None
    t_trigger: Optional[List[float]] = None
    U0: Optional[List[float]] = None
    C: Optional[List[float]] = None
    R_warm: Optional[List[float]] = None
    w: Optional[List[float]] = None
    h: Optional[List[float]] = None
    s_ins: Optional[List[float]] = None
    type_ins: Optional[List[float]] = None
    s_ins_He: Optional[List[float]] = None
    type_ins_He: Optional[List[float]] = None
    l: Optional[List[float]] = None
    l_copper: Optional[List[float]] = None
    l_stainless_steel: Optional[List[float]] = None
    f_cover: Optional[List[float]] = None


class Cliq(BaseModel):
    t_trigger: Optional[float] = None
    sym_factor: Optional[int] = None
    U0: Optional[float] = None
    I0: Optional[float] = None
    C: Optional[float] = None
    R: Optional[float] = None
    L: Optional[float] = None


class CircuitClass(BaseModel):
    R_circuit: Optional[float] = None
    L_circuit: Optional[float] = None
    R_parallel: Optional[float] = None


class QuenchProtection(BaseModel):
    Quench_Heaters: QuenchHeaters = QuenchHeaters()
    CLIQ: Cliq = Cliq()


class TimeVectorSolutionSIGMA(BaseModel):
    time_step: List[List[float]] = None


class Simulation(BaseModel):
    generate_study: Optional[bool] = None
    study_type: Optional[str] = None
    make_batch_mode_executable: bool = None
    nbr_elements_mesh_width: Optional[int] = None
    nbr_elements_mesh_height: Optional[int] = None


class Physics(BaseModel):
    FLAG_M_pers: Optional[int] = None
    FLAG_ifcc: Optional[int] = None
    FLAG_iscc_crossover: Optional[int] = None
    FLAG_iscc_adjw: Optional[int] = None
    FLAG_iscc_adjn: Optional[int] = None
    tauCC_PE: Optional[int] = None


class QuenchInitialization(BaseModel):
    PARAM_time_quench: Optional[float] = None
    FLAG_quench_all: Optional[int] = None
    FLAG_quench_off: Optional[int] = None
    num_qh_div: Optional[List[int]] = None
    th_coils: Optional[List[float]] = None
    quench_init_heat: Optional[float] = None
    quench_init_HT: Optional[List[str]] = None
    quench_stop_temp: Optional[float] = None


class Out2DAtPoints(BaseModel):
    coordinate_source: Optional[str] = None
    variables: Optional[List[str]] = None
    time: Optional[List[List[float]]] = None
    map2d: Optional[str] = None


class Out1DVsTimes(BaseModel):
    variables: Optional[List[str]] = None
    time: Optional[List[List[float]]] = None


class Out1DVsAllTimes(BaseModel):
    variables: Optional[List[str]] = None


class Postprocessing(BaseModel):
    out_2D_at_points: Out2DAtPoints = Out2DAtPoints()
    out_1D_vs_times: Out1DVsTimes = Out1DVsTimes()
    out_1D_vs_all_times: Out1DVsAllTimes = Out1DVsAllTimes()


class QuenchHeatersSIGMA(BaseModel):
    quench_heater_positions: Optional[List[List[int]]] = None
    th_coils: Optional[List[float]] = None


class SIGMA(BaseModel):
    time_vector_solution: TimeVectorSolutionSIGMA = TimeVectorSolutionSIGMA()
    simulation: Simulation = Simulation()
    physics: Physics = Physics() 
    quench_initialization: QuenchInitialization = QuenchInitialization()
    postprocessing: Postprocessing = Postprocessing()
    quench_heaters: QuenchHeatersSIGMA = QuenchHeatersSIGMA()


class DataPySIGMA(BaseModel):
    Sources: SourcesClass = SourcesClass()
    GeneralParameters: GeneralParametersClass = GeneralParametersClass()
    Power_Supply: PowerSupply = PowerSupply()
    Quench_Protection: QuenchProtection = QuenchProtection()
    Options_SIGMA: SIGMA = SIGMA()
    Circuit: CircuitClass = CircuitClass()
