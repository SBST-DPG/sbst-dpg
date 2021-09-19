import collections
import math

from sbst_dpg.bads.bads import BADS
from sbst_dpg.configs.configs_manager import ConfigsManager
from sbst_dpg.clazz import Clazz
from sbst_dpg.bads.exp_func import ExpFunc
from sbst_dpg.loggers.logger_factory import LoggerFactory


class ExpBADS(BADS):
    exp_func = None

    def __init__(self, exp_a, exp_b, exp_c):
        self.logger = LoggerFactory.get_logger(__class__.__name__)
        self.exp_func = ExpFunc(exp_a, exp_b, exp_c)

    def allocate_time_budget(self, project, time_spent_dp):
        self.logger.info('Starting ExpBADS...')
        self.rank_classes(project)
        self.assign_tiers(project)
        self.assign_weights(project)
        self.assign_time_budgets(project, time_spent_dp)
        allocated_time_budget = 0
        for clazz in project.get_clazzes():
            allocated_time_budget += clazz.get_time_budget()
        print('Allocated time budget - %d' % allocated_time_budget)

    def rank_classes(self, project):
        self.logger.debug('Ranking classes by defect scores.')
        classes = project.get_classes()
        classes = sorted(classes.items(), key=lambda kv: kv[1].get_defect_score(), reverse=True)
        classes = collections.OrderedDict(classes)
        project.set_classes(classes)    # check if this is necessary

        current_rank = 1
        for clazz in classes.values():
            clazz.set_rank(current_rank)
            self.logger.debug('%s - %d' % (clazz.get_fq_class_name(), current_rank))
            current_rank += 1

    def assign_tiers(self, project):
        tier_threshold = ConfigsManager.get_instance().get_tier_threshold()
        self.logger.debug('Assigning tiers. Tier threshold - %f' % tier_threshold)
        classes = project.get_classes()
        num_classes = len(classes)
        num_classes_first_tier = math.ceil(num_classes * tier_threshold)
        for clazz in classes.values():
            if clazz.get_rank() <= num_classes_first_tier:
                clazz.set_tier(1)
                self.logger.debug('%s - %d' % (clazz.get_fq_class_name(), 1))
            else:
                clazz.set_tier(2)
                self.logger.debug('%s - %d' % (clazz.get_fq_class_name(), 2))

    def assign_weights(self, project):
        self.logger.debug('Assigning weights.')
        group_size = self.get_group_size(len(project.get_classes()))
        self.logger.debug('Group size - %d' % group_size)
        self.assign_weights_in_tier(1, project, group_size)
        self.assign_weights_in_tier(2, project, group_size)

    def assign_weights_in_tier(self, tier, project, group_size):
        self.logger.debug('Assigning weights in tier - %d' % tier)
        num_classes = sum(map(lambda x: x.get_tier() == tier, project.get_clazzes()))
        self.logger.debug('# Classes in tier - %d' % num_classes)

        num_groups = math.ceil(num_classes / group_size)
        last_group_size = num_classes % group_size

        exp_func_step_size_x = 1 / (num_groups - 1)

        weights = dict()
        weights_sum = 0.0
        for group_index in range(1, num_groups + 1):
            x = (group_index - 1) * exp_func_step_size_x
            weight = self.exp_func.y(x)
            weights[group_index] = weight
            if group_index == num_groups:
                weights_sum += weight * last_group_size
            else:
                weights_sum += weight * group_size

        weights_norm = self.normalise_weights(weights, weights_sum)

        rank_offset = 0
        if tier == 2:
            num_classes_first_tier = 0
            for clazz in project.get_clazzes():
                if clazz.get_tier() == 1:
                    num_classes_first_tier += 1
            rank_offset = num_classes_first_tier

        for clazz in project.get_clazzes():
            if clazz.get_tier() != tier:
                continue

            group_index = math.ceil((clazz.get_rank() - rank_offset) / group_size)
            clazz.set_weight(weights_norm[group_index])
            self.logger.debug('%s - %f' % (clazz.get_fq_class_name(), clazz.get_weight()))

    def get_group_size(self, num_classes):
        grouping = ConfigsManager.get_instance().get_grouping()
        if 'p' in grouping:
            loc_p = grouping.find('p')
            grouping = grouping[0:loc_p]
            return math.ceil((int(grouping) * num_classes) / 100)
        else:
            return 1

    def normalise_weights(self, weights, weights_sum):
        weights_norm = dict()
        for group_index, weight in weights.items():
            weights_norm[group_index] = weight / weights_sum

        return weights_norm

    def assign_time_budgets(self, project, time_spent_dp):
        self.logger.debug('Assigning time budgets to classes.')
        t_min_of_tiers = dict()
        t_min_of_tiers[1] = ConfigsManager.get_instance().get_t_min_first_tier()
        t_min_of_tiers[2] = ConfigsManager.get_instance().get_t_min_second_tier()
        self.logger.debug('t_min of tier 1 - %d seconds' % t_min_of_tiers[1])
        self.logger.debug('t_min of tier 2 - %d seconds' % t_min_of_tiers[2])

        num_classes = len(project.get_classes())
        num_classes_of_tiers = dict()
        num_classes_of_tiers[1] = sum(map(lambda x: x.get_tier() == 1, project.get_clazzes()))
        num_classes_of_tiers[2] = sum(map(lambda x: x.get_tier() == 2, project.get_clazzes()))

        t_total = ConfigsManager.get_instance().get_t_total() * num_classes
        t_total_of_tiers = dict()
        t_total_of_tiers[1] = ConfigsManager.get_instance().get_t_total_first_tier() * num_classes_of_tiers[1]
        t_total_of_tiers[2] = ConfigsManager.get_instance().get_t_total_second_tier() * num_classes_of_tiers[2]
        self.logger.debug('t_total per class of tier 1 - %d seconds' %
                          ConfigsManager.get_instance().get_t_total_first_tier())
        self.logger.debug('t_total per class of tier 2 - %d seconds' %
                          ConfigsManager.get_instance().get_t_total_second_tier())
        self.logger.debug('t_total of tier 1 - %d seconds' % t_total_of_tiers[1])
        self.logger.debug('t_total of tier 2 - %d seconds' % t_total_of_tiers[2])

        time_spent_dp_of_tiers = dict()
        time_spent_dp_of_tiers[1] = (time_spent_dp / num_classes) * num_classes_of_tiers[1]
        time_spent_dp_of_tiers[2] = (time_spent_dp / num_classes) * num_classes_of_tiers[2]
        self.logger.debug('Time spent by DP for tier 1 - %f seconds' % time_spent_dp_of_tiers[1])
        self.logger.debug('Time spent by DP for tier 2 - %f seconds' % time_spent_dp_of_tiers[2])

        self.assign_time_budgets_in_tier(1, project, t_total_of_tiers[1], num_classes_of_tiers[1], t_min_of_tiers[1],
                                         time_spent_dp_of_tiers[1])
        self.assign_time_budgets_in_tier(2, project, t_total_of_tiers[2], num_classes_of_tiers[2], t_min_of_tiers[2],
                                         time_spent_dp_of_tiers[2])

    def assign_time_budgets_in_tier(self, tier, project, t_total, num_classes, t_min, time_spent_dp):
        self.logger.debug('Assigning time budgets in tier - %d' % tier)
        variable_budget = t_total - num_classes * t_min - time_spent_dp
        self.logger.debug('Variable budget - %f seconds' % variable_budget)
        for clazz in project.get_clazzes():
            if clazz.get_tier() != tier:
                continue

            time_budget = 0
            if variable_budget > 0:
                time_budget = int(clazz.get_weight() * variable_budget + t_min)
            else:
                time_budget = int((t_total - time_spent_dp) / num_classes)

            clazz.set_time_budget(time_budget)
            self.logger.debug('%s - %d seconds' % (clazz.get_fq_class_name(), time_budget))
