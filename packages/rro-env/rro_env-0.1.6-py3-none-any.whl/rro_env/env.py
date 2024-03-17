import numpy as np
import gymnasium as gym
from gymnasium import spaces
import rro_env.docker as docker
import rro_env.utils as utils


class DockerYardEnv(gym.Env):
    def __init__(self, train_type=4):
        super(DockerYardEnv, self).__init__()
        self.docker_game = None
        self.block = '01'
        self.yard_width = 16
        self.yard_height = 15
        self.yard_depth = 4
        self.train_type = train_type

        self.action_map = {}
        self.observation_list = []
        self.observation_map_item_map = {
            'BAY': 0,
            'ROW': 1,
            'TIER': 2,
            # Whether to apply for an order, those who have already applied for an order will be earlier
            'IF_USED': 3,
            # Whether it is customs inspection, those that have been inspected will be earlier.
            'IF_CHECK': 4,
            # Whether to buckle the box, the buckle box will last longer.
            'IF_BLOCK': 5,
            # Those who have done the designated cabinet may turn the box over.
            'IF_ASSIGN': 6,
            # If the homework task is bound, it may be picked up faster (after the order is processed).
            'IF_BIND': 7,
            # Appointment for the fastest pick-up of the homework task (after binding)
            'IF_BOOK': 8,
            # Actual storage days
            'REAL_DIFF': 9,
            # Forecast pick-up date - today's date
            'REMAIN_DIFF': 10,
            # Predict how many days to bring up later
            'PRE_DIFF': 11,
            # bill lading refrerence id
            'BILL_LADING_REF_ID': 12,
            # consignor name
            'CONSIGNOR_NAME': 13,
            # container type
            'CONTAINER_TYPE': 14,
            # Domestic and foreign trade, domestic trade customs do not check, foreign trade needs customs release
            'INSIDE_OR_OUTSIDE': 15,
            # Import and Export
            'IMPORT_OR_EXPORT': 16,
            # Heavy or empty
            'CONTAINER_STATE': 17,
            # if the container is in the yard
            'HAD_CONTAINER': 18,
            # reload times
            'REPLACE_TIMES': 19,
            # operation type
            'OPERATION_TYPE': 20
        }

        self.success_times = 0
        self.wrong_times = 0
        self.total_reward = 0
        self.total_wrong_time = 0
        self.total_reward_list = []
        self.total_detail_list = []
        self.total_wrong_times_list = []
        self.able_wrong_times = 300
        self.action_space = None
        self.observation_space = None
        self.create_game()

    @staticmethod
    def seed(self, seed=None):
        np.random.seed(seed)

    def create_game(self):
        self.total_wrong_time = 0
        docker_game_options = docker.DockerGameOptions(self.block, self.yard_width, self.yard_height,
                                                       self.yard_depth, train_type=self.train_type)
        self.docker_game = docker.DockerGame(docker_game_options)
        self.docker_game.create_game()
        self.action_map = self.docker_game.get_action_space()
        self.observation_list = self.docker_game.get_observation_space()

        self.action_space = spaces.Discrete(len(self.action_map.keys()))
        min_row = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        max_row = [3, 15, 4, 1, 1, 1, 1, 1, 1, 200, len(self.docker_game.cache_bill_map.keys()),
                   len(self.docker_game.cache_consignor_map.keys()), 40, 1, 1, 1, 1, 50, 3, self.able_wrong_times]
        self.observation_space = spaces.Box(
            low=np.float32([min_row for _ in range(len(self.observation_list))]),
            high=np.float32([max_row for _ in range(len(self.observation_list))])
        )

    def reset(self, **kwargs):
        seed = kwargs.get('seed', None)
        if seed is not None:
            pass
        self.create_game()
        source_observation_space = np.array(self.docker_game.get_observation_space())
        self.success_times = 0
        self.wrong_times = 0
        self.total_reward = 0
        return source_observation_space, {}

    def render(self):
        pass

    def step(self, action):
        step_reward = 0
        current_observation = None
        current_operation_status = self.observation_list[-1]
        action = self.action_map[action]
        terminated = False
        truncated = False
        if len(self.docker_game.operation_list) > 0:
            if (action[0] != 0 and action[1] != 0 and action[-1] != 0) or (
                    action[0] == 0 and action[1] == 0 and action[-1] == 2):
                action_operation_type = action[-1]
                current_operation_type = current_operation_status[
                    self.observation_map_item_map['OPERATION_TYPE'] - 2]
                current_container_size = current_operation_status[
                    self.observation_map_item_map['CONTAINER_TYPE'] - 2]
                if action_operation_type == current_operation_type:
                    if action_operation_type == 1 or action_operation_type == 3:
                        # 入堆或移箱
                        container_bay = action[0]
                        container_row = action[1]
                        c_stack = f'{self.docker_game.options.block}{utils.to_double(container_bay)}{utils.to_double(container_row)}'
                        c_stack_obj = self.docker_game.yard_stack_map[c_stack]
                        able_tier = c_stack_obj['NUMS'] + 1
                        action_pile = f'{self.docker_game.options.block}{utils.to_double(container_bay)}{utils.to_double(container_row)}{able_tier}'
                        able_pile_list = self.docker_game.get_able_pile_list()
                        if len(able_pile_list) > 0:
                            if action_pile in able_pile_list:
                                action_info = self.docker_game.take_action(action_pile)
                                self.success_times += 1
                                step_reward = action_info[2]
                                if action_operation_type == 1:
                                    step_reward = step_reward
                                current_observation = self.docker_game.get_observation_space()
                                # action success, reset wrong times
                                self.wrong_times = 0
                            else:
                                self.wrong_times += 1
                                self.total_wrong_time += 1
                        else:
                            self.wrong_times += 1
                            self.total_wrong_time += 1
                    elif action_operation_type == 2:
                        action_info = self.docker_game.take_action()
                        self.success_times += 1
                        step_reward = action_info[2]
                        current_observation = self.docker_game.get_observation_space()
                        self.wrong_times = 0
                else:
                    self.wrong_times += 1
                    self.total_wrong_time += 1
            else:
                self.wrong_times += 1
                self.total_wrong_time += 1
        else:
            action_info = self.docker_game.take_action()
            self.success_times += 1
            step_reward = action_info[2]

        if self.wrong_times >= self.able_wrong_times:
            terminated = True
            step_reward -= self.docker_game.reward_map['finish']
            self.total_wrong_times_list.append(self.total_wrong_time)
        if self.docker_game.game_over:
            truncated = True
        if current_observation is None:
            current_observation = self.observation_list
        else:
            self.observation_list = current_observation
        current_observation[-1][-1] = self.wrong_times
        self.total_reward += step_reward
        if terminated or truncated:
            self.total_reward_list.append(self.total_reward)
            self.total_detail_list.append(self.docker_game.get_cur_info())
        return np.array(current_observation), step_reward, terminated, truncated, {}