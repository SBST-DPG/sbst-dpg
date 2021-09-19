from sbst_dpg.sbst.evosuite import Evosuite
from sbst_dpg.utils.logging_utils import LoggingUtils


class SbstFactory:

    @staticmethod
    def get_sbst(sbst_type):
        if sbst_type == "EvoSuite":
            return Evosuite()
        else:
            LoggingUtils.error('Unsupported SBST tool - %s' % sbst_type)
