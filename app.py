from stable_baselines3 import A2C
from stable_baselines3 import DDPG
from stable_baselines3 import PPO
from stable_baselines3 import SAC
from stable_baselines3 import TD3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
from flask import Flask, request, jsonify
from env import TradingEnv

MODELS = {
    "A2C": A2C,
    "DDPG": DDPG,
    "PPO": PPO,
    "SAC": SAC,
    "TD3": TD3,
}

app = Flask(__name__)
env = TradingEnv()
class Agent:
    def __init__(self, env):
        self.env = env
        self.model = self.create_model()
        
    @app.route('/create-model', methods=['POST'])
    def create_model(self):
        data = request.get_json()
        agent = data['algorithm']
        if agent.upper() == 'PPO':
            model = PPO("MlpPolicy", env, verbose=1)
        else:
            assert 0
        return model

    @app.route('/learn')
    def learn(self):
        self.model.learn(total_timesteps=10000)
        return self.model
    
    @app.route('/predict', methods=['POST'])
    def predict(self):
        data = request.get_json()
        
        action, _ = self.model.predict(data)
        return action

app.run(port=8080)
    