import subprocess
import datetime
import os
import csv
import shutil

from sbst_dpg.defect_predictor.defect_predictor import DefectPredictor
from sbst_dpg.configs.configs_manager import ConfigsManager
from sbst_dpg.utils.disk_utils import DiskUtils


class Schwa(DefectPredictor):

    def __init__(self):
        super().__init__()

    def run(self, repo_path, workspace):
        current_working_dir = os.getcwd()
        os.chdir(workspace)
        schwa_start_time = datetime.datetime.now()
        schwa_command = "schwa"
        subprocess.check_call([schwa_command, repo_path])
        schwa_end_time = datetime.datetime.now()

        schwa_time = schwa_end_time - schwa_start_time
        self.time_spent = int(schwa_time.total_seconds())

        os.chdir(current_working_dir)
        # schwa_output_file = ConfigsManager.get_instance().get_defect_predictor_out()
        # DiskUtils.safe_move(schwa_output_file, workspace)

    def load_defect_scores(self, project, workspace):
        schwa_output_file = ConfigsManager.get_instance().get_defect_predictor_out()
        with open(os.path.join(workspace, schwa_output_file)) as schwa_output_csv:
            schwa_output_reader = csv.reader(schwa_output_csv, delimiter=",")

            for schwa_result_row in schwa_output_reader:
                fq_class_name = schwa_result_row[0]
                defect_score = schwa_result_row[1]
                if project.class_exists(fq_class_name):
                    project.set_defect_score(fq_class_name, defect_score)
                else:
                    print('Ignored!')

