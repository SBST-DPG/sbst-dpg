from sbst_dpg.defect_predictor.schwa import Schwa
from sbst_dpg.utils.logging_utils import LoggingUtils


class DefectPredictorFactory:

    @staticmethod
    def get_defect_predictor(dp_type):
        if dp_type == "Schwa":
            return Schwa()
        else:
            LoggingUtils.get_instance().error('Unsupported defect predictor type - %s' % dp_type)
