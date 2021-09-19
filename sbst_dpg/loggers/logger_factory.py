from sbst_dpg.loggers.console_logger import ConsoleLogger
from sbst_dpg.utils.logging_utils import LoggingUtils


class LoggerFactory:

    @staticmethod
    def get_logger(class_name):
        if LoggingUtils.get_instance().primary_logger_type == "console":
            log_level = LoggingUtils.get_instance().get_log_level()
            return ConsoleLogger(class_name, log_level)
        else:
            print('Error')
