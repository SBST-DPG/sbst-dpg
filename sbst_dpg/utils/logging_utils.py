import numpy as np
from sbst_dpg.configs.configs_manager import ConfigsManager


class LoggingUtils:
    instance = None

    def __init__(self):
        self.primary_logger_type = ConfigsManager.get_instance().primary_logger_type
        self.log_level = ConfigsManager.get_instance().log_level

    @staticmethod
    def get_instance():
        if LoggingUtils.instance is None:
            LoggingUtils.instance = LoggingUtils()

        return LoggingUtils.instance

    def debug(self, message):
        if self.log_level == 'debug':
            print(message)

    def info(self, message):
        if self.log_level == 'info':
            print(message)

    def warn(self, message):
        print(message)

    def error(self, message):
        print(message)

    def get_log_level(self):
        return self.log_level
