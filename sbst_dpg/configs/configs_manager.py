import os
import yaml


class ConfigsManager:
    configs_file = 'configs.yml'
    instance = None

    defect_predictor = ''
    defect_predictor_out = ''

    bads_mode = ''
    exp_a = 0.0
    exp_b = 0.0
    exp_c = 0.0
    tier_threshold = 0.5
    grouping = '1'
    t_total = 0
    t_total_first_tier = 0
    t_total_second_tier = 0
    t_min_first_tier = 0
    t_min_second_tier = 0

    src_path = ''
    sbst = ''
    project_cp = ''

    primary_logger_type = 'console'
    log_level = 'info'

    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir
        ConfigsManager.instance = self

    def get_yaml_configs(self):
        yaml_path = os.path.join(self.workspace_dir, self.configs_file)
        configs = {}
        if os.path.exists(yaml_path):
            stream = open(yaml_path, "r")
            configs = yaml.load(stream)
        else:
            print('Configs file does not exist: %s' % yaml_path)

        return configs

    @staticmethod
    def get_instance():
        if ConfigsManager.instance is not None:
            return ConfigsManager.instance
        else:
            print('Error')

    @staticmethod
    def create_instance(workspace_dir):
        if ConfigsManager.instance is None:
            ConfigsManager.instance = ConfigsManager(workspace_dir)

        return ConfigsManager.instance

    def load_configs(self):
        configs = self.get_yaml_configs()
        self.defect_predictor = configs.get("defect_predictor").get("name")
        self.defect_predictor_out = configs.get("defect_predictor").get("output_file")

        self.bads_mode = configs.get("bads").get("mode")
        self.exp_a = configs.get("bads").get("e_a")
        self.exp_b = configs.get("bads").get("e_b")
        self.exp_c = configs.get("bads").get("e_c")
        self.tier_threshold = configs.get("bads").get("tier_threshold")
        self.grouping = str(configs.get("bads").get("grouping"))
        self.t_total = configs.get("bads").get("t_total")
        self.t_total_first_tier = configs.get("bads").get("t_total_first_tier")
        self.t_total_second_tier = configs.get("bads").get("t_total_second_tier")
        self.t_min_first_tier = configs.get("bads").get("t_min_first_tier")
        self.t_min_second_tier = configs.get("bads").get("t_min_second_tier")

        self.src_path = configs.get("sbst").get("src_path")
        self.sbst = configs.get("sbst").get("sbst")
        self.project_cp = configs.get("sbst").get("project_classpath")

        self.primary_logger_type = configs.get('log').get('primary_logger_type')
        self.log_level = configs.get('log').get('log_level')

    def get_defect_predictor(self):
        return self.defect_predictor

    def get_src_path(self):
        return self.src_path

    def get_defect_predictor_out(self):
        return self.defect_predictor_out

    def get_tier_threshold(self):
        return self.tier_threshold

    def get_grouping(self):
        return self.grouping

    def get_bads_mode(self):
        return self.bads_mode

    def get_exp_a(self):
        return self.exp_a

    def get_exp_b(self):
        return self.exp_b

    def get_exp_c(self):
        return self.exp_c

    def get_t_total(self):
        return self.t_total

    def get_t_total_first_tier(self):
        return self.t_total_first_tier

    def get_t_total_second_tier(self):
        return self.t_total_second_tier

    def get_t_min_first_tier(self):
        return self.t_min_first_tier

    def get_t_min_second_tier(self):
        return self.t_min_second_tier

    def get_sbst(self):
        return self.sbst

    def get_project_cp(self):
        return self.project_cp
