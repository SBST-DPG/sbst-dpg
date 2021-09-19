class Clazz:
    defect_score = 0.0
    weight = 0.0
    time_budget = 0
    rank = 0
    tier = 0

    def __init__(self, fq_class_name):
        self.fq_class_name = fq_class_name

    def get_fq_class_name(self):
        return self.fq_class_name

    def set_defect_score(self, defect_score):
        self.defect_score = defect_score

    def get_defect_score(self):
        return self.defect_score

    def set_rank(self, rank):
        self.rank = rank

    def get_rank(self):
        return self.rank

    def set_tier(self, tier):
        self.tier = tier

    def get_tier(self):
        return self.tier

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

    def set_time_budget(self, time_budget):
        self.time_budget = time_budget

    def get_time_budget(self):
        return self.time_budget