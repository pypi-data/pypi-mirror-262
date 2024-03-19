import os
import unittest
from pathlib import Path

from steam_pysigma.data import DataPySIGMA as dS
from steam_pysigma.comsol.BuildComsolModel import BuildComsolModel
from steam_pysigma.plotters.PlotterPysigma import plot_magnet
from steam_pysigma.utils.Utils import get_user_settings, make_folder_if_not_existing, read_data_from_yaml


class TestBuildComsolModel(unittest.TestCase):

    def setUp(self):
        self.test_folder = Path(__file__).parent
        self.settings = get_user_settings(self.test_folder)

    def test_plot_magnet(self):
        magnet_names = ["MQXB", "MED_C_COMB", "MB_2COILS"] # Tests one normal multipole, one assymetric coil and one with elliptic arcs
        for magnet_name in magnet_names:
            working_dir_path = os.path.join(Path(os.path.dirname(__file__)), "output", 'plotters', magnet_name)
            make_folder_if_not_existing(working_dir_path)
            input_file_path = os.path.join(Path(os.path.dirname(__file__)).parent, 'tests', 'input', magnet_name, magnet_name + "_SIGMA.yaml")
            base_file_name = os.path.splitext(input_file_path)[0]
            dm = read_data_from_yaml(f'{base_file_name}.yaml', dS.DataPySIGMA)
            sdm = read_data_from_yaml(f'{base_file_name}.set', dS.MultipoleSettings)
            roxie_data = read_data_from_yaml(f'{base_file_name}.geom', dS.SIGMAGeometry)
            dm.Options_SIGMA.simulation.study_type = "Stationary"
            dm.Options_SIGMA.simulation.make_batch_mode_executable = True
            bh_curve_database = Path(os.path.dirname(input_file_path), dm.Sources.bh_curve_source).resolve()
            bcm = BuildComsolModel(model_data=dm, input_conductor_params=sdm, settings=self.settings,
                             output_path=working_dir_path, path_to_results=working_dir_path,
                             input_coordinates_path=None, roxie_data=roxie_data,
                             bh_curve_database=bh_curve_database)

            plot_magnet(bcm.iron_yoke_areas, bcm.wedge_areas, bcm.roxie_data)
