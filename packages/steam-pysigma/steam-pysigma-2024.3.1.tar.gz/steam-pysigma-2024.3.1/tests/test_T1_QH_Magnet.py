import os
import unittest
from pathlib import Path
import pandas as pd

import steam_pysigma.sigma.pysigma as ps
from steam_pysigma.data.DataPySIGMA import DataPySIGMA as dS
from steam_pysigma.utils.Utils import get_user_settings, run, build_global_variables, build_study, create_results, read_data_from_yaml


class TestT0QHMagnet(unittest.TestCase):


    def setUp(self):
        self.magnet_name = "Magnet_T1_QH"
        self.model_yaml = Path.joinpath(Path(__file__).parent, "input/T1/T1_Magnet.yaml")
        self.input_coordinates_path = ""
        self.g = ps.GatewaySIGMA()
        self.a = ps.ArraysSIGMA
        self.model_name = self.magnet_name
        if not os.path.exists(Path.joinpath(Path(__file__).parent, "../tests/output")):
            os.mkdir(Path.joinpath(Path(__file__).parent, "../tests/output"))
        self.reference_path = Path.joinpath(Path(__file__).parent, "references")

        self.split_java_file_path = []

        self.test_folder = Path(__file__).parent
        self.settings = get_user_settings(self.test_folder)
        self.COMSOL_compile_path = os.path.join(Path(self.settings.comsolexe_path).parent, 'comsolcompile.exe')
        self.COMSOL_batch_path = os.path.join(Path(self.settings.comsolexe_path).parent, 'comsolbatch.exe')
        self.COMSOL_version = os.path.basename(os.path.dirname(Path(self.settings.comsolexe_path).parent.parent.parent)).replace("COMSOL",
                                                                                                            "")
        self.java_jdk_path = self.settings.JAVA_jdk_path

        self.model_data = read_data_from_yaml(self.model_yaml, dS)
        self.run_study = self.model_data.Options_SIGMA.simulation.make_batch_mode_executable
        self.timeRange = ", ".join(["range(" + ", ".join(map(str, lst)) + ")" for lst in
                                   self.model_data.Options_SIGMA.time_vector_solution.time_step])


    def test_1_T1_QH_Magnet_Transient_Coord_File_Run_Quenched_Magnet(self):
        comsol_versions = ["53a", "60"]
        for comsol_version in comsol_versions:
            self.working_dir_path = Path.joinpath(Path(__file__).parent,
                                                  f"/output/T1/test_1_{comsol_version}")
            self.input_folder_sigma_path = os.path.join(self.working_dir_path, 'input')
            self.output_folder_sigma_path = os.path.join(self.working_dir_path, 'output')

            self.model_java_file_path = f"{os.path.join(self.input_folder_sigma_path, self.magnet_name)}.java"
            self.study_type = "Transient"
            self.export_reference_path1 = os.path.join(self.reference_path, f"I_ref_T1_test1_{comsol_version}.txt")
            self.export_reference_path2 = os.path.join(self.reference_path, f"T_T1_test1_{comsol_version}.txt")

            self.compile_batch_file_path = f"{os.path.join(self.input_folder_sigma_path, self.model_name)}_Compile_and_Open.bat"
            self.model_class_file_path = f"{os.path.join(self.input_folder_sigma_path, self.model_name)}.class"
            self.model_data.Options_SIGMA.quench_heaters.quench_heater_positions = [[2, 12, 22, 32],
                                      [94, 104, 114, 124]]
            if os.path.exists(self.input_folder_sigma_path):
                print("SIGMA directory already exists.")
            else:
                if not os.path.isdir(self.input_folder_sigma_path):
                    Path(self.input_folder_sigma_path).mkdir(parents=True, exist_ok=True)

            if os.path.exists(self.output_folder_sigma_path):
                print("SIGMA directory already exists.")
            else:
                if not os.path.isdir(self.output_folder_sigma_path):
                    Path(self.output_folder_sigma_path).mkdir(parents=True, exist_ok=True)
            self.numOfQH = self.model_data.Quench_Protection.Quench_Heaters.N_strips
            self.qh_positions = self.model_data.Options_SIGMA.quench_heaters.quench_heater_positions
            self.funLibPath = self.settings.CFunLibPath
            self.quench_init_HTs = self.model_data.Options_SIGMA.quench_initialization.quench_init_HT
            quench_init_heat = self.model_data.Options_SIGMA.quench_initialization.quench_init_heat
            setupConfigSIGMA = ps.SetupConfigSIGMA(self.g, self.model_java_file_path, self.COMSOL_batch_path,
                                                   self.COMSOL_compile_path, self.funLibPath, self.run_study,
                                                   self.numOfQH, self.study_type, self.qh_positions,
                                                   self.quench_init_HTs, quench_init_heat)

            cfg = setupConfigSIGMA.cfg


            QHPositions = self.g.gateway.jvm.java.util.ArrayList()
            for qh in self.model_data.Options_SIGMA.quench_heaters.quench_heater_positions:
                temp = self.g.gateway.jvm.java.util.ArrayList()
                for pos in qh:
                    temp.add(pos)
                QHPositions.add(temp)
            cfg.setQHPositions(QHPositions)
            magnet = self.g.Magnet_T1_QH()
            domains = magnet.getDomains()
            srv = self.g.TxtSigmaServer(cfg.getOutputModelPath(), cfg.getComsolBatchPath(), cfg.getComsolCompilePath())
            srv.connect(cfg.getComsolBatchPath())
            # Initiate variables
            self.input_coordinates_path =(os.path.join(Path.joinpath(Path(__file__).parent, "input/T1/T1_Magnet_coordinates.csv"))).replace("\\", "\\\\\\\\")
            funlibreader = ps.FunLibCSVReader()
            funlib_map = funlibreader.read_csv_funclib_create_hashmap(self.g)
            # Create map for all variables that we input in sigma.
            globalMap = build_global_variables(self.g, self.model_data)
            globalMap.put("I_0", "11.96e3")
            globalMap.put("tauCC_PE", str(self.model_data.Options_SIGMA.physics.tauCC_PE))
            self.model = self.g.MagnetMPHBuilder(cfg, srv)
            self.model.buildMPH(self.a.create_domain_array(self.g.gateway, tuple(domains)), globalMap, 4, 1, funlib_map)
            if cfg.getNumOfQHs() > 0:
                builderQH = self.g.QuenchHeaterMPHBuilder(cfg, srv)
                self.model.connectToServer()
                builderQH.buildQuenchHeaterMPH()

            build_study(self.study_type, srv, cfg, self.g.StudyAPI, self.timeRange)
            # Define result nodes>

            variables2DConverted = self.model_data.Options_SIGMA.postprocessing.out_2D_at_points.variables  # List of all exported variables
            time2DConverted = self.model_data.Options_SIGMA.postprocessing.out_2D_at_points.time  # List of all exported time
            variables1DvsTime = self.model_data.Options_SIGMA.postprocessing.out_1D_vs_all_times.variables
            time1DConverted = self.model_data.Options_SIGMA.postprocessing.out_1D_vs_times.time
            variables1DvsTimeVector = self.model_data.Options_SIGMA.postprocessing.out_1D_vs_times.variables

            create_results(srv, cfg, variables1DvsTime, time2DConverted, variables2DConverted, time1DConverted,
                           variables1DvsTimeVector, self.g.ResultsAPI,
                           self.input_coordinates_path, self.output_folder_sigma_path)
            srv.build(cfg.getOutputModelPath())

            self.model.save()

            run(self.magnet_name, self.input_folder_sigma_path, self.model_java_file_path, self.model_class_file_path,
                self.input_folder_sigma_path, self.model_name, self.split_java_file_path, self.COMSOL_compile_path,
                self.COMSOL_batch_path, self.compile_batch_file_path, self.java_jdk_path)

            df = pd.read_csv(os.path.join(self.output_folder_sigma_path,f"I_all_times.txt"), sep="\s+|\t+|\s+\t+|\t+\s+", comment='%', names=["t", "I"], engine="python")
            df_ref = pd.read_csv(self.export_reference_path1, sep="\s+|\t+|\s+\t+|\t+\s+", comment='%', names=["t", "I"],
                                 engine="python")
            df_error = abs(df - df_ref)
            print(df_error.head(60))
            print(df_error.max())
            tolerance = 1
            mean_difference = df_error["I"].mean()
            self.assertLessEqual(mean_difference, tolerance,
                                 f"Mean difference: {mean_difference} not is less than tolerance: {tolerance}")
            df = pd.read_csv(os.path.join(self.output_folder_sigma_path,f"T.txt"), sep="\s+|\t+|\s+\t+|\t+\s+", comment='%', names=["x", "y", "T"], engine="python")
            df_ref = pd.read_csv(self.export_reference_path2, sep="\s+|\t+|\s+\t+|\t+\s+", comment='%', names=["x","y", "T"],
                                 engine="python")
            df_error = abs(df - df_ref).dropna()
            print(df_error.head(60))
            print(df_error.max())
            tolerance = 1
            mean_difference = df_error["T"].mean()
            self.assertLessEqual(mean_difference, tolerance,
                                 f"Mean difference: {mean_difference} not is less than tolerance: {tolerance}")

if __name__ == '__main__':
    unittest.main()
