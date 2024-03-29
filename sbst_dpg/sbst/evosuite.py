import subprocess
import datetime
import os
import csv

from sbst_dpg.sbst.sbst import Sbst
from sbst_dpg.configs.configs_manager import ConfigsManager
from sbst_dpg.project import Project
from sbst_dpg.loggers.logger_factory import LoggerFactory


class Evosuite(Sbst):

    def __init__(self):
        super().__init__()
        self.logger = LoggerFactory.get_logger(__class__.__name__)

    def run(self, project, project_path, current_path, sbst_dpg_workspace):
        self.logger.info('Running EvoSuite...')
        project_cp = os.path.join(project_path, ConfigsManager.get_instance().get_project_cp())
        for fq_class_name in project.get_classes():
            clazz = project.get_classes()[fq_class_name]
            time_budget = clazz.get_time_budget()
            tests_dir = sbst_dpg_workspace + '/evosuite-tests'
            report_dir = sbst_dpg_workspace + '/evosuite-report'
            covered_goals_fp = report_dir + '/covered.goals'
            evosuite_logs_out = sbst_dpg_workspace + '/evosuite_logs_out.log'
            run_evosuite_command = current_path + "/evosuite_utils/run-evosuite.sh"
            self.logger.info('Generating tests for %s, time budget - %d seconds' % (fq_class_name, time_budget))
            subprocess.check_call([run_evosuite_command, fq_class_name, project_cp, str(time_budget), covered_goals_fp,
                                   tests_dir, report_dir, '120', '120', '120', '4000', evosuite_logs_out,
                                   current_path + '/evosuite_utils'])
