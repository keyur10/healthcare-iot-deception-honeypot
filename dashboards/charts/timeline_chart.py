import matplotlib.pyplot as plt

hours = [
    "10AM",
    "11AM",
    "12PM",
    "1PM",
    "2PM",
    "3PM"
]

attacks = [
    5,
    10,
    15,
    20,
    12,
    8
]

plt.figure(figsize=(8,5))

plt.plot(hours, attacks)

plt.xlabel("Time")
plt.ylabel("Attacks")
plt.title("Attack Timeline")

plt.savefig("attack_timeline.png")

plt.show()