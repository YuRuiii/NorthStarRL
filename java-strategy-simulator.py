import argparse
import requests
from env import TradingEnv

class RLStrategy:
    def __init__(self, args): # 初始化
        if args.is_train:
            self.create_agent(args)
            if args.learn_now:
                self.learn(args)
        else:
            self.crate_agent_from_pretrained(args)
        
    def create_agent(self, args): # 创建Agent
        data = {
            "agent": args.agent
        }
        response = requests.post("http://localhost:5001/create-agent", json=data)
        print(response)
    
    def create_agent_from_pretrained(self, args):
        data = {
            "agent": args.agent,
            "agent_path": args.agent_path
        }
        response = requests.post("http://localhost:5001/create-agent-from-pretrained", json=data)
        print(response)
        
    def learn(self, args):
        data = {
            "total_episodes": args.total_episodes
        }
        response = requests.post("http://localhost:5001/learn", json=data)
        print(response)
        
    def predict(self, time):
        data = {
            "time": time
        }
        response = requests.post("http://localhost:5001/predict", json=data)
        print(response)
            
    def onTick(self, tick):
        time = tick.getActionTime()
        action = self.predict(time)
        
        # 根据action执行交易
        

# 传递参数
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--is_train", type=bool, default=False, help="是否训练模型")
    parser.add_argument("--learn_now", type=bool, default=False, help="是否训练模型")
    parser.add_argument("--agent", type=str, default="PPO", help="强化学习Agent的名称")
    parser.add_argument("--initial_balance", type=int, default=10000, help="初始资金")
    
    # 如果训练模型，需要传递的参数
    parser.add_argument("--total_episodes", type=int, default=100, help="总共训练的回合数")
    parser.add_argument("--max_timesteps", type=int, default=200, help="每个回合的最大步数")
    
    # 如果使用模型，需要传递的参数
    parser.add_argument("--model_path", type=str, default="ppo_trading.zip", help="模型路径")
    
    return parser.parse_args()
    
    
if __name__ == "__main__":
    args = parse_args()
    strategy = RLStrategy(args)
    strategy.predict(1)