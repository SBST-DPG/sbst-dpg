from sbst_dpg.sbst.evosuite import Evosuite


class SbstFactory:

    @staticmethod
    def get_sbst(sbst_type):
        if sbst_type == "EvoSuite":
            return Evosuite()
        else:
            print('Error')
