from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/learn')
def learn():
    data = request.get_json()
    agent = data['algorithm']
    if agent.lower() == 'ppo':
        
    else:
        assert 0
        
    
    
@app.route()
    
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    model_path = data['model_path']
    
    