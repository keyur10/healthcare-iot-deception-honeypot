import matplotlib.pyplot as plt

passwords = [
    "admin",
    "root",
    "password",
    "123456",
    "toor"
]

attempts = [
    30,
    25,
    20,
    15,
    10
]

plt.figure(figsize=(8,5))

plt.bar(passwords, attempts)

plt.xlabel("Passwords")
plt.ylabel("Attempts")
plt.title("Most Attempted Passwords")

plt.savefig("password_attempts.png")

plt.show()