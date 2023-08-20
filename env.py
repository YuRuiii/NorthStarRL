import gymnasium as gym
from gymnasium import spaces
import requests
import random
import time
import matplotlib.pyplot as plt
import numpy as np

class TradingEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    
    def __init__(
        self,
        unified_symbol,
        initial_investment_amount,
        timestep=0
    ):
        self.timestep = timestep
        self.unified_symbol = unified_symbol # 资产代码
        self.initial_investment_amount = initial_investment_amount # 向该资产投入的资金
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,)) # 将多少比例的资产买入或卖出
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(2,), dtype=np.float32)

        # 动作空间：买入、卖出、持有
        self.state = [0.5]
        self.reward = 0
        self.asset_memory = [initial_investment_amount]
        self.price_memory = [0.5]
        self.reward_memory = []
        self.action_memory = []
        self.date_memory = [0]
        self.now_asset = initial_investment_amount
        
    def _get_reward(self, action, last_price, now_price):
        action = action[0] if isinstance(action, (list, np.ndarray)) else action
        data = {
            "action": action[0],
            "last_price": last_price,
            "current_price": now_price
        }
        response = requests.post("http://localhost:5000/get-reward", json=data)
        return response.json()["reward"]
    
    def _get_state(self, timestep, action):
        action = action[0] if isinstance(action, (list, np.ndarray)) else action
        data = {
            "action": action,
            "timestep": timestep
        }
        response = requests.post("http://localhost:5000/get-state", json=data)
        price = response.json()["price"]
        self.price_memory.append(price)
        self.timestep += 1
        self.date_memory.append(self.timestep)
        return [price]
    
    def step(self, action):
        # print(action)
        print(action, self.timestep)
        # self.state = self._get_state(action, self.timestep)
        # self.reward = self._get_reward(action, self.price_memory[-2], self.price_memory[-1])
        # self.now_asset = self.reward * self.now_asset + self.now_asset
        # print(f"timestep: {self.timestep}, action: {action}, state: {self.state:.2f}, reward: {self.reward:.2f}, now_asset: {self.now_asset:.2f}")
        
# if __name__ == '__main__':
#     env = TradingEnv("AAPL", 10)
#     for i in range(100):
#         if env.state < 0.3:
#             action = 1
#         elif env.state > 0.7:
#             action = -1
#         else:
#             action = 0
#         # action = random.uniform(-1, 1)
#         env.step(action)
        
#     plt.plot(env.price_memory)
#     plt.scatter(env.date_memory, env.price_memory, s=10)
#     plt.savefig("price.png", dpi=500)