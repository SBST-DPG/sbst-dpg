from sbst_dpg.bads.exp_bads import ExpBADS
from sbst_dpg.configs.configs_manager import ConfigsManager
from sbst_dpg.utils.logging_utils import LoggingUtils


class BADSFactory:

    @staticmethod
    def get_bads(mode):
        if mode == "exp":
            return ExpBADS(ConfigsManager.get_instance().get_exp_a(), ConfigsManager.get_instance().get_exp_b(),
                           ConfigsManager.get_instance().get_exp_c())
        else:
            LoggingUtils.get_instance().error('Unsupported BADS type - %s' % mode)
