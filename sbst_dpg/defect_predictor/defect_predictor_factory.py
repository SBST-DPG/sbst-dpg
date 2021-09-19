from sbst_dpg.defect_predictor.schwa import Schwa


class DefectPredictorFactory:

    @staticmethod
    def get_defect_predictor(dp_type):
        if dp_type == "Schwa":
            return Schwa()
        else:
            print('Unsupported defect predictor type!')