import matplotlib.pyplot as plt

countries = [
    "Russia",
    "China",
    "India",
    "USA",
    "Germany"
]

attacks = [
    50,
    35,
    25,
    15,
    10
]

plt.figure(figsize=(8,5))

plt.bar(countries, attacks)

plt.xlabel("Country")
plt.ylabel("Number of Attacks")
plt.title("Top Attack Origins")

plt.savefig("top_attack_origins.png")

plt.show()