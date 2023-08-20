import numpy as np
import gym
from gym import spaces

class CustomTradingEnv(gym.Env):
    def __init__(self, initial_balance=10000):
        super(CustomTradingEnv, self).__init__()

        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.current_step = 0
        self.max_steps = 100  # 最大步数

        # 观察空间：包括账户余额和当前步数
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(2,), dtype=np.float32)

        # 动作空间：买入、卖出、持有
        self.action_space = spaces.Discrete(3)

    def reset(self):
        self.balance = self.initial_balance
        self.current_step = 0
        return np.array([self.balance, self.current_step])

    def step(self, action):
        assert self.action_space.contains(action)

        # 模拟股价变动
        price = np.random.uniform(10, 50)
        
        # 根据动作执行交易
        if action == 0:  # 买入
            self.balance -= price
        elif action == 1:  # 卖出
            self.balance += price
        else:  # 持有
            pass

        self.current_step += 1

        # 计算奖励
        reward = self.balance - self.initial_balance

        # 检查是否达到最大步数
        done = self.current_step >= self.max_steps

        # 返回观察、奖励、终止标志和额外信息
        obs = np.array([self.balance, self.current_step])
        return obs, reward, done, {}

# 创建自定义交易环境
env = CustomTradingEnv()

# 重置环境
obs = env.reset()

# 进行交易
for _ in range(10):
    action = env.action_space.sample()  # 随机选择动作
    obs, reward, done, _ = env.step(action)
    print("Balance:", obs[0], "Step:", obs[1], "Reward:", reward, "Done:", done)
    if done:
        break
