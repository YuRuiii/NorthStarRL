import math
from random import random
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get-price', methods=['POST'])
def get_price():
    data = request.get_json()
    print("data", data)
    timestamp = data['timestep']
    response_data = {
        # "price": 0.25 * math.sin(timestamp) + 0.25 * math.sin(2 * timestamp) + 0.5 * math.sin(3 * timestamp)
        "price": math.sin(0.01 * timestamp)
    }
    return jsonify(response_data)

@app.route('/get-reward', methods=['POST'])
def get_reward():
    data = request.get_json()
    balance = data['balance']
    initial_balance = data['initial_balance']
    reward = balance - initial_balance
    response_data = {
        "reward": reward
    }
    return jsonify(response_data)
    

if __name__ == '__main__':
    app.run()
