import collections
import math


class Project:
    classes = dict()

    def get_classes(self):
        return self.classes

    def get_clazzes(self):
        return self.classes.values()

    def set_classes(self, classes):
        self.classes = classes

    def add_class(self, clazz):
        self.classes[clazz.get_fq_class_name()] = clazz

    def class_exists(self, fq_class_name):
        return fq_class_name in self.classes

    def set_defect_score(self, fq_class_name, defect_score):
        self.classes[fq_class_name].set_defect_score(defect_score)

