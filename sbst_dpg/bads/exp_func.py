import math
from sbst_dpg.loggers.logger_factory import LoggerFactory


class ExpFunc:
    exp_a = 0.0
    exp_b = 0.0
    exp_c = 0.0

    def __init__(self, exp_a, exp_b, exp_c):
        self.logger = LoggerFactory.get_logger(__class__.__name__)
        self.logger.debug('Initiating exponential function. Coefficients - e_a = %f, e_b = %f, e_c = %f' %
                          (exp_a, exp_b, exp_c))
        self.exp_a = exp_a
        self.exp_b = exp_b
        self.exp_c = exp_c

    def y(self, x):
        return self.exp_a + self.exp_b * math.exp(self.exp_c * x)