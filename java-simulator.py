import math
from random import random
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get-state', methods=['POST2'])
def get_state(data):
    data = request.get_json()
    timestamp = data['timestamp']
    response_data = {
        # "price": 0.25 * math.sin(timestamp) + 0.25 * math.sin(2 * timestamp) + 0.5 * math.sin(3 * timestamp)
        "price": math.sin(0.01 * timestamp)
    }
    return jsonify(response_data)

@app.route('/get-reward', methods=['POST'])
def get_reward():
    data = request.get_json()
    action = data['action']
    last_price = data['last_price']
    current_price = data['current_price']
    reward = action * (current_price - last_price)
    response_data = {
        "reward": reward
    }
    return jsonify(response_data)
    

if __name__ == '__main__':
    app.run()
