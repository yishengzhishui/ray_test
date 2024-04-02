import gymnasium as gym
from ray.rllib.algorithms.ppo import PPOConfig

# 使用 python 和 Farama-Foundation 的 gymnasium API 定义你的问题：
# 定义了一个简单的走廊环境，继承自 gym.Env 类。这个环境有一个起始点（S）和一个终点（G），智能体需要通过向右移动到达终点。
class SimpleCorridor(gym.Env):
    """
    一个智能体必须学会向右移动以达到出口的走廊。

        ---------------------
        | S | 1 | 2 | 3 | G |   S=起点; G=终点; 走廊长度=5
        ---------------------

        可供选择的动作有：0=左移; 1=右移
        观察结果是浮点数，表示当前位置的索引，例如，起始位置为 0.0，起始位置的下一个位置为 1.0，以此类推。
        奖励为每一步都是 -0.1，除非到达终点（+1.0）。
    """

    # 初始化走廊环境，设置走廊的长度、当前位置、动作空间和观察空间。
    def __init__(self, config):
        self.end_pos = config["corridor_length"]
        self.cur_pos = 0
        self.action_space = gym.spaces.Discrete(2)  # 左移和右移
        self.observation_space = gym.spaces.Box(0.0, self.end_pos, shape=(1,))

    def reset(self, *, seed=None, options=None):
        """重置环境。

        返回：
           新的 episode 的初始观察值和一个信息字典。
        """
        self.cur_pos = 0
        # 返回初始观察值。
        return [self.cur_pos], {}

    def step(self, action):
        """执行一个动作，更新环境状态。

        返回：
            新的观察值、奖励、终止标志、截断标志和信息字典（空）。
        """
        # 向左移动。
        if action == 0 and self.cur_pos > 0:
            self.cur_pos -= 1
        # 向右移动。
        elif action == 1:
            self.cur_pos += 1
        # 当到达走廊的末端（终点）时设置 `terminated` 标志。
        terminated = self.cur_pos >= self.end_pos
        truncated = False
        # 当到达终点时奖励为 +1，否则为 -0.1。
        reward = 1.0 if terminated else -0.1
        return [self.cur_pos], reward, terminated, truncated, {}


# 使用 PPOConfig 对象创建一个 RLlib 算法实例。
config = (
    PPOConfig().environment(
        # 使用的环境类（这里使用我们上面定义的 gym.Env 子类）。
        env=SimpleCorridor,
        # 传递给自定义环境构造函数的配置字典。
        # 使用包括 S 和 G 在内的 20 个字段的走廊。
        env_config={"corridor_length": 28},
    )
    # 并行执行环境回合。
    .rollouts(num_rollout_workers=3)
)
# 根据配置对象构建实际的（PPO）算法对象。
algo = config.build()

# 进行 n 次迭代训练并报告结果（平均 episode 奖励）。
# 由于在环境中至少需要移动 19 次才能到达终点，每次移动都会获得 -0.1 的奖励（最后一次在终点获得 +1.0），
# 我们期望达到的最佳 episode 奖励为 -0.1*18 + 1.0 = -0.8。
for i in range(5):
    results = algo.train()
    print(f"Iter: {i}; avg. reward={results['episode_reward_mean']}")

# 基于给定的环境观察值执行推理（动作计算）。
# 注意，这里使用了一个稍微不同的环境（长度为 10 而不是 20），
# 但是，这应该仍然有效，因为智能体（希望）已经学会“总是向右移动”！
env = SimpleCorridor({"corridor_length": 10})
# 获取初始观察值（应该是起始位置的 [0.0]）。
obs, info = env.reset()
terminated = truncated = False
total_reward = 0.0
# 进行一次 episode。
while not terminated and not truncated:
    # 根据环境当前观察值计算一个动作。
    action = algo.compute_single_action(obs)
    # 将计算得到的动作应用到环境中。
    obs, reward, terminated, truncated, info = env.step(action)
    # 汇总奖励以供报告。
    total_reward += reward
# 报告结果。
print(f"Played 1 episode; total-reward={total_reward}")
