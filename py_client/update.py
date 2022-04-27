import requests



endpoint = "http://localhost:8000/api/products/1/update/"

data ={
    "title":"hello world title changed",
    "price":134
}


get_response = requests.put(endpoint,json=data)

print(get_response.json())
