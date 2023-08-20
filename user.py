import requests

data = {
    "a": 5,
    "b": 7
}

response = requests.post('http://127.0.0.1:5000/add', json=data)
result = response.json()
print(result)  # 输出：{'result': 12}
