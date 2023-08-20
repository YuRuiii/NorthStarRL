import numpy as np
import gym
import requests
from gym import spaces
from stable_baselines3 import PPO

def _get_price(timestep):
    data = {
        "timestep": timestep
    }
    response = requests.post("http://localhost:5000/get-price", json=data)
    price = response.json()["price"]
    return price

def _get_reward(action, balance, initial_balance):
    data = {
        "balance": balance,
        "initial_balance": initial_balance
    }
    response = requests.post("http://localhost:5000/get-reward", json=data)
    reward = response.json()["reward"]
    return reward


class TradingEnv(gym.Env):
    def __init__(self, initial_balance=10000):
        super(TradingEnv, self).__init__()

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
        price = _get_price(self.current_step)
        
        # 根据动作执行交易
        if action == 0:  # 买入
            self.balance -= price
        elif action == 1:  # 卖出
            self.balance += price
        else:  # 持有
            pass

        self.current_step += 1

        # 计算奖励
        # reward = self.balance - self.initial_balance
        reward = _get_reward(action, self.balance, self.initial_balance)

        # 检查是否达到最大步数
        done = self.current_step >= self.max_steps

        # 返回观察、奖励、终止标志和额外信息
        obs = np.array([self.balance, self.current_step])
        return obs, reward, done, {}

# 创建自定义交易环境
env = TradingEnv()

# 创建PPO代理
model = PPO("MlpPolicy", env, verbose=1)

# 训练代理
model.learn(total_timesteps=10000)
model.save("ppo_trading")

# 测试代理
obs = env.reset()
for _ in range(10):
    action, _ = model.predict(obs)  # 使用代理进行预测
    obs, reward, done, _ = env.step(action)
    print("Balance:", obs[0], "Step:", obs[1], "Reward:", reward, "Done:", done)
    if done:
        break