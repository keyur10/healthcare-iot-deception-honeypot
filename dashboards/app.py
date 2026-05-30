from flask import Flask, render_template

app = Flask(__name__)

attack_data = {
    "total_attacks": 145,
    "top_country": "Russia",
    "top_ip": "185.220.101.1",
    "top_username": "root",
    "top_password": "admin",
    "attack_type": "SSH Brute Force"
}

@app.route("/")
def dashboard():
    return render_template(
        "index.html",
        data=attack_data
    )

if __name__ == "__main__":
    app.run(debug=True)
    