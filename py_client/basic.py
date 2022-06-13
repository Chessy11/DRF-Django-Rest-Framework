from operator import ge
import requests

endpoint = "http://localhost:8000/api/blog/1/"


get_response = requests.get(endpoint)

# status_code = get_response.status_code

# if get_response.status_code == 200:
#     print("status code: ", status_code, "OK")
# else:
#     print("Error")
print(get_response.json())
