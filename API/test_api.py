import requests
import sys

if len(sys.argv) > 1:
    query = " ".join(sys.argv[1:])
else:
    query = "What is the price of natural mosquito repellant?"

response = requests.post("http://localhost:5000/get_answer", json={'query': query})
print(response.json())
