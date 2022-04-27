import requests



endpoint = "http://localhost:8000/api/products/1/delete/"


get_response = requests.delete(endpoint)

print(get_response.status_code,get_response.status_code==204)
