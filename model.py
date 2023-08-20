from stable_baselines3 import A2C
from stable_baselines3 import DDPG
from stable_baselines3 import PPO
from stable_baselines3 import SAC
from stable_baselines3 import TD3
from env import TradingEnv
from tqdm import tqdm
import gymnasium as gym

MODELS = {
    "A2C": A2C,
    "DDPG": DDPG,
    "PPO": PPO,
    "SAC": SAC,
    "TD3": TD3,
}



class Agent:
    def __init__(self, env, model_name):
        self.env = env
        self.model = self._create_model(model_name)
        
    def _create_model(self, model_name):
        model_name = model_name.upper()
        if model_name not in MODELS:
            raise NotImplementedError("NotImplementedError")
    
        else:
            Model = MODELS[model_name]
            model = Model('MlpPolicy', self.env)
            return model
    
    def update_model(self):
        self.model.learn(total_timesteps=1)
        
    def predict(self,):
        action, _ = self.model.predict()
        return action
    
    

if __name__ == '__main__':
    env = TradingEnv
    agent = Agent(env, "A2C")
    
    total_episodes = 100  # 总共训练的回合数
    max_timesteps = 200   # 每个回合的最大步数
    
    for episode in range(total_episodes):
        obs = env.reset()  # 重置环境
        episode_reward = 0
        
        for t in range(max_timesteps):
            action = agent.predict(obs.reshape(1, -1))  # 预测动作
            obs, reward, done, _ = env.step(action)      # 与环境交互
            episode_reward += reward
            
            if done:
                break
        
        agent.update_model()  # 在每个回合结束后更新模型
        
        print(f"Episode {episode+1}: Total Reward = {episode_reward}")
