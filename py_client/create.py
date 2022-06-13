import requests

endpoint = "http://localhost:8000/api/blog/create/"

data = {
    "title": "Demo Title",
    "content": "Demo Content"
}

    
get_response = requests.post(endpoint, json=data)

print(get_response.json())