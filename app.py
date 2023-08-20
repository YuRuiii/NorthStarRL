from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/learn')
def learn():
    data = request.get_json()
    
@app.route()
    
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    model_name = data['model_name']
    model_path = data['model_path']
    
    