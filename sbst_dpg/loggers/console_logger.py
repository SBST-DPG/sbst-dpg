from sbst_dpg.loggers.logger import Logger
from datetime import datetime


class ConsoleLogger(Logger):

    def __init__(self, class_name, log_level):
        super().__init__(class_name, log_level)

    def debug(self, message):
        if self.log_level == 'debug':
            current_datetime = datetime.now()
            print('[DEBUG][' + str(current_datetime) + '][' + self.class_name + '] ' + message)

    def info(self, message):
        if self.log_level == 'info':
            current_datetime = datetime.now()
            print('[INFO][' + str(current_datetime) + '][' + self.class_name + '] ' + message)

    def warn(self, message):
        current_datetime = datetime.now()
        print('[WARN][' + str(current_datetime) + '][' + self.class_name + '] ' + message)

    def error(self, message):
        current_datetime = datetime.now()
        print('[ERROR][' + str(current_datetime) + '][' + self.class_name + '] ' + message)