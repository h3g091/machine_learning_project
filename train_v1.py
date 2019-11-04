from src.dqn import DQN
from src.sokoban_env import SokobanEnv
from src.dqn_optimizer import DqnOptimizer
from src.training_loop import train_model

import os
if not os.path.exists("model"):
    os.mkdir("model")

import warnings
warnings.filterwarnings('ignore')

BATCH_SIZE = 128
GAMMA = 0.50
EPS_START = 0.99
EPS_END = 0.05
EPS_DECAY = 2000
TARGET_UPDATE = 10
MEM_SIZE = 25000
NUM_EPISODES = 10

env = SokobanEnv()

init_screen = env.get_screen()
_, _, screen_height, screen_width = init_screen.shape

# Get number of actions from gym action space
n_actions = env.action_space.n

policy_net = DQN(screen_height, screen_width, n_actions).to(env.device)
target_net = DQN(screen_height, screen_width, n_actions).to(env.device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

dqn_optimizer = DqnOptimizer(policy_net, target_net, env.device, BATCH_SIZE, MEM_SIZE, GAMMA)
train_model(dqn_optimizer, env, NUM_EPISODES, TARGET_UPDATE)
env.reset()
