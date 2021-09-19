import os
import subprocess
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
current_path = current_path[:-9]
try:
    sys.path.index(current_path)
except ValueError:
    sys.path.append(current_path)

os.chmod(os.path.join(current_path, 'defect_predictor_utils', 'prepare-class-list.sh'), 0o777)
os.chmod(os.path.join(current_path, 'evosuite_utils', 'run-evosuite.sh'), 0o777)

from sbst_dpg.configs.configs_manager import ConfigsManager
from sbst_dpg.clazz import Clazz
from sbst_dpg.defect_predictor.defect_predictor_factory import DefectPredictorFactory
from sbst_dpg.project import Project
from sbst_dpg.bads.bads_factory import BADSFactory
from sbst_dpg.sbst.sbst_factory import SbstFactory
from sbst_dpg.loggers.logger_factory import LoggerFactory

PROJECT_PATH = sys.argv[1]


class SBSTDPG:
    defect_predictor = None
    bads = None
    project = Project()
    sbst = None

    def __init__(self, project_path):
        self.project_path = project_path
        self.sbst_dpg_workspace = os.path.join(self.project_path, "sbst_dpg")
        self.configs_manager = ConfigsManager.create_instance(self.sbst_dpg_workspace)
        self.logger = LoggerFactory.get_logger(__class__.__name__)

    def run(self):
        self.load_configs()
        self.defect_predictor = DefectPredictorFactory.get_defect_predictor(ConfigsManager.get_instance()
                                                                            .get_defect_predictor())
        self.run_defect_predictor()
        self.collect_classes_in_project(ConfigsManager.get_instance().get_src_path())
        self.collect_defect_prediction_results()
        self.bads = BADSFactory.get_bads(ConfigsManager.get_instance().get_bads_mode())
        self.run_bads()
        self.sbst = SbstFactory.get_sbst(ConfigsManager.get_instance().get_sbst())
        self.run_sbst()

    def load_configs(self):
        ConfigsManager.get_instance().load_configs()

    def run_defect_predictor(self):
        self.defect_predictor.run(self.project_path, self.sbst_dpg_workspace)

    def collect_classes_in_project(self, src_path):
        current_path = os.path.dirname(os.path.realpath(__file__))
        prepare_class_list_command = current_path + "/defect_predictor_utils/prepare-class-list.sh"
        subprocess.check_call([prepare_class_list_command, self.project_path, src_path, self.sbst_dpg_workspace])

        prepare_class_list_out_file = "all_classes.log"
        with open(os.path.join(self.sbst_dpg_workspace, prepare_class_list_out_file)) as all_classes_file:
            all_classes = all_classes_file.readlines()
            for fq_class_name in all_classes:
                clazz = Clazz(fq_class_name.rstrip("\n"))
                self.project.add_class(clazz)

    def collect_defect_prediction_results(self):
        self.defect_predictor.load_defect_scores(self.project, self.sbst_dpg_workspace)

    def run_bads(self):
        self.bads.allocate_time_budget(self.project, self.defect_predictor.get_time_spent())

    def run_sbst(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.sbst.run(self.project, self.project_path, current_path, self.sbst_dpg_workspace)


if __name__ == '__main__':
    project_path = PROJECT_PATH
    sbst_dpg = SBSTDPG(project_path)
    sbst_dpg.run()
