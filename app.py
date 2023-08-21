from stable_baselines3 import A2C
from stable_baselines3 import DDPG
from stable_baselines3 import PPO
from stable_baselines3 import SAC
from stable_baselines3 import TD3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
from flask import Flask, request, jsonify
from env import TradingEnv

AGENTS = {
    "A2C": A2C,
    "DDPG": DDPG,
    "PPO": PPO,
    "SAC": SAC,
    "TD3": TD3,
}

app = Flask(__name__)
env = TradingEnv()
class Model:
    def __init__(self, env):
        self.env = env
        self.agent = None
        
    @app.route('/create-agent', methods=['POST'])
    def create_agent(self):
        data = request.get_json()
        agent = data['agent']
        agent = AGENTS[agent.upper()]("MlpPolicy", env, verbose=1)
        return agent
    
    @app.route('/create-agent-from-pretrained', methods=['POST'])
    def create_agent_from_pretrained(self):
        data = request.get_json()
        agent = data['agent']
        agent_path = data['agent_path']
        agent = AGENTS[agent.upper()].load(agent_path)
        return agent
        

    @app.route('/learn', methods=['POST'])
    def learn(self):
        data = request.get_json()
        total_episodes = data['total_episodes']
        self.agent.learn(total_timesteps=total_episodes)
        return self.agent
    
    @app.route('/predict', methods=['POST'])
    def predict(self):
        data = request.get_json()
        action, _ = self.agent.predict(data)
        return action

app.run(port=5001)
    