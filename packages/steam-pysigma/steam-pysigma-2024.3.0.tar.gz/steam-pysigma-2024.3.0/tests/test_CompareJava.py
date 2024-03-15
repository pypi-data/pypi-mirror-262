import difflib
import filecmp
import os
import subprocess
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from steam_pysigma.comsol.BuildComsolModel import BuildComsolModel
from steam_pysigma.data import DataPySIGMA as dS
from steam_pysigma.MainPySIGMA import MainPySIGMA
from steam_pysigma.utils.Utils import get_user_settings, make_folder_if_not_existing, read_data_from_yaml


class TestBuilderSIGMA(unittest.TestCase):

    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.test_folder = Path(__file__).parent
        self.settings = get_user_settings(self.test_folder)
        # self.user_name = getpass.getuser()
        print('\nCurrent folder:          {}'.format(self.test_folder))
        print('\nTest is run from folder: {}'.format(os.getcwd()))

    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.test_folder)  # go back to initial folder

    def setup_magnet(self, magnet_name, test_name):
        output_sigma_path = os.path.join(os.path.dirname(__file__), "output", test_name, magnet_name)
        if os.path.exists(output_sigma_path):
            print("SIGMA directory already exists.")
        else:
            make_folder_if_not_existing(output_sigma_path)

        self.data_input_path = os.path.join(os.path.dirname(__file__), 'input', magnet_name)
        self.working_dir_path = os.path.join(output_sigma_path)  # os.path.join( os.path.dirname(__file__), 'output', 'SIGMA', magnet_name)
        self.reference_path = os.path.join(os.path.dirname(__file__), 'references', magnet_name)
        self.map2d_reference_path = os.path.join(self.reference_path, f'{magnet_name}.map2d')

        self.yaml_file = os.path.join(os.path.dirname(__file__), 'input', magnet_name, magnet_name + "_SIGMA.yaml")

        print('map2d_path:            {}'.format(self.map2d_reference_path))
        print('working_dir:           {}'.format(self.working_dir_path))
        print('reference_path:        {}'.format(self.reference_path))

    def test_compare_java_transient(self):
        test_names = ["test_compare_java_transient_53a", "test_compare_java_transient_60"]
        for test_name in test_names:
            magnet_name = 'MQXA'
            self.setup_magnet(magnet_name, test_name)

            mps = MainPySIGMA(model_folder=self.working_dir_path)
            mps.build(input_yaml_file_path=self.yaml_file, settings=self.settings)
            java_files_names = [f"{magnet_name}_Model_0", f"{magnet_name}_Model"]
            for file in java_files_names:
                file_gen = os.path.join(self.working_dir_path, f"{file}.java")
                file_ref = os.path.join(self.reference_path, f"{file}_REFERENCE.java")
                with open(file_gen) as file_1:
                    file_1_text = file_1.readlines()

                with open(file_ref) as file_2:
                    file_2_text = file_2.readlines()
                # Find and print the diff:
                for line in difflib.unified_diff(
                        file_1_text, file_2_text, fromfile='file1.txt',
                        tofile='file2.txt', lineterm=''):
                    print(line)

                # Assert equals
                print(self.working_dir_path)
                self.assertTrue(filecmp.cmp(os.path.join(self.working_dir_path, file_gen), os.path.join(self.working_dir_path, file_ref)))

    def test_execute_stationary_coordinate_file(self):
        comsol_versions = ["53a", "60"]
        for comsol_version in comsol_versions:
            test_name = f"test_exec_stationary_{comsol_version}"
            magnet_name = 'MQXA'
            self.setup_magnet(magnet_name, test_name)
            try:
                self.settings.comsolexe_path = self.settings.comsolexe_path.replace("53a", comsol_version)
            except:
                print("No 53a version try 60")
            try:
                self.settings.comsolexe_path = self.settings.comsolexe_path.replace("60", comsol_version)
            except:
                raise ValueError("No acceptable comsol versions")
            base_file_name = os.path.splitext(self.yaml_file)[0]
            input_file_path = f'{base_file_name}.yaml'
            self.dm = read_data_from_yaml(f'{base_file_name}.yaml', dS.DataPySIGMA)
            self.sdm = read_data_from_yaml(f'{base_file_name}.set', dS.MultipoleSettings)
            self.roxie_data = read_data_from_yaml(f'{base_file_name}.geom', dS.SIGMAGeometry)
            self.dm.Options_SIGMA.simulation.study_type = "Stationary"
            self.dm.Options_SIGMA.simulation.make_batch_mode_executable = True
            print(os.path.join(self.reference_path, magnet_name, f"{magnet_name}_coordinates_REFERENCE"))
            coordinates = os.path.join(self.reference_path, f"{magnet_name}_coordinates_REFERENCE.csv")
            # #PlotterRoxie.plot_all(self.roxie_data.Roxie_Data)
            bh_curve_database = Path(os.path.dirname(input_file_path), self.dm.Sources.bh_curve_source).resolve()
            BuildComsolModel(model_data=self.dm, input_conductor_params=self.sdm, settings=self.settings,
                             output_path=self.working_dir_path, path_to_results=self.working_dir_path,
                             input_coordinates_path=coordinates, roxie_data=self.roxie_data,
                             bh_curve_database=bh_curve_database)
            os.chdir(self.working_dir_path)
            batch_file_path = os.path.join(self.working_dir_path, f"{magnet_name}_Model_Compile_and_Open.bat")
            print(f'Running Comsol model via: {batch_file_path}')
            proc = subprocess.Popen([batch_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            (stdout, stderr) = proc.communicate()
            if proc.returncode != 0:
                print(stderr)
            else:
                print(stdout)

            df = pd.read_csv(os.path.join(self.working_dir_path, "mf.normB.txt"), sep="\s+|\t+|\s+\t+|\t+\s+",
                             comment='%', names=["x", "y", "Bmod"], engine="python")

            df2 = pd.read_csv(self.map2d_reference_path, delim_whitespace=True)
            df2["Bmod"] = np.sqrt(df2["BX/T"] ** 2 + (df2["BY/T"] ** 2))
            df["Bmod_error"] = abs(df2["Bmod"] - df["Bmod"])
            print(df["Bmod_error"].max())
            Bmod_mean_error = abs(df["Bmod_error"]).mean() * 1000
            Bmod_rel = max(df["Bmod_error"] / max(abs(df["Bmod"])))
            # Defined thresholds
            Bmod_mean_error_thres = 65
            Bmod_rel_thres = 0.03  # Relative error of maximum field strength threshold
            # Assert true
            print(f"Bmod mean error: {Bmod_mean_error} mT")
            print(f"Bmod rel error: {Bmod_rel * 100}%")

            self.assertLessEqual(Bmod_mean_error, Bmod_mean_error_thres)
            self.assertLessEqual(Bmod_rel, Bmod_rel_thres)

    # def test_execute_transient_coordinate_file(self):
    #     comsol_versions = ["53a", "60"]
    #     for comsol_version in comsol_versions:
    #         test_name = f"test_exec_trans_{comsol_version}"
    #         magnet_name = 'MQXA'
    #         self.export_reference_path1 = None
    #         self.setup_magnet(magnet_name,test_name)
    #         if Path.exists(self.system_settings_path):
    #             with open(self.system_settings_path, 'r') as stream:
    #                 self.settings = yaml.safe_load(stream)
    #
    #             # Load yaml input file=
    #         base_file_name = os.path.splitext(self.yaml_file)[0]
    #         self.dm = Util.FilesAndFolders.read_data_from_yaml(f'{base_file_name}.yaml', dS.DataSIGMA)
    #         self.sdm = Util.FilesAndFolders.read_data_from_yaml(f'{base_file_name}.set', dS.MultipoleSettings)
    #         self.roxie_data = Util.FilesAndFolders.read_data_from_yaml(f'{base_file_name}.geom', dS.SIGMAGeometry)
    #         self.export_reference_path1 = os.path.join(self.reference_path, f"I_all_times.txt")
    #         self.dm.Options_SIGMA.simulation.study_type = "Transient"
    #         self.dm.Options_SIGMA.simulation.make_batch_mode_executable = True
    #
    #         self.dm.Options_SIGMA.quench_heaters.th_coils = [1e-3, 1e-3, 1e-3,1e-3, 1e-3, 1e-3, 1e-3, 1e-3]
    #         BuildComsolModel(model_data=self.dm, input_conductor_params=self.sdm, settings=self.settings, output_path=self.working_dir_path, roxie_data=self.roxie_data, bh_curve_database=self.bh_curve_database)
    #         batch_file_path = os.path.join(self.working_dir_path, f"{magnet_name}_Model_Compile_and_Open.bat")
    #         print(f'Running Comsol model via: {batch_file_path}')
    #         subprocess.call(batch_file_path)
    #         proc = subprocess.Popen([batch_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    #         (stdout, stderr) = proc.communicate()
    #         if proc.returncode != 0:
    #             print(stderr)
    #         else:
    #             print(stdout)
    #         df = pd.read_csv(os.path.join(self.working_dir_path, f"I_all_times.txt"),
    #                          sep="\s+|\t+|\s+\t+|\t+\s+", comment='%', names=["t", "I"], engine="python")
    #         df_ref = pd.read_csv(self.export_reference_path1, sep="\s+|\t+|\s+\t+|\t+\s+", comment='%',
    #                              names=["t", "I"],
    #                              engine="python")
    #         df_error = abs(df - df_ref)
    #         print(df_error.head(60))
    #         print(df_error.max())
    #         tolerance = 1
    #         mean_difference = df_error["I"].mean()
    #         self.assertLessEqual(mean_difference, tolerance,
    #                              f"Mean difference: {mean_difference} not is less than tolerance: {tolerance}")
