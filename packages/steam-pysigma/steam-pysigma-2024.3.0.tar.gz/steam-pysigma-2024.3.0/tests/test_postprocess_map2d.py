import os
import unittest

from steam_pysigma.postprocessing.postprocessing import export_B_field_txt_to_map2d


class TestBuildComsolModel(unittest.TestCase):

    def setUp(self):
        pass

    def test_postprocess_mapt2d(self):
        magnet_name = 'MQXA'
        input_folder_path = os.path.join(os.path.dirname(__file__), "input", magnet_name)
        path_map2d_roxie = os.path.join(input_folder_path, f'{magnet_name}_ROXIE.map2d')
        path_result_txt_Bx = os.path.join(input_folder_path, f'mf.Bx.txt')
        path_result_txt_By = os.path.join(input_folder_path, f'mf.By.txt')
        path_new_file = os.path.join(input_folder_path, f'{magnet_name}_SIGMA.map2d')
        export_B_field_txt_to_map2d(path_map2d_roxie, path_result_txt_Bx, path_result_txt_By, path_new_file)