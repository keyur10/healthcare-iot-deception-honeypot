import requests

ip = "8.8.8.8"

response = requests.get(
    f"http://ip-api.com/json/{ip}"
)

data = response.json()

print(data["country"])
print(data["city"])
print(data["lat"])
print(data["lon"])